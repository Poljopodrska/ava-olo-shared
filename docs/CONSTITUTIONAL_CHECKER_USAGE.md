# Constitutional Compliance Checker Usage Guide

## Overview

The Constitutional Compliance Checker is a comprehensive tool that ensures all AVA OLO code follows the 13 constitutional principles, with special emphasis on the MANGO RULE: "Would this work for a Bulgarian mango farmer?"

## Installation

### 1. Import the Checker

```python
from implementation.constitutional_checker import ConstitutionalChecker
from implementation.constitutional_integration import (
    ConstitutionalMiddleware,
    DatabaseDashboardChecker,
    constitutional_check,
    mango_rule_check
)
from implementation.dashboard_constitutional_integration import (
    DashboardConstitutionalGuard,
    get_constitutional_guard,
    constitutional_endpoint
)
```

### 2. Basic Setup

```python
# Create checker instance
checker = ConstitutionalChecker()

# For database dashboard integration
guard = DashboardConstitutionalGuard()
```

## Usage Examples

### 1. Check Code Compliance

```python
# Check a code string
code = """
def get_crop_advice(crop_name):
    if crop_name == "tomato":
        return "Water daily"
    else:
        return "Not supported"
"""

result = await checker.check_compliance(code, "code")
print(checker.generate_report(result))
# Output: VIOLATIONS! Hardcoded crop logic detected
```

### 2. Check File Compliance

```python
# Check an entire file
result = await checker.check_compliance(
    "/path/to/your/file.py",
    "file"
)

if not result.is_compliant:
    print(f"Found {len(result.violations)} violations")
    for violation in result.violations:
        print(f"- {violation.principle}: {violation.description}")
```

### 3. Check Module Compliance

```python
# Check a Python module
import your_module

result = await checker.check_compliance(
    your_module,
    "module"
)

# Get compliance score
print(f"Compliance Score: {result.overall_score}/100")
```

## FastAPI Integration

### 1. Protect Endpoints with Decorator

```python
from fastapi import FastAPI, Depends
from dashboard_constitutional_integration import (
    constitutional_endpoint,
    get_constitutional_guard
)

app = FastAPI()

@app.post("/api/query")
@constitutional_endpoint()
async def process_query(
    query: str,
    guard: DashboardConstitutionalGuard = Depends(get_constitutional_guard)
):
    # Your endpoint is now constitutionally protected!
    # The decorator will validate inputs and outputs
    return {"response": "Constitutional response"}
```

### 2. Three-Phase Validation Pattern

```python
@app.post("/api/constitutional-query")
async def process_query(request: QueryRequest):
    guard = DashboardConstitutionalGuard()
    
    # Phase 1: Validate Input
    input_validation = await guard.validate_natural_query(
        query=request.query,
        farmer_id=request.farmer_id,
        language=request.language
    )
    
    if not input_validation['is_valid']:
        return {"error": "Input violates constitutional principles"}
    
    # Phase 2: Validate Processing (SQL)
    generated_sql = await generate_sql(request.query)
    sql_validation = await guard.validate_generated_sql(
        sql=generated_sql,
        original_query=request.query,
        context={"farmer_id": request.farmer_id}
    )
    
    if not sql_validation['sql_approved']:
        return {"error": "SQL violates constitutional principles"}
    
    # Phase 3: Validate Output
    response = await generate_response(results)
    response_validation = await guard.validate_response(
        response=response,
        original_query=request.query,
        context={"language": request.language}
    )
    
    return {
        "response": response,
        "constitutional_compliance": response_validation['response_approved']
    }
```

## Command Line Usage

### 1. Check Single File

```bash
python -m constitutional_checker check /path/to/file.py
```

### 2. Check Directory

```bash
python -m constitutional_checker check-dir /path/to/directory --recursive
```

### 3. Generate Report

```bash
python -m constitutional_checker report /path/to/file.py --output report.md
```

## Integration Patterns

### 1. CI/CD Integration

```yaml
# .github/workflows/constitutional-check.yml
name: Constitutional Compliance Check

on: [push, pull_request]

jobs:
  constitutional-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Run Constitutional Check
        run: |
          python -m pytest tests/test_constitutional_checker.py
          python -m constitutional_checker check-dir src/
```

### 2. Pre-commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit

echo "🏛️ Running Constitutional Compliance Check..."

python -m constitutional_checker check-changed

if [ $? -ne 0 ]; then
    echo "❌ Constitutional violations detected! Commit blocked."
    echo "💡 Fix violations before committing."
    exit 1
fi

echo "✅ Constitutional compliance verified! 🥭"
```

### 3. Real-time Monitoring

```python
# Real-time compliance monitoring
async def monitor_compliance():
    checker = ConstitutionalChecker()
    
    while True:
        # Check active endpoints
        for endpoint in get_active_endpoints():
            result = await checker.check_compliance(
                endpoint.handler,
                "module"
            )
            
            if not result.is_compliant:
                alert_team(f"Constitutional violation in {endpoint.path}")
        
        await asyncio.sleep(300)  # Check every 5 minutes
```

## Understanding Violations

### Severity Levels

1. **CRITICAL** - Must fix immediately
   - Hardcoded crop/country logic
   - Personal data exposure
   - Non-PostgreSQL database usage

2. **WARNING** - Should fix soon
   - Missing error handling
   - Development code in production
   - Direct service imports

3. **INFO** - Best practice recommendations
   - Missing logging
   - Inappropriate tone
   - No tests detected

### Common Violations and Fixes

#### 1. MANGO RULE Violation

**Bad:**
```python
if crop == "mango" and country == "bulgaria":
    return "Not possible"
```

**Good:**
```python
# Let LLM handle crop viability
llm_response = await llm.analyze_crop_viability(
    crop=crop,
    location=location,
    context=farmer_context
)
return llm_response
```

#### 2. LLM-FIRST Violation

**Bad:**
```python
CROP_SEASONS = {
    "tomato": "summer",
    "potato": "spring"
}
return CROP_SEASONS.get(crop, "unknown")
```

**Good:**
```python
season = await llm.determine_planting_season(
    crop=crop,
    location=farmer_location,
    climate_data=climate_context
)
return season
```

#### 3. PRIVACY-FIRST Violation

**Bad:**
```python
# Sending farmer name to external API
openai_response = await openai.complete(
    prompt=f"Advice for farmer {farmer_name}"
)
```

**Good:**
```python
# Anonymize before external calls
openai_response = await openai.complete(
    prompt=f"Advice for farmer_id {anonymize(farmer_id)}"
)
```

## Advanced Features

### 1. Custom Principle Checks

```python
# Add custom principle check
class ExtendedConstitutionalChecker(ConstitutionalChecker):
    def __init__(self):
        super().__init__()
        self.principles['CUSTOM_RULE'] = self._check_custom_rule
    
    async def _check_custom_rule(self, code: str, file_path: str):
        violations = []
        # Your custom validation logic
        return {
            'compliant': len(violations) == 0,
            'violations': violations
        }
```

### 2. Batch Checking

```python
# Check multiple files efficiently
async def batch_check(file_paths: List[str]):
    checker = ConstitutionalChecker()
    results = {}
    
    tasks = [
        checker.check_compliance(path, "file")
        for path in file_paths
    ]
    
    completed = await asyncio.gather(*tasks)
    
    for path, result in zip(file_paths, completed):
        results[path] = result
    
    return results
```

### 3. Compliance Metrics

```python
# Track compliance over time
async def track_compliance_metrics():
    checker = ConstitutionalChecker()
    
    metrics = {
        'total_checks': 0,
        'compliant_checks': 0,
        'common_violations': {},
        'compliance_trend': []
    }
    
    # Run checks and update metrics
    result = await checker.check_compliance(target, "file")
    
    metrics['total_checks'] += 1
    if result.is_compliant:
        metrics['compliant_checks'] += 1
    
    # Track violation types
    for violation in result.violations:
        principle = violation.principle
        metrics['common_violations'][principle] = \
            metrics['common_violations'].get(principle, 0) + 1
    
    # Calculate compliance rate
    compliance_rate = (
        metrics['compliant_checks'] / metrics['total_checks'] * 100
    )
    
    metrics['compliance_trend'].append({
        'timestamp': datetime.now().isoformat(),
        'rate': compliance_rate
    })
    
    return metrics
```

## Best Practices

### 1. Check Early and Often

```python
# Development workflow
async def development_workflow():
    # 1. Check before implementation
    design_result = await checker.check_compliance(
        design_doc,
        "code"
    )
    
    # 2. Check during implementation
    code_result = await checker.check_compliance(
        implementation,
        "code"
    )
    
    # 3. Check before deployment
    final_result = await checker.check_compliance(
        production_code,
        "file"
    )
```

### 2. Integrate with IDEs

```python
# VS Code extension example
async def vscode_check_on_save(file_path: str):
    checker = ConstitutionalChecker()
    result = await checker.check_compliance(file_path, "file")
    
    if not result.is_compliant:
        show_problems([
            {
                'file': file_path,
                'line': v.line_number,
                'message': f"{v.principle}: {v.description}",
                'severity': v.severity
            }
            for v in result.violations
        ])
```

### 3. Create Constitutional Tests

```python
# pytest example
import pytest
from constitutional_checker import ConstitutionalChecker

@pytest.mark.asyncio
async def test_feature_is_constitutional():
    from my_feature import process_farmer_query
    
    checker = ConstitutionalChecker()
    result = await checker.check_compliance(
        process_farmer_query,
        "module"
    )
    
    assert result.is_compliant, \
        f"Constitutional violations: {result.violations}"
    assert result.overall_score >= 95.0, \
        f"Score too low: {result.overall_score}"
```

## Troubleshooting

### Common Issues

1. **"Module not found" errors**
   ```python
   # Add to Python path
   import sys
   sys.path.append('/path/to/ava-olo-shared')
   ```

2. **Async context errors**
   ```python
   # Use asyncio.run() for synchronous contexts
   import asyncio
   result = asyncio.run(checker.check_compliance(code, "code"))
   ```

3. **Large file timeouts**
   ```python
   # Check files in chunks
   async def check_large_file(file_path: str, chunk_size: int = 1000):
       # Implementation for chunked checking
   ```

## Support

For issues or questions:
1. Check violation remedies in the report
2. Consult the [Constitution](../constitutional/AVA_OLO_CONSTITUTION.md)
3. Review [good examples](../examples/CONSTITUTIONAL_CODE_EXAMPLES.md)
4. Run with debug logging: `export CONSTITUTIONAL_DEBUG=1`

Remember: **The MANGO RULE is supreme!** 🥭

If it doesn't work for a Bulgarian mango farmer, it doesn't work at all!