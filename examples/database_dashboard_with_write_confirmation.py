"""
Database Dashboard with Write Operation Confirmation
Example implementation showing how to handle INSERT/UPDATE/DELETE with user confirmation
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any
import logging
from implementation.dashboard_constitutional_integration import DashboardConstitutionalGuard

logger = logging.getLogger(__name__)
app = FastAPI(title="AVA OLO Database Dashboard with Write Confirmation")

class QueryRequest(BaseModel):
    query: str
    farmer_id: Optional[int] = None
    write_confirmation: Optional[str] = None  # User must type "INSERT", "UPDATE", or "DELETE" to confirm

class QueryResponse(BaseModel):
    success: bool
    results: Optional[Any] = None
    error: Optional[str] = None
    needs_confirmation: Optional[bool] = False
    confirmation_message: Optional[str] = None
    operation_type: Optional[str] = None

@app.post("/api/database/query", response_model=QueryResponse)
async def execute_database_query(request: QueryRequest):
    """
    Execute database query with constitutional validation and write operation confirmation
    """
    guard = DashboardConstitutionalGuard()
    
    try:
        # Step 1: Validate the natural language query
        query_validation = await guard.validate_natural_query(
            query=request.query,
            farmer_id=request.farmer_id,
            language="en"
        )
        
        if not query_validation['is_valid']:
            return QueryResponse(
                success=False,
                error=f"Query validation failed: {query_validation['violations']}"
            )
        
        # Step 2: Generate SQL from natural language (using your LLM)
        # This is where your LLM converts "enter a farmer Suad Sakić" to INSERT SQL
        generated_sql = await generate_sql_from_query(request.query)  # Your LLM function
        
        # Step 3: Validate the generated SQL with write confirmation check
        context = {
            'farmer_id': request.farmer_id,
            'write_confirmation': request.write_confirmation
        }
        
        sql_validation = await guard.validate_generated_sql(
            sql=generated_sql,
            original_query=request.query,
            context=context
        )
        
        # Check if confirmation is needed
        if sql_validation['needs_confirmation']:
            # Find the confirmation requirement
            for violation in sql_validation['safety_violations']:
                if violation['severity'] == 'CONFIRMATION_REQUIRED':
                    return QueryResponse(
                        success=False,
                        needs_confirmation=True,
                        operation_type=violation['operation'],
                        confirmation_message=violation['remedy'],
                        error=violation['description']
                    )
        
        # Check if SQL is approved
        if not sql_validation['sql_approved']:
            critical_errors = [v for v in sql_validation['safety_violations'] 
                             if v['severity'] == 'CRITICAL']
            if critical_errors:
                return QueryResponse(
                    success=False,
                    error=f"SQL validation failed: {critical_errors[0]['description']}"
                )
        
        # Step 4: Execute the SQL (only if approved or confirmed)
        results = await execute_sql(generated_sql)  # Your database execution function
        
        # Step 5: Validate the response before sending to user
        response_validation = await guard.validate_response(
            response=str(results),
            original_query=request.query,
            context={'farmer_id': request.farmer_id}
        )
        
        # Include any warnings
        warnings = [v for v in sql_validation['safety_violations'] 
                   if v['severity'] == 'WARNING']
        
        return QueryResponse(
            success=True,
            results=results,
            error=warnings[0]['description'] if warnings else None
        )
        
    except Exception as e:
        logger.error(f"Query execution error: {e}")
        return QueryResponse(
            success=False,
            error=str(e)
        )

# Example usage in your frontend JavaScript:
"""
async function executeDatabaseQuery(query) {
    // First attempt without confirmation
    let response = await fetch('/api/database/query', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            query: query,
            farmer_id: currentFarmerId
        })
    });
    
    let result = await response.json();
    
    // Check if confirmation is needed
    if (result.needs_confirmation) {
        // Show confirmation dialog
        const confirmationDialog = `
            <div class="confirmation-dialog">
                <h3>⚠️ Write Operation Confirmation Required</h3>
                <p>${result.confirmation_message}</p>
                <p>This will perform a <strong>${result.operation_type}</strong> operation.</p>
                <p>Type "${result.operation_type}" below to confirm:</p>
                <input type="text" id="confirmation-input" />
                <button onclick="confirmWriteOperation('${query}', '${result.operation_type}')">Confirm</button>
                <button onclick="cancelOperation()">Cancel</button>
            </div>
        `;
        showDialog(confirmationDialog);
        return;
    }
    
    // Display results normally
    displayResults(result);
}

async function confirmWriteOperation(originalQuery, operationType) {
    const confirmation = document.getElementById('confirmation-input').value;
    
    // Retry with confirmation
    let response = await fetch('/api/database/query', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            query: originalQuery,
            farmer_id: currentFarmerId,
            write_confirmation: confirmation
        })
    });
    
    let result = await response.json();
    displayResults(result);
}
"""

# Helper functions (implement these based on your system)
async def generate_sql_from_query(query: str) -> str:
    """Your LLM function to convert natural language to SQL"""
    # This is where the LLM converts "enter a farmer Suad Sakić" to INSERT SQL
    pass

async def execute_sql(sql: str) -> Any:
    """Your database execution function"""
    # This executes the SQL against your PostgreSQL database
    pass