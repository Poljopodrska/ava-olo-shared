#!/usr/bin/env python3
"""
Visual Regression Testing System
Prevents dashboard breaking changes through automated screenshot comparison
"""

import os
import json
import time
import hashlib
from datetime import datetime
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image, ImageDraw, ImageChops
import subprocess

class VisualRegressionTester:
    """Comprehensive visual regression testing for dashboard elements"""
    
    def __init__(self, base_url="http://localhost:8080"):
        self.base_url = base_url
        self.baseline_dir = "/mnt/c/Users/HP/ava-olo-constitutional/ava-olo-shared/regression_prevention/baselines"
        self.comparison_dir = "/mnt/c/Users/HP/ava-olo-constitutional/ava-olo-shared/regression_prevention/comparisons"
        self.diff_dir = "/mnt/c/Users/HP/ava-olo-constitutional/ava-olo-shared/regression_prevention/diffs"
        
        # Ensure directories exist
        for directory in [self.baseline_dir, self.comparison_dir, self.diff_dir]:
            os.makedirs(directory, exist_ok=True)
        
        # Critical UI elements that must never break
        self.critical_elements = {
            'yellow_debug_box': {
                'selector': '[style*="background"][style*="#FFD700"], .debug-box, [style*="background"][style*="yellow"]',
                'description': 'Yellow debug box (Constitutional requirement)',
                'tolerance': 0  # Zero tolerance for changes
            },
            'farmer_count_display': {
                'selector': '.farmer-count, [data-testid="farmer-count"], .total-farmers',
                'description': 'Farmer count display',
                'tolerance': 5  # Small tolerance for number changes
            },
            'dashboard_header': {
                'selector': '.dashboard-header, header, .main-header',
                'description': 'Main dashboard header',
                'tolerance': 10
            },
            'navigation_menu': {
                'selector': '.navigation, .nav-menu, .sidebar',
                'description': 'Navigation menu structure',
                'tolerance': 5
            },
            'database_dashboard': {
                'selector': '.database-dashboard, [data-dashboard="database"]',
                'description': 'Database dashboard layout',
                'tolerance': 10
            },
            'monitoring_cards': {
                'selector': '.monitoring-card, .dashboard-card, .metric-card',
                'description': 'Monitoring dashboard cards',
                'tolerance': 15
            }
        }
        
        # Dashboard pages to test
        self.test_pages = [
            {'path': '/', 'name': 'home', 'wait_for': 'body'},
            {'path': '/dashboards/database', 'name': 'database_dashboard', 'wait_for': '.dashboard-content'},
            {'path': '/dashboards/database/retrieval', 'name': 'database_retrieval', 'wait_for': '.main-content'},
            {'path': '/dashboards/monitoring', 'name': 'monitoring_dashboard', 'wait_for': '.dashboard-grid'},
        ]
    
    def setup_driver(self):
        """Setup Chrome driver for screenshots"""
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--disable-gpu')
        
        driver = webdriver.Chrome(options=chrome_options)
        return driver
    
    def capture_baseline(self):
        """Capture baseline screenshots of current working state"""
        print("🔍 Capturing visual baseline screenshots...")
        
        driver = self.setup_driver()
        baseline_metadata = {
            'timestamp': datetime.now().isoformat(),
            'git_commit': self.get_git_commit(),
            'screenshots': {},
            'elements': {}
        }
        
        try:
            for page in self.test_pages:
                print(f"  📸 Capturing {page['name']}...")
                
                # Navigate to page
                full_url = f"{self.base_url}{page['path']}"
                driver.get(full_url)
                
                # Wait for page to load
                try:
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, page['wait_for']))
                    )
                    time.sleep(2)  # Additional stability wait
                except Exception as e:
                    print(f"    ⚠️ Warning: Could not wait for {page['wait_for']} on {page['name']}: {e}")
                
                # Capture full page screenshot
                screenshot_path = os.path.join(self.baseline_dir, f"{page['name']}_full.png")
                driver.save_screenshot(screenshot_path)
                
                baseline_metadata['screenshots'][page['name']] = {
                    'full_page': screenshot_path,
                    'url': full_url,
                    'timestamp': datetime.now().isoformat()
                }
                
                # Capture individual critical elements
                for element_name, element_config in self.critical_elements.items():
                    try:
                        elements = driver.find_elements(By.CSS_SELECTOR, element_config['selector'])
                        if elements:
                            element = elements[0]  # Take first match
                            
                            # Scroll element into view
                            driver.execute_script("arguments[0].scrollIntoView(true);", element)
                            time.sleep(0.5)
                            
                            # Capture element screenshot
                            element_screenshot = os.path.join(
                                self.baseline_dir, 
                                f"{page['name']}_{element_name}.png"
                            )
                            element.screenshot(element_screenshot)
                            
                            # Store element info
                            if page['name'] not in baseline_metadata['elements']:
                                baseline_metadata['elements'][page['name']] = {}
                            
                            baseline_metadata['elements'][page['name']][element_name] = {
                                'screenshot': element_screenshot,
                                'description': element_config['description'],
                                'tolerance': element_config['tolerance'],
                                'found': True,
                                'location': element.location,
                                'size': element.size
                            }
                            
                            print(f"    ✅ Captured {element_name}")
                        else:
                            print(f"    ❌ Element not found: {element_name} ({element_config['selector']})")
                            
                            if page['name'] not in baseline_metadata['elements']:
                                baseline_metadata['elements'][page['name']] = {}
                            baseline_metadata['elements'][page['name']][element_name] = {
                                'found': False,
                                'description': element_config['description']
                            }
                    
                    except Exception as e:
                        print(f"    ⚠️ Error capturing {element_name}: {e}")
        
        finally:
            driver.quit()
        
        # Save baseline metadata
        metadata_path = os.path.join(self.baseline_dir, 'baseline_metadata.json')
        with open(metadata_path, 'w') as f:
            json.dump(baseline_metadata, f, indent=2)
        
        print(f"✅ Baseline captured and saved to {self.baseline_dir}")
        return baseline_metadata
    
    def compare_with_baseline(self):
        """Compare current state with baseline"""
        print("🔍 Comparing current state with baseline...")
        
        # Load baseline metadata
        baseline_metadata_path = os.path.join(self.baseline_dir, 'baseline_metadata.json')
        if not os.path.exists(baseline_metadata_path):
            raise FileNotFoundError("No baseline found. Run capture_baseline() first.")
        
        with open(baseline_metadata_path, 'r') as f:
            baseline_metadata = json.load(f)
        
        driver = self.setup_driver()
        comparison_results = {
            'timestamp': datetime.now().isoformat(),
            'git_commit': self.get_git_commit(),
            'baseline_commit': baseline_metadata.get('git_commit'),
            'pages': {},
            'summary': {
                'total_pages': 0,
                'passed_pages': 0,
                'failed_pages': 0,
                'critical_failures': 0,
                'warnings': 0
            }
        }
        
        try:
            for page in self.test_pages:
                print(f"  🔍 Comparing {page['name']}...")
                
                page_results = {
                    'status': 'PASS',
                    'elements': {},
                    'full_page_diff': None,
                    'critical_failures': [],
                    'warnings': []
                }
                
                # Navigate to page
                full_url = f"{self.base_url}{page['path']}"
                driver.get(full_url)
                
                try:
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, page['wait_for']))
                    )
                    time.sleep(2)
                except Exception as e:
                    page_results['warnings'].append(f"Page load warning: {e}")
                
                # Capture current screenshot
                current_screenshot = os.path.join(self.comparison_dir, f"{page['name']}_current.png")
                driver.save_screenshot(current_screenshot)
                
                # Compare full page if baseline exists
                baseline_screenshot = baseline_metadata['screenshots'][page['name']]['full_page']
                if os.path.exists(baseline_screenshot):
                    diff_path = os.path.join(self.diff_dir, f"{page['name']}_full_diff.png")
                    diff_score = self.compare_images(baseline_screenshot, current_screenshot, diff_path)
                    
                    page_results['full_page_diff'] = {
                        'diff_score': diff_score,
                        'diff_image': diff_path,
                        'baseline': baseline_screenshot,
                        'current': current_screenshot
                    }
                    
                    if diff_score > 20:  # Significant change
                        page_results['status'] = 'FAIL'
                        page_results['critical_failures'].append(f"Major layout change detected (diff: {diff_score}%)")
                
                # Compare individual elements
                if page['name'] in baseline_metadata.get('elements', {}):
                    baseline_elements = baseline_metadata['elements'][page['name']]
                    
                    for element_name, baseline_element in baseline_elements.items():
                        if not baseline_element.get('found', False):
                            continue
                        
                        element_config = self.critical_elements[element_name]
                        element_result = {
                            'status': 'PASS',
                            'found': False,
                            'diff_score': None,
                            'issues': []
                        }
                        
                        try:
                            elements = driver.find_elements(By.CSS_SELECTOR, element_config['selector'])
                            if elements:
                                element = elements[0]
                                element_result['found'] = True
                                
                                # Capture current element
                                current_element_screenshot = os.path.join(
                                    self.comparison_dir, 
                                    f"{page['name']}_{element_name}_current.png"
                                )
                                element.screenshot(current_element_screenshot)
                                
                                # Compare with baseline
                                baseline_element_screenshot = baseline_element['screenshot']
                                if os.path.exists(baseline_element_screenshot):
                                    element_diff_path = os.path.join(
                                        self.diff_dir, 
                                        f"{page['name']}_{element_name}_diff.png"
                                    )
                                    
                                    diff_score = self.compare_images(
                                        baseline_element_screenshot,
                                        current_element_screenshot,
                                        element_diff_path
                                    )
                                    
                                    element_result['diff_score'] = diff_score
                                    tolerance = element_config['tolerance']
                                    
                                    if diff_score > tolerance:
                                        element_result['status'] = 'FAIL'
                                        element_result['issues'].append(
                                            f"Visual change exceeds tolerance: {diff_score}% > {tolerance}%"
                                        )
                                        
                                        # Critical elements cause page failure
                                        if element_name in ['yellow_debug_box', 'farmer_count_display']:
                                            page_results['status'] = 'FAIL'
                                            page_results['critical_failures'].append(
                                                f"CRITICAL: {element_config['description']} changed by {diff_score}%"
                                            )
                                        else:
                                            page_results['warnings'].append(
                                                f"Warning: {element_config['description']} changed by {diff_score}%"
                                            )
                            else:
                                element_result['issues'].append("Element not found on page")
                                if element_name in ['yellow_debug_box', 'farmer_count_display']:
                                    page_results['status'] = 'FAIL'
                                    page_results['critical_failures'].append(
                                        f"CRITICAL: {element_config['description']} missing from page"
                                    )
                        
                        except Exception as e:
                            element_result['issues'].append(f"Error comparing element: {e}")
                        
                        page_results['elements'][element_name] = element_result
                
                comparison_results['pages'][page['name']] = page_results
                
                # Update summary
                comparison_results['summary']['total_pages'] += 1
                if page_results['status'] == 'PASS':
                    comparison_results['summary']['passed_pages'] += 1
                else:
                    comparison_results['summary']['failed_pages'] += 1
                
                comparison_results['summary']['critical_failures'] += len(page_results['critical_failures'])
                comparison_results['summary']['warnings'] += len(page_results['warnings'])
                
                print(f"    {'✅' if page_results['status'] == 'PASS' else '❌'} {page['name']}: {page_results['status']}")
        
        finally:
            driver.quit()
        
        # Save comparison results
        results_path = os.path.join(self.comparison_dir, 'comparison_results.json')
        with open(results_path, 'w') as f:
            json.dump(comparison_results, f, indent=2)
        
        # Generate report
        self.generate_comparison_report(comparison_results)
        
        return comparison_results
    
    def compare_images(self, baseline_path, current_path, diff_output_path):
        """Compare two images and generate diff, return percentage difference"""
        try:
            baseline_img = Image.open(baseline_path).convert('RGB')
            current_img = Image.open(current_path).convert('RGB')
            
            # Resize images to match if different
            if baseline_img.size != current_img.size:
                current_img = current_img.resize(baseline_img.size)
            
            # Calculate difference
            diff_img = ImageChops.difference(baseline_img, current_img)
            
            # Convert to grayscale for analysis
            diff_gray = diff_img.convert('L')
            
            # Calculate percentage of changed pixels
            diff_data = list(diff_gray.getdata())
            total_pixels = len(diff_data)
            changed_pixels = sum(1 for pixel in diff_data if pixel > 30)  # Threshold for "changed"
            
            diff_percentage = (changed_pixels / total_pixels) * 100
            
            # Create visual diff with highlighting
            diff_visual = Image.new('RGB', baseline_img.size)
            diff_pixels = []
            
            for i, (base_pixel, curr_pixel) in enumerate(zip(baseline_img.getdata(), current_img.getdata())):
                # Calculate color difference
                color_diff = sum(abs(b - c) for b, c in zip(base_pixel, curr_pixel)) / 3
                
                if color_diff > 30:  # Significant difference
                    diff_pixels.append((255, 0, 0))  # Red for changes
                else:
                    diff_pixels.append(curr_pixel)  # Original color
            
            diff_visual.putdata(diff_pixels)
            diff_visual.save(diff_output_path)
            
            return round(diff_percentage, 2)
        
        except Exception as e:
            print(f"Error comparing images: {e}")
            return 100  # Assume maximum difference on error
    
    def generate_comparison_report(self, results):
        """Generate comprehensive HTML report"""
        html_report = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Visual Regression Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .header {{ background: #f0f0f0; padding: 20px; border-radius: 5px; }}
                .summary {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin: 20px 0; }}
                .metric {{ background: #e8f4f8; padding: 15px; text-align: center; border-radius: 5px; }}
                .pass {{ color: green; }}
                .fail {{ color: red; }}
                .critical {{ background: #ffebee; border-left: 5px solid red; }}
                .warning {{ background: #fff3e0; border-left: 5px solid orange; }}
                .page-section {{ margin: 20px 0; border: 1px solid #ddd; padding: 15px; }}
                .element-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 15px; }}
                .element-card {{ border: 1px solid #eee; padding: 10px; }}
                .diff-images {{ display: flex; gap: 10px; flex-wrap: wrap; }}
                .diff-images img {{ max-width: 200px; border: 1px solid #ddd; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Visual Regression Test Report</h1>
                <p><strong>Generated:</strong> {results['timestamp']}</p>
                <p><strong>Git Commit:</strong> {results['git_commit']}</p>
                <p><strong>Baseline Commit:</strong> {results.get('baseline_commit', 'Unknown')}</p>
            </div>
            
            <div class="summary">
                <div class="metric">
                    <h3>{results['summary']['total_pages']}</h3>
                    <p>Pages Tested</p>
                </div>
                <div class="metric">
                    <h3 class="pass">{results['summary']['passed_pages']}</h3>
                    <p>Passed</p>
                </div>
                <div class="metric">
                    <h3 class="fail">{results['summary']['failed_pages']}</h3>
                    <p>Failed</p>
                </div>
                <div class="metric">
                    <h3 class="fail">{results['summary']['critical_failures']}</h3>
                    <p>Critical Issues</p>
                </div>
            </div>
        """
        
        # Add page details
        for page_name, page_result in results['pages'].items():
            status_class = 'pass' if page_result['status'] == 'PASS' else 'fail'
            
            html_report += f"""
            <div class="page-section">
                <h2 class="{status_class}">📄 {page_name.replace('_', ' ').title()} - {page_result['status']}</h2>
            """
            
            # Critical failures
            if page_result['critical_failures']:
                html_report += '<div class="critical"><h4>🚨 Critical Failures:</h4><ul>'
                for failure in page_result['critical_failures']:
                    html_report += f'<li>{failure}</li>'
                html_report += '</ul></div>'
            
            # Warnings
            if page_result['warnings']:
                html_report += '<div class="warning"><h4>⚠️ Warnings:</h4><ul>'
                for warning in page_result['warnings']:
                    html_report += f'<li>{warning}</li>'
                html_report += '</ul></div>'
            
            # Element comparison details
            if page_result['elements']:
                html_report += '<h4>Element Comparisons:</h4><div class="element-grid">'
                
                for element_name, element_result in page_result['elements'].items():
                    element_status = 'pass' if element_result['status'] == 'PASS' else 'fail'
                    diff_score = element_result.get('diff_score', 'N/A')
                    
                    html_report += f"""
                    <div class="element-card">
                        <h5 class="{element_status}">{element_name.replace('_', ' ').title()}</h5>
                        <p><strong>Status:</strong> {element_result['status']}</p>
                        <p><strong>Found:</strong> {element_result['found']}</p>
                        <p><strong>Difference:</strong> {diff_score}%</p>
                    """
                    
                    if element_result['issues']:
                        html_report += '<p><strong>Issues:</strong></p><ul>'
                        for issue in element_result['issues']:
                            html_report += f'<li>{issue}</li>'
                        html_report += '</ul>'
                    
                    html_report += '</div>'
                
                html_report += '</div>'
            
            html_report += '</div>'
        
        html_report += """
        </body>
        </html>
        """
        
        # Save report
        report_path = os.path.join(self.comparison_dir, 'visual_regression_report.html')
        with open(report_path, 'w') as f:
            f.write(html_report)
        
        print(f"📊 Visual regression report saved: {report_path}")
        return report_path
    
    def get_git_commit(self):
        """Get current git commit hash"""
        try:
            result = subprocess.run(
                ['git', 'rev-parse', 'HEAD'], 
                capture_output=True, 
                text=True,
                cwd=Path(__file__).parent
            )
            return result.stdout.strip()
        except:
            return "unknown"

def main():
    """Main test execution"""
    tester = VisualRegressionTester()
    
    print("🎯 Visual Regression Testing System")
    print("=" * 50)
    
    # Check if baseline exists
    baseline_metadata_path = os.path.join(tester.baseline_dir, 'baseline_metadata.json')
    
    if not os.path.exists(baseline_metadata_path):
        print("📸 No baseline found. Capturing baseline screenshots...")
        tester.capture_baseline()
    else:
        print("🔍 Baseline exists. Running comparison...")
        results = tester.compare_with_baseline()
        
        print(f"\n📊 Results Summary:")
        print(f"  Total Pages: {results['summary']['total_pages']}")
        print(f"  Passed: {results['summary']['passed_pages']}")
        print(f"  Failed: {results['summary']['failed_pages']}")
        print(f"  Critical Issues: {results['summary']['critical_failures']}")
        print(f"  Warnings: {results['summary']['warnings']}")
        
        if results['summary']['critical_failures'] > 0:
            print("\n🚨 CRITICAL FAILURES DETECTED!")
            print("Visual regression testing FAILED.")
            return 1
        elif results['summary']['failed_pages'] > 0:
            print("\n⚠️ Some pages failed visual regression tests.")
            return 1
        else:
            print("\n✅ All visual regression tests PASSED!")
            return 0

if __name__ == "__main__":
    exit(main())