# 📡 API Endpoints Reference

## 🌐 Overview

AVA OLO provides RESTful APIs across two main services: monitoring dashboards for visualization and agricultural core for data processing. All endpoints follow constitutional principles with 100% LLM-first processing.

## 🔗 Base URLs

### Production Endpoints
```
Monitoring Dashboards: https://[dashboard-id].us-east-1.awsapprunner.com
Agricultural Core: https://[core-id].us-east-1.awsapprunner.com
```

### Health Check URLs
```
Dashboards Health: https://[dashboard-id].us-east-1.awsapprunner.com/health
Core Health: https://[core-id].us-east-1.awsapprunner.com/health
```

## 📊 Monitoring Dashboards APIs

### Dashboard Navigation

#### GET /
**Purpose:** Main dashboard selector interface

**Response:**
```json
{
  "status": "operational",
  "available_dashboards": [
    {
      "name": "Business Analytics",
      "url": "/business",
      "description": "Farm business metrics and analytics"
    },
    {
      "name": "Agronomic Management",
      "url": "/agronomic",
      "description": "Crop and field management interface"
    },
    {
      "name": "Administration",
      "url": "/admin",
      "description": "System administration panel"
    }
  ],
  "constitutional_compliance": true
}
```

### Health & Status

#### GET /health
**Purpose:** Service health check for AWS App Runner

**Response:**
```json
{
  "status": "healthy",
  "service": "ava-olo-monitoring-dashboards",
  "version": "2.1.0",
  "database_connected": true,
  "timestamp": "2024-01-13T10:30:00Z"
}
```

### Business Dashboard

#### GET /business
**Purpose:** Business analytics dashboard interface

**Query Parameters:**
- `farmer_id` (optional): Filter by specific farmer
- `date_from` (optional): Start date for analytics
- `date_to` (optional): End date for analytics
- `language` (optional): UI language code

**Response:** HTML dashboard interface

#### GET /api/business/metrics
**Purpose:** Get business metrics data

**Request:**
```json
{
  "farmer_id": 123,
  "metric_type": "revenue",
  "period": "monthly",
  "year": 2024
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "metric_type": "revenue",
    "values": [
      {"month": "January", "value": 15000, "currency": "EUR"},
      {"month": "February", "value": 12000, "currency": "EUR"}
    ],
    "total": 27000,
    "currency": "EUR"
  }
}
```

### Agronomic Dashboard

#### GET /agronomic
**Purpose:** Agronomic management dashboard interface

**Features:**
- Field management
- Crop tracking
- Task scheduling
- Weather integration

#### GET /api/agronomic/fields/{farmer_id}
**Purpose:** Get farmer's field data

**Response:**
```json
{
  "success": true,
  "fields": [
    {
      "field_id": 1,
      "name": "North Field",
      "size_hectares": 5.5,
      "crops": [
        {
          "crop_name": "Tomatoes",
          "planted_date": "2024-03-15",
          "expected_harvest": "2024-07-20",
          "status": "growing"
        }
      ],
      "soil_type": "Loamy",
      "last_analysis": "2024-01-10"
    }
  ]
}
```

#### GET /api/agronomic/tasks/{farmer_id}
**Purpose:** Get agricultural tasks

**Query Parameters:**
- `status`: pending|completed|overdue
- `crop`: Filter by crop type
- `urgency`: high|medium|low

**Response:**
```json
{
  "success": true,
  "tasks": [
    {
      "task_id": 101,
      "description": "Apply fertilizer to tomato field",
      "due_date": "2024-01-20",
      "priority": "high",
      "field_id": 1,
      "status": "pending",
      "instructions": "Use NPK 15-15-15 at 200kg/ha"
    }
  ]
}
```

### Administrative Dashboard

#### GET /admin
**Purpose:** System administration interface

**Required:** Admin authentication

#### GET /api/admin/stats
**Purpose:** System-wide statistics

**Response:**
```json
{
  "total_farmers": 1250,
  "active_farmers": 980,
  "total_fields": 5420,
  "total_area_hectares": 12500,
  "countries_served": 15,
  "languages_active": 12,
  "constitutional_compliance": {
    "mango_rule": true,
    "llm_first": true,
    "privacy_first": true
  }
}
```

## 🌾 Agricultural Core APIs

### Natural Language Query Processing

#### POST /api/v1/farmer/query
**Purpose:** Process natural language queries with LLM-first approach

**Request:**
```json
{
  "query": "Koliko hektara zemlje imam?",  // Croatian: How many hectares of land do I have?
  "farmer_id": 123,
  "language": "hr",
  "country_code": "HR"
}
```

**Response:**
```json
{
  "success": true,
  "response": "Imate ukupno 15.5 hektara zemlje raspoređenih na 3 parcele: Sjeverna parcela (5.5 ha), Južna parcela (6 ha) i Zapadna parcela (4 ha).",
  "constitutional_compliance": true,
  "method": "llm_first",
  "metadata": {
    "timestamp": "2024-01-13T10:30:00Z",
    "language": "hr",
    "country_code": "HR",
    "compliance": {
      "llm_first": true,
      "mango_rule": true,
      "privacy_first": true
    }
  }
}
```

#### POST /api/v1/farmer/query (Hungarian Minority Example)
**Purpose:** Demonstrate minority farmer support

**Request:**
```json
{
  "query": "Milyen növényeket termesztek?",  // Hungarian: What crops am I growing?
  "farmer_id": 456,
  "language": "hu",
  "phone_number": "+385987654321",  // Croatian number
  "ethnicity": "Hungarian"
}
```

**Response:**
```json
{
  "success": true,
  "response": "Jelenleg a következő növényeket termeszti: paradicsomot (2 hektáron), paprikát (1.5 hektáron) és uborkát (1 hektáron). A paradicsom július végén lesz betakarítható.",
  "constitutional_compliance": true,
  "method": "llm_first",
  "metadata": {
    "language_detected": "hr",
    "language_used": "hu",
    "override_applied": true,
    "country": "HR"
  }
}
```

### Farmer-Specific Endpoints

#### GET /api/v1/farmer/{farmer_id}/fields
**Purpose:** Get farmer's fields (LLM-enhanced)

**Parameters:**
- `farmer_id`: Required farmer identifier
- `language`: Optional language code (default: auto-detect)

**Response:**
```json
{
  "success": true,
  "response": "You have 3 fields totaling 15.5 hectares. Your North Field (5.5 ha) has tomatoes, South Field (6 ha) has peppers, and West Field (4 ha) is currently fallow.",
  "farmer_id": 123,
  "constitutional_compliance": true
}
```

#### GET /api/v1/farmer/{farmer_id}/crops
**Purpose:** Get current crops information

**Response:**
```json
{
  "success": true,
  "response": "You are currently growing: tomatoes (2 hectares, harvest in July), peppers (1.5 hectares, harvest in August), and preparing corn planting for next season.",
  "farmer_id": 123,
  "constitutional_compliance": true
}
```

#### GET /api/v1/farmer/{farmer_id}/tasks
**Purpose:** Get agricultural tasks with LLM formatting

**Query Parameters:**
- `urgency`: Filter by task urgency
- `language`: Response language

**Response:**
```json
{
  "success": true,
  "response": "You have 3 urgent tasks this week: 1) Fertilize tomato field by Friday (use NPK 15-15-15), 2) Check irrigation system in South Field, 3) Schedule soil analysis for West Field.",
  "farmer_id": 123,
  "constitutional_compliance": true
}
```

### Constitutional Compliance Tests

#### POST /api/v1/test/mango-rule
**Purpose:** Test Bulgarian mango farmer scenario

**Request:** None required (uses test data)

**Response:**
```json
{
  "test": "Bulgarian Mango Farmer",
  "passed": true,
  "constitutional_compliance": true,
  "response": "Имате 25 манго дървета на площ от 2 хектара. Очакваната реколта е 5 тона манго през август.",
  "details": {
    "query": "Колко манго дървета имам?",
    "language": "bg",
    "country": "BG",
    "method": "llm_first"
  }
}
```

#### POST /api/v1/test/slovenian-farmer
**Purpose:** Test Slovenian farmer localization

**Response:**
```json
{
  "test": "Slovenian Tomato Farmer",
  "passed": true,
  "constitutional_compliance": true,
  "response": "Paradižnik morate škropiti proti plesni vsakih 10-14 dni v vlažnem vremenu. Uporabite bakrene pripravke ali sistemične fungicide."
}
```

#### POST /api/v1/test/complex-query
**Purpose:** Test complex agricultural query processing

**Response:**
```json
{
  "test": "Complex Agricultural Query",
  "passed": true,
  "constitutional_compliance": true,
  "response": "You have tomatoes planted in 2 fields: North Field (1.5 ha, harvest July 20) and East Field (0.5 ha, harvest July 25). Total expected yield: 120 tons."
}
```

### Knowledge & Search APIs

#### POST /api/v1/knowledge/search
**Purpose:** Search agricultural knowledge base

**Request:**
```json
{
  "query": "tomato blight treatment organic",
  "language": "en",
  "farmer_location": "HR"
}
```

**Response:**
```json
{
  "success": true,
  "results": [
    {
      "title": "Organic Tomato Blight Control",
      "content": "Use copper-based fungicides, ensure proper spacing, remove infected leaves...",
      "relevance_score": 0.95,
      "source": "Agricultural Extension Database"
    }
  ]
}
```

#### POST /api/v1/external/weather
**Purpose:** Get weather data for farm location

**Request:**
```json
{
  "farmer_id": 123,
  "days_ahead": 7
}
```

**Response:**
```json
{
  "success": true,
  "location": "Zagreb, Croatia",
  "forecast": [
    {
      "date": "2024-01-14",
      "temp_high": 8,
      "temp_low": 2,
      "precipitation_mm": 5,
      "conditions": "Light rain"
    }
  ],
  "farming_advisory": "Light rain expected - good for recent plantings, check drainage in low areas."
}
```

## 🔐 Authentication & Security

### API Key Authentication

**Header Format:**
```
Authorization: Bearer {api_key}
X-Farmer-ID: {farmer_id}
```

### Rate Limiting
- **Default:** 1000 requests/hour per API key
- **Burst:** 50 requests/minute
- **Query endpoint:** 100 requests/hour per farmer

### Error Responses

#### 400 Bad Request
```json
{
  "error": "Invalid request",
  "message": "Missing required parameter: farmer_id",
  "code": "MISSING_PARAMETER"
}
```

#### 401 Unauthorized
```json
{
  "error": "Unauthorized",
  "message": "Invalid or missing API key",
  "code": "AUTH_FAILED"
}
```

#### 429 Too Many Requests
```json
{
  "error": "Rate limit exceeded",
  "message": "Too many requests. Please retry after 3600 seconds",
  "retry_after": 3600
}
```

#### 500 Internal Server Error
```json
{
  "error": "Internal server error",
  "message": "An unexpected error occurred",
  "request_id": "req_12345",
  "constitutional_note": "Error logged with privacy compliance"
}
```

## 🌍 Localization Support

### Supported Languages
```json
{
  "supported_languages": [
    {"code": "en", "name": "English"},
    {"code": "hr", "name": "Croatian"},
    {"code": "sl", "name": "Slovenian"},
    {"code": "bg", "name": "Bulgarian"},
    {"code": "hu", "name": "Hungarian"},
    {"code": "sr", "name": "Serbian"},
    {"code": "de", "name": "German"},
    {"code": "it", "name": "Italian"},
    {"code": "es", "name": "Spanish"},
    {"code": "pt", "name": "Portuguese"}
  ]
}
```

### Language Detection Flow
1. Check `language` parameter in request
2. Detect from `phone_number` if provided
3. Use farmer's `preferred_language` from database
4. Default to country's primary language
5. Fallback to English

## 📝 Request/Response Examples

### Example 1: Simple Field Query
```bash
curl -X POST https://[core-id].awsapprunner.com/api/v1/farmer/query \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "query": "How many fields do I have?",
    "farmer_id": 123
  }'
```

### Example 2: Complex Multi-language Query
```bash
curl -X POST https://[core-id].awsapprunner.com/api/v1/farmer/query \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "query": "Покажи ми всички домати",
    "farmer_id": 789,
    "language": "bg",
    "country_code": "BG"
  }'
```

### Example 3: Minority Farmer Support
```bash
curl -X POST https://[core-id].awsapprunner.com/api/v1/farmer/query \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "query": "Mutasd meg a terméseimet",
    "farmer_id": 456,
    "language": "hu",
    "phone_number": "+385123456789",
    "ethnicity": "Hungarian"
  }'
```

## 🧪 Testing Endpoints

### Health Check Test
```bash
curl https://[dashboard-id].awsapprunner.com/health
```

### Constitutional Compliance Test
```bash
curl -X POST https://[core-id].awsapprunner.com/api/v1/test/mango-rule
```

### Load Test Example
```bash
# Test with Apache Bench
ab -n 1000 -c 10 https://[core-id].awsapprunner.com/health
```

---

**Constitutional Note:** All endpoints follow the MANGO RULE - they work equally well for a Bulgarian mango farmer or a Hungarian minority farmer in Croatia. Every response is generated using LLM-first principles with complete privacy protection.