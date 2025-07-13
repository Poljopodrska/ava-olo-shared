# ⚡ Quick Start Guide

Get AVA OLO running in 5 minutes! This guide is for experienced developers who want to start contributing immediately.

## 🏃 5-Minute Setup

### 1. Clone Essential Repos
```bash
# Clone all three repos
git clone https://github.com/Poljopodrska/ava-olo-monitoring-dashboards.git
git clone https://github.com/Poljopodrska/ava-olo-agricultural-core.git
git clone https://github.com/Poljopodrska/ava-olo-shared.git
```

### 2. Environment Setup
```bash
# Create .env in both service directories
cat > .env << EOF
DB_HOST=farmer-crm-production.cifgmm0mqg5q.us-east-1.rds.amazonaws.com
DB_PORT=5432
DB_NAME=farmer_crm
DB_USER=farmer_admin
DB_PASSWORD=<get-from-team>
OPENAI_API_KEY=<get-from-team>
ENABLE_LLM_FIRST=true
ENABLE_COUNTRY_LOCALIZATION=true
EOF
```

### 3. Quick Install
```bash
# For each service directory
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### 4. Database Test
```bash
python -c "
from database_operations import ConstitutionalDatabaseOperations
db = ConstitutionalDatabaseOperations()
print('✅ Connected!' if db.health_check() else '❌ Failed!')
"
```

### 5. Constitutional Check
```bash
# Test the MANGO RULE
curl -X POST http://localhost:8080/api/v1/test/mango-rule
```

## 🏛️ Key Constitutional Rules

### 🥭 MANGO RULE (Never Forget!)
**Every feature must work for a Bulgarian mango farmer**

```python
# ❌ BAD - Hardcoded
if country == "USA":
    return "Plant in spring"

# ✅ GOOD - Universal
return llm.advise_planting(crop, location)
```

### 🧠 LLM-FIRST
**AI makes decisions, not hardcoded logic**

```python
# ❌ BAD - Hardcoded SQL
sql = "SELECT * FROM farmers WHERE country = 'Croatia'"

# ✅ GOOD - LLM-generated
sql = llm.generate_sql(natural_language_query)
```

### 🔒 PRIVACY-FIRST  
**No personal data to external APIs**

```python
# ❌ BAD - Leaks farmer data
openai.complete(f"Farmer John has 5 hectares")

# ✅ GOOD - Anonymous patterns
openai.complete(f"A farmer has 5 hectares")
```

### 🚀 AWS Requirements
- **Port:** Must be 8080 (not 8000!)
- **Health endpoint:** Required at `/health`
- **No localhost:** Use `0.0.0.0`

## 💻 Common Development Tasks

### Adding Dashboard Features

1. **Locate the dashboard file:**
   ```bash
   cd ava-olo-monitoring-dashboards
   # Edit business_dashboard.py or agronomic_dashboard.py
   ```

2. **Add constitutional feature:**
   ```python
   @app.route('/api/new-metric')
   async def new_metric(farmer_id: int):
       # Use LLM for processing
       result = await db_ops.process_natural_query(
           f"Calculate new metric for farmer {farmer_id}",
           farmer_id=farmer_id
       )
       return {"success": True, "data": result}
   ```

3. **Test locally:**
   ```bash
   python main.py
   # Visit http://localhost:8080
   ```

### Modifying Database Queries

1. **Never hardcode SQL:**
   ```python
   # In llm_first_database_engine.py
   async def process_query(self, natural_query: str):
       # LLM generates SQL
       sql = await self.llm.generate_sql(
           query=natural_query,
           schema=self.get_schema()
       )
       return self.execute_safely(sql)
   ```

2. **Add safety checks:**
   ```python
   def execute_safely(self, sql: str):
       # Constitutional safety
       if not sql.upper().startswith('SELECT'):
           raise ConstitutionalViolation("Only SELECT allowed")
       return self.db.execute(sql)
   ```

### Implementing New Localization

1. **Add to smart detector:**
   ```python
   # In smart_country_detector.py
   'MK': {  # North Macedonia
       'country_name': 'North Macedonia',
       'primary_language': 'mk',
       'secondary_languages': ['sq', 'en'],
       'phone_prefixes': ['+389'],
       'minorities': ['albanian', 'turkish']
   }
   ```

2. **Test minority support:**
   ```python
   # Albanian minority in Macedonia
   result = detector.detect_with_override(
       phone_number="+389123456",
       language_override="sq",
       ethnicity="Albanian"
   )
   ```

### Testing and Deployment

1. **Run constitutional tests:**
   ```bash
   python test_constitutional_compliance.py
   ```

2. **Commit properly:**
   ```bash
   git add -A
   git commit -m "Add Macedonian support - Constitutional Amendment #13 compliance"
   git push origin main
   ```

3. **Monitor deployment:**
   - AWS App Runner auto-deploys in 3-4 minutes
   - Check: https://[your-service].awsapprunner.com/health

## 🔧 Quick Commands

### Development
```bash
# Start monitoring dashboards
cd ava-olo-monitoring-dashboards && python main.py

# Start agricultural core
cd ava-olo-agricultural-core && python app.py

# Run all tests
pytest tests/ -v

# Check constitutional compliance
python test_constitutional_compliance.py
```

### Debugging
```bash
# Check logs
tail -f app.log

# Test database connection
python -c "from database_operations import test_connection; test_connection()"

# Test LLM
python -c "from llm_engine import test_llm; test_llm()"
```

### AWS Commands
```bash
# View logs (requires AWS CLI)
aws logs tail /aws/apprunner/ava-olo-agricultural-core/application

# Check service status
aws apprunner list-services

# Force redeployment
aws apprunner start-deployment --service-arn <service-arn>
```

## 📋 Task Templates

### New API Endpoint
```python
@app.post("/api/v1/farmer/new-endpoint")
async def new_endpoint(request: FarmerRequest):
    """Constitutional endpoint following MANGO RULE"""
    try:
        # LLM-first processing
        result = await llm_engine.process(
            request.query,
            farmer_id=request.farmer_id,
            language=request.language
        )
        
        # Privacy-first response
        return {
            "success": True,
            "response": result,
            "constitutional_compliance": True
        }
    except Exception as e:
        logger.error(f"Constitutional error: {e}")
        raise HTTPException(status_code=500)
```

### New Language Support
```python
# 1. Add to country mapping
'XX': {
    'country_name': 'New Country',
    'primary_language': 'xx',
    'phone_prefixes': ['+XXX']
}

# 2. Add translation test
async def test_new_language():
    result = await process_query({
        "query": "Query in new language",
        "language": "xx"
    })
    assert result.constitutional_compliance
```

## 🚨 Emergency Procedures

### Service Down
1. Check AWS App Runner console
2. View CloudWatch logs
3. Check recent deployments
4. Rollback if needed

### Database Issues
1. Verify connection string
2. Check AWS RDS status
3. Test with read-only user
4. Contact DBA team

### Constitutional Violation
1. Revert the commit
2. Fix the violation
3. Add test to prevent recurrence
4. Document in TROUBLESHOOTING_GUIDE.md

## 📚 Essential Reading

- **MUST READ:** `constitutional/AVA_OLO_CONSTITUTION.md`
- **Architecture:** `architecture/CURRENT_SYSTEM_ARCHITECTURE.md`
- **APIs:** `architecture/API_ENDPOINTS_REFERENCE.md`
- **Troubleshooting:** `docs/TROUBLESHOOTING_GUIDE.md`

## 🎯 Quick Wins

1. **Add a missing language test**
2. **Improve error messages**  
3. **Add logging for debugging**
4. **Update documentation**
5. **Add constitutional compliance checks**

---

**Remember: The MANGO RULE is supreme. Every Bulgarian mango farmer depends on your code!** 🥭