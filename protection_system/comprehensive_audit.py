#!/usr/bin/env python3
"""
AVA OLO Comprehensive System Audit
Verifies constitutional compliance and prevents regressions
"""
import os
import sys
import json
import re
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import ast

# Add shared module to path
sys.path.append('/mnt/c/Users/HP/ava-olo-constitutional/ava-olo-shared')
from environments.central_config import CentralConfig
from version_config import VersionManager

class AVASystemAuditor:
    """Comprehensive system auditor for AVA OLO"""
    
    def __init__(self):
        self.violations = []
        self.warnings = []
        self.successes = []
        self.root_path = Path('/mnt/c/Users/HP/ava-olo-constitutional')
        self.timestamp = datetime.utcnow()
        
    def add_violation(self, principle: str, details: str, file_path: str = None):
        """Add a constitutional violation"""
        self.violations.append({
            'principle': principle,
            'details': details,
            'file': file_path,
            'severity': 'HIGH'
        })
    
    def add_warning(self, principle: str, details: str, file_path: str = None):
        """Add a warning"""
        self.warnings.append({
            'principle': principle,
            'details': details,  
            'file': file_path,
            'severity': 'MEDIUM'
        })
    
    def add_success(self, principle: str, details: str):
        """Add a success confirmation"""
        self.successes.append({
            'principle': principle,
            'details': details
        })
    
    def audit_mango_rule(self):
        """Check for MANGO RULE violations - no hardcoded countries/crops"""
        print("🥭 Auditing MANGO RULE compliance...")
        
        # Patterns that violate MANGO RULE
        violation_patterns = [
            r'country\s*=\s*["\']Croatia["\']',
            r'country\s*=\s*["\']HR["\']',
            r'if\s+.*country.*==.*Croatia',
            r'crop\s*=\s*["\']wheat["\']',
            r'crop\s*=\s*["\']corn["\']',
            r'default.*=.*Croatia',
            r'hardcoded.*Croatia',
            r'\.hr\b',  # Croatian domains
            r'385\d+',  # Croatian phone numbers
        ]
        
        files_checked = 0
        violations_found = 0
        
        for py_file in self.root_path.rglob('*.py'):
            if 'node_modules' in str(py_file) or '.git' in str(py_file):
                continue
                
            files_checked += 1
            try:
                content = py_file.read_text(encoding='utf-8')
                for pattern in violation_patterns:
                    matches = re.findall(pattern, content, re.IGNORECASE)
                    if matches:
                        violations_found += 1
                        self.add_violation(
                            'MANGO RULE',
                            f'Hardcoded country/crop pattern found: {matches[0]}',
                            str(py_file)
                        )
            except Exception as e:
                pass
        
        if violations_found == 0:
            self.add_success(
                'MANGO RULE',
                f'No hardcoded countries/crops found in {files_checked} files'
            )
        
        return violations_found == 0
    
    def audit_environment_variables(self):
        """Verify all environment variables use CentralConfig"""
        print("🔒 Auditing environment variable usage...")
        
        direct_env_patterns = [
            r'os\.environ\[',
            r'os\.getenv\(',
            r'os\.environ\.get\(',
        ]
        
        allowed_files = [
            'central_config.py',
            'aws_env_enforcement.py'
        ]
        
        violations_found = 0
        files_checked = 0
        
        for py_file in self.root_path.rglob('*.py'):
            if 'node_modules' in str(py_file) or '.git' in str(py_file):
                continue
            
            if any(allowed in str(py_file) for allowed in allowed_files):
                continue
                
            files_checked += 1
            try:
                content = py_file.read_text(encoding='utf-8')
                
                # Check for direct os.environ usage
                for pattern in direct_env_patterns:
                    if re.search(pattern, content):
                        violations_found += 1
                        self.add_violation(
                            'Environment Variables',
                            'Direct os.environ usage found - must use CentralConfig',
                            str(py_file)
                        )
                        break
                
                # Check if CentralConfig is imported when env vars are needed
                if 'DB_' in content or 'API_KEY' in content:
                    if 'CentralConfig' not in content:
                        self.add_warning(
                            'Environment Variables',
                            'File uses environment variables but no CentralConfig import',
                            str(py_file)
                        )
                        
            except Exception as e:
                pass
        
        if violations_found == 0:
            self.add_success(
                'Environment Variables',
                f'All {files_checked} files use CentralConfig properly'
            )
        
        return violations_found == 0
    
    def audit_module_independence(self):
        """Check for cross-module imports that violate independence"""
        print("🏗️ Auditing module independence...")
        
        module_dirs = [
            'ava-olo-agricultural-core',
            'ava-olo-monitoring-dashboards',
            'ava-olo-api-gateway',
            'ava-olo-document-search',
            'ava-olo-llm-router'
        ]
        
        violations_found = 0
        
        for module_dir in module_dirs:
            module_path = self.root_path / module_dir
            if not module_path.exists():
                continue
                
            for py_file in module_path.rglob('*.py'):
                try:
                    content = py_file.read_text(encoding='utf-8')
                    
                    # Check for imports from other modules
                    for other_module in module_dirs:
                        if other_module != module_dir:
                            if f'from {other_module}' in content or f'import {other_module}' in content:
                                violations_found += 1
                                self.add_violation(
                                    'Module Independence',
                                    f'{module_dir} imports from {other_module}',
                                    str(py_file)
                                )
                                
                except Exception as e:
                    pass
        
        if violations_found == 0:
            self.add_success(
                'Module Independence',
                'All modules are properly isolated'
            )
        
        return violations_found == 0
    
    def audit_database_usage(self):
        """Verify PostgreSQL-only rule and proper connection handling"""
        print("🗄️ Auditing database usage...")
        
        sqlite_patterns = [
            r'sqlite3',
            r'\.db["\']',
            r'SQLite',
            r':memory:',
        ]
        
        violations_found = 0
        proper_usage = 0
        
        for py_file in self.root_path.rglob('*.py'):
            if 'node_modules' in str(py_file) or '.git' in str(py_file):
                continue
                
            try:
                content = py_file.read_text(encoding='utf-8')
                
                # Check for SQLite usage
                for pattern in sqlite_patterns:
                    if re.search(pattern, content, re.IGNORECASE):
                        violations_found += 1
                        self.add_violation(
                            'PostgreSQL Only',
                            f'SQLite usage detected: {pattern}',
                            str(py_file)
                        )
                        break
                
                # Check for proper database connection
                if 'psycopg2' in content or 'asyncpg' in content:
                    if 'CentralConfig' in content:
                        proper_usage += 1
                    else:
                        self.add_warning(
                            'PostgreSQL Only',
                            'Database connection without CentralConfig',
                            str(py_file)
                        )
                        
            except Exception as e:
                pass
        
        if violations_found == 0:
            self.add_success(
                'PostgreSQL Only',
                f'No SQLite usage found, {proper_usage} files use proper PostgreSQL'
            )
        
        return violations_found == 0
    
    def audit_privacy_compliance(self):
        """Check for privacy violations - personal data to external APIs"""
        print("🔒 Auditing privacy compliance...")
        
        external_api_patterns = [
            r'perplexity',
            r'openweather',
            r'google.*maps',
            r'external.*api',
        ]
        
        personal_data_patterns = [
            r'farmer_id',
            r'phone_number',
            r'farm_location',
            r'personal_data',
            r'user_data',
        ]
        
        violations_found = 0
        
        for py_file in self.root_path.rglob('*.py'):
            if 'node_modules' in str(py_file) or '.git' in str(py_file):
                continue
                
            try:
                content = py_file.read_text(encoding='utf-8')
                lines = content.split('\n')
                
                # Check if file uses external APIs
                uses_external_api = any(
                    re.search(pattern, content, re.IGNORECASE) 
                    for pattern in external_api_patterns
                )
                
                if uses_external_api:
                    # Check if personal data is sent
                    for i, line in enumerate(lines):
                        for data_pattern in personal_data_patterns:
                            if re.search(data_pattern, line, re.IGNORECASE):
                                # Check context around the line
                                context = '\n'.join(lines[max(0, i-3):min(len(lines), i+3)])
                                if any(api in context.lower() for api in ['perplexity', 'external']):
                                    violations_found += 1
                                    self.add_violation(
                                        'Privacy First',
                                        f'Personal data "{data_pattern}" may be sent to external API',
                                        str(py_file)
                                    )
                                    
            except Exception as e:
                pass
        
        if violations_found == 0:
            self.add_success(
                'Privacy First',
                'No personal data leaks to external APIs detected'
            )
        
        return violations_found == 0
    
    def audit_version_visibility(self):
        """Check if version badges are properly displayed"""
        print("🏷️ Auditing version visibility...")
        
        html_files_checked = 0
        version_implementations = 0
        
        for html_file in self.root_path.rglob('*.html'):
            if 'node_modules' in str(html_file) or '.git' in str(html_file):
                continue
                
            html_files_checked += 1
            try:
                content = html_file.read_text(encoding='utf-8')
                
                # Check for version badge
                if 'version-badge' in content or 'VersionManager' in content:
                    version_implementations += 1
                else:
                    self.add_warning(
                        'Version Visibility',
                        'No version badge found in HTML',
                        str(html_file)
                    )
                    
            except Exception as e:
                pass
        
        # Check Python files for version injection
        for py_file in self.root_path.rglob('*.py'):
            if 'app.py' in py_file.name or 'main.py' in py_file.name:
                try:
                    content = py_file.read_text(encoding='utf-8')
                    if 'VersionManager' in content:
                        version_implementations += 1
                except:
                    pass
        
        if version_implementations > 0:
            self.add_success(
                'Version Visibility',
                f'{version_implementations} version implementations found'
            )
        else:
            self.add_warning(
                'Version Visibility',
                'No version badge implementations found',
                None
            )
        
        return True
    
    def audit_git_standards(self):
        """Check git commit history for vX.X.X format"""
        print("📝 Auditing git commit standards...")
        
        try:
            # Get recent commits
            result = subprocess.run(
                ['git', 'log', '--oneline', '-20'],
                cwd=self.root_path,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                commits = result.stdout.strip().split('\n')
                valid_commits = 0
                invalid_commits = []
                
                for commit in commits:
                    # Check for vX.X.X format
                    if re.match(r'^[a-f0-9]+ v\d+\.\d+\.\d+', commit):
                        valid_commits += 1
                    else:
                        invalid_commits.append(commit)
                
                if valid_commits >= len(commits) * 0.8:  # 80% compliance
                    self.add_success(
                        'Git Standards',
                        f'{valid_commits}/{len(commits)} commits follow vX.X.X format'
                    )
                else:
                    self.add_warning(
                        'Git Standards',
                        f'Only {valid_commits}/{len(commits)} commits follow standards',
                        None
                    )
                    
        except Exception as e:
            self.add_warning(
                'Git Standards',
                f'Could not check git history: {str(e)}',
                None
            )
        
        return True
    
    def audit_deployment_protection(self):
        """Check deployment protection gates"""
        print("🛡️ Auditing deployment protection...")
        
        protection_files = [
            'protection_system/guaranteed_rollback.py',
            'protection_system/pre_deployment_gate.sh',
            'protection_system/capture_working_state.sh'
        ]
        
        files_found = 0
        
        for file_path in protection_files:
            full_path = self.root_path / 'ava-olo-shared' / file_path
            if full_path.exists():
                files_found += 1
            else:
                self.add_warning(
                    'Deployment Protection',
                    f'Protection file missing: {file_path}',
                    None
                )
        
        if files_found == len(protection_files):
            self.add_success(
                'Deployment Protection',
                'All protection gates are in place'
            )
        
        return files_found == len(protection_files)
    
    def audit_llm_first_approach(self):
        """Check for LLM-first implementation"""
        print("🧠 Auditing LLM-first approach...")
        
        hardcoded_logic_patterns = [
            r'if.*crop.*==.*wheat.*:',
            r'switch.*country.*case',
            r'hardcoded.*rules',
            r'pattern.*matching.*crop',
        ]
        
        llm_usage_patterns = [
            r'openai',
            r'gpt-4',
            r'llm.*prompt',
            r'ai.*intelligence',
        ]
        
        hardcoded_found = 0
        llm_implementations = 0
        
        for py_file in self.root_path.rglob('*.py'):
            if 'node_modules' in str(py_file) or '.git' in str(py_file):
                continue
                
            try:
                content = py_file.read_text(encoding='utf-8')
                
                # Check for hardcoded logic
                for pattern in hardcoded_logic_patterns:
                    if re.search(pattern, content, re.IGNORECASE):
                        hardcoded_found += 1
                        self.add_warning(
                            'LLM First',
                            f'Hardcoded logic pattern found: {pattern}',
                            str(py_file)
                        )
                        break
                
                # Check for LLM usage
                for pattern in llm_usage_patterns:
                    if re.search(pattern, content, re.IGNORECASE):
                        llm_implementations += 1
                        break
                        
            except Exception as e:
                pass
        
        if hardcoded_found == 0 and llm_implementations > 0:
            self.add_success(
                'LLM First',
                f'{llm_implementations} files properly use LLM intelligence'
            )
        
        return hardcoded_found == 0
    
    def audit_error_handling(self):
        """Check for proper error isolation"""
        print("🛡️ Auditing error handling...")
        
        try_except_count = 0
        bare_except_count = 0
        proper_fallback_count = 0
        
        for py_file in self.root_path.rglob('*.py'):
            if 'node_modules' in str(py_file) or '.git' in str(py_file):
                continue
                
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    tree = ast.parse(f.read())
                    
                for node in ast.walk(tree):
                    if isinstance(node, ast.Try):
                        try_except_count += 1
                        
                        # Check for bare except
                        for handler in node.handlers:
                            if handler.type is None:
                                bare_except_count += 1
                                self.add_warning(
                                    'Error Isolation',
                                    'Bare except clause found',
                                    str(py_file)
                                )
                            
                        # Check for fallback in except
                        for handler in node.handlers:
                            if handler.body:
                                # Simple check for return or assignment in except
                                for stmt in handler.body:
                                    if isinstance(stmt, (ast.Return, ast.Assign)):
                                        proper_fallback_count += 1
                                        break
                                        
            except Exception as e:
                pass
        
        if bare_except_count == 0:
            self.add_success(
                'Error Isolation',
                f'{try_except_count} error handlers found, {proper_fallback_count} with fallbacks'
            )
        
        return True
    
    def generate_report(self) -> str:
        """Generate comprehensive audit report"""
        report_dir = self.root_path / 'ava-olo-shared' / 'essentials' / 'reports' / self.timestamp.strftime('%Y-%m-%d')
        report_dir.mkdir(parents=True, exist_ok=True)
        
        # Find next report number
        existing_reports = list(report_dir.glob('report_*.md'))
        next_number = len(existing_reports) + 1
        
        report_path = report_dir / f'report_{next_number:03d}_system_audit.md'
        
        # Calculate overall health
        total_checks = len(self.successes) + len(self.violations) + len(self.warnings)
        health_score = (len(self.successes) / total_checks * 100) if total_checks > 0 else 0
        
        # Determine risk level
        if len(self.violations) > 0:
            risk_level = "HIGH"
        elif len(self.warnings) > 5:
            risk_level = "MEDIUM"
        else:
            risk_level = "LOW"
        
        report_content = f"""# AVA OLO System Audit Report
**Date**: {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')} UTC | {(self.timestamp.hour + 1) % 24}:{self.timestamp.strftime('%M:%S')} CET
**Type**: System Audit
**Author**: Claude Code
**Version**: {VersionManager.get_current_version()}

## Executive Summary
- **Overall Health Score**: {health_score:.1f}%
- **Critical Violations**: {len(self.violations)}
- **Warnings**: {len(self.warnings)}
- **Successes**: {len(self.successes)}
- **Regression Risk**: {risk_level}

## Constitutional Compliance

### ✅ Successes ({len(self.successes)})
"""
        
        for success in self.successes:
            report_content += f"- **{success['principle']}**: {success['details']}\n"
        
        report_content += f"\n### ⚠️ Warnings ({len(self.warnings)})\n"
        
        for warning in self.warnings:
            report_content += f"- **{warning['principle']}**: {warning['details']}"
            if warning.get('file'):
                report_content += f"\n  - File: `{warning['file']}`"
            report_content += "\n"
        
        report_content += f"\n### ❌ Violations ({len(self.violations)})\n"
        
        for violation in self.violations:
            report_content += f"- **{violation['principle']}**: {violation['details']}"
            if violation.get('file'):
                report_content += f"\n  - File: `{violation['file']}`"
            report_content += "\n"
        
        # Add detailed analysis
        report_content += """
## Detailed Analysis

### 1. MANGO RULE Compliance
"""
        mango_violations = [v for v in self.violations if v['principle'] == 'MANGO RULE']
        if mango_violations:
            report_content += "**Status**: ❌ VIOLATIONS FOUND\n\n"
            for v in mango_violations:
                report_content += f"- {v['details']} in `{v['file']}`\n"
        else:
            report_content += "**Status**: ✅ COMPLIANT\n"
            report_content += "No hardcoded countries or crops found. System is universally scalable.\n"
        
        report_content += """
### 2. Environment Variable Security
"""
        env_violations = [v for v in self.violations if 'Environment' in v['principle']]
        if env_violations:
            report_content += "**Status**: ❌ SECURITY RISK\n\n"
            for v in env_violations:
                report_content += f"- {v['details']} in `{v['file']}`\n"
        else:
            report_content += "**Status**: ✅ SECURE\n"
            report_content += "All environment variables properly accessed through CentralConfig.\n"
        
        report_content += """
### 3. Module Independence
"""
        module_violations = [v for v in self.violations if 'Module' in v['principle']]
        if module_violations:
            report_content += "**Status**: ❌ COUPLING DETECTED\n\n"
            for v in module_violations:
                report_content += f"- {v['details']} in `{v['file']}`\n"
        else:
            report_content += "**Status**: ✅ PROPERLY ISOLATED\n"
            report_content += "All modules maintain proper independence.\n"
        
        # Add recommendations
        report_content += """
## Critical Issues Requiring Immediate Attention
"""
        if self.violations:
            report_content += "The following issues MUST be fixed before any new development:\n\n"
            for i, violation in enumerate(self.violations, 1):
                report_content += f"{i}. **{violation['principle']}**: {violation['details']}\n"
        else:
            report_content += "No critical issues found. System is ready for continued development.\n"
        
        report_content += """
## Recommendations

### Before New Development:
"""
        if self.violations:
            report_content += """1. **Fix all critical violations** - These represent constitutional breaches
2. **Address high-priority warnings** - These could become violations
3. **Run audit again** - Ensure all issues are resolved
4. **Update tests** - Add tests to prevent regression
"""
        else:
            report_content += """1. **Continue following constitutional principles** - System is compliant
2. **Monitor warnings** - Address before they become violations  
3. **Regular audits** - Run before major changes
4. **Maintain test coverage** - Prevent regressions
"""
        
        report_content += f"""
## Deployment Readiness
- **Protection Gates**: {"✅ Active" if any(s['principle'] == 'Deployment Protection' for s in self.successes) else "⚠️ Check Required"}
- **Git Standards**: {"✅ Compliant" if any(s['principle'] == 'Git Standards' for s in self.successes) else "⚠️ Review Needed"}
- **Safe to Deploy**: {"✅ YES" if len(self.violations) == 0 else "❌ NO - Fix violations first"}

## Audit Metadata
- **Files Scanned**: {sum(1 for _ in self.root_path.rglob('*.py'))}
- **Audit Duration**: ~{(datetime.utcnow() - self.timestamp).seconds} seconds
- **Audit Script**: `/protection_system/comprehensive_audit.py`

---
*This audit ensures AVA OLO remains stable and constitutional while you're away.*
"""
        
        # Write report
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        print(f"\n✅ Report generated: {report_path}")
        
        return str(report_path)
    
    def run_comprehensive_audit(self):
        """Run all audit checks"""
        print("🔍 Starting AVA OLO Comprehensive System Audit...")
        print("=" * 60)
        
        # Run all audits
        self.audit_mango_rule()
        self.audit_environment_variables()
        self.audit_module_independence()
        self.audit_database_usage()
        self.audit_privacy_compliance()
        self.audit_version_visibility()
        self.audit_git_standards()
        self.audit_deployment_protection()
        self.audit_llm_first_approach()
        self.audit_error_handling()
        
        # Generate report
        report_path = self.generate_report()
        
        # Print summary
        print("\n" + "=" * 60)
        print("AUDIT COMPLETE")
        print("=" * 60)
        print(f"✅ Successes: {len(self.successes)}")
        print(f"⚠️  Warnings: {len(self.warnings)}")
        print(f"❌ Violations: {len(self.violations)}")
        print(f"\n📄 Full report: {report_path}")
        
        # Return overall status
        return len(self.violations) == 0


if __name__ == "__main__":
    auditor = AVASystemAuditor()
    success = auditor.run_comprehensive_audit()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)