# 🔧 Troubleshooting Guide

This guide helps resolve common issues in AVA OLO development. Remember: Most problems stem from constitutional violations!

## 📋 Table of Contents
1. [Constitutional Violations](#constitutional-violations)
2. [AWS Deployment Issues](#aws-deployment-issues)
3. [Development Issues](#development-issues)
4. [Database Problems](#database-problems)
5. [LLM Integration Issues](#llm-integration-issues)
6. [Quick Fixes](#quick-fixes)

## 🏛️ Constitutional Violations

### Hardcoded Pattern Detected

**Error:**
```
ConstitutionalViolation: Hardcoded pattern detected in function get_crop_advice
```

**Symptoms:**
- Code contains hardcoded logic for specific crops/countries
- Fails MANGO RULE test
- Constitutional compliance check returns False

**Solutions:**

1. **Identify the violation:**
   ```python
   # ❌ VIOLATION - Hardcoded logic
   def get_crop_advice(crop):
       if crop == "tomato":
           return "Plant in spring"
       elif crop == "corn":
           return "Plant in summer"
   ```

2. **Fix with LLM-first approach:**
   ```python
   # ✅ CONSTITUTIONAL
   async def get_crop_advice(crop, location, context):
       prompt = f"Provide planting advice for {crop} in {location}"
       return await llm.generate(prompt, context)
   ```

3. **Add test to prevent recurrence:**
   ```python
   async def test_mango_rule_crop_advice():
       # Test with Bulgarian mango
       advice = await get_crop_advice("mango", "Bulgaria", {})
       assert advice is not None
       assert "constitutional_violation" not in advice
   ```

### Privacy Violation - Personal Data in External API

**Error:**
```
PrivacyViolation: Farmer personal data detected in external API call
```

**Symptoms:**
- Farmer names, IDs, or personal info sent to OpenAI
- Privacy audit fails
- GDPR compliance at risk

**Solutions:**

1. **Identify the leak:**
   ```python
   # ❌ VIOLATION - Personal data exposed
   prompt = f"Farmer {farmer_name} with ID {farmer_id} has {field_size} hectares"
   ```

2. **Anonymize before external calls:**
   ```python
   # ✅ CONSTITUTIONAL
   prompt = f"A farmer has {field_size} hectares of {crop_type}"
   # Process with farmer context internally after receiving response
   ```

3. **Add privacy wrapper:**
   ```python
   def privacy_safe_prompt(template, **kwargs):
       # Remove any PII
       safe_kwargs = {k: v for k, v in kwargs.items() 
                      if k not in ['farmer_id', 'farmer_name', 'phone']}
       return template.format(**safe_kwargs)
   ```

### Module Dependency Violation

**Error:**
```
ModuleDependencyViolation: Direct import between services detected
```

**Symptoms:**
- One service directly imports from another
- Circular dependencies
- Service fails to start independently

**Solutions:**

1. **Remove direct imports:**
   ```python
   # ❌ VIOLATION
   from ava_olo_monitoring_dashboards.business_logic import calculate_revenue
   
   # ✅ CONSTITUTIONAL - Use API calls
   async def get_revenue(farmer_id):
       response = await http_client.get(
           f"{DASHBOARD_SERVICE_URL}/api/revenue/{farmer_id}"
       )
       return response.json()
   ```

2. **Use shared libraries correctly:**
   ```python
   # ✅ OK - Shared utilities
   from ava_olo_shared.config_manager import config
   
   # ✅ OK - Common interfaces  
   from ava_olo_shared.smart_country_detector import detect_country
   ```

## 🚀 AWS Deployment Issues

### App Runner Build Failure

**Error:**
```
AWS App Runner build failed: pip install error
```

**Symptoms:**
- Deployment fails during build phase
- "Module not found" errors
- Requirements installation fails

**Solutions:**

1. **Check requirements.txt:**
   ```bash
   # Verify all dependencies are listed
   pip freeze > requirements_check.txt
   diff requirements.txt requirements_check.txt
   ```

2. **Fix version conflicts:**
   ```txt
   # requirements.txt - Pin specific versions
   fastapi==0.104.1
   uvicorn==0.24.0
   psycopg2-binary==2.9.9  # Use binary for AWS
   openai==1.12.0
   ```

3. **Check Python version:**
   ```python
   # Ensure compatibility with AWS App Runner Python 3.11
   import sys
   assert sys.version_info >= (3, 11), "Python 3.11+ required"
   ```

### Runtime Failure - Wrong Port

**Error:**
```
Application failed to start: Connection refused on port 8080
```

**Symptoms:**
- Build succeeds but runtime fails
- Health checks fail
- "Connection refused" in logs

**Solutions:**

1. **Fix port configuration:**
   ```python
   # ❌ WRONG - Common mistake
   uvicorn.run(app, host="0.0.0.0", port=8000)  # Wrong port!
   
   # ✅ CORRECT - AWS App Runner requires 8080
   uvicorn.run(app, host="0.0.0.0", port=8080)
   ```

2. **Check all entry points:**
   ```bash
   # Find all port references
   grep -r "port.*8000" .
   grep -r "localhost" .  # Should be 0.0.0.0
   ```

3. **Update startup command:**
   ```python
   # app.py or main.py
   if __name__ == "__main__":
       port = int(os.getenv("PORT", 8080))  # AWS sets PORT env var
       uvicorn.run(app, host="0.0.0.0", port=port)
   ```

### Environment Variable Missing

**Error:**
```
KeyError: 'OPENAI_API_KEY'
```

**Symptoms:**
- Service starts but functionality broken
- Database connection fails
- API calls fail

**Solutions:**

1. **Add error handling:**
   ```python
   # Graceful degradation
   OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
   if not OPENAI_API_KEY:
       logger.warning("OpenAI API key not found - LLM features disabled")
       LLM_ENABLED = False
   ```

2. **Copy from working service:**
   ```bash
   # In AWS Console
   1. Go to working service (monitoring-dashboards)
   2. Copy all environment variables
   3. Paste to new service (agricultural-core)
   ```

3. **Verify in code:**
   ```python
   # config_check.py
   required_vars = [
       'DB_HOST', 'DB_NAME', 'DB_USER', 'DB_PASSWORD',
       'OPENAI_API_KEY'
   ]
   missing = [var for var in required_vars if not os.getenv(var)]
   if missing:
       print(f"❌ Missing: {missing}")
   ```

## 💻 Development Issues

### Import Error - Module Not Found

**Error:**
```
ImportError: No module named 'smart_country_detector'
```

**Symptoms:**
- Local development works, AWS fails
- Tests pass locally but fail in CI
- Inconsistent import errors

**Solutions:**

1. **Fix Python path:**
   ```python
   # Add to top of main files
   import sys
   import os
   sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
   ```

2. **Use proper imports:**
   ```python
   # ❌ WRONG - Relative import issues
   from smart_country_detector import detect
   
   # ✅ CORRECT - Explicit path
   from ava_olo_shared.smart_country_detector import detect
   
   # ✅ ALSO CORRECT - Try multiple paths
   try:
       from ava_olo_shared.smart_country_detector import detect
   except ImportError:
       from smart_country_detector import detect
   ```

3. **Structure imports properly:**
   ```python
   # __init__.py files in each directory
   # ava_olo_shared/__init__.py
   from .smart_country_detector import SmartCountryDetector
   from .config_manager import config
   ```

### Local vs AWS Environment Differences

**Symptoms:**
- Works locally, fails on AWS
- Different behavior in production
- Timezone issues

**Solutions:**

1. **Environment parity:**
   ```python
   # Use same Python version
   # .python-version
   3.11.7
   
   # Dockerfile (if using)
   FROM python:3.11.7-slim
   ```

2. **Handle timezone differences:**
   ```python
   # Always use UTC
   from datetime import datetime, timezone
   now = datetime.now(timezone.utc)
   ```

3. **Path handling:**
   ```python
   # Use pathlib for cross-platform paths
   from pathlib import Path
   
   # ❌ WRONG
   config_file = "config/settings.json"
   
   # ✅ CORRECT  
   config_file = Path(__file__).parent / "config" / "settings.json"
   ```

## 🗄️ Database Problems

### Connection Pool Exhausted

**Error:**
```
psycopg2.OperationalError: FATAL: remaining connection slots are reserved
```

**Symptoms:**
- Database connections max out
- Queries hang
- Service becomes unresponsive

**Solutions:**

1. **Implement connection pooling:**
   ```python
   from psycopg2 import pool
   
   # Create pool
   connection_pool = pool.ThreadedConnectionPool(
       minconn=1,
       maxconn=20,
       host=config.db_host,
       database=config.db_name,
       user=config.db_user,
       password=config.db_password
   )
   
   # Use connections properly
   def execute_query(query):
       conn = connection_pool.getconn()
       try:
           with conn.cursor() as cur:
               cur.execute(query)
               return cur.fetchall()
       finally:
           connection_pool.putconn(conn)
   ```

2. **Add connection limits:**
   ```python
   # In database class
   MAX_CONNECTIONS = 10
   active_connections = 0
   
   async def get_connection():
       global active_connections
       if active_connections >= MAX_CONNECTIONS:
           raise Exception("Connection limit reached")
       active_connections += 1
   ```

### Schema Mismatch

**Error:**
```
column "country_code" does not exist
```

**Symptoms:**
- Queries fail with column errors
- New features don't work
- Migration not applied

**Solutions:**

1. **Check schema version:**
   ```sql
   -- Run in Aurora
   SELECT * FROM schema_migrations ORDER BY version DESC LIMIT 5;
   ```

2. **Apply missing migrations:**
   ```sql
   -- Run amendment #13 schema
   \i aurora_schema_update_smart_localization.sql
   ```

3. **Verify schema:**
   ```python
   def verify_schema():
       required_columns = {
           'farmers': ['country_code', 'whatsapp_number', 'preferred_language'],
           'country_language_mapping': ['country_code', 'primary_language']
       }
       
       for table, columns in required_columns.items():
           for column in columns:
               query = f"""
                   SELECT column_name 
                   FROM information_schema.columns 
                   WHERE table_name = '{table}' 
                   AND column_name = '{column}'
               """
               if not db.execute(query):
                   print(f"❌ Missing: {table}.{column}")
   ```

## 🤖 LLM Integration Issues

### OpenAI API Rate Limit

**Error:**
```
openai.error.RateLimitError: Rate limit reached
```

**Symptoms:**
- Queries fail intermittently
- 429 errors
- Degraded performance

**Solutions:**

1. **Implement retry logic:**
   ```python
   import time
   from tenacity import retry, wait_exponential, stop_after_attempt
   
   @retry(
       wait=wait_exponential(min=1, max=60),
       stop=stop_after_attempt(5)
   )
   async def call_openai(prompt):
       try:
           return await openai.complete(prompt)
       except RateLimitError:
           logger.warning("Rate limit hit, retrying...")
           raise
   ```

2. **Add caching:**
   ```python
   from functools import lru_cache
   import hashlib
   
   @lru_cache(maxsize=1000)
   def cached_llm_query(query_hash):
       return llm.complete(query_hash)
   
   def get_llm_response(query):
       # Cache similar queries
       query_hash = hashlib.md5(query.encode()).hexdigest()
       return cached_llm_query(query_hash)
   ```

3. **Implement rate limiting:**
   ```python
   from asyncio import Semaphore
   
   # Limit concurrent LLM calls
   llm_semaphore = Semaphore(5)
   
   async def rate_limited_llm(prompt):
       async with llm_semaphore:
           return await llm.complete(prompt)
   ```

### LLM Response Timeout

**Error:**
```
TimeoutError: OpenAI API call exceeded 30 seconds
```

**Solutions:**

1. **Increase timeout:**
   ```python
   client = OpenAI(
       api_key=config.openai_api_key,
       timeout=60.0  # Increase from default
   )
   ```

2. **Simplify prompts:**
   ```python
   # Break complex queries into smaller parts
   async def process_complex_query(query):
       # Step 1: Generate SQL
       sql = await llm.generate_sql(query, timeout=20)
       
       # Step 2: Process results
       response = await llm.format_response(results, timeout=20)
       
       return response
   ```

## ⚡ Quick Fixes

### Reset Local Environment
```bash
# Clean reinstall
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Clear Python Cache
```bash
find . -type d -name __pycache__ -exec rm -r {} +
find . -type f -name '*.pyc' -delete
```

### Test Database Connection
```python
# quick_test.py
from database_operations import ConstitutionalDatabaseOperations
try:
    db = ConstitutionalDatabaseOperations()
    print("✅ Database connected!")
    print(f"Test query: {db.health_check()}")
except Exception as e:
    print(f"❌ Failed: {e}")
```

### Force AWS Redeployment
```bash
# Make a small change
echo "# Force redeploy $(date)" >> README.md
git add README.md
git commit -m "Force AWS App Runner redeployment"
git push origin main
```

### Emergency Rollback
```bash
# Revert last commit
git revert HEAD
git push origin main

# Or revert to specific commit
git reset --hard <commit-hash>
git push --force origin main
```

## 📞 When to Escalate

Escalate to team lead if:
1. **Constitutional interpretation unclear**
2. **Production data at risk**
3. **Multiple services down**
4. **Security concern identified**
5. **Cannot resolve within 2 hours**

## 📚 Additional Resources

- **Emergency Procedures:** `EMERGENCY_DEVELOPER_RECOVERY.md`
- **Architecture Details:** `architecture/CURRENT_SYSTEM_ARCHITECTURE.md`
- **Constitutional Law:** `constitutional/AVA_OLO_CONSTITUTION.md`

---

**Remember: 99% of issues are constitutional violations. When in doubt, check the MANGO RULE!** 🥭