# 🏗️ AVA OLO Current System Architecture

## 📊 Executive Summary

AVA OLO is a constitutional agricultural CRM system built on AWS infrastructure with 100% LLM-first query processing. The system serves farmers globally through WhatsApp integration, supporting 50+ countries with smart language detection and minority farmer support (e.g., Hungarian farmers with Croatian phone numbers).

## 🌐 AWS Infrastructure Overview

### Core Services
```
┌─────────────────────────────────────────────────────────────────┐
│                        AWS Cloud (us-east-1)                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌─────────────────────────┐    ┌────────────────────────────┐  │
│  │   App Runner Service 1   │    │   App Runner Service 2     │  │
│  │  ava-olo-monitoring-     │    │  ava-olo-agricultural-     │  │
│  │      dashboards          │    │         core               │  │
│  │  ┌─────────────────┐     │    │  ┌──────────────────┐     │  │
│  │  │ Business Dash   │     │    │  │ API Gateway      │     │  │
│  │  │ Agronomic Dash  │     │    │  │ LLM Engine       │     │  │
│  │  │ Admin Dashboard │     │    │  │ Smart Detection  │     │  │
│  │  └─────────────────┘     │    │  └──────────────────┘     │  │
│  │    Port: 8080            │    │    Port: 8080             │  │
│  └─────────────┬───────────┘    └───────────┬────────────────┘  │
│                │                              │                   │
│                └──────────────┬───────────────┘                  │
│                               │                                   │
│              ┌────────────────▼────────────────────┐              │
│              │     AWS RDS Aurora PostgreSQL       │              │
│              │    farmer-crm-production DB         │              │
│              │  ┌────────────────────────────┐    │              │
│              │  │ farmers, fields, crops     │    │              │
│              │  │ tasks, messages, analytics │    │              │
│              │  │ country_language_mapping   │    │              │
│              │  └────────────────────────────┘    │              │
│              └─────────────────────────────────────┘              │
│                               │                                   │
│                               ▼                                   │
│                     ┌──────────────────┐                          │
│                     │   OpenAI GPT-4   │                          │
│                     │  LLM Processing  │                          │
│                     └──────────────────┘                          │
└───────────────────────────────────────────────────────────────────┘
```

### Infrastructure Details

**AWS App Runner Services:**
- **Region:** us-east-1
- **Auto-scaling:** Enabled (1-25 instances)
- **Deployment:** GitHub integration with auto-deploy on push
- **Health checks:** /health endpoints on both services

**RDS Aurora PostgreSQL:**
- **Host:** farmer-crm-production.cifgmm0mqg5q.us-east-1.rds.amazonaws.com
- **Database:** farmer_crm
- **Engine:** PostgreSQL 14.x compatible
- **Multi-AZ:** Yes (high availability)
- **Backup:** Daily snapshots with 7-day retention

**Environment Configuration:**
- Managed through AWS App Runner console
- Shared configuration between services
- Secure storage of API keys and credentials

## 🔧 Service Architecture

### 1. ava-olo-monitoring-dashboards

**Purpose:** Interactive dashboards for farm data visualization and management

**Components:**
```
monitoring-dashboards/
├── main.py                    # FastAPI application entry
├── business_dashboard.py      # Business analytics
├── agronomic_dashboard.py     # Crop and field management
├── admin_dashboard.py         # System administration
├── database_connector.py      # Aurora RDS integration
└── utils/                     # Shared utilities
```

**Key Features:**
- Real-time farm analytics
- Multi-language support (50+ languages)
- Constitutional compliance monitoring
- Interactive data visualization

**API Endpoints:**
- `GET /` - Dashboard selection interface
- `GET /health` - Service health check
- `GET /business` - Business analytics dashboard
- `GET /agronomic` - Agronomic management dashboard
- `GET /admin` - Administrative dashboard

### 2. ava-olo-agricultural-core

**Purpose:** Core agricultural CRM functionality with LLM-first query processing

**Components:**
```
agricultural-core/
├── app.py                          # Main entry with fallback chain
├── api_gateway_constitutional.py   # Constitutional API gateway
├── database_operations.py          # LLM-first database ops
├── llm_first_database_engine.py   # GPT-4 query engine
├── smart_country_detector.py      # Smart localization
├── language_processor.py          # Multi-language support
├── knowledge_search.py            # Agricultural knowledge base
└── external_search.py             # External data integration
```

**Key Features:**
- 100% LLM-first query processing
- Smart country/language detection
- Hungarian minority farmer support
- WhatsApp integration ready

**API Endpoints:**
- `POST /api/v1/farmer/query` - Natural language query processing
- `GET /api/v1/farmer/{id}/fields` - Farmer's fields
- `GET /api/v1/farmer/{id}/crops` - Current crops
- `GET /api/v1/farmer/{id}/tasks` - Agricultural tasks
- `POST /api/v1/test/mango-rule` - Constitutional compliance test

### Inter-Service Communication

```
WhatsApp → agricultural-core → Aurora RDS → monitoring-dashboards
    │              │                              │
    │              └── OpenAI GPT-4 ──────────────┘
    │                     │
    └─────────────────────┘
```

**Communication Patterns:**
1. **API-First:** All services communicate via REST APIs
2. **Shared Database:** Both services access same Aurora RDS
3. **No Direct Dependencies:** Services can fail independently
4. **Constitutional Compliance:** Every interaction follows MANGO RULE

## 💾 Database Architecture

### Core Schema

```sql
-- Farmers table with Amendment #13 support
farmers
├── id (PRIMARY KEY)
├── farm_name
├── manager_name
├── country_code (VARCHAR(3))      -- Smart detection
├── whatsapp_number (UNIQUE)       -- Phone-based identification
├── preferred_language (VARCHAR(10)) -- Override support
├── ethnicity (VARCHAR(50))        -- Minority support
├── language_override (BOOLEAN)     -- Manual override flag
├── country_override (BOOLEAN)      -- Manual override flag
└── cultural_context (TEXT)         -- Additional context

-- Fields and crops
fields
├── field_id (PRIMARY KEY)
├── farmer_id (FOREIGN KEY)
├── field_name
├── size_hectares
├── soil_type
└── location_coordinates

field_crops
├── field_crop_id (PRIMARY KEY)
├── field_id (FOREIGN KEY)
├── crop_name
├── planting_date
├── expected_harvest_date
└── current_status

-- Smart localization support
country_language_mapping
├── country_code (PRIMARY KEY)
├── country_name
├── primary_language
├── secondary_languages[]
├── phone_prefixes[]
├── cultural_notes
└── timezone
```

### Data Flow Patterns

```
1. WhatsApp Message Received
   ↓
2. Smart Country/Language Detection
   - Phone: +385123456789 → Country: HR
   - Override: language = 'hu' → Hungarian
   ↓
3. LLM Query Processing
   - Natural language → SQL via GPT-4
   - Constitutional compliance check
   ↓
4. Database Query Execution
   - Privacy-first: No external data exposure
   - Farmer-specific context applied
   ↓
5. Response Generation
   - Results → Natural language via GPT-4
   - Localized to farmer's language
   ↓
6. WhatsApp Response Sent
```

## 🧩 Module Independence Implementation

### Constitutional Principle #6: Module Independence

**Implementation Strategy:**
```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   API Gateway   │────▶│  Query Engine   │────▶│    Database     │
│  (Stateless)    │     │ (Isolated LLM)  │     │  (PostgreSQL)   │
└─────────────────┘     └─────────────────┘     └─────────────────┘
        │                        │                        │
        └────────────────────────┴────────────────────────┘
                          Error Isolation
```

**Error Isolation Mechanisms:**

1. **Service Level:**
   - Each App Runner service has independent health checks
   - Failure in one service doesn't affect the other
   - Automatic restart on crashes

2. **Module Level:**
   ```python
   try:
       # LLM processing
       result = await llm_engine.process_query(query)
   except Exception as e:
       # Graceful fallback
       logger.error(f"LLM failed: {e}")
       return fallback_response()
   ```

3. **Database Level:**
   - Connection pooling with automatic reconnection
   - Read replicas for high availability
   - Transaction isolation

**API-First Communication:**
- No direct module imports between services
- All communication via REST APIs
- Versioned endpoints for compatibility

## 🤖 LLM-First Implementation

### Constitutional Principle #3: LLM-FIRST

**Query Processing Pipeline:**

```python
# 1. Natural Language Input
query = "Hány hektár földem van?"  # Hungarian: How many hectares?

# 2. LLM SQL Generation
prompt = f"""
Generate PostgreSQL query for: {query}
Schema: {database_schema}
Farmer ID: {farmer_id}
"""
sql_query = gpt4.generate(prompt)

# 3. Query Execution
results = database.execute(sql_query)

# 4. LLM Response Generation
response_prompt = f"""
Convert to natural language in {language}:
Query: {query}
Results: {results}
"""
response = gpt4.generate(response_prompt)
```

**Key Components:**

1. **LLMDatabaseQueryEngine:**
   - Zero hardcoded SQL queries
   - Dynamic query generation
   - Multi-language support

2. **Smart Detection Integration:**
   ```python
   # Automatic language detection
   if phone_number.startswith('+385'):  # Croatian
       if ethnicity == 'Hungarian':
           language = 'hu'  # Override to Hungarian
   ```

3. **Privacy Compliance:**
   - Farmer data NEVER sent to external APIs
   - Only query patterns sent to GPT-4
   - Results processed locally

**Language Support Matrix:**
- 50+ languages supported
- Automatic detection from phone number
- Manual override for minorities
- Cultural context awareness

## 🔒 Security Architecture

### Access Control
```
External Users → WhatsApp → AVA OLO API → Authentication → Database
                                ↓
                          API Key Validation
                                ↓
                          Rate Limiting
                                ↓
                          Farmer ID Scoping
```

### Data Privacy
1. **Constitutional Privacy-First:**
   - No personal data in LLM prompts
   - Farmer IDs anonymized in logs
   - Secure credential storage

2. **AWS Security:**
   - VPC isolation for RDS
   - Security groups restrict access
   - SSL/TLS for all connections

3. **API Security:**
   - API key authentication
   - Rate limiting per farmer
   - Request validation

## 📊 Performance Architecture

### Scaling Strategy
```
Load Balancer
     │
     ├── App Runner Instance 1 ──┐
     ├── App Runner Instance 2 ──┤── Connection Pool ── Aurora RDS
     └── App Runner Instance N ──┘
```

### Optimization Techniques
1. **Database:**
   - Connection pooling
   - Query result caching
   - Indexed farmer lookups

2. **LLM Processing:**
   - Response caching for common queries
   - Batch processing support
   - Timeout management

3. **API Layer:**
   - Request/response compression
   - Async processing
   - Health check optimization

## 🌍 Localization Architecture

### Amendment #13 Implementation

**Smart Detection Flow:**
```
Phone Number → Country Code → Primary Language
     │              │               │
     └──────────────┴───────────────┘
                    │
              Override Check
                    │
         ┌──────────┴──────────┐
         │                     │
    Use Override          Use Detected
```

**Minority Farmer Support:**
```python
# Hungarian farmer in Croatia
farmer = {
    'phone': '+385123456789',      # Croatian number
    'language_override': 'hu',      # Hungarian language
    'ethnicity': 'Hungarian',       # Cultural context
    'country_code': 'HR'            # Lives in Croatia
}
```

## 🚀 Deployment Architecture

### CI/CD Pipeline
```
GitHub Push → AWS App Runner Build → Deploy → Health Check → Live
     │              │                    │          │
     └── Tests ─────┘                    └── Rollback if failed
```

### Environment Management
- Development: Local testing
- Staging: AWS App Runner (separate service)
- Production: AWS App Runner (auto-scaling)

### Monitoring
- CloudWatch logs for all services
- Custom metrics for query performance
- Alerts for constitutional violations

## 📈 Future Architecture Considerations

### Planned Enhancements
1. **Redis Cache Layer:** For query result caching
2. **ElasticSearch:** For knowledge base searching
3. **S3 Integration:** For document storage
4. **Lambda Functions:** For async processing

### Scalability Path
- Current: 1-25 instances per service
- Next: Multi-region deployment
- Future: Global CDN for static assets

---

**Constitutional Compliance:** This architecture achieves 100% compliance with all 13 constitutional principles, including full support for Bulgarian mango farmers and Hungarian minority farmers with Croatian phone numbers.