# Database Write Operation Confirmation Guide

## Overview

The AVA OLO monitoring dashboards now support INSERT, UPDATE, and DELETE operations with a mandatory confirmation mechanism to prevent accidental data modifications.

## How It Works

### 1. Write Operation Detection
When the system detects an INSERT, UPDATE, or DELETE SQL query, it will:
- Block the operation initially
- Request explicit confirmation from the user
- Only proceed if the user types the exact operation name

### 2. Confirmation Flow

```python
# Example: User wants to insert a farmer
User Input: "Please enter a farmer Suad Sakić, wa number 043 223 443"
↓
System generates SQL: "INSERT INTO farmers (farm_name, ...) VALUES (...)"
↓
System Response: "INSERT operation detected - confirmation required. Please type 'INSERT' to confirm this write operation"
↓
User must type: "INSERT"
↓
System executes the INSERT query
```

### 3. Integration in Your Dashboard

To fix your existing database dashboard, you need to:

1. **Update the SQL validation context** to include write confirmation:

```python
# In your database query endpoint
context = {
    'farmer_id': request.farmer_id,
    'write_confirmation': request.write_confirmation  # Add this field
}

sql_validation = await guard.validate_generated_sql(
    sql=generated_sql,
    original_query=query,
    context=context
)
```

2. **Handle the confirmation requirement** in your response:

```python
if sql_validation['needs_confirmation']:
    return {
        'success': False,
        'needs_confirmation': True,
        'operation_type': sql_validation['write_operation'],
        'message': f"Please type '{sql_validation['write_operation']}' to confirm this operation"
    }
```

3. **Update your frontend** to handle confirmations:

```javascript
// Check if confirmation is needed
if (result.needs_confirmation) {
    const userConfirmation = prompt(result.message);
    
    // Retry with confirmation
    const confirmedResult = await fetch('/api/query', {
        method: 'POST',
        body: JSON.stringify({
            query: originalQuery,
            write_confirmation: userConfirmation
        })
    });
}
```

## Security Notes

### Still Blocked Operations
The following operations remain completely blocked for security:
- DROP (tables, databases)
- ALTER (table structures)
- CREATE (tables, databases)
- TRUNCATE
- GRANT/REVOKE (permissions)

### Allowed with Confirmation
- INSERT - Add new data
- UPDATE - Modify existing data  
- DELETE - Remove data

### Best Practices
1. Always validate the generated SQL before execution
2. Log all write operations for audit trails
3. Consider adding farmer_id scoping for UPDATE/DELETE operations
4. Implement proper error handling for database connection issues

## Quick Fix for Your Issue

The error "database 'farmer_crm' does not exist" might be happening because:

1. The INSERT is being blocked by the constitutional validation
2. The error message is misleading

To fix:
1. Add the `write_confirmation` field to your request
2. Handle the confirmation flow in your UI
3. If the database truly doesn't exist, check your AWS RDS instance

## Example Implementation

See `/examples/database_dashboard_with_write_confirmation.py` for a complete working example.

## Testing

After implementing the confirmation mechanism:

```python
# Test 1: INSERT without confirmation (should be blocked)
response = await query_endpoint({
    "query": "enter a farmer Suad Sakić",
    "write_confirmation": None
})
assert response["needs_confirmation"] == True

# Test 2: INSERT with wrong confirmation (should be blocked)
response = await query_endpoint({
    "query": "enter a farmer Suad Sakić",
    "write_confirmation": "YES"
})
assert response["needs_confirmation"] == True

# Test 3: INSERT with correct confirmation (should succeed)
response = await query_endpoint({
    "query": "enter a farmer Suad Sakić", 
    "write_confirmation": "INSERT"
})
assert response["success"] == True
```