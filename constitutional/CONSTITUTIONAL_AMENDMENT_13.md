# 📜 CONSTITUTIONAL AMENDMENT #13: COUNTRY-BASED LOCALIZATION

## 🆕 NEW CONSTITUTIONAL PRINCIPLE #13

### 🌍 COUNTRY-AWARE LOCALIZATION: WhatsApp-Driven Intelligence
- **WhatsApp number determines farmer's country** (phone prefix)
- **System auto-localizes for that specific country**
- **All responses tailored to farmer's location context**
- **LLM intelligence handles country-specific agricultural practices**

## 🏷️ INFORMATION RELEVANCE HIERARCHY

Every piece of information in the system must be **explicitly labeled** with relevance scope:

### 🧑‍🌾 FARMER-SPECIFIC (Highest Priority)
```python
# Examples:
- "John's tomato field needs watering"
- "Maria's harvest scheduled for next week"
- "Farmer's specific crop rotation plan"

# Database: farmer_id linked
# Usage: Only for that specific farmer
# Privacy: NEVER external APIs
```

### 🇸🇮 COUNTRY-SPECIFIC (Medium Priority)  
```python
# Examples:
- "Slovenia's organic certification requirements"
- "Bulgarian mango growing season timing"
- "Croatian pesticide regulations for tomatoes"

# Database: country_code linked
# RAG Sources: Country-specific documents
# Usage: All farmers from that country
```

### 🌍 GLOBAL (Lowest Priority)
```python
# Examples:
- "General tomato pest management"
- "Universal crop rotation principles"
- "Basic irrigation techniques"

# Sources: Global agricultural knowledge
# Usage: Fallback when no country-specific info
# External: Perplexity for general research
```

## 🔄 LOCALIZATION WORKFLOW

### 1. **WhatsApp Number Analysis**
```python
def determine_farmer_country(whatsapp_number):
    # +386 → Slovenia
    # +359 → Bulgaria  
    # +385 → Croatia
    # +1 → USA/Canada
    # etc.
    
    country_code = extract_country_from_phone(whatsapp_number)
    return country_code
```

### 2. **Contextualized Query Processing**
```python
def process_farmer_query(query, whatsapp_number):
    farmer = get_farmer_by_phone(whatsapp_number)
    country = determine_farmer_country(whatsapp_number)
    
    # Priority 1: Farmer-specific data
    farmer_result = search_farmer_data(query, farmer.id)
    
    # Priority 2: Country-specific knowledge
    country_result = search_country_knowledge(query, country)
    
    # Priority 3: Global knowledge
    global_result = search_global_knowledge(query)
    
    # LLM combines with country context
    return llm_synthesize(farmer_result, country_result, global_result, country)
```

### 3. **Language Intelligence**
```python
def get_farmer_language(whatsapp_number, country):
    # LLM determines appropriate language
    # Slovenia → Slovenian (primary)
    # Bulgaria → Bulgarian (primary)  
    # Multi-language countries → detect or ask
    
    return llm_determine_language(country, farmer_preferences)
```

## 🗄️ DATABASE SCHEMA ENHANCEMENT

### Enhanced Farmer Table
```sql
-- Constitutional compliance: PostgreSQL only
ALTER TABLE farmers ADD COLUMN country_code VARCHAR(3);
ALTER TABLE farmers ADD COLUMN preferred_language VARCHAR(10);
ALTER TABLE farmers ADD COLUMN whatsapp_number VARCHAR(20) UNIQUE;

-- Examples:
-- +386123456789 → SI, slovenian
-- +359123456789 → BG, bulgarian
-- +385123456789 → HR, croatian
```

### Knowledge Source Labeling
```sql
-- Every knowledge source labeled by relevance
CREATE TABLE knowledge_sources (
    id SERIAL PRIMARY KEY,
    content TEXT,
    relevance_type VARCHAR(20), -- 'FARMER', 'COUNTRY', 'GLOBAL'
    farmer_id INTEGER,          -- NULL if not farmer-specific
    country_code VARCHAR(3),    -- NULL if not country-specific
    language VARCHAR(10),
    source_type VARCHAR(50)     -- 'database', 'rag', 'external'
);
```

## 🎯 CONSTITUTIONAL COMPLIANCE

### ✅ Maintains All Existing Principles

**🥭 MANGO RULE**: Enhanced! 
- Bulgarian mango farmer gets Bulgarian language
- Bulgarian agricultural regulations
- Bulgarian seasonal timing
- But still works universally

**🔒 PRIVACY-FIRST**: Enhanced!
- Farmer data stays farmer-specific
- Country data shared only within country
- Global data available to all

**🧠 LLM-FIRST**: Enhanced!
- AI determines appropriate country context
- LLM handles language/cultural nuances
- No hardcoded country-specific rules

## 🌍 IMPLEMENTATION EXAMPLE

### Scenario: Bulgarian Mango Farmer
```python
# WhatsApp: +359123456789 (Bulgaria)
query = "Кога да бера манго?" (When to harvest mango?)

# System response:
1. Farmer-specific: "Your mango trees in field #3..."
2. Country-specific: "In Bulgaria, mango harvest typically..."  
3. Global fallback: "Mango harvest signs include..."
4. Language: Response in Bulgarian
5. Context: Bulgarian climate, regulations, practices
```

### Scenario: Slovenian Tomato Farmer  
```python
# WhatsApp: +386123456789 (Slovenia)
query = "Ali lahko uporabim Prosaro?"

# System response:
1. Farmer-specific: "On your tomato field, last spray was..."
2. Country-specific: "Prosaro PHI in Slovenia is 14 days..."
3. Global fallback: "Prosaro general usage guidelines..."
4. Language: Response in Slovenian
5. Context: EU regulations, Slovenian approval status
```

## 🚨 CONSTITUTIONAL VIOLATIONS TO AVOID

### ❌ WRONG: Hardcoded Country Logic
```python
# VIOLATION: Hardcoded patterns
if country == "Slovenia":
    return "Use metric system"
elif country == "USA":
    return "Use imperial system"
```

### ✅ CORRECT: LLM-First Country Intelligence
```python
# Constitutional: LLM handles country context
country_context = f"Farmer is in {country}"
response = llm_process_with_context(query, country_context)
```

## 🧪 MANGO TEST ENHANCEMENT

### Updated Constitutional Test
**"Can a Bulgarian mango farmer ask 'When to harvest mango?' in Bulgarian and get a response that considers Bulgarian climate, regulations, and seasonal timing?"**

**Expected Result:**
- ✅ Response in Bulgarian language
- ✅ Bulgarian agricultural context
- ✅ Farmer's specific mango field data
- ✅ Bulgarian seasonal timing
- ✅ Bulgarian regulatory compliance

## 📊 BENEFITS

1. **Enhanced User Experience**: Farmers get locally relevant information
2. **Regulatory Compliance**: Country-specific agricultural laws respected  
3. **Cultural Sensitivity**: Local farming practices incorporated
4. **Language Intelligence**: Natural communication in farmer's language
5. **Scalability**: Easy expansion to new countries
6. **Privacy Maintained**: Information shared appropriately by relevance level

## 🔄 MIGRATION STRATEGY

1. **Phase 1**: Add country detection from WhatsApp numbers
2. **Phase 2**: Label existing knowledge sources by relevance
3. **Phase 3**: Implement country-aware query processing
4. **Phase 4**: Add country-specific RAG sources
5. **Phase 5**: Test with farmers from multiple countries

This amendment transforms AVA OLO from a universal system to an **intelligently localized** system while maintaining constitutional compliance and global scalability! 🌾🌍