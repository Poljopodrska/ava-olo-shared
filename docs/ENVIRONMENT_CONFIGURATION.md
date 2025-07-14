# 🔧 AVA OLO Environment Configuration Guide

## 🏛️ Constitutional Configuration Management

As of 2025-07-13, AVA OLO uses a **single centralized .env file** in the root directory to maintain constitutional compliance and prevent configuration drift.

### 📍 Configuration Location

```
/ava-olo-constitutional/
├── .env              # ← SINGLE SOURCE OF TRUTH (production values)
├── .env.example      # ← Template for new deployments
└── [no other .env files in subdirectories]
```

### 🚨 IMPORTANT: Configuration Hierarchy

1. **Root .env file** (`/ava-olo-constitutional/.env`)
   - Contains ALL configuration for ALL services
   - This is the ONLY .env file that should exist
   - All services inherit from this single configuration

2. **No subdirectory .env files**
   - Previously had 10 duplicate .env files in subdirectories
   - These have been removed to prevent configuration conflicts
   - Services should reference the root .env file

## 🏛️ Constitutional Principles in Configuration

### 1. PostgreSQL Only (Principle #2)
```env
DB_HOST=farmer-crm-production.cifgmm0mqg5q.us-east-1.rds.amazonaws.com
DB_NAME=farmer_crm
DB_USER=postgres
DB_PASSWORD=<secure-password>
DB_PORT=5432
DATABASE_URL=postgresql://${DB_USER}:${DB_PASSWORD}@${DB_HOST}:${DB_PORT}/${DB_NAME}
```

### 2. LLM-First (Principle #3)
```env
OPENAI_API_KEY=sk-proj-<your-key>
OPENAI_MODEL=gpt-4
OPENAI_TEMPERATURE=0.7
```

### 3. Privacy-First (Principle #5)
```env
PERPLEXITY_API_KEY=pplx-<your-key>
ENABLE_PRIVACY_MODE=true
```

### 4. Production-Ready (Principle #10)
```env
APP_ENV=production
AWS_REGION=us-east-1
AWS_RDS_ENDPOINT=<production-endpoint>
```

### 5. Country-Aware (Amendment #13)
```env
DEFAULT_LANGUAGE=en
SUPPORTED_LANGUAGES=en,sl,hr,bg,de,fr,es,it,pt,sr
TIMEZONE_DEFAULT=UTC
```

## 🔐 Security Considerations

### Sensitive Values
The following keys contain sensitive data and should NEVER be committed to Git:
- `DB_PASSWORD`
- `OPENAI_API_KEY`
- `PERPLEXITY_API_KEY`
- `PINECONE_API_KEY`
- `SESSION_SECRET`

### Environment-Specific Values
```env
# Development
APP_ENV=development
LOG_LEVEL=DEBUG
API_GATEWAY_URL=http://localhost:8000

# Production
APP_ENV=production
LOG_LEVEL=INFO
API_GATEWAY_URL=https://api.ava-olo.com
```

## 🚀 Setup Instructions

### For New Deployments

1. **Copy the template**:
   ```bash
   cp .env.example .env
   ```

2. **Fill in your values**:
   ```bash
   nano .env
   # or
   vim .env
   ```

3. **Verify configuration**:
   ```bash
   # Check if all required values are set
   grep -E "your-|here" .env
   # Should return nothing if properly configured
   ```

### For Docker Deployments

Docker Compose automatically reads from `.env` in the root:

```yaml
version: '3.8'
services:
  api-gateway:
    env_file:
      - ./.env  # References root .env
```

### For Local Development

Services can access the root .env file using relative paths:

```python
# In any service directory
from dotenv import load_dotenv
import os

# Load from root .env
load_dotenv(os.path.join(os.path.dirname(__file__), '../../.env'))
```

## 📊 Configuration Categories

### 1. Database Configuration
- `DB_HOST`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_PORT`
- `DATABASE_URL` (constructed from above)

### 2. LLM & AI Configuration
- `OPENAI_API_KEY`, `OPENAI_MODEL`, `OPENAI_TEMPERATURE`
- `PERPLEXITY_API_KEY`

### 3. RAG/Vector Database
- `PINECONE_API_KEY`, `PINECONE_ENV`, `PINECONE_HOST`
- `PINECONE_INDEX_NAME`, `RUN_RAG`

### 4. AWS Infrastructure
- `AWS_REGION`, `AWS_RDS_ENDPOINT`

### 5. Application Settings
- `APP_ENV`, `LOG_LEVEL`, `MAX_QUERY_RETRIES`
- `QUERY_TIMEOUT`, `API_GATEWAY_URL`

### 6. Monitoring
- `ENABLE_METRICS`, `METRICS_PORT`, `HEALTH_CHECK_INTERVAL`

### 7. Localization
- `DEFAULT_LANGUAGE`, `SUPPORTED_LANGUAGES`, `TIMEZONE_DEFAULT`

### 8. Security
- `SESSION_SECRET`, `RATE_LIMIT_PER_HOUR`, `ENABLE_CORS`

### 9. Service Ports
- `API_GATEWAY_PORT`, `MONITORING_DASHBOARD_PORT`
- `AGRONOMIC_DASHBOARD_PORT`, `BUSINESS_DASHBOARD_PORT`

### 10. Feature Flags
- `ENABLE_LLM_FIRST`, `ENABLE_COUNTRY_LOCALIZATION`
- `ENABLE_PRIVACY_MODE`, `ENABLE_CONSTITUTIONAL_CHECKS`

## 🧪 Testing Configuration

### Verify Database Connection
```bash
# Test PostgreSQL connection
psql $DATABASE_URL -c "SELECT 1"
```

### Verify API Keys
```python
# Test OpenAI connection
import openai
openai.api_key = os.getenv('OPENAI_API_KEY')
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Hello"}],
    max_tokens=5
)
```

## 🚨 Common Issues & Solutions

### Issue: Service can't find configuration
**Solution**: Ensure service is loading from root .env:
```python
# Correct path to root .env
dotenv_path = os.path.join(os.path.dirname(__file__), '../../.env')
load_dotenv(dotenv_path)
```

### Issue: Configuration conflicts
**Solution**: Remove any subdirectory .env files:
```bash
# Find rogue .env files
find . -name ".env" -not -path "./.env"

# Remove if found
rm ./service-name/.env
```

### Issue: Missing environment variables
**Solution**: Check against .env.example:
```bash
# Compare current .env with template
diff .env .env.example | grep "^>"
```

## 🏛️ Constitutional Compliance

This centralized configuration approach ensures:

1. ✅ **Single Source of Truth**: One .env file for all services
2. ✅ **No Configuration Drift**: Prevents inconsistent settings
3. ✅ **Security**: Sensitive data in one secured location
4. ✅ **Simplicity**: Easy to manage and deploy
5. ✅ **MANGO RULE**: Works globally without geographic hardcoding

## 📝 Migration from Multiple .env Files

If upgrading from the old multi-.env structure:

1. **Backup existing configurations**:
   ```bash
   mkdir env-backup
   find . -name ".env" -exec cp {} env-backup/ \;
   ```

2. **Consolidate into root .env**:
   - Use the most recent/complete configuration
   - The root .env (2,182 bytes) contains production values
   - Subdirectory .env files (561 bytes) were templates

3. **Remove subdirectory .env files**:
   ```bash
   find . -name ".env" -not -path "./.env" -type f -exec rm {} \;
   ```

4. **Update service code** to reference root .env

## 🥭 MANGO RULE Compliance

This configuration system ensures:
- No hardcoded geographic restrictions
- All languages supported via `SUPPORTED_LANGUAGES`
- No crop-specific configuration
- Works for Bulgarian mango farmers and everyone else!

---

**Remember**: The root `.env` file is the ONLY configuration file. All services must reference it. 🏛️