# AWS Environment Variables Setup Guide
**Complete Protection System v3.5.5 - AWS-Only Environment Enforcement**

## 🔒 Constitutional Rule: ALL environment variables MUST come from AWS

This guide shows how to properly configure environment variables in AWS ECS task definitions ONLY. Local .env files are FORBIDDEN and will be blocked by our protection system.

---

## 🚨 CRITICAL: Why AWS-Only?

1. **Security**: Secrets never exist in code or local files
2. **Constitutional Compliance**: Principle 8 - No hardcoded values
3. **Bulgarian Mango Farmer Test**: Works universally without local setup
4. **Protection**: Git hooks and CI/CD block any local .env files

---

## 📋 Required Environment Variables

### Critical Variables (MUST be set in AWS)
```bash
# Database
DB_PASSWORD=your_production_db_password

# API Keys
OPENAI_API_KEY=your_openai_api_key_here
OPENWEATHER_API_KEY=your_weather_api_key
GOOGLE_MAPS_API_KEY=your_google_maps_key
PERPLEXITY_API_KEY=your_perplexity_key

# Security
SECRET_KEY=your_secret_key
JWT_SECRET_KEY=your_jwt_secret
```

### Optional Variables (have defaults)
```bash
# Application
APP_VERSION=3.5.5
ENVIRONMENT=production
SERVICE_NAME=ava-olo-agricultural

# AWS
AWS_REGION=us-east-1
AWS_ACCOUNT_ID=127679825789
ECS_CLUSTER=ava-olo-production

# Features
ENABLE_WEATHER=true
ENABLE_PERPLEXITY=true
ENABLE_WHATSAPP=true
ENABLE_DEBUG=false
```

---

## 🛠️ AWS ECS Task Definition Setup

### 1. Using AWS CLI

```bash
# Get current task definition
aws ecs describe-task-definition \
  --task-definition ava-olo-agricultural-task \
  --region us-east-1

# Update task definition with environment variables
aws ecs register-task-definition \
  --family ava-olo-agricultural-task \
  --requires-compatibilities FARGATE \
  --network-mode awsvpc \
  --cpu 256 \
  --memory 512 \
  --execution-role-arn arn:aws:iam::127679825789:role/ecsTaskExecutionRole \
  --container-definitions '[
    {
      "name": "ava-olo-agricultural",
      "image": "127679825789.dkr.ecr.us-east-1.amazonaws.com/ava-olo-agricultural:latest",
      "essential": true,
      "portMappings": [
        {
          "containerPort": 8080,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {"name": "DB_HOST", "value": "farmer-crm-production.cifgmm0mqg5q.us-east-1.rds.amazonaws.com"},
        {"name": "DB_NAME", "value": "farmer_crm"},
        {"name": "DB_USER", "value": "postgres"},
        {"name": "DB_PASSWORD", "value": "YOUR_SECURE_DB_PASSWORD"},
        {"name": "OPENAI_API_KEY", "value": "YOUR_OPENAI_API_KEY_HERE"},
        {"name": "OPENWEATHER_API_KEY", "value": "YOUR_WEATHER_KEY"},
        {"name": "GOOGLE_MAPS_API_KEY", "value": "YOUR_GOOGLE_KEY"},
        {"name": "APP_VERSION", "value": "3.5.5"},
        {"name": "ENVIRONMENT", "value": "production"},
        {"name": "AWS_REGION", "value": "us-east-1"},
        {"name": "SERVICE_NAME", "value": "ava-olo-agricultural"}
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/ava-olo-agricultural",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]'
```

### 2. Using AWS Console

1. Navigate to **ECS Console** → **Task Definitions**
2. Select `ava-olo-agricultural-task`
3. Click **Create new revision**
4. Scroll to **Container Definitions** → **Environment**
5. Add each environment variable:
   - **Key**: `DB_PASSWORD` **Value**: `your_secure_password`
   - **Key**: `OPENAI_API_KEY` **Value**: `your_openai_key_here`
   - (Continue for all required variables)
6. Click **Update** then **Create**

### 3. Using AWS Secrets Manager (Recommended for Sensitive Data)

```bash
# Store secrets in AWS Secrets Manager
aws secretsmanager create-secret \
  --name "ava-olo/production/database" \
  --description "Database credentials for AVA OLO" \
  --secret-string '{"password":"your_secure_db_password"}'

aws secretsmanager create-secret \
  --name "ava-olo/production/openai" \
  --description "OpenAI API key for AVA OLO" \
  --secret-string '{"api_key":"your_openai_key_here"}'
```

Then reference in task definition:
```json
{
  "name": "DB_PASSWORD",
  "valueFrom": "arn:aws:secretsmanager:us-east-1:127679825789:secret:ava-olo/production/database:password::"
}
```

---

## 🔧 Deployment Steps

### 1. Update Task Definition
```bash
aws ecs register-task-definition --cli-input-json file://task-definition.json
```

### 2. Update Service
```bash
aws ecs update-service \
  --cluster ava-olo-production \
  --service ava-olo-agricultural-service \
  --task-definition ava-olo-agricultural-task:LATEST
```

### 3. Wait for Deployment
```bash
aws ecs wait services-stable \
  --cluster ava-olo-production \
  --services ava-olo-agricultural-service
```

---

## 🧪 Verification

### 1. Check Task Definition
```bash
aws ecs describe-task-definition \
  --task-definition ava-olo-agricultural-task:LATEST \
  --query 'taskDefinition.containerDefinitions[0].environment'
```

### 2. Check Running Task
```bash
# Get running task ARN
TASK_ARN=$(aws ecs list-tasks \
  --cluster ava-olo-production \
  --service-name ava-olo-agricultural-service \
  --query 'taskArns[0]' --output text)

# Check task details
aws ecs describe-tasks \
  --cluster ava-olo-production \
  --tasks $TASK_ARN
```

### 3. Check Application Logs
```bash
aws logs get-log-events \
  --log-group-name /ecs/ava-olo-agricultural \
  --log-stream-name "ecs/ava-olo-agricultural/$(date +%Y/%m/%d)"
```

---

## 🚫 What NOT to Do

### ❌ FORBIDDEN: Local .env files
```bash
# This is BLOCKED by our protection system
echo "DB_PASSWORD=secret123" > .env
echo "OPENAI_API_KEY=your_key_here" >> .env
```

### ❌ FORBIDDEN: Hardcoded secrets in code
```python
# This will be detected and blocked
OPENAI_API_KEY = "hardcoded_key_example"
DB_PASSWORD = "hardcoded_password_example"
```

### ❌ FORBIDDEN: Environment variables in Docker
```dockerfile
# This bypasses AWS-only enforcement
ENV OPENAI_API_KEY=your_key_here
ENV DB_PASSWORD=your_password_here
```

---

## ✅ Correct Usage

### ✅ CORRECT: Use CentralConfig
```python
from ava_olo_shared.environments.central_config import CentralConfig

# This properly gets variables from AWS ECS
api_key = CentralConfig.OPENAI_API_KEY
db_password = CentralConfig.DB_PASSWORD
```

### ✅ CORRECT: Environment variable in ECS only
```json
{
  "environment": [
    {"name": "OPENAI_API_KEY", "value": "your_key_from_aws_here"}
  ]
}
```

---

## 🛡️ Protection System Features

Our AWS-only enforcement includes:

1. **Git Hooks**: Block commits with .env files or hardcoded secrets
2. **GitHub Actions**: CI/CD blocks PRs with violations
3. **Runtime Enforcement**: Applications exit if .env files detected
4. **Central Config**: Single source of truth for all variables
5. **Constitutional Compliance**: Automatic Principle 8 enforcement

---

## 🔍 Troubleshooting

### Issue: "Missing environment variable"
```bash
# Check if variable is in task definition
aws ecs describe-task-definition \
  --task-definition ava-olo-agricultural-task:LATEST \
  --query 'taskDefinition.containerDefinitions[0].environment[?name==`OPENAI_API_KEY`]'
```

### Issue: "AWS enforcement blocked execution"
```bash
# Remove any .env files
find . -name ".env*" -delete

# Verify no .env files exist
find . -name ".env*" 2>/dev/null || echo "No .env files found"
```

### Issue: "Application not picking up variables"
```python
# Debug environment in application
from ava_olo_shared.environments.central_config import CentralConfig
CentralConfig.debug_environment()
```

---

## 📞 Support

If you encounter issues:

1. **Check AWS task definition** has all required variables
2. **Verify service is running latest revision**
3. **Ensure no .env files exist** (protection system will block)
4. **Use CentralConfig class** for all environment access
5. **Check application logs** in CloudWatch

---

## 🥭 Bulgarian Mango Farmer Compliance

This setup ensures that a Bulgarian mango farmer can:
1. Deploy the application using only AWS
2. Never need local .env files  
3. Have all secrets managed securely in AWS
4. Follow constitutional principles automatically

**🏛️ Constitutional Rule Enforced: Principle 8 - No hardcoded values, AWS-only secrets**