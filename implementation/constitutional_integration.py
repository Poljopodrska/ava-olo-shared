"""
Constitutional Integration Helper
Easy integration of constitutional checking into existing systems

Usage examples:
1. Database dashboard integration
2. API endpoint validation
3. Real-time compliance monitoring
"""

from fastapi import HTTPException
from typing import Any, Dict
import asyncio
import json
from constitutional_checker import ConstitutionalChecker, ComplianceResult

class ConstitutionalMiddleware:
    """Middleware for constitutional compliance checking"""
    
    def __init__(self, enable_realtime: bool = True):
        self.checker = ConstitutionalChecker()
        self.enable_realtime = enable_realtime
        
    async def check_request_compliance(self, request_data: Dict[str, Any]) -> ComplianceResult:
        """Check if request data follows constitutional principles"""
        # Convert request to code-like structure for checking
        code_representation = self._request_to_code(request_data)
        return await self.checker.check_compliance(code_representation, "code")
    
    def _request_to_code(self, request_data: Dict[str, Any]) -> str:
        """Convert request data to checkable code format"""
        # Simple conversion - in practice this could be more sophisticated
        return f"""
# Generated from request data
query = "{request_data.get('query', '')}"
farmer_id = {request_data.get('farmer_id', 'None')}
language = "{request_data.get('language', '')}"
country = "{request_data.get('country', '')}"
"""

class DatabaseDashboardChecker:
    """Specific checker for database dashboard compliance"""
    
    def __init__(self):
        self.checker = ConstitutionalChecker()
    
    async def check_sql_query_compliance(self, sql_query: str, context: Dict[str, Any]) -> ComplianceResult:
        """Check if generated SQL follows constitutional principles"""
        
        # Create pseudo-code representation
        pseudo_code = f"""
# SQL Query Compliance Check
sql_query = '''{sql_query}'''
farmer_id = {context.get('farmer_id', 'None')}
language = "{context.get('language', 'en')}"
context = {json.dumps(context, indent=2)}
"""
        
        result = await self.checker.check_compliance(pseudo_code, "code")
        
        # Add SQL-specific checks
        sql_violations = await self._check_sql_specific(sql_query, context)
        result.violations.extend(sql_violations)
        
        return result
    
    async def _check_sql_specific(self, sql: str, context: Dict[str, Any]) -> list:
        """SQL-specific constitutional checks"""
        violations = []
        
        # Check for hardcoded crop names in SQL
        hardcoded_crops = ['tomato', 'corn', 'wheat', 'potato']
        sql_lower = sql.lower()
        
        for crop in hardcoded_crops:
            if f"'{crop}'" in sql_lower or f'"{crop}"' in sql_lower:
                violations.append({
                    'principle': 'MANGO_RULE',
                    'severity': 'CRITICAL',
                    'description': f'Hardcoded crop in SQL: {crop}',
                    'code_snippet': sql[:100],
                    'remedy': 'Use parameterized queries, let LLM generate crop-agnostic SQL'
                })
        
        # Check for geographic discrimination
        hardcoded_countries = ['croatia', 'usa', 'us', 'bulgaria']
        for country in hardcoded_countries:
            if f"'{country}'" in sql_lower:
                violations.append({
                    'principle': 'MANGO_RULE',
                    'severity': 'CRITICAL', 
                    'description': f'Geographic discrimination in SQL: {country}',
                    'code_snippet': sql[:100],
                    'remedy': 'Use country_code parameter, support all countries equally'
                })
        
        # Check for privacy violations (personal data exposure)
        privacy_fields = ['farmer_name', 'phone', 'email', 'address']
        for field in privacy_fields:
            if field in sql_lower and 'select' in sql_lower:
                violations.append({
                    'principle': 'PRIVACY_FIRST',
                    'severity': 'WARNING',
                    'description': f'Personal data in SELECT: {field}',
                    'code_snippet': sql[:100],
                    'remedy': 'Ensure personal data is properly protected and anonymized'
                })
        
        return violations

# Integration decorators
def constitutional_check():
    """Decorator for constitutional compliance checking"""
    def decorator(func):
        async def wrapper(*args, **kwargs):
            checker = ConstitutionalChecker()
            
            # Check function compliance
            result = await checker.check_compliance(func, "module")
            
            if not result.is_compliant:
                critical_violations = [v for v in result.violations if v.severity == 'CRITICAL']
                if critical_violations:
                    raise HTTPException(
                        status_code=500,
                        detail=f"Constitutional violations prevent execution: {len(critical_violations)} critical issues"
                    )
            
            # Execute function
            return await func(*args, **kwargs)
        return wrapper
    return decorator

def mango_rule_check():
    """Specific decorator for MANGO RULE compliance"""
    def decorator(func):
        async def wrapper(*args, **kwargs):
            # Quick mango rule check
            result = await quick_mango_check(func, args, kwargs)
            if not result['passes']:
                raise HTTPException(
                    status_code=400,
                    detail=f"MANGO RULE violation: {result['reason']}"
                )
            return await func(*args, **kwargs)
        return wrapper
    return decorator

async def quick_mango_check(func, args, kwargs) -> Dict[str, Any]:
    """Quick check if function call would work for Bulgarian mango farmer"""
    
    # Check arguments for hardcoded limitations
    for arg in args:
        if isinstance(arg, str):
            if 'not supported' in arg.lower() or 'invalid crop' in arg.lower():
                return {
                    'passes': False,
                    'reason': 'Function refuses certain crops/scenarios'
                }
    
    for key, value in kwargs.items():
        if isinstance(value, str):
            if 'bulgaria' in value.lower() and 'not' in value.lower():
                return {
                    'passes': False,
                    'reason': 'Geographic discrimination detected'
                }
    
    return {'passes': True, 'reason': 'Mango rule compliant'}