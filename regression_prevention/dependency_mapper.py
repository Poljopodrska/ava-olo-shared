#!/usr/bin/env python3
"""
Dependency Mapping and Change Impact Analysis
Maps module dependencies to prevent unintended side effects during changes
"""

import os
import re
import json
import ast
from pathlib import Path
from typing import Dict, List, Set, Tuple
from dataclasses import dataclass
# import networkx as nx  # Optional for advanced graph analysis
# import matplotlib.pyplot as plt  # Optional for visualization

@dataclass
class DependencyRelation:
    source_file: str
    target_file: str
    dependency_type: str  # import, template, static, api_call
    line_number: int
    context: str

class DependencyMapper:
    """Comprehensive dependency analysis for change impact assessment"""
    
    def __init__(self):
        self.dependencies = []
        self.file_index = {}
        self.dependency_graph = {}  # Simple dict-based graph
        
        # Repository paths to analyze
        self.repo_paths = [
            '/mnt/c/Users/HP/ava-olo-constitutional/ava-olo-agricultural-core',
            '/mnt/c/Users/HP/ava-olo-constitutional/ava-olo-monitoring-dashboards'
        ]
        
        # File patterns to analyze
        self.file_patterns = {
            'python': r'.*\.py$',
            'javascript': r'.*\.(js|jsx)$',
            'typescript': r'.*\.(ts|tsx)$',
            'html': r'.*\.html$',
            'css': r'.*\.css$',
            'json': r'.*\.json$'
        }
        
        # Dependency patterns to detect
        self.dependency_patterns = {
            'python_import': r'^(from\s+[\w.]+\s+import\s+.*|import\s+[\w.]+)',
            'javascript_import': r'(import\s+.*\s+from\s+["\'].*["\']|require\(["\'].*["\']\))',
            'html_template': r'(\{\%\s*extends\s+["\'].*["\']|\{\%\s*include\s+["\'].*["\'])',
            'css_import': r'@import\s+["\'].*["\']',
            'api_endpoint': r'(\/api\/[\w\/\-]+|fetch\(["\'].*["\']|\$\.get\(["\'].*["\'])',
            'static_reference': r'(href=["\'].*["\']|src=["\'].*["\']|url\(["\'].*["\']\))'
        }
        
        # Critical UI components that must never break
        self.critical_components = {
            'yellow_debug_box': [
                'debug-box', 'debug_box', '#FFD700', 'background.*yellow',
                'constitutional-debug', 'farmer-debug'
            ],
            'farmer_count_display': [
                'farmer-count', 'total-farmers', 'farmer_count',
                'count.*farmer', 'farmer.*total'
            ],
            'dashboard_layout': [
                'dashboard-grid', 'dashboard-layout', 'main-dashboard',
                'dashboard-container', 'grid-layout'
            ],
            'navigation_menu': [
                'nav-menu', 'navigation', 'sidebar', 'menu-container'
            ]
        }
    
    def analyze_repositories(self):
        """Analyze all repositories for dependencies"""
        print("🔍 Starting comprehensive dependency analysis...")
        
        for repo_path in self.repo_paths:
            if os.path.exists(repo_path):
                print(f"  📂 Analyzing {repo_path}...")
                self.analyze_directory(repo_path)
        
        self.build_dependency_graph()
        print(f"✅ Analysis complete. Found {len(self.dependencies)} dependencies.")
        
        return self.dependencies
    
    def analyze_directory(self, directory: str):
        """Recursively analyze directory for dependencies"""
        for root, dirs, files in os.walk(directory):
            # Skip common directories that don't contain application code
            dirs[:] = [d for d in dirs if d not in [
                '__pycache__', '.git', 'node_modules', '.env', 'venv', 'env',
                '.pytest_cache', '.coverage', 'dist', 'build'
            ]]
            
            for file in files:
                file_path = os.path.join(root, file)
                
                # Check if file matches any pattern we care about
                for file_type, pattern in self.file_patterns.items():
                    if re.match(pattern, file, re.IGNORECASE):
                        self.analyze_file(file_path, file_type)
                        break
    
    def analyze_file(self, file_path: str, file_type: str):
        """Analyze individual file for dependencies"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                lines = content.split('\n')
            
            # Index file for quick lookup
            self.file_index[file_path] = {
                'type': file_type,
                'size': len(content),
                'lines': len(lines),
                'content': content
            }
            
            # Analyze based on file type
            if file_type == 'python':
                self.analyze_python_file(file_path, content, lines)
            elif file_type in ['javascript', 'typescript']:
                self.analyze_javascript_file(file_path, content, lines)
            elif file_type == 'html':
                self.analyze_html_file(file_path, content, lines)
            elif file_type == 'css':
                self.analyze_css_file(file_path, content, lines)
    
    def analyze_css_file(self, file_path: str, content: str, lines: List[str]):
        """Analyze CSS file for imports and dependencies"""
        for line_num, line in enumerate(lines, 1):
            line = line.strip()
            
            # CSS imports
            import_match = re.search(r'@import\s+["\']([^"\']+)["\']', line)
            if import_match:
                imported_css = import_match.group(1)
                target_file = self.resolve_static_path(imported_css, file_path)
                if target_file:
                    self.add_dependency(
                        file_path, target_file, 'css_import',
                        line_num, line
                    )
    
    def analyze_python_file(self, file_path: str, content: str, lines: List[str]):
        """Analyze Python file for imports and dependencies"""
        for line_num, line in enumerate(lines, 1):
            line = line.strip()
            
            # Python imports
            if re.match(self.dependency_patterns['python_import'], line):
                # Extract imported module
                if line.startswith('from'):
                    match = re.match(r'from\s+([\w.]+)\s+import', line)
                    if match:
                        module = match.group(1)
                        target_file = self.resolve_python_module(module, file_path)
                        if target_file:
                            self.add_dependency(
                                file_path, target_file, 'python_import', 
                                line_num, line
                            )
                elif line.startswith('import'):
                    match = re.match(r'import\s+([\w.]+)', line)
                    if match:
                        module = match.group(1)
                        target_file = self.resolve_python_module(module, file_path)
                        if target_file:
                            self.add_dependency(
                                file_path, target_file, 'python_import',
                                line_num, line
                            )
            
            # API endpoint calls
            api_match = re.search(r'["\']/(api/[\w/\-]+)["\']', line)
            if api_match:
                endpoint = api_match.group(1)
                self.add_dependency(
                    file_path, f"api_endpoint:{endpoint}", 'api_call',
                    line_num, line
                )
            
            # Template references
            template_match = re.search(r'render_template\(["\']([^"\']+)["\']', line)
            if template_match:
                template_name = template_match.group(1)
                template_file = self.resolve_template_path(template_name, file_path)
                if template_file:
                    self.add_dependency(
                        file_path, template_file, 'template_render',
                        line_num, line
                    )
    
    def analyze_html_file(self, file_path: str, content: str, lines: List[str]):
        """Analyze HTML file for template dependencies and static references"""
        for line_num, line in enumerate(lines, 1):
            line = line.strip()
            
            # Template extends/includes
            extends_match = re.search(r'\{\%\s*extends\s+["\']([^"\']+)["\']', line)
            if extends_match:
                template_name = extends_match.group(1)
                template_file = self.resolve_template_path(template_name, file_path)
                if template_file:
                    self.add_dependency(
                        file_path, template_file, 'template_extends',
                        line_num, line
                    )
            
            include_match = re.search(r'\{\%\s*include\s+["\']([^"\']+)["\']', line)
            if include_match:
                template_name = include_match.group(1)
                template_file = self.resolve_template_path(template_name, file_path)
                if template_file:
                    self.add_dependency(
                        file_path, template_file, 'template_include',
                        line_num, line
                    )
            
            # Static file references
            static_matches = re.findall(r'(href|src)=["\']([^"\']+)["\']', line)
            for attr, url in static_matches:
                if url.startswith('/static/') or url.endswith(('.css', '.js', '.png', '.jpg', '.jpeg')):
                    static_file = self.resolve_static_path(url, file_path)
                    if static_file:
                        self.add_dependency(
                            file_path, static_file, f'static_{attr}',
                            line_num, line
                        )
            
            # Critical component usage
            for component_name, patterns in self.critical_components.items():
                for pattern in patterns:
                    if re.search(pattern, line, re.IGNORECASE):
                        self.add_dependency(
                            file_path, f"critical_component:{component_name}",
                            'critical_component', line_num, line
                        )
    
    def analyze_javascript_file(self, file_path: str, content: str, lines: List[str]):
        """Analyze JavaScript/TypeScript files"""
        for line_num, line in enumerate(lines, 1):
            line = line.strip()
            
            # ES6 imports
            import_match = re.search(r'import\s+.*\s+from\s+["\']([^"\']+)["\']', line)
            if import_match:
                module_path = import_match.group(1)
                target_file = self.resolve_js_module(module_path, file_path)
                if target_file:
                    self.add_dependency(
                        file_path, target_file, 'es6_import',
                        line_num, line
                    )
            
            # API calls
            api_patterns = [
                r'fetch\(["\']([^"\']+)["\']',
                r'\$\.get\(["\']([^"\']+)["\']',
                r'\$\.post\(["\']([^"\']+)["\']',
                r'axios\.(get|post)\(["\']([^"\']+)["\']'
            ]
            
            for pattern in api_patterns:
                match = re.search(pattern, line)
                if match:
                    if 'axios' in pattern:
                        endpoint = match.group(2)
                    else:
                        endpoint = match.group(1)
                    
                    self.add_dependency(
                        file_path, f"api_endpoint:{endpoint}", 'api_call',
                        line_num, line
                    )
    
    def add_dependency(self, source: str, target: str, dep_type: str, line_num: int, context: str):
        """Add dependency relationship"""
        dependency = DependencyRelation(
            source_file=source,
            target_file=target,
            dependency_type=dep_type,
            line_number=line_num,
            context=context.strip()
        )
        self.dependencies.append(dependency)
    
    def build_dependency_graph(self):
        """Build simple graph from dependencies"""
        for dep in self.dependencies:
            if dep.source_file not in self.dependency_graph:
                self.dependency_graph[dep.source_file] = []
            
            self.dependency_graph[dep.source_file].append({
                'target': dep.target_file,
                'type': dep.dependency_type,
                'line': dep.line_number,
                'context': dep.context
            })
    
    def analyze_change_impact(self, changed_files: List[str]) -> Dict:
        """Analyze impact of changing specific files"""
        print(f"🎯 Analyzing impact of changing: {changed_files}")
        
        impact_analysis = {
            'changed_files': changed_files,
            'directly_affected': set(),
            'indirectly_affected': set(),
            'critical_components_at_risk': set(),
            'api_endpoints_affected': set(),
            'risk_level': 'LOW',
            'recommended_tests': [],
            'change_scope': 'ISOLATED'
        }
        
        for changed_file in changed_files:
            # Find all files that depend on this file
            direct_dependents = self.find_dependents(changed_file)
            impact_analysis['directly_affected'].update(direct_dependents)
            
            # Find indirect dependencies (dependencies of dependencies)
            for dependent in direct_dependents:
                indirect_dependents = self.find_dependents(dependent)
                impact_analysis['indirectly_affected'].update(indirect_dependents)
            
            # Check if critical components are affected
            critical_deps = [
                dep for dep in self.dependencies 
                if dep.source_file == changed_file and 
                dep.dependency_type == 'critical_component'
            ]
            
            for critical_dep in critical_deps:
                component_name = critical_dep.target_file.replace('critical_component:', '')
                impact_analysis['critical_components_at_risk'].add(component_name)
            
            # Check API endpoints affected
            api_deps = [
                dep for dep in self.dependencies
                if dep.source_file == changed_file and
                dep.dependency_type == 'api_call'
            ]
            
            for api_dep in api_deps:
                endpoint = api_dep.target_file.replace('api_endpoint:', '')
                impact_analysis['api_endpoints_affected'].add(endpoint)
        
        # Calculate risk level
        total_affected = len(impact_analysis['directly_affected']) + len(impact_analysis['indirectly_affected'])
        critical_affected = len(impact_analysis['critical_components_at_risk'])
        
        if critical_affected > 0:
            impact_analysis['risk_level'] = 'CRITICAL'
            impact_analysis['change_scope'] = 'SYSTEM_WIDE'
        elif total_affected > 10:
            impact_analysis['risk_level'] = 'HIGH'
            impact_analysis['change_scope'] = 'CROSS_MODULE'
        elif total_affected > 3:
            impact_analysis['risk_level'] = 'MEDIUM'
            impact_analysis['change_scope'] = 'MODULE_LOCAL'
        else:
            impact_analysis['risk_level'] = 'LOW'
            impact_analysis['change_scope'] = 'ISOLATED'
        
        # Generate test recommendations
        impact_analysis['recommended_tests'] = self.generate_test_recommendations(impact_analysis)
        
        return impact_analysis
    
    def find_dependents(self, file_path: str) -> Set[str]:
        """Find all files that depend on the given file"""
        dependents = set()
        
        for dep in self.dependencies:
            if dep.target_file == file_path:
                dependents.add(dep.source_file)
        
        return dependents
    
    def generate_test_recommendations(self, impact_analysis: Dict) -> List[str]:
        """Generate testing recommendations based on impact"""
        recommendations = []
        
        if impact_analysis['critical_components_at_risk']:
            recommendations.append("🚨 MANDATORY: Visual regression test for critical UI components")
            recommendations.append("🚨 MANDATORY: Constitutional compliance verification")
            
            for component in impact_analysis['critical_components_at_risk']:
                recommendations.append(f"🔍 Test {component} functionality specifically")
        
        if impact_analysis['api_endpoints_affected']:
            recommendations.append("🔍 API endpoint testing required")
            for endpoint in impact_analysis['api_endpoints_affected']:
                recommendations.append(f"📡 Test API endpoint: {endpoint}")
        
        if impact_analysis['directly_affected']:
            recommendations.append("🧪 Unit tests for directly affected modules")
            recommendations.append("🔗 Integration tests for module interactions")
        
        if impact_analysis['risk_level'] in ['HIGH', 'CRITICAL']:
            recommendations.append("🎯 Full system regression testing")
            recommendations.append("🌐 End-to-end testing required")
            recommendations.append("📊 Performance impact testing")
        
        return recommendations
    
    def resolve_python_module(self, module_name: str, source_file: str) -> str:
        """Resolve Python module import to actual file path"""
        # This is simplified - a full implementation would handle:
        # - Relative imports
        # - Package structure
        # - Virtual environment packages
        # - System packages
        
        # For now, just handle local module references
        if '.' in module_name:
            # Package import
            parts = module_name.split('.')
            potential_path = os.path.join(os.path.dirname(source_file), *parts) + '.py'
            if os.path.exists(potential_path):
                return potential_path
        
        return None
    
    def resolve_template_path(self, template_name: str, source_file: str) -> str:
        """Resolve template path"""
        # Look for template in common template directories
        base_dir = os.path.dirname(source_file)
        while base_dir and base_dir != '/':
            template_dirs = [
                os.path.join(base_dir, 'templates'),
                os.path.join(base_dir, 'app', 'templates'),
                os.path.join(base_dir, 'src', 'templates')
            ]
            
            for template_dir in template_dirs:
                template_path = os.path.join(template_dir, template_name)
                if os.path.exists(template_path):
                    return template_path
            
            base_dir = os.path.dirname(base_dir)
        
        return None
    
    def resolve_static_path(self, static_url: str, source_file: str) -> str:
        """Resolve static file path"""
        # Handle /static/ URLs
        if static_url.startswith('/static/'):
            static_path = static_url[8:]  # Remove /static/
            base_dir = os.path.dirname(source_file)
            
            while base_dir and base_dir != '/':
                static_dirs = [
                    os.path.join(base_dir, 'static'),
                    os.path.join(base_dir, 'app', 'static'),
                    os.path.join(base_dir, 'src', 'static')
                ]
                
                for static_dir in static_dirs:
                    full_path = os.path.join(static_dir, static_path)
                    if os.path.exists(full_path):
                        return full_path
                
                base_dir = os.path.dirname(base_dir)
        
        return None
    
    def resolve_js_module(self, module_path: str, source_file: str) -> str:
        """Resolve JavaScript module path"""
        if module_path.startswith('./') or module_path.startswith('../'):
            # Relative import
            source_dir = os.path.dirname(source_file)
            resolved = os.path.normpath(os.path.join(source_dir, module_path))
            
            # Try different extensions
            for ext in ['.js', '.ts', '.jsx', '.tsx']:
                if os.path.exists(resolved + ext):
                    return resolved + ext
        
        return None
    
    def generate_dependency_report(self) -> str:
        """Generate comprehensive dependency report"""
        report = f"""# Dependency Analysis Report
Generated: {datetime.now().isoformat()}

## Summary
- Total Dependencies: {len(self.dependencies)}
- Files Analyzed: {len(self.file_index)}
- Dependency Types: {len(set(dep.dependency_type for dep in self.dependencies))}

## Dependency Breakdown by Type
"""
        
        # Group by dependency type
        by_type = {}
        for dep in self.dependencies:
            if dep.dependency_type not in by_type:
                by_type[dep.dependency_type] = []
            by_type[dep.dependency_type].append(dep)
        
        for dep_type, deps in sorted(by_type.items()):
            report += f"\n### {dep_type.replace('_', ' ').title()} ({len(deps)})\n"
            
            # Show top 10 dependencies of this type
            for dep in deps[:10]:
                report += f"- `{os.path.basename(dep.source_file)}` → `{os.path.basename(dep.target_file)}`\n"
            
            if len(deps) > 10:
                report += f"- ... and {len(deps) - 10} more\n"
        
        # Critical components analysis
        critical_deps = [dep for dep in self.dependencies if dep.dependency_type == 'critical_component']
        if critical_deps:
            report += f"\n## 🚨 Critical Component Dependencies ({len(critical_deps)})\n"
            
            critical_by_component = {}
            for dep in critical_deps:
                component = dep.target_file.replace('critical_component:', '')
                if component not in critical_by_component:
                    critical_by_component[component] = []
                critical_by_component[component].append(dep)
            
            for component, deps in critical_by_component.items():
                report += f"\n### {component.replace('_', ' ').title()}\n"
                report += f"Used in {len(deps)} files:\n"
                
                for dep in deps:
                    report += f"- `{os.path.basename(dep.source_file)}` (line {dep.line_number})\n"
        
        return report
    
    def save_analysis(self, output_dir: str):
        """Save comprehensive analysis results"""
        os.makedirs(output_dir, exist_ok=True)
        
        # Save raw dependency data
        dependencies_data = []
        for dep in self.dependencies:
            dependencies_data.append({
                'source_file': dep.source_file,
                'target_file': dep.target_file,
                'dependency_type': dep.dependency_type,
                'line_number': dep.line_number,
                'context': dep.context
            })
        
        with open(os.path.join(output_dir, 'dependencies.json'), 'w') as f:
            json.dump(dependencies_data, f, indent=2)
        
        # Save dependency report
        report = self.generate_dependency_report()
        with open(os.path.join(output_dir, 'dependency_report.md'), 'w') as f:
            f.write(report)
        
        # Save file index
        with open(os.path.join(output_dir, 'file_index.json'), 'w') as f:
            json.dump(self.file_index, f, indent=2)
        
        print(f"📊 Dependency analysis saved to {output_dir}")

def main():
    """Main analysis execution"""
    mapper = DependencyMapper()
    
    print("🔗 Dependency Mapping and Change Impact Analysis")
    print("=" * 60)
    
    # Analyze repositories
    dependencies = mapper.analyze_repositories()
    
    # Save analysis
    output_dir = '/mnt/c/Users/HP/ava-olo-constitutional/ava-olo-shared/regression_prevention/dependency_analysis'
    mapper.save_analysis(output_dir)
    
    # Example impact analysis
    print("\n🎯 Example: Impact of changing database.py")
    test_files = [
        '/mnt/c/Users/HP/ava-olo-constitutional/ava-olo-monitoring-dashboards/modules/dashboards/database.py'
    ]
    
    if any(os.path.exists(f) for f in test_files):
        existing_files = [f for f in test_files if os.path.exists(f)]
        impact = mapper.analyze_change_impact(existing_files)
        
        print(f"Risk Level: {impact['risk_level']}")
        print(f"Change Scope: {impact['change_scope']}")
        print(f"Directly Affected: {len(impact['directly_affected'])}")
        print(f"Critical Components at Risk: {len(impact['critical_components_at_risk'])}")
        
        if impact['recommended_tests']:
            print("\nRecommended Tests:")
            for test in impact['recommended_tests']:
                print(f"  {test}")
    
    return dependencies

if __name__ == "__main__":
    from datetime import datetime
    main()