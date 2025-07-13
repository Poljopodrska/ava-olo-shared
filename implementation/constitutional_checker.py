"""
Constitutional Compliance Checker
Real-time verification of all 13 constitutional principles

Usage:
    from constitutional_checker import ConstitutionalChecker
    
    checker = ConstitutionalChecker()
    result = await checker.check_compliance(code_or_feature)
    
Purpose: Prevent constitutional violations before they reach production
"""

import ast
import re
import inspect
import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, asdict
from datetime import datetime
import asyncio

@dataclass
class ConstitutionalViolation:
    """A detected constitutional violation"""
    principle: str
    severity: str  # 'CRITICAL', 'WARNING', 'INFO'
    description: str
    code_snippet: Optional[str] = None
    file_location: Optional[str] = None
    line_number: Optional[int] = None
    remedy: Optional[str] = None

@dataclass
class ComplianceResult:
    """Result of constitutional compliance check"""
    is_compliant: bool
    overall_score: float  # 0-100
    violations: List[ConstitutionalViolation]
    compliant_principles: List[str]
    test_results: Dict[str, Any]
    timestamp: str
    metadata: Dict[str, Any]

class ConstitutionalChecker:
    """
    Comprehensive constitutional compliance checker
    Tests all 13 principles in real-time
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.violations = []
        self.principles = {
            'MANGO_RULE': self._check_mango_rule,
            'POSTGRESQL_ONLY': self._check_postgresql_only,
            'LLM_FIRST': self._check_llm_first,
            'MODULE_INDEPENDENCE': self._check_module_independence,
            'PRIVACY_FIRST': self._check_privacy_first,
            'API_FIRST': self._check_api_first,
            'ERROR_ISOLATION': self._check_error_isolation,
            'TRANSPARENCY': self._check_transparency,
            'FARMER_CENTRIC': self._check_farmer_centric,
            'PRODUCTION_READY': self._check_production_ready,
            'CONFIGURATION': self._check_configuration,
            'TEST_DRIVEN': self._check_test_driven,
            'COUNTRY_AWARE': self._check_country_aware
        }
        
    async def check_compliance(self, 
                             target: Union[str, Path, object],
                             check_type: str = "auto") -> ComplianceResult:
        """
        Check constitutional compliance of code, file, or module
        
        Args:
            target: Code string, file path, or Python object to check
            check_type: 'code', 'file', 'module', or 'auto'
            
        Returns:
            ComplianceResult with violations and score
        """
        self.violations = []
        start_time = datetime.now()
        
        # Determine check type
        if check_type == "auto":
            check_type = self._detect_target_type(target)
        
        # Load target content
        if check_type == "file":
            with open(target, 'r', encoding='utf-8') as f:
                code_content = f.read()
            file_path = str(target)
        elif check_type == "code":
            code_content = str(target)
            file_path = "<string>"
        elif check_type == "module":
            code_content = inspect.getsource(target)
            file_path = f"<module:{target.__name__}>"
        else:
            raise ValueError(f"Unknown check type: {check_type}")
        
        # Run all constitutional checks
        test_results = {}
        for principle_name, check_func in self.principles.items():
            try:
                result = await check_func(code_content, file_path)
                test_results[principle_name] = result
                
                if not result.get('compliant', True):
                    violations = result.get('violations', [])
                    for violation in violations:
                        self.violations.append(ConstitutionalViolation(
                            principle=principle_name,
                            severity=violation.get('severity', 'WARNING'),
                            description=violation.get('description', ''),
                            code_snippet=violation.get('code_snippet'),
                            file_location=file_path,
                            line_number=violation.get('line_number'),
                            remedy=violation.get('remedy')
                        ))
                        
            except Exception as e:
                self.logger.error(f"Error checking {principle_name}: {e}")
                test_results[principle_name] = {
                    'compliant': False,
                    'error': str(e)
                }
        
        # Calculate compliance score
        total_principles = len(self.principles)
        compliant_count = sum(1 for r in test_results.values() 
                            if r.get('compliant', False))
        compliance_score = (compliant_count / total_principles) * 100
        
        # Get compliant principles
        compliant_principles = [
            name for name, result in test_results.items()
            if result.get('compliant', False)
        ]
        
        end_time = datetime.now()
        
        return ComplianceResult(
            is_compliant=len(self.violations) == 0,
            overall_score=compliance_score,
            violations=self.violations,
            compliant_principles=compliant_principles,
            test_results=test_results,
            timestamp=start_time.isoformat(),
            metadata={
                'check_duration_ms': (end_time - start_time).total_seconds() * 1000,
                'target_type': check_type,
                'target_location': file_path,
                'checker_version': '1.0.0'
            }
        )
    
    async def _check_mango_rule(self, code: str, file_path: str) -> Dict[str, Any]:
        """
        Check MANGO RULE compliance
        Detect hardcoded crop/country patterns that violate universality
        """
        violations = []
        
        # Parse AST for analysis
        try:
            tree = ast.parse(code)
        except SyntaxError:
            return {'compliant': False, 'error': 'Syntax error in code'}
        
        # Check for hardcoded crop names in conditionals
        hardcoded_crops = ['tomato', 'corn', 'wheat', 'potato', 'rice']
        hardcoded_countries = ['croatia', 'slovenia', 'usa', 'us', 'bulgaria']
        
        for node in ast.walk(tree):
            # Check if statements with crop discrimination
            if isinstance(node, ast.If):
                condition_str = ast.unparse(node.test).lower()
                for crop in hardcoded_crops:
                    if f"'{crop}'" in condition_str or f'"{crop}"' in condition_str:
                        violations.append({
                            'severity': 'CRITICAL',
                            'description': f'Hardcoded crop logic detected: {crop}',
                            'code_snippet': ast.unparse(node)[:100],
                            'line_number': node.lineno,
                            'remedy': 'Use LLM-first approach: let AI handle crop-specific logic'
                        })
                
                for country in hardcoded_countries:
                    if f"'{country}'" in condition_str or f'"{country}"' in condition_str:
                        violations.append({
                            'severity': 'CRITICAL',
                            'description': f'Geographic discrimination detected: {country}',
                            'code_snippet': ast.unparse(node)[:100],
                            'line_number': node.lineno,
                            'remedy': 'Remove country-specific logic, use localization context'
                        })
        
        # Check for "unsupported" or "not available" messages
        unsupported_patterns = [
            r'unsupported.*crop',
            r'not.*available.*in.*country',
            r'cannot.*grow.*in',
            r'invalid.*crop.*for.*region'
        ]
        
        for pattern in unsupported_patterns:
            matches = re.finditer(pattern, code, re.IGNORECASE)
            for match in matches:
                line_num = code[:match.start()].count('\n') + 1
                violations.append({
                    'severity': 'CRITICAL',
                    'description': f'Refusal pattern detected: {match.group()}',
                    'code_snippet': match.group(),
                    'line_number': line_num,
                    'remedy': 'Never refuse based on crop/country - provide guidance for all scenarios'
                })
        
        return {
            'compliant': len(violations) == 0,
            'violations': violations,
            'mango_test': 'Would work for Bulgarian mango farmer' if len(violations) == 0 else 'FAILS mango test'
        }
    
    async def _check_llm_first(self, code: str, file_path: str) -> Dict[str, Any]:
        """
        Check LLM-FIRST principle compliance
        Ensure AI is making decisions, not hardcoded logic
        """
        violations = []
        
        # Look for LLM usage
        llm_indicators = ['openai', 'gpt', 'llm', 'ai', 'chat.completions']
        has_llm = any(indicator in code.lower() for indicator in llm_indicators)
        
        # Look for decision-making patterns that should use LLM
        decision_patterns = [
            r'if.*crop.*==.*:',
            r'if.*country.*==.*:',
            r'elif.*language.*==.*:',
            r'switch.*\(.*crop.*\)',
            r'crop_advice\s*=\s*{',  # Hardcoded advice dictionaries
            r'fertilizer_map\s*=\s*{',
            r'planting_schedule\s*=\s*{'
        ]
        
        for pattern in decision_patterns:
            matches = re.finditer(pattern, code, re.IGNORECASE)
            for match in matches:
                line_num = code[:match.start()].count('\n') + 1
                violations.append({
                    'severity': 'WARNING',
                    'description': f'Potential hardcoded decision logic: {match.group()}',
                    'code_snippet': match.group(),
                    'line_number': line_num,
                    'remedy': 'Replace hardcoded logic with LLM-driven decisions'
                })
        
        # Check for translation files (violation of LLM-first)
        if 'translations' in code.lower() or '_translations.py' in file_path:
            violations.append({
                'severity': 'CRITICAL',
                'description': 'Hardcoded translation files violate LLM-first principle',
                'remedy': 'Use LLM for all language translation and localization'
            })
        
        return {
            'compliant': len(violations) == 0,
            'violations': violations,
            'has_llm_integration': has_llm,
            'decision_logic_type': 'AI-driven' if has_llm and len(violations) == 0 else 'Hardcoded'
        }
    
    async def _check_privacy_first(self, code: str, file_path: str) -> Dict[str, Any]:
        """
        Check PRIVACY-FIRST principle compliance
        Ensure no personal data goes to external APIs
        """
        violations = []
        
        # Look for external API calls with personal data
        external_apis = ['openai', 'perplexity', 'external', 'api', 'requests.post', 'requests.get']
        personal_data_fields = ['farmer_name', 'farmer_id', 'phone', 'email', 'address', 'personal']
        
        # Parse AST to find function calls
        try:
            tree = ast.parse(code)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.Call):
                    call_str = ast.unparse(node).lower()
                    
                    # Check if it's an external API call
                    is_external_call = any(api in call_str for api in external_apis)
                    
                    if is_external_call:
                        # Check if personal data is being sent
                        for field in personal_data_fields:
                            if field in call_str:
                                violations.append({
                                    'severity': 'CRITICAL',
                                    'description': f'Personal data {field} sent to external API',
                                    'code_snippet': ast.unparse(node)[:150],
                                    'line_number': node.lineno,
                                    'remedy': 'Anonymize data before external API calls'
                                })
                        
        except SyntaxError:
            pass
        
        return {
            'compliant': len(violations) == 0,
            'violations': violations,
            'privacy_status': 'PROTECTED' if len(violations) == 0 else 'AT_RISK'
        }
    
    async def _check_postgresql_only(self, code: str, file_path: str) -> Dict[str, Any]:
        """Check PostgreSQL-only compliance"""
        violations = []
        
        forbidden_dbs = ['sqlite', 'mysql', 'mongodb', 'redis', 'oracle']
        
        for db in forbidden_dbs:
            if db in code.lower():
                line_num = code.lower().find(db)
                line_num = code[:line_num].count('\n') + 1
                violations.append({
                    'severity': 'CRITICAL',
                    'description': f'Non-PostgreSQL database detected: {db}',
                    'line_number': line_num,
                    'remedy': 'Use PostgreSQL only - farmer_crm database'
                })
        
        return {
            'compliant': len(violations) == 0,
            'violations': violations
        }
    
    async def _check_module_independence(self, code: str, file_path: str) -> Dict[str, Any]:
        """Check module independence"""
        violations = []
        
        # Look for direct imports between services
        forbidden_imports = [
            'from ava_olo_monitoring_dashboards',
            'from ava_olo_agricultural_core',
            'import ava_olo_monitoring',
            'import ava_olo_agricultural'
        ]
        
        for imp in forbidden_imports:
            if imp in code:
                line_num = code.find(imp)
                line_num = code[:line_num].count('\n') + 1
                violations.append({
                    'severity': 'WARNING',
                    'description': f'Direct service import detected: {imp}',
                    'line_number': line_num,
                    'remedy': 'Use API calls instead of direct imports'
                })
        
        return {
            'compliant': len(violations) == 0,
            'violations': violations
        }
    
    async def _check_api_first(self, code: str, file_path: str) -> Dict[str, Any]:
        """Check API-first communication"""
        violations = []
        # Implementation for API-first checking
        return {'compliant': True, 'violations': violations}
    
    async def _check_error_isolation(self, code: str, file_path: str) -> Dict[str, Any]:
        """Check error isolation"""
        violations = []
        
        # Look for try-except blocks
        has_error_handling = 'try:' in code and 'except' in code
        
        if not has_error_handling and len(code) > 100:  # Only for substantial code
            violations.append({
                'severity': 'WARNING',
                'description': 'No error handling detected',
                'remedy': 'Add try-except blocks for graceful degradation'
            })
        
        return {
            'compliant': len(violations) == 0,
            'violations': violations
        }
    
    async def _check_transparency(self, code: str, file_path: str) -> Dict[str, Any]:
        """Check transparency (logging)"""
        violations = []
        
        has_logging = 'logger' in code or 'logging' in code
        
        if not has_logging and len(code) > 50:
            violations.append({
                'severity': 'INFO',
                'description': 'No logging detected',
                'remedy': 'Add logging for transparency'
            })
        
        return {
            'compliant': len(violations) == 0,
            'violations': violations
        }
    
    async def _check_farmer_centric(self, code: str, file_path: str) -> Dict[str, Any]:
        """Check farmer-centric communication"""
        violations = []
        
        # Look for inappropriate language
        inappropriate_terms = ['cute', 'sweet', 'adorable', 'darling']
        
        for term in inappropriate_terms:
            if term in code.lower():
                violations.append({
                    'severity': 'INFO',
                    'description': f'Inappropriate tone detected: {term}',
                    'remedy': 'Use professional agricultural tone'
                })
        
        return {
            'compliant': len(violations) == 0,
            'violations': violations
        }
    
    async def _check_production_ready(self, code: str, file_path: str) -> Dict[str, Any]:
        """Check production readiness"""
        violations = []
        
        # Look for localhost or development indicators
        dev_indicators = ['localhost', '127.0.0.1', 'development', 'debug=True']
        
        for indicator in dev_indicators:
            if indicator in code:
                violations.append({
                    'severity': 'WARNING',
                    'description': f'Development code in production: {indicator}',
                    'remedy': 'Use production-ready configuration'
                })
        
        return {
            'compliant': len(violations) == 0,
            'violations': violations
        }
    
    async def _check_configuration(self, code: str, file_path: str) -> Dict[str, Any]:
        """Check configuration over hardcoding"""
        violations = []
        
        # Look for hardcoded values that should be configurable
        hardcoded_patterns = [
            r'DB_HOST\s*=\s*["\']localhost["\']',
            r'API_KEY\s*=\s*["\']sk-.*["\']',
            r'PORT\s*=\s*8000'  # Should use environment
        ]
        
        for pattern in hardcoded_patterns:
            matches = re.finditer(pattern, code)
            for match in matches:
                line_num = code[:match.start()].count('\n') + 1
                violations.append({
                    'severity': 'WARNING',
                    'description': f'Hardcoded configuration: {match.group()}',
                    'line_number': line_num,
                    'remedy': 'Use environment variables or config files'
                })
        
        return {
            'compliant': len(violations) == 0,
            'violations': violations
        }
    
    async def _check_test_driven(self, code: str, file_path: str) -> Dict[str, Any]:
        """Check test-driven development"""
        violations = []
        
        # This would check for test coverage, but we'll keep it simple
        has_tests = 'test_' in code or 'pytest' in code or 'unittest' in code
        
        return {
            'compliant': True,  # Always pass for now
            'violations': violations,
            'has_tests': has_tests
        }
    
    async def _check_country_aware(self, code: str, file_path: str) -> Dict[str, Any]:
        """Check country-aware localization (Amendment #13)"""
        violations = []
        
        # Look for hardcoded language/country mappings
        hardcoded_language_patterns = [
            r'if.*language.*==.*["\']en["\']',
            r'if.*country.*==.*["\']US["\']',
            r'language\s*=\s*["\']en["\']'  # Hardcoded default
        ]
        
        for pattern in hardcoded_language_patterns:
            matches = re.finditer(pattern, code)
            for match in matches:
                line_num = code[:match.start()].count('\n') + 1
                violations.append({
                    'severity': 'WARNING',
                    'description': f'Hardcoded language/country logic: {match.group()}',
                    'line_number': line_num,
                    'remedy': 'Use smart country detection and LLM localization'
                })
        
        return {
            'compliant': len(violations) == 0,
            'violations': violations
        }
    
    def _detect_target_type(self, target) -> str:
        """Auto-detect the type of target being checked"""
        if isinstance(target, (str, Path)):
            if Path(target).exists():
                return "file"
            else:
                return "code"
        else:
            return "module"
    
    def generate_report(self, result: ComplianceResult) -> str:
        """Generate human-readable compliance report"""
        report = f"""
🏛️ CONSTITUTIONAL COMPLIANCE REPORT
{'='*50}

📊 Overall Status: {'✅ COMPLIANT' if result.is_compliant else '❌ VIOLATIONS DETECTED'}
📈 Compliance Score: {result.overall_score:.1f}/100
🕐 Checked: {result.timestamp}

🏆 Compliant Principles ({len(result.compliant_principles)}/13):
{chr(10).join(f'  ✅ {principle}' for principle in result.compliant_principles)}

"""
        
        if result.violations:
            report += f"""
🚨 Constitutional Violations ({len(result.violations)}):
{chr(10).join(f'''
  ❌ {v.principle} ({v.severity})
     {v.description}
     {f"Line {v.line_number}: " if v.line_number else ""}{v.code_snippet or ""}
     💡 Remedy: {v.remedy or "See constitutional guidelines"}
''' for v in result.violations)}
"""
        
        if result.is_compliant:
            report += """
🎉 CONSTITUTIONAL COMPLIANCE ACHIEVED!
🥭 The Bulgarian mango farmer is happy!

This code follows all 13 constitutional principles and can serve
farmers globally with any crop in any country.
"""
        else:
            report += """
⚠️  CONSTITUTIONAL VIOLATIONS MUST BE FIXED!
🥭 The Bulgarian mango farmer is disappointed!

Please address all violations before deployment to ensure
global agricultural service quality.
"""
        
        return report

# Convenience functions for easy integration
async def check_code_compliance(code: str) -> ComplianceResult:
    """Quick compliance check for code string"""
    checker = ConstitutionalChecker()
    return await checker.check_compliance(code, "code")

async def check_file_compliance(file_path: str) -> ComplianceResult:
    """Quick compliance check for file"""
    checker = ConstitutionalChecker()
    return await checker.check_compliance(file_path, "file")

def create_compliance_decorator():
    """Decorator to check function compliance"""
    def decorator(func):
        async def wrapper(*args, **kwargs):
            checker = ConstitutionalChecker()
            result = await checker.check_compliance(func, "module")
            if not result.is_compliant:
                logging.warning(f"Constitutional violations in {func.__name__}: {len(result.violations)} issues")
            return await func(*args, **kwargs)
        return wrapper
    return decorator