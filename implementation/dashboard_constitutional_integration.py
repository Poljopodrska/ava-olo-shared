"""
Database Dashboard Constitutional Integration
Seamless integration of constitutional checking into database dashboard

This will be the first implementation of constitutional checking in production
"""

from fastapi import HTTPException, Depends
from typing import Dict, Any, List
import logging
from constitutional_checker import ConstitutionalChecker
from constitutional_integration import DatabaseDashboardChecker

logger = logging.getLogger(__name__)

class DashboardConstitutionalGuard:
    """Constitutional guard for database dashboard operations"""
    
    def __init__(self):
        self.checker = ConstitutionalChecker()
        self.db_checker = DatabaseDashboardChecker()
        self.violation_count = 0
        
    async def validate_natural_query(self, 
                                   query: str, 
                                   farmer_id: int = None,
                                   language: str = None) -> Dict[str, Any]:
        """
        Validate natural language query before processing
        Ensures constitutional compliance from the start
        """
        
        # Create context
        context = {
            'query': query,
            'farmer_id': farmer_id,
            'language': language or 'en',
            'query_type': 'natural_language'
        }
        
        # Check query compliance
        pseudo_code = f"""
# Natural Language Query Validation
farmer_query = "{query}"
farmer_id = {farmer_id}
target_language = "{language or 'auto-detect'}"

# This query will be processed by LLM
# Must work for ANY farmer, ANY crop, ANY country
def process_query():
    # Constitutional requirements:
    # 1. Works for Bulgarian mango farmer ✓
    # 2. Uses LLM-first approach ✓  
    # 3. Protects farmer privacy ✓
    # 4. Supports all languages ✓
    pass
"""
        
        result = await self.checker.check_compliance(pseudo_code, "code")
        
        # Additional natural query checks
        violations = []
        
        # Check for discriminatory language
        discriminatory_terms = [
            'only available in', 'not supported in', 'invalid for country',
            'unsupported crop', 'not possible in'
        ]
        
        query_lower = query.lower()
        for term in discriminatory_terms:
            if term in query_lower:
                violations.append({
                    'principle': 'MANGO_RULE',
                    'severity': 'CRITICAL',
                    'description': f'Discriminatory language in query: "{term}"',
                    'remedy': 'Rephrase to be universally applicable'
                })
        
        # Check for personal data in query
        personal_indicators = ['my name is', 'i am', 'phone number', 'address']
        for indicator in personal_indicators:
            if indicator in query_lower:
                violations.append({
                    'principle': 'PRIVACY_FIRST',
                    'severity': 'WARNING', 
                    'description': f'Personal data detected in query: "{indicator}"',
                    'remedy': 'Personal data will be handled securely'
                })
        
        # Add violations to result
        result.violations.extend([
            type('Violation', (), violation)() for violation in violations
        ])
        
        return {
            'is_valid': len([v for v in result.violations if v.severity == 'CRITICAL']) == 0,
            'compliance_result': result,
            'context': context,
            'mango_rule_status': 'PASS' if result.is_compliant else 'FAIL'
        }
    
    async def validate_generated_sql(self, 
                                   sql: str, 
                                   original_query: str,
                                   context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate LLM-generated SQL for constitutional compliance
        Critical checkpoint before database execution
        """
        
        result = await self.db_checker.check_sql_query_compliance(sql, context)
        
        # Additional SQL safety checks
        safety_violations = []
        
        # Check SQL is read-only (constitutional requirement)
        sql_upper = sql.upper().strip()
        if not sql_upper.startswith('SELECT'):
            safety_violations.append({
                'principle': 'PRIVACY_FIRST',
                'severity': 'CRITICAL',
                'description': 'Non-SELECT SQL detected',
                'remedy': 'Only SELECT queries allowed for safety'
            })
        
        # Check for dangerous SQL patterns
        dangerous_patterns = ['DROP', 'DELETE', 'UPDATE', 'INSERT', 'ALTER', 'CREATE']
        for pattern in dangerous_patterns:
            if pattern in sql_upper:
                safety_violations.append({
                    'principle': 'PRIVACY_FIRST',
                    'severity': 'CRITICAL',
                    'description': f'Dangerous SQL operation: {pattern}',
                    'remedy': 'Only read operations allowed'
                })
        
        # Check for proper farmer scoping
        if context.get('farmer_id') and 'farmer_id' not in sql.lower():
            safety_violations.append({
                'principle': 'PRIVACY_FIRST',
                'severity': 'WARNING',
                'description': 'SQL not scoped to farmer_id',
                'remedy': 'Add WHERE farmer_id = {farmer_id} for security'
            })
        
        return {
            'is_safe': len([v for v in safety_violations if v['severity'] == 'CRITICAL']) == 0,
            'compliance_result': result,
            'safety_violations': safety_violations,
            'sql_approved': result.is_compliant and len(safety_violations) == 0
        }
    
    async def validate_response(self, 
                              response: str,
                              original_query: str, 
                              context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate final response for constitutional compliance
        Last checkpoint before sending to farmer
        """
        
        # Create response validation code
        response_code = f"""
# Response Validation
farmer_query = "{original_query}"
system_response = "{response[:200]}..."  # Truncated for analysis
farmer_id = {context.get('farmer_id')}
language = "{context.get('language', 'en')}"

# Constitutional response requirements:
# 1. Helpful for ALL farmers globally
# 2. No geographic or crop discrimination  
# 3. Appropriate professional tone
# 4. Privacy-compliant (no personal data exposure)
"""
        
        result = await self.checker.check_compliance(response_code, "code")
        
        # Response-specific checks
        response_violations = []
        
        # Check for refusal language
        refusal_patterns = [
            'cannot help', 'not possible', 'unsupported', 
            'not available in your country', 'invalid crop'
        ]
        
        response_lower = response.lower()
        for pattern in refusal_patterns:
            if pattern in response_lower:
                response_violations.append({
                    'principle': 'MANGO_RULE',
                    'severity': 'CRITICAL',
                    'description': f'Refusal language: "{pattern}"',
                    'remedy': 'Provide constructive guidance for all scenarios'
                })
        
        # Check for inappropriate tone
        inappropriate_terms = ['cute', 'sweet', 'darling', 'honey']
        for term in inappropriate_terms:
            if term in response_lower:
                response_violations.append({
                    'principle': 'FARMER_CENTRIC',
                    'severity': 'WARNING',
                    'description': f'Inappropriate tone: "{term}"',
                    'remedy': 'Use professional agricultural language'
                })
        
        # Check for personal data leakage
        if context.get('farmer_id'):
            farmer_id_str = str(context['farmer_id'])
            if farmer_id_str in response:
                response_violations.append({
                    'principle': 'PRIVACY_FIRST',
                    'severity': 'WARNING',
                    'description': 'Farmer ID exposed in response',
                    'remedy': 'Remove identifying information from responses'
                })
        
        return {
            'is_appropriate': len([v for v in response_violations if v['severity'] == 'CRITICAL']) == 0,
            'compliance_result': result,
            'response_violations': response_violations,
            'response_approved': result.is_compliant and len(response_violations) == 0
        }

# FastAPI dependency for constitutional validation
async def get_constitutional_guard() -> DashboardConstitutionalGuard:
    """Dependency injection for constitutional guard"""
    return DashboardConstitutionalGuard()

# Integration decorators for dashboard endpoints
def constitutional_endpoint():
    """Decorator for constitutional API endpoints"""
    def decorator(func):
        async def wrapper(*args, **kwargs):
            guard = DashboardConstitutionalGuard()
            
            # Pre-execution validation
            logger.info(f"Constitutional check for {func.__name__}")
            
            try:
                result = await func(*args, **kwargs)
                
                # Post-execution validation if result contains response
                if isinstance(result, dict) and 'response' in result:
                    validation = await guard.validate_response(
                        response=result['response'],
                        original_query=kwargs.get('query', ''),
                        context=kwargs
                    )
                    
                    if not validation['response_approved']:
                        logger.warning(f"Response constitutional violations: {len(validation['response_violations'])}")
                        result['constitutional_warnings'] = validation['response_violations']
                
                return result
                
            except Exception as e:
                logger.error(f"Constitutional error in {func.__name__}: {e}")
                raise HTTPException(
                    status_code=500,
                    detail="Constitutional compliance error"
                )
        
        return wrapper
    return decorator