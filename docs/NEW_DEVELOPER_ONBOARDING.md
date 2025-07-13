# 🚀 New Developer Onboarding Guide

Welcome to AVA OLO! This guide will help you understand our constitutional principles and get you productive quickly. AVA OLO is an agricultural CRM that serves farmers globally with 100% AI-driven intelligence.

## 📋 Table of Contents
1. [Constitutional Orientation](#constitutional-orientation)
2. [System Setup](#system-setup)
3. [Development Environment](#development-environment)
4. [First Tasks](#first-tasks)
5. [Getting Help](#getting-help)

## 🏛️ Constitutional Orientation

### The Sacred Constitution
Before writing any code, you MUST understand these principles:

#### 🥭 The MANGO RULE (Most Important!)
**"Would this work for a Bulgarian mango farmer?"**

This is our universal test. Every feature must work for:
- Any crop (mangoes in Bulgaria? Yes!)
- Any country (Bulgaria to Brazil)
- Any language (50+ supported)
- Any farmer size (subsistence to industrial)

**Example Violations:**
```python
# ❌ WRONG - Hardcoded for tomatoes
if crop_type == "tomato":
    return "Apply fertilizer in spring"

# ✅ RIGHT - Works for any crop
response = await llm.generate(f"When to fertilize {crop_type} in {location}")
```

#### 🧠 LLM-FIRST Principle
**"AI intelligence over hardcoded logic"**

```python
# ❌ WRONG - Hardcoded SQL
def get_farmer_fields(farmer_id):
    return db.execute("SELECT * FROM fields WHERE farmer_id = ?", farmer_id)

# ✅ RIGHT - LLM generates query
def get_farmer_fields(farmer_id, query):
    sql = await llm.generate_sql(query, farmer_id)
    return db.execute(sql)
```

#### 🔒 PRIVACY-FIRST Principle
**"Farmer data never leaves our servers"**

```python
# ❌ WRONG - Sending farmer data to external API
openai.complete(f"Farmer {farmer_name} has {field_size} hectares")

# ✅ RIGHT - Only patterns, no personal data
openai.complete(f"A farmer has {field_size} hectares, what crops to suggest?")
```

### Amendment #13: Smart Localization

Our newest constitutional amendment supports minority farmers:

**Real Example:** Hungarian farmer in Croatia
- Phone: +385 (Croatian)
- Language: Hungarian
- System: Automatically detects Croatia, allows Hungarian override

```python
# System handles this automatically
farmer = {
    "phone": "+385123456789",     # Croatian number
    "language": "hu",              # Hungarian preference
    "country": "HR"                # Lives in Croatia
}
```

### Constitutional Compliance Checklist

Before ANY commit, verify:
- [ ] 🥭 Passes MANGO RULE (works for Bulgarian mango farmer)
- [ ] 🧠 Uses LLM-FIRST approach (no hardcoded patterns)
- [ ] 🔒 Maintains PRIVACY-FIRST (no personal data in external calls)
- [ ] 🌍 Supports all languages/countries
- [ ] 📱 Works on AWS App Runner
- [ ] 🧩 Maintains module independence

## 💻 System Setup

### 1. Repository Access

**Main Repositories:**
```bash
# Documentation and Constitutional documents
git clone https://github.com/Poljopodrska/ava-olo-shared.git

# Monitoring dashboards service
git clone https://github.com/Poljopodrska/ava-olo-monitoring-dashboards.git

# Agricultural core service  
git clone https://github.com/Poljopodrska/ava-olo-agricultural-core.git
```

### 2. AWS Access Requirements

You'll need access to:
- AWS Console (for App Runner services)
- CloudWatch Logs (for debugging)
- RDS Aurora (read-only for development)

Contact your team lead for:
- AWS IAM credentials
- Service URLs
- Emergency contacts

### 3. Environment Variables

Create `.env` file in each service:
```bash
# Database Configuration
DB_HOST=farmer-crm-production.cifgmm0mqg5q.us-east-1.rds.amazonaws.com
DB_PORT=5432
DB_NAME=farmer_crm
DB_USER=farmer_admin
DB_PASSWORD=<get-from-team-lead>

# OpenAI Configuration
OPENAI_API_KEY=<get-from-team-lead>
OPENAI_MODEL=gpt-4

# Constitutional Settings
ENABLE_LLM_FIRST=true
ENABLE_COUNTRY_LOCALIZATION=true
ENABLE_CONSTITUTIONAL_CHECKS=true
```

### 4. Database Connection Test

Test your setup:
```python
# test_connection.py
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

try:
    conn = psycopg2.connect(
        host=os.getenv('DB_HOST'),
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD')
    )
    print("✅ Database connected!")
    conn.close()
except Exception as e:
    print(f"❌ Connection failed: {e}")
```

## 🛠️ Development Environment

### Required Tools

1. **Python 3.11+**
   ```bash
   python --version  # Should show 3.11.x
   ```

2. **Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # or
   venv\Scripts\activate  # Windows
   ```

3. **Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **VS Code Extensions (Recommended)**
   - Python
   - Pylance
   - GitLens
   - AWS Toolkit

### Local Development Setup

1. **Run Monitoring Dashboards:**
   ```bash
   cd ava-olo-monitoring-dashboards
   python main.py
   # Visit http://localhost:8080
   ```

2. **Run Agricultural Core:**
   ```bash
   cd ava-olo-agricultural-core
   python app.py
   # API at http://localhost:8080
   ```

### Constitutional Development Mode

Enable strict constitutional checking:
```python
# In your development environment
os.environ['STRICT_CONSTITUTIONAL_MODE'] = 'true'
```

This will:
- Log all potential violations
- Reject hardcoded patterns
- Verify MANGO RULE compliance

### Testing Procedures

1. **Unit Tests:**
   ```bash
   pytest tests/ -v
   ```

2. **Constitutional Tests:**
   ```bash
   python test_constitutional_compliance.py
   ```

3. **Mango Rule Test:**
   ```bash
   curl -X POST http://localhost:8080/api/v1/test/mango-rule
   ```

## 👨‍💻 First Tasks

### Task 1: Understanding the Codebase

1. **Read Constitutional Documents:**
   - `constitutional/AVA_OLO_CONSTITUTION.md`
   - `constitutional/CONSTITUTIONAL_AMENDMENT_13.md`

2. **Explore the Architecture:**
   - `architecture/CURRENT_SYSTEM_ARCHITECTURE.md`
   - `architecture/API_ENDPOINTS_REFERENCE.md`

3. **Run the Test Suite:**
   ```bash
   # In agricultural-core
   python test_constitutional_compliance.py
   ```

### Task 2: Make Your First Change

**Beginner Task:** Add a new test for Romanian farmers

1. **Create test file:**
   ```python
   # test_romanian_farmer.py
   async def test_romanian_farmer():
       query = {
           "query": "Câte hectare de porumb am?",  # How many hectares of corn?
           "farmer_id": 999,
           "language": "ro",
           "country_code": "RO"
       }
       
       result = await process_query(query)
       assert result.success
       assert result.constitutional_compliance
       assert "hectare" in result.response
   ```

2. **Test locally:**
   ```bash
   python test_romanian_farmer.py
   ```

3. **Commit with constitutional message:**
   ```bash
   git add test_romanian_farmer.py
   git commit -m "Add Romanian farmer test - Constitutional compliance for RO/ro locale"
   ```

### Task 3: Deploy Your Change

1. **Push to GitHub:**
   ```bash
   git push origin main
   ```

2. **Monitor Deployment:**
   - Watch AWS App Runner console
   - Check CloudWatch logs
   - Verify health endpoint

3. **Test in Production:**
   ```bash
   curl https://[your-service].awsapprunner.com/health
   ```

### Common First PRs

1. **Add a new language test**
2. **Improve error messages**
3. **Add constitutional compliance logging**
4. **Enhance minority farmer support**
5. **Add new crop-specific knowledge**

## 🆘 Getting Help

### Resources

1. **Documentation:**
   - This repository (`ava-olo-shared`)
   - Architecture docs
   - API references

2. **Team Communication:**
   - Slack: #ava-olo-dev
   - Emergency: Check `EMERGENCY_DEVELOPER_RECOVERY.md`

3. **Constitutional Questions:**
   - Always check: "Does it pass the MANGO RULE?"
   - When in doubt, use LLM-FIRST approach
   - Ask team lead for constitutional interpretation

### Debugging Tips

1. **Constitutional Violations:**
   ```python
   # Add logging to trace violations
   import logging
   logging.basicConfig(level=logging.DEBUG)
   logger = logging.getLogger('constitutional')
   ```

2. **Database Issues:**
   ```python
   # Test connection
   from database_operations import test_connection
   test_connection()
   ```

3. **LLM Problems:**
   ```python
   # Check OpenAI API
   from llm_engine import test_llm
   test_llm()
   ```

### Common Issues

1. **"Import Error: config_manager"**
   - Solution: Check PYTHONPATH includes ava-olo-shared

2. **"Database connection failed"**
   - Solution: Verify .env file and VPN connection

3. **"Constitutional violation detected"**
   - Solution: Review the MANGO RULE, remove hardcoded logic

4. **"Deployment failed"**
   - Solution: Check port is 8080, not 8000

### Code Review Checklist

Before requesting review:
- [ ] Passes all tests
- [ ] Follows MANGO RULE
- [ ] No hardcoded patterns
- [ ] Includes tests
- [ ] Updates documentation
- [ ] Constitutional commit message

## 🎯 Next Steps

1. **Week 1:** Understand constitution, run local environment
2. **Week 2:** Make first contribution, deploy to AWS
3. **Week 3:** Take on a minority farmer support task
4. **Month 1:** Lead a small feature implementation

### Advanced Topics

Once comfortable, explore:
- `docs/TROUBLESHOOTING_GUIDE.md`
- `examples/CONSTITUTIONAL_CODE_EXAMPLES.md`
- `architecture/AWS_DEPLOYMENT_ARCHITECTURE.md`

## 🌟 Welcome to AVA OLO!

Remember: Every line of code you write helps farmers worldwide, from Bulgarian mango growers to Hungarian minorities in Croatia. Your code matters!

**The MANGO RULE is your guide. When in doubt, think of that Bulgarian mango farmer!** 🥭

---

*"Code constitutionally, deploy confidently, serve farmers globally!"*