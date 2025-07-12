# 🆘 EMERGENCY DEVELOPER RECOVERY GUIDE

## 📜 CRITICAL: READ THIS FIRST
If the original developer is unavailable, this guide provides everything needed to maintain and continue AVA OLO development.

## 🎯 SYSTEM OVERVIEW

**AVA OLO is a global agricultural CRM system following 12 constitutional principles.**

### Core Principle: 🥭 MANGO RULE
Everything must work for ANY crop in ANY country. Test: "Would this work for a Bulgarian mango farmer?"

### Architecture: LLM-FIRST
AI handles complexity, not hardcoded rules. NO pattern matching, trust GPT-4 intelligence.

## 🌐 CURRENT AWS INFRASTRUCTURE

### **Production Services:**
AWS App Runner Services:

Monitoring Hub: https://6pmgiripe.us-east-1.awsapprunner.com
Agricultural Core: https://3ksdvgdtud.us-east-1.awsapprunner.com

AWS RDS Database:

Instance: farmer-crm-production
Engine: PostgreSQL
Region: us-east-1
Database Name: farmer_crm


### **Dashboard Endpoints:**

Health Dashboard: https://6pmgiripe.us-east-1.awsapprunner.com/health/
Agronomic Dashboard: https://6pmgiripe.us-east-1.awsapprunner.com/agronomic/
Business Dashboard: https://6pmgiripe.us-east-1.awsapprunner.com/business/
Database Dashboard: https://6pmgiripe.us-east-1.awsapprunner.com/database/


## 🔑 CRITICAL ACCESS INFORMATION

### **GitHub Repositories:**
Organization: Poljopodrska
Key Repositories:

ava-olo-monitoring-dashboards (main dashboards)
ava-olo-agricultural-core (core farming system)
ava-olo-shared (constitutional documents)

Access Required: Admin access to Poljopodrska organization

### **AWS Environment Variables (configured in App Runner):**
Database Connection:

DB_HOST: farmer-crm-production.xxxxx.us-east-1.rds.amazonaws.com
DB_NAME: farmer_crm
DB_USER: postgres
DB_PASSWORD: [configured in AWS]
DB_PORT: 5432

API Keys:

OPENAI_API_KEY: sk-xxxxx (for LLM-first processing)
PERPLEXITY_API_KEY: pplx-xxxxx (for external knowledge)
PINECONE_API_KEY: pcsk-xxxxx (for RAG/vector search)

Pinecone Configuration:

PINECONE_ENV: eu-west-1
PINECONE_HOST: https://pinecone-host
PINECONE_INDEX_NAME: pinecone-crm-index


## 🗄️ DATABASE INFORMATION

### **Critical Database Details:**
Current Data:

Active farmers (including KMETIJA VRZEL - Blaž Vrzel as reference)
System database tables
Conversation messages preserved
Agricultural fields with crop plantings

Key Tables:

farmers (farmer information)
fields (agricultural fields)
field_crops (crop plantings)
tasks (farming tasks)
incoming_messages (farmer communications)


### **Database Recovery:**
```sql
-- Verify system health
SELECT COUNT(*) FROM farmers; -- Should return active farmers
SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public'; -- Should return system tables

-- Key farmer verification
SELECT name, email FROM farmers WHERE name LIKE '%Vrzel%'; -- Reference farmer for testing
```

## 🚀 DEPLOYMENT PROCEDURES

### **Code Deployment:**
```bash
# All services auto-deploy from GitHub main branch
# When you push to main branch, AWS App Runner automatically deploys

# Manual deployment trigger (if needed):
# Go to AWS App Runner console
# Select service
# Click "Deploy latest commit"
```

### **Constitutional Compliance:**
BEFORE ANY CHANGES:
1. Read AVA_OLO_CONSTITUTION.md completely
2. Test mango compliance: "Would this work for Bulgarian mango farmer?"
3. Ensure LLM-first approach (no hardcoded patterns)
4. Verify privacy-first (no personal data to external APIs)
5. Maintain module independence

## 🧪 SYSTEM TESTING

### **Critical Tests:**
```python
# Constitutional compliance test
def test_mango_rule():
    # Bulgarian mango farmer query
    query = "Колко манго дървета имам?"
    result = database_query(query)
    assert result["success"] == True
    
def test_privacy_compliance():
    # Verify no personal data in external API calls
    assert no_farmer_data_in_external_logs()
    
def test_llm_first():
    # Verify no hardcoded language patterns
    assert no_hardcoded_translations_in_code()
```

### **Health Check URLs:**
- System Health: https://6pmgiripe.us-east-1.awsapprunner.com/health/
- Database Status: https://6pmgiripe.us-east-1.awsapprunner.com/database/
- Core API Status: https://3ksdvgdtud.us-east-1.awsapprunner.com/health

## 🆘 EMERGENCY PROCEDURES

### **If Services Are Down:**
1. Check AWS App Runner console for deployment status
2. Verify environment variables are set
3. Check database connectivity
4. Review recent GitHub commits for issues

### **If Database Issues:**
1. AWS RDS console → farmer-crm-production
2. Check connection parameters
3. Verify security groups allow App Runner access
4. Check database logs for errors

### **If Constitutional Violations Found:**
1. STOP development immediately
2. Review constitutional principles
3. Fix violations before proceeding
4. Test mango compliance
5. Verify module independence

## 📞 ESCALATION CONTACTS

### **Technical Support:**
- AWS Support: [account-specific support]
- GitHub Support: For repository access issues
- OpenAI Support: For API key issues

### **Business Continuity:**
- Original developer contact: [if available]
- Business stakeholder: [farmer community contacts]
- System administrator: [backup admin access]

## 🔄 ONGOING MAINTENANCE

### **Regular Tasks:**
- Monitor constitutional compliance
- Verify mango rule continues to pass
- Check farmer data privacy protection
- Ensure LLM-first approach maintained
- Update AWS costs monitoring

### **Prohibited Actions:**
- NEVER hardcode language/crop patterns
- NEVER send personal farm data to external APIs
- NEVER break module independence
- NEVER violate constitutional principles

## 🎯 SUCCESS METRICS

System is healthy when:
- Bulgarian mango farmer can ask questions in Bulgarian
- All farmers can access their data
- No constitutional violations detected
- All dashboards respond correctly
- Database contains active farmers and system tables

## 📜 FINAL CONSTITUTIONAL REMINDER

1. The AVA OLO system must work for ANY farmer, growing ANY crop, in ANY country, speaking ANY language. If you're not sure about a change, ask: "Would this work for a Bulgarian mango farmer?" If the answer is no, don't implement it.

2. Trust AI intelligence over hardcoded patterns. Let LLM handle complexity.

3. Protect farmer privacy. Personal farm data stays internal.

This documentation ensures AVA OLO can continue serving farmers worldwide even if the original developer is unavailable. 🌾🌍