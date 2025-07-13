# 🔧 INTEGRATION GUIDE: Constitutional Amendment #13

## 📋 Overview

This guide helps integrate the Country-Based Localization system (Amendment #13) into existing AVA OLO modules. The integration maintains constitutional compliance while adding intelligent localization.

## 🚀 Quick Start

### 1. Import Required Modules
```python
from ava_olo_shared.country_detector import CountryDetector
from ava_olo_shared.localization_handler import LocalizationHandler, LocalizationContext
from ava_olo_shared.information_hierarchy import InformationHierarchyManager
from ava_olo_shared.llm_router_with_localization import LocalizedLLMRouter, LLMRouterAdapter
```

### 2. Basic Usage
```python
# Initialize the enhanced router
router = LocalizedLLMRouter()

# Process a farmer query
result = await router.route_farmer_query(
    query="When should I plant tomatoes?",
    whatsapp_number="+386123456789",  # Slovenia
    farmer_id=123
)

# Response will be in Slovenian with Slovenia-specific context
print(result["response"])
```

## 🔄 Module-by-Module Integration

### 📡 API Gateway Integration

**File:** `ava-olo-agricultural-core/api_gateway_simple.py`

Replace existing query processing:

```python
# OLD CODE (Constitutional Violation - Hardcoded)
async def process_query(query: str, farmer_id: int):
    # Hardcoded Croatian context
    response = "For Croatia, corn planting..."
    return response

# NEW CODE (Constitutional Compliance)
from ava_olo_shared.llm_router_with_localization import LLMRouterAdapter

router_adapter = LLMRouterAdapter()

async def process_query(query: str, whatsapp_number: str, farmer_id: int):
    # Automatic country detection and localization
    response = await router_adapter.process_message(
        message=query,
        phone_number=whatsapp_number,
        farmer_id=farmer_id
    )
    return response
```

### 🗄️ Database Operations Integration

**File:** `ava-olo-database-ops/database_operations.py`

Add country context to queries:

```python
# NEW: Add country-aware methods
async def get_farmer_with_context(self, whatsapp_number: str):
    """Get farmer with full localization context"""
    query = """
    SELECT f.*, flc.*
    FROM farmers f
    JOIN v_farmer_localization_context flc 
        ON f.farmer_id = flc.farmer_id
    WHERE f.whatsapp_number = %s
    """
    
    result = await self.execute_query(query, (whatsapp_number,))
    return result

async def get_hierarchical_knowledge(self, farmer_id: int, country_code: str):
    """Get knowledge respecting information hierarchy"""
    query = "SELECT * FROM get_hierarchical_knowledge(%s, %s, 10)"
    return await self.execute_query(query, (farmer_id, country_code))
```

### 🔍 Knowledge Search Integration

**File:** `ava-olo-document-search/knowledge_search.py`

Add country filtering to RAG queries:

```python
# NEW: Country-aware RAG search
async def search_with_country_context(self, 
                                    query: str, 
                                    country_code: str,
                                    language: str):
    """Search knowledge with country context"""
    # Add country to search metadata
    metadata_filter = {
        "country_code": country_code,
        "language": language
    }
    
    # Search with enhanced context
    results = await self.vector_search(
        query=query,
        filter=metadata_filter,
        top_k=10
    )
    
    # Convert to InformationItems
    items = []
    for result in results:
        items.append(InformationItem(
            content=result.content,
            relevance=InformationRelevance.COUNTRY_SPECIFIC,
            country_code=country_code,
            source_type="rag",
            metadata=result.metadata
        ))
    
    return items
```

### 💬 WhatsApp Mock Integration

**File:** `ava-olo-mock-whatsapp/whatsapp_mock.py`

Update to include phone numbers:

```python
# NEW: Include WhatsApp number in all requests
@app.post("/webhook")
async def whatsapp_webhook(request: Request):
    data = await request.json()
    
    # Extract phone number (required for localization)
    whatsapp_number = data.get("from", "")
    message = data.get("message", "")
    
    # Process with localization
    response = await router_adapter.process_message(
        message=message,
        phone_number=whatsapp_number
    )
    
    return {
        "response": response,
        "to": whatsapp_number,
        "language_detected": router_adapter.get_context_for_farmer(whatsapp_number)["language"]
    }
```

### 📊 Monitoring Dashboard Integration

**File:** `ava-olo-monitoring-dashboards/admin_dashboard.py`

Add country analytics:

```python
# NEW: Country-based analytics
async def get_farmer_distribution_by_country():
    """Get farmer distribution across countries"""
    query = """
    SELECT 
        country_code,
        COUNT(*) as farmer_count,
        array_agg(DISTINCT preferred_language) as languages
    FROM farmers
    WHERE country_code IS NOT NULL
    GROUP BY country_code
    ORDER BY farmer_count DESC
    """
    
    return await db.execute_query(query)

# Add to dashboard display
@app.get("/analytics/countries")
async def country_analytics():
    distribution = await get_farmer_distribution_by_country()
    return {
        "country_distribution": distribution,
        "total_countries": len(distribution)
    }
```

## 🗄️ Database Migration

Run the schema updates:

```bash
# Connect to PostgreSQL
psql -U your_user -d farmer_crm

# Run the migration
\i /path/to/ava-olo-shared/database_schema_amendment_13.sql

# Verify new tables
\dt knowledge_sources
\dt country_agricultural_profiles
\dt localization_audit_log
```

## 🧪 Testing Integration

### Unit Test Updates

Update existing tests to include country context:

```python
# OLD TEST (Incomplete)
def test_farmer_query():
    response = process_query("When to plant?", farmer_id=123)
    assert "plant" in response

# NEW TEST (With Localization)
async def test_farmer_query_with_localization():
    # Test Bulgarian farmer
    response = await router_adapter.process_message(
        message="Кога да садя домати?",
        phone_number="+359123456789",
        farmer_id=123
    )
    
    # Verify Bulgarian response
    assert "домати" in response  # "tomatoes" in Bulgarian
    
    # Test Slovenian farmer  
    response = await router_adapter.process_message(
        message="Kdaj saditi paradižnik?",
        phone_number="+386123456789",
        farmer_id=456
    )
    
    # Verify Slovenian response
    assert "paradižnik" in response  # "tomato" in Slovenian
```

### Integration Test

```python
# Full integration test
async def test_complete_localization_flow():
    # 1. Farmer sends WhatsApp message
    whatsapp_number = "+359987654321"  # Bulgaria
    message = "Кога да бера манго?"  # When to harvest mango?
    
    # 2. System detects country
    detector = CountryDetector()
    country_info = detector.get_country_info(whatsapp_number)
    assert country_info['country_code'] == 'BG'
    
    # 3. System processes with localization
    router = LocalizedLLMRouter()
    result = await router.route_farmer_query(
        query=message,
        whatsapp_number=whatsapp_number,
        farmer_id=789
    )
    
    # 4. Verify response is appropriate
    assert result['context']['country'] == 'BG'
    assert result['context']['language'] == 'bg'
    assert len(result['response']) > 0
```

## ⚠️ Common Integration Issues

### 1. Missing WhatsApp Numbers
**Problem:** Existing code doesn't pass phone numbers
**Solution:** Update all entry points to include WhatsApp number

```python
# Add default handling for missing numbers
whatsapp_number = request.get('whatsapp_number', '')
if not whatsapp_number and farmer_id:
    # Fallback: Get from database
    farmer = await db.get_farmer(farmer_id)
    whatsapp_number = farmer.get('whatsapp_number', '')
```

### 2. Hardcoded Language Responses
**Problem:** Existing code has hardcoded Croatian/English
**Solution:** Replace all hardcoded text with LLM-generated responses

```python
# REMOVE hardcoded responses like:
response = "For Croatia, plant in April"

# REPLACE with:
response = await synthesize_localized_response(query, context)
```

### 3. Database Connection Issues
**Problem:** New tables not accessible
**Solution:** Ensure proper permissions

```sql
GRANT ALL ON TABLE knowledge_sources TO ava_olo_user;
GRANT ALL ON TABLE country_agricultural_profiles TO ava_olo_user;
GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public TO ava_olo_user;
```

## 📈 Performance Optimization

### 1. Cache Country Detection
```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def get_cached_country(phone_number: str) -> str:
    detector = CountryDetector()
    return detector.extract_country_code(phone_number)
```

### 2. Batch Information Queries
```python
# Process multiple farmers efficiently
async def process_batch_queries(queries: List[Dict]):
    # Group by country for efficient processing
    by_country = {}
    for q in queries:
        country = get_cached_country(q['whatsapp_number'])
        if country not in by_country:
            by_country[country] = []
        by_country[country].append(q)
    
    # Process each country group
    results = []
    for country, country_queries in by_country.items():
        # Reuse country context
        context = LocalizationContext(
            country_code=country,
            # ... other fields
        )
        # Process all queries for this country
        # ...
```

## 🔒 Security Considerations

### 1. Validate Phone Numbers
```python
import re

def validate_whatsapp_number(number: str) -> bool:
    """Validate WhatsApp number format"""
    pattern = r'^\+?[1-9]\d{1,14}$'
    return bool(re.match(pattern, number))
```

### 2. Rate Limiting by Country
```python
# Implement country-specific rate limits
RATE_LIMITS = {
    "default": 100,  # requests per hour
    "BG": 150,      # Higher limit for active regions
    "SI": 150,
    "HR": 150
}

def get_rate_limit(country_code: str) -> int:
    return RATE_LIMITS.get(country_code, RATE_LIMITS["default"])
```

## 📊 Monitoring Integration

Add localization metrics:

```python
# Track usage by country
METRICS = {
    "queries_by_country": Counter(),
    "response_languages": Counter(),
    "avg_response_time_by_country": {}
}

# In your processing code
METRICS["queries_by_country"][context.country_code] += 1
METRICS["response_languages"][context.preferred_language] += 1
```

## 🚀 Deployment Checklist

- [ ] Database schema updated with Amendment #13 tables
- [ ] All hardcoded country/language references removed
- [ ] WhatsApp numbers passed to all query endpoints
- [ ] Country detection tested for all supported countries
- [ ] Information hierarchy properly implemented
- [ ] Monitoring includes country-based metrics
- [ ] Error handling includes localization context
- [ ] Tests updated with multi-country scenarios
- [ ] Documentation updated with localization examples
- [ ] Performance benchmarks for different countries

## 📚 Additional Resources

- `CONSTITUTIONAL_AMENDMENT_13.md` - Full amendment details
- `test_constitutional_amendment_13.py` - Complete test suite
- `country_detector.py` - Country detection implementation
- `localization_handler.py` - Localization logic
- `information_hierarchy.py` - Information relevance system

## 🆘 Support

For integration issues:
1. Check the test suite for working examples
2. Verify database schema is updated
3. Ensure OpenAI API key is set for LLM operations
4. Review logs for country detection failures

Remember: The goal is to make AVA OLO work for **any farmer, any crop, any country** while maintaining privacy and using LLM intelligence!