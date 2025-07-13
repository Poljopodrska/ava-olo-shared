"""
Example: Constitutional Integration in Database Dashboard
Shows how to integrate constitutional checking into the existing database dashboard

This demonstrates the first production use of constitutional checking
"""

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, Dict, Any
import logging

# Import constitutional components
from constitutional_checker import ConstitutionalChecker
from dashboard_constitutional_integration import (
    DashboardConstitutionalGuard, 
    get_constitutional_guard,
    constitutional_endpoint
)

app = FastAPI(title="Constitutional Database Dashboard")
logger = logging.getLogger(__name__)

class QueryRequest(BaseModel):
    """Constitutional query request model"""
    query: str
    farmer_id: Optional[int] = None
    language: Optional[str] = None
    constitutional_check: bool = True

class QueryResponse(BaseModel):
    """Constitutional query response model"""
    success: bool
    response: str
    constitutional_compliance: bool
    mango_rule_status: str
    violations: list = []
    metadata: Dict[str, Any] = {}

@app.post("/api/constitutional-query", response_model=QueryResponse)
@constitutional_endpoint()
async def process_constitutional_query(
    request: QueryRequest,
    guard: DashboardConstitutionalGuard = Depends(get_constitutional_guard)
):
    """
    Process database query with full constitutional compliance checking
    
    This endpoint demonstrates the three-phase constitutional validation:
    1. Input validation (query)
    2. Processing validation (SQL) 
    3. Output validation (response)
    """
    
    try:
        # Phase 1: Validate incoming query
        logger.info(f"Phase 1: Validating natural query: {request.query[:50]}...")
        query_validation = await guard.validate_natural_query(
            query=request.query,
            farmer_id=request.farmer_id,
            language=request.language
        )
        
        if not query_validation['is_valid']:
            # Return constitutional violation error
            critical_violations = [
                v for v in query_validation['compliance_result'].violations 
                if v.severity == 'CRITICAL'
            ]
            
            return QueryResponse(
                success=False,
                response="Query contains constitutional violations",
                constitutional_compliance=False,
                mango_rule_status="FAIL",
                violations=[{
                    'principle': v.principle,
                    'description': v.description,
                    'remedy': v.remedy
                } for v in critical_violations],
                metadata={
                    'phase': 'input_validation',
                    'compliance_score': query_validation['compliance_result'].overall_score
                }
            )
        
        # Phase 2: Generate and validate SQL
        logger.info("Phase 2: Generating constitutional SQL...")
        generated_sql = await generate_constitutional_sql(
            request.query, 
            request.farmer_id, 
            request.language
        )
        
        sql_validation = await guard.validate_generated_sql(
            sql=generated_sql,
            original_query=request.query,
            context={
                'farmer_id': request.farmer_id,
                'language': request.language,
                'query_type': 'natural_language'
            }
        )
        
        if not sql_validation['sql_approved']:
            return QueryResponse(
                success=False,
                response="Generated SQL violates constitutional principles",
                constitutional_compliance=False,
                mango_rule_status="FAIL",
                violations=[{
                    'principle': 'SQL_SAFETY',
                    'description': 'Generated SQL is not constitutionally compliant',
                    'remedy': 'Review LLM SQL generation logic'
                }],
                metadata={
                    'phase': 'sql_validation',
                    'generated_sql': generated_sql[:100]
                }
            )
        
        # Phase 3: Execute query and validate response
        logger.info("Phase 3: Executing SQL and validating response...")
        query_results = await execute_constitutional_sql(generated_sql, request.farmer_id)
        
        # Generate natural language response
        natural_response = await generate_constitutional_response(
            query_results,
            request.query,
            request.language or 'en'
        )
        
        # Validate final response
        response_validation = await guard.validate_response(
            response=natural_response,
            original_query=request.query,
            context={
                'farmer_id': request.farmer_id,
                'language': request.language,
                'results_count': len(query_results) if query_results else 0
            }
        )
        
        # Prepare final response
        warnings = []
        if not response_validation['response_approved']:
            warnings = [{
                'type': 'constitutional_warning',
                'violations': response_validation['response_violations']
            }]
        
        return QueryResponse(
            success=True,
            response=natural_response,
            constitutional_compliance=response_validation['response_approved'],
            mango_rule_status="PASS",
            violations=warnings,
            metadata={
                'phase': 'complete',
                'sql_generated': generated_sql,
                'results_count': len(query_results) if query_results else 0,
                'compliance_score': response_validation['compliance_result'].overall_score
            }
        )
        
    except Exception as e:
        logger.error(f"Constitutional query processing error: {e}")
        return QueryResponse(
            success=False,
            response="Constitutional processing error occurred",
            constitutional_compliance=False,
            mango_rule_status="ERROR",
            violations=[{
                'principle': 'ERROR_ISOLATION',
                'description': str(e),
                'remedy': 'Check system logs and constitutional compliance'
            }],
            metadata={'phase': 'error', 'error': str(e)}
        )

async def generate_constitutional_sql(query: str, farmer_id: int, language: str) -> str:
    """
    Generate SQL using LLM with constitutional compliance
    This would integrate with existing LLM SQL generation
    """
    
    # Placeholder for LLM integration
    # In real implementation, this would call your existing LLM SQL generator
    # but with constitutional prompts
    
    constitutional_prompt = f"""
Generate PostgreSQL query for: {query}

Constitutional Requirements:
1. MANGO RULE: Must work for ANY crop (including mangoes in Bulgaria)
2. PRIVACY FIRST: Only SELECT queries, scope to farmer_id
3. LLM FIRST: No hardcoded crop/country logic
4. UNIVERSAL: Support all farmers globally

Farmer Context:
- farmer_id: {farmer_id}
- language: {language}

Generate SQL that follows all constitutional principles.
"""
    
    # Mock SQL generation (replace with actual LLM call)
    if farmer_id:
        sql = f"""
        SELECT f.field_name, fc.crop_name, fc.planting_date 
        FROM fields f 
        JOIN field_crops fc ON f.field_id = fc.field_id 
        WHERE f.farmer_id = {farmer_id}
        ORDER BY fc.planting_date DESC
        LIMIT 10
        """
    else:
        sql = "SELECT COUNT(*) as total_farmers FROM farmers WHERE is_active = true"
    
    return sql.strip()

async def execute_constitutional_sql(sql: str, farmer_id: int) -> list:
    """
    Execute SQL with constitutional safety checks
    """
    
    # Mock database execution (replace with actual database call)
    if "COUNT(*)" in sql:
        return [{"total_farmers": 1250}]
    else:
        return [
            {
                "field_name": "North Field",
                "crop_name": "Mango",  # Constitutional: Supports ANY crop
                "planting_date": "2024-03-15"
            },
            {
                "field_name": "South Field", 
                "crop_name": "Dragon Fruit",  # Constitutional: Exotic crops supported
                "planting_date": "2024-02-20"
            }
        ]

async def generate_constitutional_response(results: list, query: str, language: str) -> str:
    """
    Generate natural language response using LLM with constitutional principles
    """
    
    constitutional_response_prompt = f"""
Generate response for farmer query: {query}
Results: {results}
Language: {language}

Constitutional Requirements:
1. MANGO RULE: Work for any farmer globally with any crop
2. FARMER CENTRIC: Professional agricultural tone (not overly sweet)
3. HELPFUL: Provide constructive guidance always
4. PRIVACY: No personal identifying information
5. UNIVERSAL: No geographic or crop discrimination

Respond in {language} language with helpful agricultural guidance.
"""
    
    # Mock response generation (replace with actual LLM call)
    if language == 'bg':  # Bulgarian
        return "Имате 2 поля с екзотични култури - манго и драконов плод. Тези култури изискват специални грижи в българския климат."
    else:
        return f"You have {len(results)} fields with crops including exotic varieties. These crops require special care considerations for your climate zone."

@app.get("/api/constitutional-status")
async def get_constitutional_status():
    """
    Get overall constitutional compliance status of the system
    """
    checker = ConstitutionalChecker()
    
    # Check this file's constitutional compliance
    import inspect
    current_module = inspect.getmodule(inspect.currentframe())
    result = await checker.check_compliance(current_module, "module")
    
    return {
        "constitutional_compliance": result.is_compliant,
        "compliance_score": result.overall_score,
        "compliant_principles": result.compliant_principles,
        "violation_count": len(result.violations),
        "mango_rule_status": "PASS" if result.is_compliant else "NEEDS_WORK",
        "system_status": "Constitutional" if result.is_compliant else "Requires_Attention"
    }

@app.get("/health")
async def health_check():
    """Constitutional health check"""
    return {
        "status": "healthy",
        "constitutional_compliance": True,
        "mango_rule": "ACTIVE",
        "message": "Serving farmers globally with constitutional compliance"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)