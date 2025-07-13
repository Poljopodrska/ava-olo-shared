# 🧪 Testing Procedures

Comprehensive testing guide for maintaining AVA OLO's constitutional compliance. Every test must pass the MANGO RULE!

## 📋 Table of Contents
1. [Mango Rule Testing](#mango-rule-testing)
2. [Privacy Compliance Testing](#privacy-compliance-testing)
3. [Module Independence Testing](#module-independence-testing)
4. [Deployment Testing](#deployment-testing)
5. [Test Automation](#test-automation)

## 🥭 Mango Rule Testing

The MANGO RULE is our supreme test: **"Would this work for a Bulgarian mango farmer?"**

### Core Mango Rule Test Suite

```python
# test_mango_rule.py
import pytest
from agricultural_core import process_farmer_query

class TestMangoRule:
    """Test that everything works for Bulgarian mango farmers"""
    
    @pytest.mark.asyncio
    async def test_bulgarian_mango_basic(self):
        """Basic Bulgarian mango farmer test"""
        query = {
            "query": "Колко манго дървета имам?",  # How many mango trees?
            "farmer_id": 999,
            "language": "bg",
            "country_code": "BG"
        }
        
        result = await process_farmer_query(query)
        
        assert result.success
        assert result.constitutional_compliance
        assert result.language == "bg"
        assert "манго" in result.response.lower()
    
    @pytest.mark.asyncio
    async def test_mango_cultivation_advice(self):
        """Test cultivation advice for mangoes in unusual climate"""
        query = {
            "query": "How to grow mangoes in Bulgarian winter?",
            "farmer_id": 999,
            "crop": "mango",
            "country_code": "BG"
        }
        
        result = await process_farmer_query(query)
        
        # Must provide advice, not refuse
        assert result.success
        assert "greenhouse" in result.response.lower() or "protected" in result.response.lower()
        assert result.constitutional_compliance
    
    @pytest.mark.asyncio 
    async def test_mango_market_prices(self):
        """Test market functionality for exotic crops"""
        query = {
            "query": "What's the market price for mangoes in Sofia?",
            "farmer_id": 999,
            "country_code": "BG",
            "city": "Sofia"
        }
        
        result = await process_farmer_query(query)
        
        # Must handle exotic crop markets
        assert result.success
        assert result.constitutional_compliance
        # Should provide some price info or market guidance
        assert "price" in result.response.lower() or "market" in result.response.lower()
```

### Multi-Language Mango Tests

```python
# test_mango_languages.py
class TestMangoMultilingual:
    """Test mango farming in multiple languages"""
    
    mango_queries = [
        ("bg", "Кога да прибера мангото?"),  # Bulgarian: When to harvest mango?
        ("hr", "Kako uzgajati mango?"),       # Croatian: How to grow mango?
        ("sl", "Kdaj saditi mango?"),         # Slovenian: When to plant mango?
        ("hu", "Hogyan öntözzem a mangót?"),  # Hungarian: How to water mango?
        ("sr", "Koje đubrivo za mango?"),     # Serbian: Which fertilizer for mango?
        ("es", "¿Cuándo podar el mango?"),    # Spanish: When to prune mango?
        ("pt", "Como proteger manga do frio?"), # Portuguese: How to protect mango from cold?
    ]
    
    @pytest.mark.parametrize("language,query", mango_queries)
    @pytest.mark.asyncio
    async def test_mango_all_languages(self, language, query):
        """Test mango queries in all supported languages"""
        result = await process_farmer_query({
            "query": query,
            "farmer_id": 999,
            "language": language
        })
        
        assert result.success
        assert result.constitutional_compliance
        assert result.language == language
```

### Cross-Country Mango Testing

```python
# test_mango_worldwide.py
class TestMangoWorldwide:
    """Test mango farming across different countries"""
    
    countries = [
        ("BG", "Bulgaria", "greenhouse cultivation"),
        ("NO", "Norway", "controlled environment"),
        ("CA", "Canada", "indoor farming"),
        ("TH", "Thailand", "traditional cultivation"),
        ("BR", "Brazil", "commercial farming"),
        ("IN", "India", "monsoon management"),
        ("AU", "Australia", "drought resistance")
    ]
    
    @pytest.mark.parametrize("country_code,country_name,expected_keyword", countries)
    @pytest.mark.asyncio
    async def test_mango_cultivation_worldwide(self, country_code, country_name, expected_keyword):
        """Test mango cultivation advice for different climates"""
        query = {
            "query": f"Best practices for mango farming in {country_name}",
            "farmer_id": 999,
            "country_code": country_code
        }
        
        result = await process_farmer_query(query)
        
        assert result.success
        assert result.constitutional_compliance
        # Should mention climate-appropriate techniques
        assert any(word in result.response.lower() for word in 
                  [expected_keyword, "mango", "cultivation", "growing"])
```

### Edge Case Mango Tests

```python
# test_mango_edge_cases.py
class TestMangoEdgeCases:
    """Test extreme mango farming scenarios"""
    
    @pytest.mark.asyncio
    async def test_urban_mango_farming(self):
        """Test mango farming in urban environment"""
        result = await process_farmer_query({
            "query": "How to grow mangoes on my Sofia apartment balcony?",
            "farmer_id": 999,
            "country_code": "BG",
            "environment": "urban"
        })
        
        assert result.success
        assert "container" in result.response.lower() or "pot" in result.response.lower()
    
    @pytest.mark.asyncio
    async def test_mango_crop_rotation(self):
        """Test impossible crop rotation with mangoes"""
        result = await process_farmer_query({
            "query": "Can I rotate mangoes with wheat seasonally?",
            "farmer_id": 999
        })
        
        assert result.success
        # Should explain why this is impractical but still provide guidance
        assert result.constitutional_compliance
    
    @pytest.mark.asyncio
    async def test_mango_in_zero_hectares(self):
        """Test mango farming with no land"""
        result = await process_farmer_query({
            "query": "I have 0 hectares but want to grow mangoes",
            "farmer_id": 999,
            "land_size": 0
        })
        
        assert result.success
        # Should suggest alternatives like container farming
        assert any(word in result.response.lower() for word in 
                  ["container", "hydroponic", "vertical", "indoor"])
```

## 🔒 Privacy Compliance Testing

### Personal Data Protection Tests

```python
# test_privacy_compliance.py
import re
from unittest.mock import patch

class TestPrivacyCompliance:
    """Ensure no personal data leaks to external services"""
    
    @pytest.mark.asyncio
    async def test_no_farmer_names_in_llm(self):
        """Verify farmer names never sent to OpenAI"""
        with patch('openai.ChatCompletion.create') as mock_openai:
            await process_farmer_query({
                "query": "What should I plant?",
                "farmer_id": 123,
                "farmer_name": "John Smith"
            })
            
            # Check all calls to OpenAI
            for call in mock_openai.call_args_list:
                prompt = str(call)
                assert "John Smith" not in prompt
                assert "123" not in prompt  # No farmer IDs either
    
    @pytest.mark.asyncio
    async def test_no_phone_numbers_external(self):
        """Verify phone numbers stay internal"""
        test_phone = "+385123456789"
        
        with patch('openai.ChatCompletion.create') as mock_openai:
            await process_farmer_query({
                "query": "My crop status?",
                "phone_number": test_phone
            })
            
            for call in mock_openai.call_args_list:
                assert test_phone not in str(call)
    
    def test_anonymization_function(self):
        """Test data anonymization utilities"""
        from privacy_utils import anonymize_prompt
        
        original = "Farmer John (ID: 123) at +385123456789 has 5 hectares"
        anonymized = anonymize_prompt(original)
        
        assert "John" not in anonymized
        assert "123" not in anonymized
        assert "+385123456789" not in anonymized
        assert "5 hectares" in anonymized  # Keep non-personal data
    
    @pytest.mark.asyncio
    async def test_gdpr_data_request(self):
        """Test GDPR compliance - data retrieval"""
        # Farmer should be able to get all their data
        result = await process_farmer_query({
            "query": "Show me all my personal data",
            "farmer_id": 123,
            "gdpr_request": True
        })
        
        assert result.success
        # Should return data but only to authenticated farmer
        assert result.requires_authentication
```

### Database Security Tests

```python
# test_database_security.py
class TestDatabaseSecurity:
    """Test database access controls"""
    
    @pytest.mark.asyncio
    async def test_sql_injection_prevention(self):
        """Test SQL injection is prevented"""
        malicious_queries = [
            "'; DROP TABLE farmers; --",
            "1 OR 1=1",
            "'; DELETE FROM farmers WHERE '1'='1",
            "UNION SELECT * FROM farmers"
        ]
        
        for malicious in malicious_queries:
            result = await process_farmer_query({
                "query": malicious,
                "farmer_id": 123
            })
            
            # Should handle safely, not execute malicious SQL
            assert result.success or result.error
            # Verify tables still exist
            assert await db.table_exists('farmers')
    
    @pytest.mark.asyncio
    async def test_farmer_data_isolation(self):
        """Test farmers can't access other farmers' data"""
        # Farmer 123 tries to access farmer 456's data
        result = await process_farmer_query({
            "query": "Show me data for farmer ID 456",
            "farmer_id": 123
        })
        
        # Should only return farmer 123's data or error
        if result.success:
            assert "456" not in result.response
            assert result.farmer_id == 123
    
    @pytest.mark.asyncio
    async def test_api_key_validation(self):
        """Test API key security"""
        from api_auth import validate_api_key
        
        # Test invalid keys
        assert not validate_api_key("")
        assert not validate_api_key("invalid-key")
        assert not validate_api_key("sk-1234")  # Wrong format
        
        # Test valid key format (not actual key)
        assert validate_api_key("sk-proj-" + "x" * 40)
```

## 🧩 Module Independence Testing

### Service Isolation Tests

```python
# test_module_independence.py
import asyncio
from unittest.mock import patch

class TestModuleIndependence:
    """Test that modules work independently"""
    
    @pytest.mark.asyncio
    async def test_dashboard_without_core(self):
        """Dashboard should work if agricultural-core is down"""
        # Simulate agricultural-core being unavailable
        with patch('requests.get', side_effect=ConnectionError):
            from monitoring_dashboards import app
            
            # Dashboard should still start
            response = await app.test_client().get('/health')
            assert response.status_code == 200
            
            # Basic functionality should work
            response = await app.test_client().get('/business')
            assert response.status_code in [200, 503]  # OK or degraded
    
    @pytest.mark.asyncio
    async def test_core_without_dashboards(self):
        """Agricultural-core should work independently"""
        # Don't start monitoring-dashboards
        result = await process_farmer_query({
            "query": "What are my crops?",
            "farmer_id": 123
        })
        
        assert result.success
        assert result.constitutional_compliance
    
    def test_no_circular_imports(self):
        """Detect circular import dependencies"""
        import ast
        import os
        
        def find_imports(filename):
            with open(filename, 'r') as f:
                tree = ast.parse(f.read())
            
            imports = []
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    imports.extend(alias.name for alias in node.names)
                elif isinstance(node, ast.ImportFrom):
                    imports.append(node.module)
            return imports
        
        # Check for circular dependencies
        service_files = {
            'dashboards': ['monitoring_dashboards/*.py'],
            'core': ['agricultural_core/*.py']
        }
        
        # Each service should not import from the other
        for service, patterns in service_files.items():
            for pattern in patterns:
                for file in glob.glob(pattern):
                    imports = find_imports(file)
                    other_service = 'core' if service == 'dashboards' else 'dashboards'
                    
                    for imp in imports:
                        assert other_service not in imp, \
                            f"{file} imports from {other_service}: {imp}"
```

### Error Isolation Tests

```python
# test_error_isolation.py
class TestErrorIsolation:
    """Test that errors in one module don't crash others"""
    
    @pytest.mark.asyncio
    async def test_llm_failure_handling(self):
        """System should handle LLM failures gracefully"""
        with patch('openai.ChatCompletion.create', side_effect=Exception("API Down")):
            result = await process_farmer_query({
                "query": "What should I plant?",
                "farmer_id": 123
            })
            
            # Should return graceful error, not crash
            assert not result.success
            assert "service temporarily unavailable" in result.error.lower()
            assert result.status_code == 503
    
    @pytest.mark.asyncio
    async def test_database_failure_handling(self):
        """System should handle database failures"""
        with patch('psycopg2.connect', side_effect=Exception("DB Down")):
            # Should fall back to cached responses or safe defaults
            result = await process_farmer_query({
                "query": "What's the weather tomorrow?",
                "farmer_id": 123
            })
            
            # External queries might still work
            assert result.partial_success or not result.success
    
    @pytest.mark.asyncio
    async def test_cascading_failure_prevention(self):
        """One service failure shouldn't cascade"""
        failures = []
        
        async def simulate_service_failure(service_name):
            await asyncio.sleep(0.1)
            raise Exception(f"{service_name} failed")
        
        # Start multiple services with one failing
        tasks = [
            simulate_service_failure("weather_service"),
            process_farmer_query({"query": "crop status", "farmer_id": 123}),
            check_dashboard_health()
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # First should fail, others should succeed
        assert isinstance(results[0], Exception)
        assert results[1].success  # Core query works
        assert results[2]["status"] == "healthy"  # Dashboard works
```

### API Interface Testing

```python
# test_api_contracts.py
class TestAPIContracts:
    """Test API interfaces between modules"""
    
    @pytest.mark.asyncio
    async def test_api_versioning(self):
        """Test API version compatibility"""
        endpoints = [
            "/api/v1/farmer/query",
            "/api/v1/health",
            "/api/v2/farmer/query"  # Future version
        ]
        
        for endpoint in endpoints:
            if "v1" in endpoint:
                # v1 endpoints must exist
                response = await client.get(endpoint)
                assert response.status_code != 404
            elif "v2" in endpoint:
                # v2 endpoints return version info
                response = await client.get(endpoint)
                if response.status_code == 200:
                    assert response.json().get("api_version") == "v2"
    
    def test_response_schema_validation(self):
        """Validate API response schemas"""
        from pydantic import ValidationError
        from api_schemas import FarmerQueryResponse
        
        # Valid response
        valid_response = {
            "success": True,
            "response": "You have 5 hectares",
            "constitutional_compliance": True,
            "method": "llm_first",
            "metadata": {}
        }
        
        try:
            FarmerQueryResponse(**valid_response)
        except ValidationError:
            pytest.fail("Valid response failed validation")
        
        # Invalid response should fail
        invalid_response = {
            "success": True
            # Missing required fields
        }
        
        with pytest.raises(ValidationError):
            FarmerQueryResponse(**invalid_response)
```

## 🚀 Deployment Testing

### AWS Compatibility Tests

```python
# test_aws_deployment.py
class TestAWSDeployment:
    """Test AWS App Runner compatibility"""
    
    def test_port_configuration(self):
        """Verify port 8080 is used"""
        import main
        
        # Check all uvicorn.run calls
        with open('main.py', 'r') as f:
            content = f.read()
            
        assert 'port=8080' in content or 'port = 8080' in content
        assert 'localhost' not in content  # Should use 0.0.0.0
        assert '127.0.0.1' not in content
    
    def test_health_endpoint_exists(self):
        """AWS App Runner requires /health endpoint"""
        from main import app
        
        # Check health endpoint is registered
        routes = [route.path for route in app.routes]
        assert '/health' in routes
        
        # Test health endpoint response
        client = TestClient(app)
        response = client.get('/health')
        
        assert response.status_code == 200
        assert response.json()["status"] in ["healthy", "degraded"]
    
    def test_environment_variables_handled(self):
        """Test missing environment variables don't crash app"""
        import os
        
        # Temporarily remove env vars
        original_key = os.environ.pop('OPENAI_API_KEY', None)
        
        try:
            # App should still start
            from main import app
            client = TestClient(app)
            response = client.get('/health')
            
            assert response.status_code == 200
            # Might be degraded but not crashed
            assert response.json()["status"] in ["healthy", "degraded"]
            
        finally:
            if original_key:
                os.environ['OPENAI_API_KEY'] = original_key
    
    @pytest.mark.asyncio
    async def test_concurrent_requests(self):
        """Test handling concurrent requests (AWS scaling)"""
        async def make_request(farmer_id):
            return await process_farmer_query({
                "query": "What are my crops?",
                "farmer_id": farmer_id
            })
        
        # Simulate 50 concurrent requests
        tasks = [make_request(i) for i in range(50)]
        results = await asyncio.gather(*tasks)
        
        # All should complete
        success_count = sum(1 for r in results if r.success)
        assert success_count >= 45  # Allow some failures under load
```

### Performance Testing

```python
# test_performance.py
import time
import statistics

class TestPerformance:
    """Test system performance requirements"""
    
    @pytest.mark.asyncio
    async def test_query_response_time(self):
        """Test query response times"""
        response_times = []
        
        for _ in range(10):
            start = time.time()
            result = await process_farmer_query({
                "query": "Show my fields",
                "farmer_id": 123
            })
            end = time.time()
            
            if result.success:
                response_times.append(end - start)
        
        # Check performance metrics
        avg_time = statistics.mean(response_times)
        p95_time = statistics.quantiles(response_times, n=20)[18]  # 95th percentile
        
        assert avg_time < 3.0  # Average under 3 seconds
        assert p95_time < 5.0  # 95% under 5 seconds
    
    @pytest.mark.asyncio
    async def test_database_connection_pooling(self):
        """Test connection pool efficiency"""
        from database_operations import connection_pool
        
        initial_connections = connection_pool.size
        
        # Make multiple concurrent queries
        tasks = [
            process_farmer_query({"query": f"Query {i}", "farmer_id": i})
            for i in range(20)
        ]
        
        await asyncio.gather(*tasks)
        
        # Pool should reuse connections
        assert connection_pool.size <= initial_connections + 5
        assert connection_pool.available > 0
```

### End-to-End Testing

```python
# test_end_to_end.py
class TestEndToEnd:
    """Full system integration tests"""
    
    @pytest.mark.asyncio
    async def test_complete_farmer_journey(self):
        """Test complete farmer interaction flow"""
        farmer_id = 999
        
        # 1. Farmer asks about their fields
        result1 = await process_farmer_query({
            "query": "Колко полета имам?",  # Bulgarian: How many fields?
            "farmer_id": farmer_id,
            "language": "bg"
        })
        assert result1.success
        assert "bg" in result1.metadata["language"]
        
        # 2. Farmer asks about specific crop
        result2 = await process_farmer_query({
            "query": "Кога да засадя манго?",  # When to plant mango?
            "farmer_id": farmer_id,
            "language": "bg"
        })
        assert result2.success
        assert result2.constitutional_compliance
        
        # 3. Check dashboard shows updated data
        dashboard_response = await get_dashboard_data(farmer_id)
        assert dashboard_response.success
        
        # 4. Verify audit trail
        audit = await get_audit_log(farmer_id)
        assert len(audit) >= 2
        assert audit[0]["action"] == "query"
    
    @pytest.mark.asyncio
    async def test_minority_farmer_complete_flow(self):
        """Test Hungarian minority farmer in Croatia"""
        # Complete flow for minority farmer
        farmer_data = {
            "phone_number": "+385987654321",  # Croatian number
            "language": "hu",  # Hungarian speaker
            "ethnicity": "Hungarian",
            "farmer_id": 456
        }
        
        # Multiple interactions in Hungarian
        queries = [
            "Milyen növényeket termeszthetek?",  # What crops can I grow?
            "Mikor kell öntözni?",  # When to water?
            "Hol adhatok el mangót?"  # Where to sell mangoes?
        ]
        
        for query in queries:
            result = await process_farmer_query({
                **farmer_data,
                "query": query
            })
            
            assert result.success
            assert result.metadata["language_used"] == "hu"
            assert result.metadata["country_detected"] == "HR"
            assert result.constitutional_compliance
```

## 🤖 Test Automation

### Continuous Integration Tests

```yaml
# .github/workflows/constitutional-tests.yml
name: Constitutional Compliance Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r requirements-test.txt
      
      - name: Run Constitutional Tests
        run: |
          pytest tests/test_mango_rule.py -v
          pytest tests/test_privacy_compliance.py -v
          pytest tests/test_module_independence.py -v
      
      - name: Run Performance Tests
        run: |
          pytest tests/test_performance.py -v --benchmark
      
      - name: Constitutional Compliance Report
        if: always()
        run: |
          python generate_compliance_report.py
```

### Automated Test Runner

```python
# run_all_tests.py
#!/usr/bin/env python3
"""
Run all constitutional compliance tests
"""

import subprocess
import sys
import json
from datetime import datetime

def run_test_suite(name, command):
    """Run a test suite and return results"""
    print(f"\n{'='*60}")
    print(f"Running {name}")
    print('='*60)
    
    start_time = datetime.now()
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    end_time = datetime.now()
    
    return {
        "name": name,
        "passed": result.returncode == 0,
        "duration": (end_time - start_time).total_seconds(),
        "output": result.stdout,
        "errors": result.stderr
    }

def main():
    """Run all test suites"""
    test_suites = [
        ("Mango Rule Tests", "pytest tests/test_mango_rule.py -v"),
        ("Privacy Compliance", "pytest tests/test_privacy_compliance.py -v"),
        ("Module Independence", "pytest tests/test_module_independence.py -v"),
        ("AWS Deployment", "pytest tests/test_aws_deployment.py -v"),
        ("Performance Tests", "pytest tests/test_performance.py -v"),
        ("End-to-End Tests", "pytest tests/test_end_to_end.py -v")
    ]
    
    results = []
    all_passed = True
    
    for name, command in test_suites:
        result = run_test_suite(name, command)
        results.append(result)
        if not result["passed"]:
            all_passed = False
    
    # Generate report
    print("\n" + "="*60)
    print("CONSTITUTIONAL COMPLIANCE TEST REPORT")
    print("="*60)
    
    for result in results:
        status = "✅ PASSED" if result["passed"] else "❌ FAILED"
        print(f"{result['name']}: {status} ({result['duration']:.2f}s)")
    
    print("\n" + "="*60)
    if all_passed:
        print("🎉 ALL TESTS PASSED - CONSTITUTIONALLY COMPLIANT!")
        print("🥭 The Bulgarian mango farmer is happy!")
    else:
        print("❌ CONSTITUTIONAL VIOLATIONS DETECTED!")
        print("🥭 The Bulgarian mango farmer is disappointed!")
        sys.exit(1)
    
    # Save detailed report
    with open('test_report.json', 'w') as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "all_passed": all_passed,
            "results": results
        }, f, indent=2)

if __name__ == "__main__":
    main()
```

### Test Coverage Requirements

```python
# pytest.ini
[pytest]
minversion = 6.0
addopts = 
    --cov=agricultural_core
    --cov=monitoring_dashboards
    --cov-report=html
    --cov-report=term
    --cov-fail-under=80

testpaths = tests

# coverage_check.py
def check_constitutional_coverage():
    """Ensure critical paths have test coverage"""
    critical_functions = [
        "process_farmer_query",
        "smart_country_detection", 
        "llm_generate_sql",
        "privacy_check",
        "mango_rule_validation"
    ]
    
    coverage_report = load_coverage_report()
    
    for func in critical_functions:
        coverage = coverage_report.get(func, 0)
        assert coverage == 100, f"{func} has only {coverage}% coverage!"
```

## 📊 Test Metrics and Reporting

### Constitutional Compliance Dashboard

```python
# generate_test_dashboard.py
def generate_compliance_dashboard():
    """Generate HTML dashboard of test results"""
    
    template = """
    <html>
    <head><title>AVA OLO Constitutional Compliance</title></head>
    <body>
        <h1>🏛️ Constitutional Compliance Dashboard</h1>
        
        <h2>🥭 Mango Rule Compliance: {mango_score}%</h2>
        <ul>
            <li>Languages tested: {languages_tested}/50</li>
            <li>Countries tested: {countries_tested}/50</li>
            <li>Edge cases passed: {edge_cases}/10</li>
        </ul>
        
        <h2>🔒 Privacy Compliance: {privacy_score}%</h2>
        <ul>
            <li>No PII leaks: {no_pii_leaks}</li>
            <li>GDPR compliant: {gdpr_compliant}</li>
            <li>Secure queries: {secure_queries}/100</li>
        </ul>
        
        <h2>🧩 Module Independence: {independence_score}%</h2>
        <ul>
            <li>No circular imports: {no_circular}</li>
            <li>Error isolation: {error_isolation}</li>
            <li>API contracts: {api_contracts}</li>
        </ul>
        
        <h2>🚀 Deployment Ready: {deployment_score}%</h2>
        <ul>
            <li>AWS compatible: {aws_compatible}</li>
            <li>Performance SLA: {performance_sla}</li>
            <li>Scalability tested: {scalability}</li>
        </ul>
        
        <h2>Overall Constitutional Score: {overall_score}%</h2>
        <p>Generated: {timestamp}</p>
    </body>
    </html>
    """
    
    # Calculate scores from test results
    metrics = calculate_test_metrics()
    
    with open('compliance_dashboard.html', 'w') as f:
        f.write(template.format(**metrics))
```

---

**Remember: Every test must pass the MANGO RULE. If it doesn't work for a Bulgarian mango farmer, it doesn't work at all!** 🥭