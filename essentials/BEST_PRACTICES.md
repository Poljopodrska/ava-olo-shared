# AVA OLO Best Practices
*Real-world lessons from production deployments*

## 🥭 MANGO RULE PRINCIPLE
> **"Would this work for a Bulgarian mango farmer?"**  
> Every practice must be universal, scalable, and accessible globally.

## Table of Contents
1. [ECS Deployment Timeline](#ecs-deployment-timeline)
2. [Troubleshooting Guide](#troubleshooting-guide)
3. [What NOT to Do](#what-not-to-do)
4. [Monitoring Commands](#monitoring-commands)
5. [Common Scenarios](#common-scenarios)
6. [Performance Best Practices](#performance-best-practices)
7. [Database Best Practices](#database-best-practices)
8. [Security Best Practices](#security-best-practices)
9. [Git Workflow Best Practices](#git-workflow-best-practices)

---

## 🚀 ECS Deployment Timeline

### ⏱️ Expected Timeline: 12-17 Minutes
**DON'T PANIC!** ECS deployments are deliberately slow for safety and stability.

#### Visual Timeline
```
GitHub Push → GitHub Actions → ECR Build → ECS Deploy → Health Checks → Traffic Switch → Complete
     ↓              ↓             ↓           ↓            ↓              ↓            ↓
   30sec          2-3min        1-2min      1min       5-10min       1-2min       30sec
   
Total: 12-17 minutes (NORMAL!)
```

### 🔄 Real Deployment Experience

#### Phase 1: Code Push (30 seconds)
```bash
git push origin main --tags
# Expected: Immediate success
# GitHub webhook triggers within 30 seconds
```

#### Phase 2: GitHub Actions (2-3 minutes)
```bash
# Monitor at: https://github.com/Poljopodrska/ava-olo-monitoring-dashboards/actions
# Expected stages:
# ✅ Checkout code (30s)
# ✅ Build Docker image (90s)
# ✅ Push to ECR (60s)
```

#### Phase 3: ECR Build Complete (1-2 minutes)
```bash
# Image appears in AWS ECR
# ECS begins pulling new image
# Task definition updates automatically
```

#### Phase 4: ECS Task Creation (1 minute)
```bash
# New task starts alongside old task
# Both tasks run during transition
# Load balancer begins health checks
```

#### Phase 5: Health Checks (5-10 minutes) ⚠️ LONGEST PHASE
```bash
# AWS Application Load Balancer performs health checks
# Checks /health endpoint every 30 seconds
# Requires 2 consecutive successes before switching traffic
# Old task continues serving traffic during this phase

# This is where developers often panic - DON'T!
# The system is designed to be cautious
```

#### Phase 6: Traffic Switch (1-2 minutes)
```bash
# Load balancer switches traffic to new task
# Old task begins draining connections
# Version endpoint updates to new version
```

#### Phase 7: Completion (30 seconds)
```bash
# Old task terminates
# Deployment marked as PRIMARY
# New version fully active
```

### 📊 Timeline Expectations by Version Type

| Change Type | Expected Duration | Why |
|-------------|------------------|-----|
| Configuration only | 8-12 minutes | No Docker rebuild |
| Code changes | 12-17 minutes | Full rebuild + health checks |
| Database migrations | 15-25 minutes | Additional migration time |
| Major version | 15-20 minutes | Extra caution in health checks |

---

## 🔧 Troubleshooting Guide

### 🌳 Decision Tree

```
Is new version showing after 5 minutes?
├─ NO → Check deployment status
│   ├─ GitHub Actions failed? → Fix code issues, re-push
│   ├─ ECS deployment PENDING? → Wait, this is normal (up to 15 min)
│   ├─ ECS deployment FAILED? → Check CloudWatch logs
│   └─ No new deployment? → Check GitHub webhook/permissions
└─ YES → Deployment successful! 🎉
```

### 🚨 Common Issues & Solutions

#### Issue 1: Version Not Updating After 20 Minutes
**Symptoms**: Old version still showing, ECS deployment stuck
```bash
# Check deployment status
aws ecs describe-services --cluster ava-olo-production \
  --services monitoring-dashboards \
  --query 'services[0].deployments[?status==`PRIMARY`]'

# If stuck in PENDING:
# 1. Check health check endpoint manually
curl https://ava-olo-alb-65365776.us-east-1.elb.amazonaws.com/health

# 2. Check CloudWatch logs for errors
aws logs tail /ecs/monitoring-dashboards --follow

# 3. If task keeps restarting, rollback:
aws ecs update-service --cluster ava-olo-production \
  --service monitoring-dashboards \
  --task-definition ava-olo-monitoring-task:[PREVIOUS_REVISION]
```

#### Issue 2: Database Connection Errors
**Symptoms**: Health checks failing, "database connection" errors
```bash
# Check RDS status
aws rds describe-db-instances --db-instance-identifier farmer-crm

# Verify security groups allow ECS → RDS traffic
aws ec2 describe-security-groups --group-ids sg-xxxxxxxxx

# Check database credentials in task definition
aws ecs describe-task-definition --task-definition ava-olo-monitoring-task:latest \
  --query 'taskDefinition.containerDefinitions[0].environment'
```

#### Issue 3: Memory/CPU Issues
**Symptoms**: Tasks restarting, performance degradation
```bash
# Check resource utilization
aws ecs describe-services --cluster ava-olo-production \
  --services monitoring-dashboards \
  --query 'services[0].deployments[0].{Running:runningCount,Desired:desiredCount}'

# Increase memory/CPU in task definition if needed
# Current: 512 CPU, 1024 Memory
# Consider: 1024 CPU, 2048 Memory for high load
```

---

## ❌ What NOT to Do

### 🚫 Never Do These During Deployment

#### 1. DON'T Panic After 5 Minutes
```bash
# ❌ WRONG: Force restart after 5 minutes
aws ecs update-service --force-new-deployment

# ✅ RIGHT: Wait up to 15 minutes, monitor progress
aws ecs describe-services --cluster ava-olo-production --services monitoring-dashboards
```

#### 2. DON'T Deploy Multiple Versions Simultaneously
```bash
# ❌ WRONG: Push new version while deployment in progress
git tag v2.5.8-hotfix
git push origin main --tags  # While v2.5.7 still deploying

# ✅ RIGHT: Wait for deployment completion
# Check: Version endpoint returns expected version
curl https://ava-olo-alb-65365776.us-east-1.elb.amazonaws.com/version
```

#### 3. DON'T Hardcode Environment-Specific Values
```python
# ❌ WRONG: Environment hardcoding
if server_name == "production":
    db_host = "farmer-crm.cluster-xyz.us-east-1.rds.amazonaws.com"

# ✅ RIGHT: Use environment variables
db_host = os.getenv('DB_HOST')
```

#### 4. DON'T Skip Pre-Deployment Checks
```bash
# ❌ WRONG: Deploy without testing
git commit -m "fix database issue"
git push origin main

# ✅ RIGHT: Run protection gates
./.pre-commit-compliance.sh
# Check SYSTEM_CHANGELOG.md updated
# Verify version bumped
```

#### 5. DON'T Deploy on Fridays After 3 PM
**Why**: If something breaks, you'll spend weekend fixing it
**Better**: Deploy Tuesday-Thursday for easier issue resolution

---

## 📊 Monitoring Commands

### 🔍 Essential Monitoring Commands

#### Real-Time Deployment Status
```bash
# Watch deployment progress (updates every 30 seconds)
watch -n 30 "aws ecs describe-services --cluster ava-olo-production \
  --services monitoring-dashboards \
  --query 'services[0].deployments[0].{
    Status:status,
    Running:runningCount,
    Desired:desiredCount,
    CreatedAt:createdAt
  }' --output table"
```

#### Quick Health Check
```bash
# Check if service is responding
curl -s https://ava-olo-alb-65365776.us-east-1.elb.amazonaws.com/health | jq .

# Expected output:
{
  "status": "healthy",
  "version": "v2.5.6-schema-nlq-prompt-fix",
  "database": "connected",
  "timestamp": "2025-07-26T16:45:00Z"
}
```

#### Version Verification
```bash
# Check current deployed version
curl -s https://ava-olo-alb-65365776.us-east-1.elb.amazonaws.com/version | jq .

# Expected format:
{
  "version": "v2.5.6-schema-nlq-prompt-fix-a1b2c3d4",
  "service": "monitoring-dashboards",
  "deployment_time": "2025-07-26T16:45:00Z"
}
```

#### CloudWatch Logs Monitoring
```bash
# Watch application logs in real-time
aws logs tail /ecs/monitoring-dashboards --follow

# Filter for errors only
aws logs filter-log-events --log-group-name /ecs/monitoring-dashboards \
  --filter-pattern "ERROR" --start-time $(date -d '5 minutes ago' +%s)000
```

#### Resource Utilization
```bash
# Check CPU and memory usage
aws cloudwatch get-metric-statistics \
  --namespace AWS/ECS \
  --metric-name CPUUtilization \
  --dimensions Name=ServiceName,Value=monitoring-dashboards \
              Name=ClusterName,Value=ava-olo-production \
  --start-time $(date -d '1 hour ago' -u +%Y-%m-%dT%H:%M:%S) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%S) \
  --period 300 \
  --statistics Average
```

---

## 🎯 Common Scenarios

### Scenario 1: v2.5.4 Database Fix Deployment
**Timeline**: 15 minutes (actual experience)
```bash
# 16:30 - Git push
git tag v2.5.4-db-fixed
git push origin main --tags

# 16:32 - GitHub Actions started
# 16:35 - Docker build complete
# 16:36 - ECS deployment started
# 16:41 - Health checks began (longest phase)
# 16:45 - Traffic switch completed
# Expected version available at 16:45

# Monitoring during deployment:
watch -n 60 "curl -s https://ava-olo-alb-65365776.us-east-1.elb.amazonaws.com/version"
```

### Scenario 2: Schema Button Feature (v3.2.0)
**Timeline**: 13 minutes
```bash
# Major feature deployment
# Expected longer due to database schema changes
# Health checks take extra time for DB-heavy features

# Pre-deployment verification:
curl -s https://ava-olo-alb-65365776.us-east-1.elb.amazonaws.com/dashboards/database/api/database-schema
# Should return new schema endpoint after deployment
```

### Scenario 3: Configuration-Only Change
**Timeline**: 8 minutes
```bash
# Fastest deployment type
# Only environment variable changes
# No Docker rebuild required

# Example: Database password update
# Task definition updated directly
# Faster health checks (service already proven stable)
```

---

## ⚡ Performance Best Practices

### 🔋 Database Optimization

#### Connection Pooling
```python
# ✅ BEST PRACTICE: Use connection pooling
DB_POOL_SETTINGS = {
    "pool_size": int(os.getenv("DB_POOL_SIZE", "20")),
    "max_overflow": int(os.getenv("DB_MAX_OVERFLOW", "30")),
    "pool_pre_ping": True,
    "pool_recycle": int(os.getenv("DB_POOL_RECYCLE", "300"))
}

# ❌ AVOID: New connection per request
def get_db_connection():
    return psycopg2.connect(host=..., database=...)  # Creates new connection every time
```

#### Query Optimization
```sql
-- ✅ BEST PRACTICE: Use indexes and LIMIT
SELECT id, name, phone_number 
FROM farmers 
WHERE subscription_status = 'active' 
  AND country = 'Croatia'
ORDER BY created_at DESC 
LIMIT 100;

-- ❌ AVOID: Unfiltered queries
SELECT * FROM farmers;  -- Returns ALL farmers globally
```

#### Database Schema Best Practices
```sql
-- ✅ BEST PRACTICE: Use proper indexes
CREATE INDEX idx_farmers_country_status ON farmers(country, subscription_status);
CREATE INDEX idx_fields_farmer_id ON fields(farmer_id);

-- ✅ BEST PRACTICE: Foreign key constraints
ALTER TABLE fields ADD CONSTRAINT fk_fields_farmer 
FOREIGN KEY (farmer_id) REFERENCES farmers(id);
```

### 🚀 Application Performance

#### Caching Strategy
```python
# ✅ BEST PRACTICE: Cache expensive operations
from functools import lru_cache

@lru_cache(maxsize=128)
def get_farmer_statistics(country: str):
    # Expensive database aggregation
    return calculate_stats(country)

# Cache database schema for 5 minutes
SCHEMA_CACHE_TTL = 300
```

#### Memory Management
```python
# ✅ BEST PRACTICE: Process large datasets in chunks
def process_large_dataset(data):
    chunk_size = 1000
    for i in range(0, len(data), chunk_size):
        chunk = data[i:i + chunk_size]
        process_chunk(chunk)
        # Memory gets freed between chunks
```

---

## 🗄️ Database Best Practices

### 📋 Migration Strategy

#### Safe Migration Process
```bash
# 1. Always backup before changes
pg_dump farmer_crm > backup_$(date +%Y%m%d_%H%M%S).sql

# 2. Test migrations on staging first
psql -h staging-db.cluster-xyz.rds.amazonaws.com -d farmer_crm -f migration.sql

# 3. Apply during low-traffic hours
# Best time: 02:00-04:00 UTC (low farmer activity globally)

# 4. Monitor during migration
tail -f /var/log/postgresql/postgresql.log
```

#### Database Versioning
```sql
-- ✅ BEST PRACTICE: Track schema version
CREATE TABLE schema_versions (
    version VARCHAR(50) PRIMARY KEY,
    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    description TEXT
);

INSERT INTO schema_versions (version, description) 
VALUES ('v3.2.0', 'Added schema button endpoints and indexes');
```

### 🔒 Data Protection

#### Farmer Data Encryption
```python
# ✅ BEST PRACTICE: Encrypt personal data
from cryptography.fernet import Fernet

class FarmerDataManager:
    def __init__(self):
        self.cipher = Fernet(os.getenv('ENCRYPTION_KEY'))
    
    def encrypt_phone(self, phone_number: str) -> str:
        return self.cipher.encrypt(phone_number.encode()).decode()
    
    def decrypt_phone(self, encrypted_phone: str) -> str:
        return self.cipher.decrypt(encrypted_phone.encode()).decode()
```

#### Data Retention Policy
```sql
-- Archive old conversations (keep 2 years)
DELETE FROM conversations 
WHERE timestamp < NOW() - INTERVAL '2 years';

-- Keep farmer data indefinitely (GDPR compliance with explicit consent)
-- But anonymize on request
UPDATE farmers 
SET name = 'ANONYMIZED', phone_number = 'REMOVED', email = 'REMOVED'
WHERE id = ? AND gdpr_removal_requested = true;
```

---

## 🔐 Security Best Practices

### 🛡️ Credential Management

#### AWS Secrets Manager Integration
```python
# ✅ BEST PRACTICE: Use AWS Secrets Manager
import boto3
import json

def get_database_credentials():
    secrets_client = boto3.client('secretsmanager', region_name='us-east-1')
    
    response = secrets_client.get_secret_value(SecretId='ava-olo/database/credentials')
    credentials = json.loads(response['SecretString'])
    
    return {
        'host': credentials['host'],
        'username': credentials['username'],
        'password': credentials['password'],
        'database': credentials['database']
    }

# ❌ NEVER: Hardcode credentials
DB_PASSWORD = "j2D8J4LH:~eFrUz>$:kkNT(P$Rq_"  # Exposed in git!
```

#### Environment Variable Security
```bash
# ✅ BEST PRACTICE: Use parameter store for sensitive data
aws ssm put-parameter --name "/ava-olo/production/db-password" \
  --value "secure-password" --type "SecureString"

# Reference in task definition:
{
  "name": "DB_PASSWORD",
  "valueFrom": "arn:aws:ssm:us-east-1:account:parameter/ava-olo/production/db-password"
}
```

### 🔑 API Security

#### Rate Limiting
```python
# ✅ BEST PRACTICE: Implement rate limiting
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["1000 per day", "100 per hour"]
)

@app.route('/api/farmers')
@limiter.limit("10 per minute")
def get_farmers():
    # Protected endpoint
    pass
```

#### Input Validation
```python
# ✅ BEST PRACTICE: Validate all inputs
from marshmallow import Schema, fields, ValidationError

class FarmerSchema(Schema):
    name = fields.Str(required=True, validate=lambda x: len(x) > 0)
    phone_number = fields.Str(required=True, validate=lambda x: x.startswith('+'))
    country = fields.Str(required=True, validate=lambda x: len(x) >= 2)

def create_farmer(data):
    schema = FarmerSchema()
    try:
        validated_data = schema.load(data)
    except ValidationError as err:
        return {"error": "Invalid data", "details": err.messages}, 400
```

---

## 🌿 Git Workflow Best Practices

### 🔴 MANDATORY VERSION NUMBERING 🔴

**CRITICAL: Every commit MUST start with a version number in format `vX.X.X`**

```bash
# ✅ CORRECT - Version number included:
git commit -m "v3.5.2 - Fix database connection pooling issue"
git commit -m "v3.6.0 - Add natural language query feature"

# ❌ WRONG - No version number:
git commit -m "Fix database bug"
git commit -m "feat: add new feature"

# ❌ WRONG - Incorrect format:
git commit -m "3.5.2 - Missing v prefix"
git commit -m "version 3.5.2 - Wrong format"
```

**Git hooks are configured to REJECT commits without proper version format!**

### 📝 Commit Message Format

#### Standard Format (AFTER version number)
```bash
# ✅ BEST PRACTICE: Version + descriptive message
git commit -m "v3.5.2 - feat: add database schema button with Aurora verification

- Added Get Database Schema button to monitoring dashboard
- Implemented Aurora connection verification across all dashboards
- Created comprehensive schema display with expandable tables
- Enhanced UI with PK/FK badges and relationship indicators

Closes #123
MANGO TEST: Bulgarian mango farmer can view database structure

🤖 Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

#### Message Categories
```bash
feat: new feature
fix: bug fix
docs: documentation changes
style: formatting, missing semi colons, etc.
refactor: code change that neither fixes a bug nor adds a feature
test: adding missing tests
chore: maintain, dependencies, etc.
```

### 🏷️ Version Tagging Strategy

#### Semantic Versioning with Descriptions
```bash
# ✅ BEST PRACTICE: Descriptive tags
v3.2.0-schema-button-aurora     # Major feature with Aurora integration
v2.5.4-db-fixed                # Critical database fix
v2.5.5-hotfix-security         # Security patch
v3.0.0-breaking-api-changes    # Breaking changes

# ❌ AVOID: Non-descriptive tags
v2.5.4                         # What does this version do?
backup-20250726                # Not a release tag
fix-123                        # Unclear scope
```

#### Tag Management
```bash
# Create annotated tags with descriptions
git tag -a v3.2.0-schema-button-aurora -m "Database schema viewer with Aurora verification

Features:
- Complete database schema display
- Aurora connection verification
- Interactive table/column exploration
- Foreign key relationship mapping

Target: Bulgarian mango farmers can understand database structure"

# Push tags
git push origin --tags

# List recent tags
git tag -l | grep "^v" | sort -V | tail -10
```

### 🔄 Branch Protection

#### Development Workflow
```bash
# ✅ BEST PRACTICE: Feature branch workflow
git checkout -b feature/schema-button-implementation
# Implement feature
git commit -m "feat: implement database schema button"
git push origin feature/schema-button-implementation
# Create pull request for review

# After review:
git checkout main
git merge feature/schema-button-implementation
git tag v3.2.0-schema-button-aurora
git push origin main --tags
```

---

## 🌍 MANGO RULE Applications

### 🥭 Real Examples of Global Thinking

#### Language Localization
```python
# ✅ MANGO COMPLIANT: Language-agnostic approach
def get_farmer_greeting(farmer):
    return llm.generate(f"Generate a greeting for farmer in {farmer.country} language")

# ❌ MANGO VIOLATION: Hardcoded languages
def get_farmer_greeting(farmer):
    if farmer.country == "Croatia":
        return "Dobrodošli!"
    elif farmer.country == "Bulgaria":
        return "Добре дошли!"
    # What about other countries?
```

#### Currency and Units
```python
# ✅ MANGO COMPLIANT: Dynamic currency/units
def format_price(amount, country):
    locale_data = get_country_locale(country)
    return f"{amount:.2f} {locale_data['currency']}"

# ❌ MANGO VIOLATION: Assumed currency
def format_price(amount):
    return f"{amount:.2f} EUR"  # Not all farmers use EUR!
```

#### Agricultural Practices
```python
# ✅ MANGO COMPLIANT: LLM handles variations
def get_planting_advice(crop, country, soil_data):
    prompt = f"Advise on planting {crop} in {country} with soil: {soil_data}"
    return llm.generate(prompt)

# ❌ MANGO VIOLATION: Regional assumptions
def get_planting_advice(crop):
    if crop == "corn":
        return "Plant in April"  # Wrong for Southern Hemisphere!
```

### 🔍 Common Hardcoding Mistakes

#### Geographic Assumptions
```python
# ❌ WRONG: Northern Hemisphere bias
PLANTING_SEASONS = {
    "spring": ["March", "April", "May"],
    "summer": ["June", "July", "August"]
}

# ✅ RIGHT: Let LLM handle seasonal variations
def get_season_for_country(country, month):
    return llm.generate(f"What season is {month} in {country}?")
```

#### Cultural Assumptions
```python
# ❌ WRONG: Western name format assumption
def format_farmer_name(first_name, last_name):
    return f"{first_name} {last_name}"

# ✅ RIGHT: Flexible name handling
def format_farmer_name(name_data):
    return llm.generate(f"Format name appropriately for culture: {name_data}")
```

---

## 📈 Monitoring and Alerting

### 🚨 Critical Alerts

#### Production Health Monitoring
```bash
# Set up CloudWatch alarms for:

# 1. High error rate (>5% in 5 minutes)
aws cloudwatch put-metric-alarm \
  --alarm-name "ava-olo-high-error-rate" \
  --alarm-description "High error rate detected" \
  --metric-name ErrorRate \
  --namespace AWS/ApplicationELB \
  --statistic Average \
  --period 300 \
  --threshold 5.0 \
  --comparison-operator GreaterThanThreshold

# 2. Database connection failures
aws cloudwatch put-metric-alarm \
  --alarm-name "ava-olo-db-connection-failures" \
  --alarm-description "Database connection issues" \
  --metric-name DatabaseConnectionErrors \
  --namespace AWS/RDS \
  --statistic Sum \
  --period 300 \
  --threshold 10 \
  --comparison-operator GreaterThanThreshold
```

#### Performance Monitoring
```python
# ✅ BEST PRACTICE: Monitor response times
import time
from functools import wraps

def monitor_performance(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        duration = time.time() - start_time
        
        # Log slow queries (>2 seconds)
        if duration > 2.0:
            logger.warning(f"Slow operation: {func.__name__} took {duration:.2f}s")
            
        return result
    return wrapper

@monitor_performance
def get_database_schema():
    # This function is monitored for performance
    pass
```

---

## 🎯 Summary

### ✅ Key Takeaways

1. **ECS Deployments Take 12-17 Minutes** - This is normal, don't panic!
2. **Health Checks Are the Longest Phase** - 5-10 minutes of health checking is expected
3. **Monitor, Don't Interfere** - Use monitoring commands, avoid force restarts
4. **MANGO RULE Everything** - Think globally, code universally
5. **Security First** - Never commit secrets, use AWS Secrets Manager
6. **Document Everything** - Update SYSTEM_CHANGELOG.md for every deployment

### 🚀 Quick Reference Commands

```bash
# Deployment status
aws ecs describe-services --cluster ava-olo-production --services monitoring-dashboards

# Health check
curl https://ava-olo-alb-65365776.us-east-1.elb.amazonaws.com/health

# Version check
curl https://ava-olo-alb-65365776.us-east-1.elb.amazonaws.com/version

# Logs
aws logs tail /ecs/monitoring-dashboards --follow

# Database backup
pg_dump farmer_crm > backup_$(date +%Y%m%d_%H%M%S).sql
```

### 🥭 Bulgarian Mango Farmer Test

Before implementing any practice, ask:
- **"Would this work for a Bulgarian mango farmer?"**
- **"Is this scalable to any country/crop combination?"**
- **"Are there hardcoded assumptions that would break in Bulgaria?"**

If the answer to any is "no", revise the approach using LLM/CAVA for intelligence instead of hardcoded logic.

---

**Remember**: These practices are learned from real production deployments. Share your experiences and update this document as the system evolves!