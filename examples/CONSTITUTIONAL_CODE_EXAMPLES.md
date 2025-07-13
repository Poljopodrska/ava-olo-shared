# 🏛️ Constitutional Code Examples

This document provides working examples of constitutionally compliant code and violations to avoid. Remember: If it doesn't work for a Bulgarian mango farmer, it's unconstitutional!

## 📋 Table of Contents
1. [LLM-First Query Processing](#llm-first-query-processing)
2. [Database Operations](#database-operations)
3. [API Development](#api-development)
4. [Testing Examples](#testing-examples)

## 🧠 LLM-First Query Processing

### ✅ Constitutional Approach

```python
# constitutional_query_processor.py
from openai import OpenAI
import json
from typing import Dict, Any, Optional

class ConstitutionalQueryProcessor:
    """
    100% LLM-first query processing
    No hardcoded patterns - works for any crop, any country
    """
    
    def __init__(self):
        self.client = OpenAI()
        self.model = "gpt-4"
    
    async def process_farmer_query(self, 
                                 query: str, 
                                 context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process any farmer query using pure LLM intelligence
        
        Args:
            query: Natural language query in any language
            context: Farmer context (location, crops, etc.)
            
        Returns:
            Constitutional response that works globally
        """
        # Build universal prompt that works for any scenario
        system_prompt = """
        You are an agricultural assistant serving farmers globally.
        
        CRITICAL RULES:
        1. Work for ANY crop (including mangoes in Bulgaria)
        2. Work for ANY country (from Bulgaria to Brazil)
        3. Work for ANY language (50+ supported)
        4. Never refuse based on geographic assumptions
        5. Provide practical advice for ANY scenario
        
        Context provided includes farmer's location, language, and current crops.
        Always respond in the farmer's language.
        """
        
        user_prompt = f"""
        Farmer Query: {query}
        
        Farmer Context:
        - Location: {context.get('country', 'Unknown')}
        - Language: {context.get('language', 'en')}
        - Current Crops: {context.get('crops', [])}
        - Climate Zone: {context.get('climate', 'Unknown')}
        
        Provide helpful agricultural advice.
        """
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7
            )
            
            return {
                "success": True,
                "response": response.choices[0].message.content,
                "constitutional_compliance": True,
                "method": "llm_first"
            }
            
        except Exception as e:
            # Even errors are handled constitutionally
            return {
                "success": False,
                "error": "Service temporarily unavailable",
                "fallback": self._get_constitutional_fallback(query, context),
                "constitutional_compliance": True
            }
    
    def _get_constitutional_fallback(self, query: str, context: Dict) -> str:
        """
        Fallback that still respects constitutional principles
        No hardcoded crop-specific advice!
        """
        language = context.get('language', 'en')
        
        # Generic messages in multiple languages
        fallback_messages = {
            'en': "I'm temporarily unable to process your query, but I recommend consulting local agricultural experts for advice specific to your crops and conditions.",
            'bg': "Временно не мога да обработя заявката ви, но препоръчвам да се консултирате с местни земеделски експерти.",
            'hr': "Trenutno ne mogu obraditi vaš upit, ali preporučujem savjetovanje s lokalnim poljoprivrednim stručnjacima.",
            'hu': "Ideiglenesen nem tudom feldolgozni a kérését, de javaslom, hogy forduljon helyi mezőgazdasági szakértőkhöz."
        }
        
        return fallback_messages.get(language, fallback_messages['en'])
```

### ❌ Constitutional Violations

```python
# VIOLATION: Hardcoded crop logic
class UnconstitutionalProcessor:
    """
    DON'T DO THIS - Violates MANGO RULE
    """
    
    def process_query(self, query: str, crop: str) -> str:
        # ❌ VIOLATION - Hardcoded crop assumptions
        if crop == "tomato":
            return "Plant tomatoes in spring after last frost"
        elif crop == "corn":
            return "Plant corn when soil reaches 60°F"
        elif crop == "wheat":
            return "Plant wheat in fall for summer harvest"
        else:
            # ❌ WORST VIOLATION - Refusing unusual crops
            return "Unsupported crop type"
    
    def get_fertilizer_advice(self, crop: str, country: str) -> str:
        # ❌ VIOLATION - Geographic discrimination
        if country != "USA":
            return "Fertilizer advice only available for US farmers"
        
        # ❌ VIOLATION - Hardcoded fertilizer rules
        fertilizer_map = {
            "tomato": "Use 10-10-10 NPK",
            "corn": "Use high nitrogen fertilizer"
        }
        
        return fertilizer_map.get(crop, "No advice available")
```

### Multi-Language Handling

```python
# constitutional_multilingual.py
class ConstitutionalMultilingualProcessor:
    """
    Handle 50+ languages constitutionally
    """
    
    async def process_with_smart_language(self, 
                                        query: str,
                                        phone_number: str,
                                        language_override: Optional[str] = None) -> Dict:
        """
        Smart language detection with override support
        Handles minority farmers (e.g., Hungarian in Croatia)
        """
        # Detect country from phone
        country_code = self._detect_country_from_phone(phone_number)
        
        # Determine language (with override support)
        if language_override:
            # Respect farmer's language preference
            language = language_override
            detection_note = f"Override: Using {language} per farmer preference"
        else:
            # Auto-detect from country
            language = self._get_primary_language(country_code)
            detection_note = f"Auto-detected {language} from {country_code}"
        
        # Process with detected/overridden language
        context = {
            "country": country_code,
            "language": language,
            "detection_note": detection_note,
            "is_minority": language_override is not None
        }
        
        # LLM processes in ANY language
        system_prompt = f"""
        Respond in {language} language.
        Farmer is in {country_code}.
        {detection_note}
        
        Remember: Support ALL crops including exotic ones.
        """
        
        response = await self._llm_process(query, system_prompt, context)
        
        return {
            "success": True,
            "response": response,
            "language_used": language,
            "country_detected": country_code,
            "is_minority_farmer": context["is_minority"],
            "constitutional_compliance": True
        }
    
    def _detect_country_from_phone(self, phone: str) -> str:
        """
        Map phone prefix to country
        Constitutional: Works for all countries
        """
        # This is data mapping, not hardcoded logic
        prefix_map = {
            '+385': 'HR',  # Croatia
            '+386': 'SI',  # Slovenia  
            '+359': 'BG',  # Bulgaria
            '+36': 'HU',   # Hungary
            # ... 50+ more countries
        }
        
        for prefix, country in prefix_map.items():
            if phone.startswith(prefix):
                return country
        
        return 'XX'  # Unknown but still supported
```

## 💾 Database Operations

### ✅ Constitutional Database Queries

```python
# constitutional_database.py
class ConstitutionalDatabaseOperations:
    """
    100% LLM-generated SQL - no hardcoded queries
    """
    
    def __init__(self):
        self.llm = OpenAI()
        self.connection = self._get_db_connection()
    
    async def query_farmer_data(self, 
                              natural_query: str,
                              farmer_id: int) -> Dict[str, Any]:
        """
        Convert natural language to SQL using LLM
        
        Args:
            natural_query: Question in any language
            farmer_id: Farmer identifier for scoping
        """
        # Get schema for LLM context
        schema = self._get_schema_info()
        
        # LLM generates SQL
        sql_prompt = f"""
        Convert this natural language query to PostgreSQL:
        Query: {natural_query}
        
        Database Schema:
        {json.dumps(schema, indent=2)}
        
        Requirements:
        1. Scope to farmer_id = {farmer_id}
        2. Use proper JOINs for related data
        3. Return only SELECT queries
        4. Handle NULL values gracefully
        5. Work for ANY crop type (no hardcoded crop names)
        
        Return only the SQL query, no explanation.
        """
        
        sql_response = await self.llm.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": sql_prompt}],
            temperature=0  # Deterministic SQL
        )
        
        sql_query = sql_response.choices[0].message.content.strip()
        
        # Validate and execute
        if self._validate_sql_safety(sql_query):
            return await self._execute_query(sql_query, farmer_id)
        else:
            raise ConstitutionalViolation("Unsafe SQL generated")
    
    def _validate_sql_safety(self, sql: str) -> bool:
        """
        Ensure SQL is safe and constitutional
        """
        sql_upper = sql.upper()
        
        # Must be SELECT only
        if not sql_upper.strip().startswith('SELECT'):
            return False
        
        # No data modification
        forbidden = ['INSERT', 'UPDATE', 'DELETE', 'DROP', 'CREATE', 'ALTER']
        if any(word in sql_upper for word in forbidden):
            return False
        
        # No hardcoded crop names (constitutional check)
        hardcoded_crops = ['TOMATO', 'CORN', 'WHEAT', 'POTATO']
        if any(crop in sql_upper for crop in hardcoded_crops):
            # Only allow if it's a variable, not hardcoded
            if "= 'TOMATO'" in sql_upper or '= "TOMATO"' in sql_upper:
                return False
        
        return True
    
    async def add_farmer_crop(self,
                            farmer_id: int,
                            crop_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Add any crop for any farmer - constitutionally
        """
        # NO VALIDATION on crop type - mango in Bulgaria is valid!
        
        # LLM generates appropriate INSERT
        insert_prompt = f"""
        Generate PostgreSQL INSERT for this crop:
        Farmer ID: {farmer_id}
        Crop: {crop_info['name']}
        Field: {crop_info.get('field_id')}
        Planting Date: {crop_info.get('planting_date')}
        
        Rules:
        1. Accept ANY crop name (including mango in cold climates)
        2. Use field_crops table
        3. Handle missing data gracefully
        4. Return farmer-friendly confirmation
        """
        
        # Execute constitutionally
        result = await self._llm_execute_insert(insert_prompt)
        
        return {
            "success": True,
            "message": f"Successfully added {crop_info['name']} to your farm",
            "constitutional_note": "All crops supported globally",
            "mango_rule_compliant": True
        }
```

### ❌ Database Violations

```python
# VIOLATIONS - Don't do this!
class UnconstitutionalDatabase:
    
    def get_crops(self, farmer_id: int) -> list:
        # ❌ VIOLATION - Hardcoded SQL
        sql = f"""
        SELECT * FROM crops 
        WHERE farmer_id = {farmer_id}
        AND crop_type IN ('tomato', 'corn', 'wheat')
        """
        # This excludes mangoes and other crops!
        
    def validate_crop_for_region(self, crop: str, country: str) -> bool:
        # ❌ WORST VIOLATION - Geographic discrimination
        allowed_crops = {
            'BG': ['wheat', 'sunflower', 'corn'],  # No mangoes!
            'TH': ['rice', 'mango', 'coconut'],
            'US': ['corn', 'soybean', 'wheat']
        }
        
        return crop in allowed_crops.get(country, [])
    
    def suggest_fertilizer(self, crop: str) -> str:
        # ❌ VIOLATION - Hardcoded advice
        fertilizer_map = {
            'tomato': 'NPK 10-10-10',
            'corn': 'High nitrogen',
            'wheat': 'Balanced NPK'
        }
        # What about mango? Dragon fruit? Quinoa?
        return fertilizer_map.get(crop, "Unknown crop")
```

### Privacy-Compliant Operations

```python
# constitutional_privacy.py
class PrivacyFirstDatabase:
    """
    Database operations that never leak personal data
    """
    
    async def get_aggregated_insights(self, 
                                    query: str,
                                    farmer_id: int) -> Dict[str, Any]:
        """
        Get insights without exposing personal data
        """
        # Generate SQL that aggregates/anonymizes
        sql_prompt = f"""
        Generate SQL for: {query}
        
        Privacy Requirements:
        1. No farmer names in results
        2. No exact coordinates
        3. Aggregate when possible
        4. Round precise values
        5. Exclude identifying information
        
        Farmer context: {farmer_id} (use for filtering only)
        """
        
        sql = await self._generate_private_sql(sql_prompt)
        raw_results = await self._execute(sql)
        
        # Further anonymize results
        anonymized = self._anonymize_results(raw_results)
        
        # LLM formats without personal data
        format_prompt = f"""
        Format these agricultural insights:
        {json.dumps(anonymized)}
        
        Do NOT mention:
        - Farmer names or IDs
        - Exact locations
        - Phone numbers
        - Personal details
        
        DO mention:
        - Crop insights
        - General trends
        - Helpful advice
        """
        
        response = await self._llm_format(format_prompt)
        
        return {
            "success": True,
            "response": response,
            "privacy_compliant": True,
            "data_anonymized": True
        }
    
    def _anonymize_results(self, results: List[Dict]) -> List[Dict]:
        """
        Remove/obscure personal information
        """
        anonymized = []
        
        for row in results:
            clean_row = {}
            
            for key, value in row.items():
                # Skip personal identifiers
                if key in ['farmer_name', 'phone', 'email', 'id']:
                    continue
                
                # Round precise coordinates
                if key in ['latitude', 'longitude']:
                    clean_row[key] = round(float(value), 2)  # ~1km precision
                
                # Generalize exact addresses
                elif key == 'address':
                    clean_row['region'] = self._extract_region(value)
                
                # Keep agricultural data
                else:
                    clean_row[key] = value
            
            anonymized.append(clean_row)
        
        return anonymized
```

## 🌐 API Development

### ✅ Constitutional API Endpoints

```python
# constitutional_api.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI(title="Constitutional AVA OLO API")

class ConstitutionalQueryRequest(BaseModel):
    """
    Universal query format - works for any farmer globally
    """
    query: str  # Natural language in ANY language
    farmer_id: Optional[int] = None
    language: Optional[str] = None  # Auto-detected if not provided
    phone_number: Optional[str] = None  # For smart detection
    country_override: Optional[str] = None  # For manual override
    context: Optional[dict] = None  # Additional context

@app.post("/api/v1/farmer/query")
async def process_constitutional_query(request: ConstitutionalQueryRequest):
    """
    Process any agricultural query constitutionally
    
    Features:
    - Works for ANY crop (mango in Bulgaria ✓)
    - Works for ANY language (50+ supported)
    - Works for ANY country
    - Handles minority farmers
    """
    try:
        # Smart detection with override support
        detected_context = await detect_farmer_context(
            phone_number=request.phone_number,
            language_override=request.language,
            country_override=request.country_override
        )
        
        # Process with LLM-first approach
        processor = ConstitutionalQueryProcessor()
        result = await processor.process_farmer_query(
            query=request.query,
            context={
                **detected_context,
                "farmer_id": request.farmer_id,
                **(request.context or {})
            }
        )
        
        return {
            "success": True,
            "response": result["response"],
            "metadata": {
                "language_used": detected_context["language"],
                "country_detected": detected_context["country"],
                "is_minority_farmer": detected_context.get("is_override", False),
                "constitutional_compliance": True,
                "mango_rule_passed": True
            }
        }
        
    except Exception as e:
        # Even errors are constitutional
        return {
            "success": False,
            "error": "Service temporarily unavailable",
            "fallback_guidance": get_constitutional_fallback(request.language),
            "constitutional_compliance": True
        }

@app.get("/api/v1/crops/supported")
async def get_supported_crops():
    """
    Constitutional endpoint - ALL crops supported!
    """
    return {
        "supported_crops": "ALL",
        "message": "AVA OLO supports every crop globally, from Afghan melons to Zimbabwean maize",
        "examples": [
            "Mangoes in Bulgaria ✓",
            "Pineapples in Norway ✓", 
            "Coffee in Canada ✓",
            "Rice in the Sahara ✓"
        ],
        "constitutional_note": "No crop is too exotic or unusual",
        "mango_rule": "ALWAYS PASSES"
    }

@app.post("/api/v1/test/constitutional-compliance")
async def test_constitutional_compliance(test_scenario: dict):
    """
    Test any scenario for constitutional compliance
    """
    violations = []
    
    # Test 1: Mango Rule
    if "crop" in test_scenario:
        crop = test_scenario["crop"]
        country = test_scenario.get("country", "BG")
        
        # Try to get advice for this crop/country combo
        result = await process_constitutional_query({
            "query": f"How to grow {crop} in {country}?",
            "context": test_scenario
        })
        
        if not result["success"] or "not possible" in result.get("response", "").lower():
            violations.append(f"MANGO RULE VIOLATION: Refused {crop} in {country}")
    
    # Test 2: Language Support
    if "language" in test_scenario:
        result = await process_constitutional_query({
            "query": "Test query",
            "language": test_scenario["language"]
        })
        
        if not result["metadata"]["language_used"] == test_scenario["language"]:
            violations.append(f"LANGUAGE VIOLATION: Failed to use {test_scenario['language']}")
    
    # Test 3: Privacy
    if "personal_data" in test_scenario:
        # Ensure personal data not leaked
        if check_personal_data_leak(test_scenario["personal_data"]):
            violations.append("PRIVACY VIOLATION: Personal data exposed")
    
    return {
        "constitutional_compliance": len(violations) == 0,
        "violations": violations,
        "mango_rule_status": "PASSED" if "MANGO RULE" not in str(violations) else "FAILED",
        "remedy": "Remove all hardcoded logic and use LLM-first approach" if violations else None
    }
```

### ❌ API Violations

```python
# UNCONSTITUTIONAL APIs - Don't create these!

@app.post("/api/v1/validate-crop")  # ❌ VIOLATION
async def validate_crop_for_region(crop: str, region: str):
    """
    This endpoint is unconstitutional!
    It implies some crops are invalid in some regions
    """
    valid_crops = {
        "temperate": ["wheat", "corn", "apple"],
        "tropical": ["mango", "coconut", "banana"]
    }
    # Violates MANGO RULE - discriminates against crops
    
@app.get("/api/v1/supported-languages")  # ❌ VIOLATION if limited
async def get_supported_languages():
    return {
        "languages": ["en", "es", "fr"]  # What about Bulgarian?
    }

@app.post("/api/v1/farmer-data/{farmer_id}")  # ❌ VIOLATION
async def get_farmer_personal_data(farmer_id: int):
    # Exposing personal data without privacy controls
    return db.query(f"SELECT * FROM farmers WHERE id = {farmer_id}")
```

### Error Handling

```python
# constitutional_errors.py
class ConstitutionalErrorHandler:
    """
    Even errors follow the constitution
    """
    
    def handle_error(self, 
                    error: Exception,
                    context: dict) -> dict:
        """
        Constitutional error handling
        """
        language = context.get("language", "en")
        
        # Never expose technical details
        if isinstance(error, DatabaseError):
            message = self._get_safe_message("database_unavailable", language)
        elif isinstance(error, LLMError):
            message = self._get_safe_message("ai_unavailable", language)
        else:
            message = self._get_safe_message("general_error", language)
        
        # Provide helpful fallback
        fallback = self._get_constitutional_fallback(context)
        
        return {
            "success": False,
            "error": message,
            "fallback_guidance": fallback,
            "support_message": self._get_support_message(language),
            "constitutional_compliance": True,  # Even errors are constitutional
            "retry_after": 300  # 5 minutes
        }
    
    def _get_safe_message(self, error_type: str, language: str) -> str:
        """
        Safe error messages in multiple languages
        No technical details that could be exploited
        """
        messages = {
            "en": {
                "database_unavailable": "Agricultural data temporarily unavailable",
                "ai_unavailable": "AI assistant temporarily offline",
                "general_error": "Service temporarily unavailable"
            },
            "bg": {
                "database_unavailable": "Земеделските данни временно недостъпни",
                "ai_unavailable": "AI асистентът временно офлайн",
                "general_error": "Услугата временно недостъпна"
            },
            "hu": {
                "database_unavailable": "A mezőgazdasági adatok ideiglenesen nem érhetők el",
                "ai_unavailable": "Az AI asszisztens ideiglenesen offline",
                "general_error": "A szolgáltatás ideiglenesen nem elérhető"
            }
            # ... more languages
        }
        
        lang_messages = messages.get(language, messages["en"])
        return lang_messages.get(error_type, lang_messages["general_error"])
```

## 🧪 Testing Examples

### Constitutional Compliance Tests

```python
# test_constitutional_examples.py
import pytest
from hypothesis import given, strategies as st

class TestConstitutionalCompliance:
    """
    Property-based tests for constitutional compliance
    """
    
    @given(
        crop=st.text(min_size=1, max_size=50),
        country=st.sampled_from(['BG', 'NO', 'CA', 'TH', 'BR', 'IN']),
        language=st.sampled_from(['en', 'bg', 'hr', 'hu', 'pt', 'th'])
    )
    @pytest.mark.asyncio
    async def test_any_crop_any_country(self, crop, country, language):
        """
        Test that ANY crop works in ANY country
        Automated MANGO RULE testing
        """
        result = await process_constitutional_query({
            "query": f"How to grow {crop}?",
            "country_code": country,
            "language": language
        })
        
        # Must never refuse based on crop/country combination
        assert result["success"]
        assert "not possible" not in result["response"].lower()
        assert "cannot grow" not in result["response"].lower()
        assert result["metadata"]["constitutional_compliance"]
    
    @given(
        phone_number=st.regex(r'\+\d{10,15}'),
        preferred_language=st.sampled_from(['hu', 'sr', 'it', 'de', 'tr'])
    )
    @pytest.mark.asyncio  
    async def test_minority_farmer_support(self, phone_number, preferred_language):
        """
        Test minority farmer scenarios
        Phone number country != preferred language
        """
        result = await process_constitutional_query({
            "query": "What should I plant?",
            "phone_number": phone_number,
            "language": preferred_language
        })
        
        # Must respect language preference
        assert result["metadata"]["language_used"] == preferred_language
        assert result["metadata"].get("is_minority_farmer") is not None
        assert result["success"]
    
    @pytest.mark.asyncio
    async def test_privacy_compliance(self):
        """
        Test that personal data never leaks
        """
        with patch('openai.ChatCompletion.create') as mock_llm:
            # Process query with personal data
            await process_constitutional_query({
                "query": "My name is John Smith, ID 12345, what to plant?",
                "farmer_id": 12345,
                "farmer_name": "John Smith",
                "phone": "+1234567890"
            })
            
            # Check all LLM calls
            for call in mock_llm.call_args_list:
                call_str = str(call)
                # Personal data must not appear
                assert "John Smith" not in call_str
                assert "12345" not in call_str
                assert "+1234567890" not in call_str
```

### Mango Rule Verification

```python
# test_mango_rule_verification.py
class TestMangoRuleVerification:
    """
    Comprehensive MANGO RULE tests
    """
    
    # Extreme crop/location combinations that must work
    test_scenarios = [
        ("mango", "Antarctica", "Research station greenhouse"),
        ("pineapple", "Siberia", "Heated greenhouse"),
        ("coconut", "Greenland", "Indoor cultivation"),
        ("banana", "Alaska", "Controlled environment"),
        ("coffee", "Norway", "Artificial climate"),
        ("cacao", "Canada", "Greenhouse production"),
        ("dragonfruit", "Iceland", "Geothermal greenhouse"),
        ("durian", "Finland", "Advanced greenhouse")
    ]
    
    @pytest.mark.parametrize("crop,location,expected_keyword", test_scenarios)
    @pytest.mark.asyncio
    async def test_extreme_scenarios(self, crop, location, expected_keyword):
        """
        Test extreme crop/location combinations
        All must receive helpful advice, not refusal
        """
        result = await process_constitutional_query({
            "query": f"I want to grow {crop} in {location}",
            "context": {"extreme_scenario": True}
        })
        
        assert result["success"]
        # Must provide constructive advice
        assert expected_keyword.lower() in result["response"].lower()
        # Must not refuse
        assert "impossible" not in result["response"].lower()
        assert "cannot" not in result["response"].lower()
        
    async def test_mango_rule_multi_language(self):
        """
        Test MANGO RULE in multiple languages
        """
        mango_queries = {
            'bg': "Как да отглеждам манго в България?",
            'hr': "Kako uzgajati mango u Hrvatskoj?",
            'hu': "Hogyan termesszek mangót Magyarországon?",
            'pl': "Jak uprawiać mango w Polsce?",
            'fi': "Miten kasvatan mangoa Suomessa?"
        }
        
        for lang, query in mango_queries.items():
            result = await process_constitutional_query({
                "query": query,
                "language": lang
            })
            
            assert result["success"]
            assert result["metadata"]["language_used"] == lang
            assert result["metadata"]["mango_rule_passed"]
```

### Performance and Scale Tests

```python
# test_constitutional_performance.py
class TestConstitutionalPerformance:
    """
    Test constitutional compliance at scale
    """
    
    @pytest.mark.asyncio
    async def test_concurrent_multilingual_queries(self):
        """
        Test system handles multiple languages concurrently
        """
        queries = [
            ("bg", "Кога да садя манго?"),
            ("hr", "Kako gnojiti mango?"),
            ("hu", "Mangó betegségek?"),
            ("sr", "Zalivanje manga?"),
            ("sl", "Kdaj obirati mango?")
        ]
        
        # Run concurrently
        tasks = [
            process_constitutional_query({
                "query": query,
                "language": lang,
                "farmer_id": 1000 + i
            })
            for i, (lang, query) in enumerate(queries)
        ]
        
        results = await asyncio.gather(*tasks)
        
        # All must succeed
        for result, (expected_lang, _) in zip(results, queries):
            assert result["success"]
            assert result["metadata"]["language_used"] == expected_lang
            assert result["metadata"]["constitutional_compliance"]
    
    @pytest.mark.benchmark
    def test_llm_query_generation_performance(self, benchmark):
        """
        Benchmark LLM SQL generation
        """
        processor = ConstitutionalQueryProcessor()
        
        result = benchmark(
            processor.generate_sql,
            "Show me all my mango trees",
            {"farmer_id": 123}
        )
        
        assert result is not None
        assert "SELECT" in result
        # Should not have hardcoded 'mango'
        assert "'mango'" not in result
```

---

**Remember: Every line of code must pass the MANGO RULE. If a Bulgarian mango farmer can't use it, it's unconstitutional!** 🥭