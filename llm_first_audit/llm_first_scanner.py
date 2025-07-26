#!/usr/bin/env python3
"""
LLM-First Compliance Scanner
Detects business logic violations that should use LLM instead of hardcoded rules
"""

import os
import re
import json
from dataclasses import dataclass
from typing import List, Dict, Tuple
from pathlib import Path

@dataclass
class LLMFirstViolation:
    file: str
    line: int
    code: str
    severity: str  # CRITICAL, HIGH, MEDIUM, LOW
    pattern: str
    suggestion: str
    context: str = ""

class LLMFirstScanner:
    """Comprehensive scanner for LLM-first violations"""
    
    def __init__(self):
        self.violations = []
        self.violation_patterns = {
            'CRITICAL': [
                # Business rules in code - Constitutional violations
                (r'if\s+crop\s*[=!]=', 'Crop-specific logic should use LLM - violates MANGO RULE'),
                (r'if\s+country\s*[=!]=', 'Country hardcoding violates MANGO RULE - use LLM for global logic'),
                (r'RULES\s*=\s*\{.*\}', 'Rule dictionaries should be LLM prompts, not hardcoded data'),
                (r'elif.*crop.*elif.*crop', 'Complex crop decision trees must use LLM evaluation'),
                (r'if.*["\']italy["\']|if.*["\']croatia["\']', 'Hardcoded country names violate global-first principle'),
                (r'def.*recommend.*if.*elif.*elif', 'Recommendation logic with multiple conditions needs LLM'),
                
                # Constitutional violations
                (r'language\s*==\s*["\']english["\']', 'Language hardcoding - should support all languages via LLM'),
                (r'currency\s*==\s*["\']usd["\']|currency\s*==\s*["\']eur["\']', 'Currency hardcoding - use LLM for global support'),
            ],
            'HIGH': [
                # Complex decision trees
                (r'elif.*elif.*elif.*elif', 'Complex conditions (4+ branches) need LLM evaluation'),
                (r'def.*calculate.*business.*if.*elif', 'Business calculations with conditions should use AI'),
                (r'def.*interpret.*if.*else', 'Interpretation logic must use LLM, not hardcoded rules'),
                (r'def.*validate.*if.*elif.*elif', 'Complex validation should use LLM understanding'),
                (r'def.*classify.*if.*elif', 'Classification logic should use LLM intelligence'),
                
                # Natural language processing in code
                (r'\.split\(\s*["\'][,;|]["\'].*if.*in', 'Text parsing with business logic should use LLM'),
                (r'regex.*if.*match', 'Pattern matching for business rules should use LLM'),
                (r'\.lower\(\).*if.*in.*list', 'Text normalization + business rules = LLM territory'),
                
                # Recommendation systems
                (r'def.*recommend.*return.*if', 'Any recommendation function should primarily use LLM'),
                (r'suggestion.*=.*if.*else', 'Suggestion generation should use LLM creativity'),
            ],
            'MEDIUM': [
                # User input interpretation
                (r'parse.*natural.*language', 'Use LLM for natural language parsing tasks'),
                (r'interpret.*user.*input', 'User input interpretation needs AI understanding'),
                (r'def.*understand.*text', 'Text understanding should leverage LLM capabilities'),
                (r'def.*extract.*meaning', 'Meaning extraction is perfect for LLM processing'),
                
                # Decision support
                (r'if.*risk.*high.*elif.*medium', 'Risk assessment should use LLM evaluation'),
                (r'priority.*=.*if.*urgent', 'Priority assignment should use LLM judgment'),
                (r'status.*=.*if.*condition', 'Status determination should consider LLM analysis'),
                
                # Data enrichment
                (r'def.*enrich.*data.*if', 'Data enrichment should use LLM intelligence'),
                (r'def.*enhance.*information', 'Information enhancement is ideal for LLM processing'),
            ],
            'LOW': [
                # Simple business logic that could benefit from LLM
                (r'if.*notification.*send', 'Notification decisions could use LLM personalization'),
                (r'default.*message.*if', 'Default message selection could use LLM context'),
                (r'format.*output.*if', 'Output formatting could benefit from LLM adaptation'),
            ]
        }
        
        self.file_extensions = ['.py', '.js', '.ts', '.jsx', '.tsx']
        self.ignore_patterns = [
            'test_', 'tests/', '__pycache__', '.git/', 'node_modules/',
            'venv/', 'env/', '.env', 'migrations/', 'static/css/', 'static/js/lib'
        ]
    
    def should_ignore_file(self, file_path: str) -> bool:
        """Check if file should be ignored based on patterns"""
        return any(pattern in file_path for pattern in self.ignore_patterns)
    
    def scan_file(self, file_path: str) -> List[LLMFirstViolation]:
        """Scan a single file for LLM-first violations"""
        violations = []
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
            
            for line_num, line in enumerate(lines, 1):
                line_stripped = line.strip()
                if not line_stripped or line_stripped.startswith('#'):
                    continue
                
                # Check all violation patterns
                for severity, patterns in self.violation_patterns.items():
                    for pattern, suggestion in patterns:
                        if re.search(pattern, line, re.IGNORECASE):
                            # Get context (surrounding lines)
                            context_start = max(0, line_num - 3)
                            context_end = min(len(lines), line_num + 2)
                            context = ''.join(lines[context_start:context_end])
                            
                            violation = LLMFirstViolation(
                                file=file_path,
                                line=line_num,
                                code=line_stripped,
                                severity=severity,
                                pattern=pattern,
                                suggestion=suggestion,
                                context=context
                            )
                            violations.append(violation)
                            break  # Only one violation per line
        
        except Exception as e:
            print(f"Error scanning {file_path}: {e}")
        
        return violations
    
    def scan_directory(self, directory: str) -> List[LLMFirstViolation]:
        """Scan entire directory recursively"""
        all_violations = []
        
        for root, dirs, files in os.walk(directory):
            # Skip ignored directories
            dirs[:] = [d for d in dirs if not any(pattern in d for pattern in self.ignore_patterns)]
            
            for file in files:
                if any(file.endswith(ext) for ext in self.file_extensions):
                    file_path = os.path.join(root, file)
                    if not self.should_ignore_file(file_path):
                        violations = self.scan_file(file_path)
                        all_violations.extend(violations)
        
        return all_violations
    
    def generate_report(self, violations: List[LLMFirstViolation]) -> Dict:
        """Generate comprehensive compliance report"""
        # Group violations by severity
        by_severity = {'CRITICAL': [], 'HIGH': [], 'MEDIUM': [], 'LOW': []}
        for violation in violations:
            by_severity[violation.severity].append(violation)
        
        # Group violations by file
        by_file = {}
        for violation in violations:
            if violation.file not in by_file:
                by_file[violation.file] = []
            by_file[violation.file].append(violation)
        
        # Calculate compliance score
        total_violations = len(violations)
        critical_violations = len(by_severity['CRITICAL'])
        high_violations = len(by_severity['HIGH'])
        
        # Compliance score: penalize critical/high violations more
        penalty_score = (critical_violations * 10) + (high_violations * 5) + \
                       (len(by_severity['MEDIUM']) * 2) + len(by_severity['LOW'])
        
        # Score out of 100 (lower penalty = higher score)
        max_penalty = total_violations * 10  # If all were critical
        compliance_score = max(0, 100 - (penalty_score / max(1, max_penalty) * 100))
        
        # Convert violations to serializable format for the report
        serializable_violations = []
        for violation in violations:
            serializable_violations.append({
                'file': violation.file,
                'line': violation.line,
                'code': violation.code,
                'severity': violation.severity,
                'pattern': violation.pattern,
                'suggestion': violation.suggestion,
                'context': violation.context
            })
        
        return {
            'total_violations': total_violations,
            'by_severity': {k: len(v) for k, v in by_severity.items()},
            'by_file': {k: len(v) for k, v in by_file.items()},
            'compliance_score': round(compliance_score, 1),
            'violations': serializable_violations,
            'violations_objects': violations,  # Keep original objects for processing
            'top_violating_files': sorted(by_file.items(), key=lambda x: len(x[1]), reverse=True)[:10]
        }
    
    def save_report(self, report: Dict, output_file: str):
        """Save report to JSON file"""
        # Create new report without original violation objects
        report_data = {
            'total_violations': report['total_violations'],
            'by_severity': report['by_severity'],
            'by_file': report['by_file'],
            'compliance_score': report['compliance_score'],
            'top_violating_files': report['top_violating_files'],
            'violations': report['violations']  # Already serializable
        }
        
        with open(output_file, 'w') as f:
            json.dump(report_data, f, indent=2)

def main():
    """Main scanner execution"""
    scanner = LLMFirstScanner()
    
    # Scan both agricultural and monitoring repositories
    scan_paths = [
        '/mnt/c/Users/HP/ava-olo-constitutional/ava-olo-agricultural-core',
        '/mnt/c/Users/HP/ava-olo-constitutional/ava-olo-monitoring-dashboards'
    ]
    
    all_violations = []
    for path in scan_paths:
        if os.path.exists(path):
            print(f"Scanning {path}...")
            violations = scanner.scan_directory(path)
            all_violations.extend(violations)
            print(f"Found {len(violations)} violations in {path}")
    
    # Generate comprehensive report
    report = scanner.generate_report(all_violations)
    
    print(f"\n=== LLM-FIRST COMPLIANCE REPORT ===")
    print(f"Total Violations: {report['total_violations']}")
    print(f"Compliance Score: {report['compliance_score']}/100")
    print(f"Critical: {report['by_severity']['CRITICAL']}")
    print(f"High: {report['by_severity']['HIGH']}")
    print(f"Medium: {report['by_severity']['MEDIUM']}")
    print(f"Low: {report['by_severity']['LOW']}")
    
    # Save detailed report (skip JSON for now due to serialization)
    output_dir = '/mnt/c/Users/HP/ava-olo-constitutional/ava-olo-shared/llm_first_audit'
    
    # Print detailed violations for manual analysis
    print(f"\n=== DETAILED VIOLATIONS ===")
    for violation in report['violations_objects']:
        print(f"\nFile: {violation.file}")
        print(f"Line {violation.line}: {violation.code}")
        print(f"Severity: {violation.severity}")
        print(f"Issue: {violation.suggestion}")
        print("---")
    
    return report

if __name__ == "__main__":
    main()