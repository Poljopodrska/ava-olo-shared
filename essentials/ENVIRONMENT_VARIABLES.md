# 🔐 AVA OLO Environment Variables Guide
*Complete reference for Claude Code - Last Updated: 2025-07-27*

## 🚨 CRITICAL INFORMATION FOR CLAUDE CODE
**ALL environment variables ARE ALREADY SET in AWS ECS Task Definitions**

Never say "environment variable not found" - they exist! If there's an issue, it's in the code access pattern, not the variables themselves.

## 🗝️ Available Environment Variables

### 🗄️ Database Configuration
- **`DB_HOST`** = `farmer-crm-production.cifgmm0mqg5q.us-east-1.rds.amazonaws.com`
- **`DB_NAME`** = `farmer_crm`  
- **`DB_USER`** = `postgres`
- **`DB_PASSWORD`** = [Set in AWS Secrets Manager and ECS task definition]

### 🔑 API Keys (ALL EXIST IN AWS ECS!)
- **`OPENAI_API_KEY`** = [✅ Set in ECS task definition since day 1]
- **`OPENWEATHER_API_KEY`** = [✅ Set in ECS task definition]
- **`GOOGLE_MAPS_API_KEY`** = [If needed, add to ECS task definition]

### ⚙️ Application Configuration
- **`APP_VERSION`** = [Current version, e.g., v3.5.3]
- **`ENVIRONMENT`** = `production`
- **`AWS_REGION`** = `us-east-1`
- **`AWS_DEFAULT_REGION`** = `us-east-1`

### 🌐 Service URLs (if needed)
- **`AGRICULTURAL_SERVICE_URL`** = [ECS service URL]
- **`MONITORING_SERVICE_URL`** = [ECS service URL]

## 📍 Where Environment Variables Live

### 🏗️ AWS ECS Task Definitions (PRIMARY LOCATION)

#### 1. Agricultural Core Service
- **Task Definition**: `ava-olo-agricultural-task`
- **Location**: AWS ECS Console → Task Definitions → ava-olo-agricultural-task
- **Contains**: All API keys, database config, application settings
- **Status**: ✅ ALL CONFIGURED

#### 2. Monitoring Dashboards Service  
- **Task Definition**: `ava-olo-monitoring-task`
- **Location**: AWS ECS Console → Task Definitions → ava-olo-monitoring-task  
- **Contains**: Same API keys and configuration as agricultural service
- **Status**: ✅ ALL CONFIGURED

### 🔒 AWS Secrets Manager (for sensitive data)
- **Secret Name**: `ava-olo-production-secrets`
- **Contains**: Database passwords, API keys
- **Integration**: Automatically injected into ECS task definitions

### 💻 Local Development Only
Create `.env` file in project root (NEVER commit to git):

```bash
# Local development only - DO NOT COMMIT
DB_HOST=farmer-crm-production.cifgmm0mqg5q.us-east-1.rds.amazonaws.com
DB_NAME=farmer_crm
DB_USER=postgres
DB_PASSWORD=your_local_password_here
OPENAI_API_KEY=your_openai_key_here
OPENWEATHER_API_KEY=your_weather_key_here
APP_VERSION=development
ENVIRONMENT=development
```

## 🐍 How to Access in Python Code

### ✅ CORRECT METHOD (Always use this):

```python
# Import the central configuration
from ava_olo_shared.environments.central_config import CentralConfig

# Access environment variables
openai_key = CentralConfig.OPENAI_API_KEY
db_host = CentralConfig.DB_HOST
db_password = CentralConfig.DB_PASSWORD

# Validate all required keys are present
if not CentralConfig.validate_required_keys():
    print("❌ Environment validation failed")
    CentralConfig.debug_environment()  # Shows what's missing
else:
    print("✅ All environment variables validated")
```

### ❌ INCORRECT METHODS (Don't use these):

```python
# DON'T DO THIS - bypasses central config
import os
openai_key = os.getenv('OPENAI_API_KEY')  # ❌ Wrong

# DON'T DO THIS - hardcoded values
openai_key = "sk-abc123..."  # ❌ Wrong

# DON'T DO THIS - assuming missing
if not openai_key:
    print("OpenAI key not found")  # ❌ Wrong assumption
```

## 🔧 Code Examples

### Database Connection
```python
from ava_olo_shared.environments.central_config import CentralConfig
import psycopg2

# Get database configuration
db_config = {
    'host': CentralConfig.DB_HOST,
    'database': CentralConfig.DB_NAME,
    'user': CentralConfig.DB_USER,
    'password': CentralConfig.DB_PASSWORD
}

# Create connection
connection = psycopg2.connect(**db_config)
```

### OpenAI API Integration
```python
from ava_olo_shared.environments.central_config import CentralConfig
import openai

# Configure OpenAI client
openai.api_key = CentralConfig.OPENAI_API_KEY

# Use the API
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Hello"}]
)
```

### Weather API Integration
```python
from ava_olo_shared.environments.central_config import CentralConfig
import requests

# Get weather data
weather_api_key = CentralConfig.OPENWEATHER_API_KEY
url = f"http://api.openweathermap.org/data/2.5/weather?q=Sofia&appid={weather_api_key}"

response = requests.get(url)
weather_data = response.json()
```

## 🚨 Troubleshooting Common Issues

### "OpenAI API key not found"
**✅ SOLUTION**: The key EXISTS in AWS ECS. Check:
1. Using `CentralConfig.OPENAI_API_KEY` (not `os.getenv`)
2. Importing from correct path: `ava_olo_shared.environments.central_config`
3. ECS service is running latest task definition
4. No typos in variable access

### "Database connection failed"
**✅ SOLUTION**: Database credentials ARE set. Check:
1. Using `CentralConfig.DB_PASSWORD` 
2. Network connectivity to AWS RDS
3. VPC security groups allow connection
4. Database is running and accessible

### "Environment variable missing" 
**✅ SOLUTION**: Variables ARE there. Debug with:
```python
from ava_olo_shared.environments.central_config import CentralConfig

# Run debug to see what's actually available
CentralConfig.debug_environment()

# Validate all required keys
CentralConfig.validate_required_keys()
```

## 📝 Adding New Environment Variables

When you need to add a new environment variable:

### 1. Update AWS ECS Task Definition
```bash
# AWS CLI example
aws ecs describe-task-definition --task-definition ava-olo-agricultural-task
# Add new environment variable to containerDefinitions[0].environment
# Update task definition with new revision
```

### 2. Update CentralConfig.py
```python
# Add to ava-olo-shared/environments/central_config.py
NEW_API_KEY = os.getenv('NEW_API_KEY')
```

### 3. Update This Documentation
- Add to the environment variables list above
- Include usage example
- Update troubleshooting section if needed

### 4. Redeploy Services
```bash
# Force new deployment to pick up new task definition
aws ecs update-service --cluster ava-olo-production --service ava-olo-agricultural-service --force-new-deployment
aws ecs update-service --cluster ava-olo-production --service ava-olo-monitoring-service --force-new-deployment
```

## 🏛️ Constitutional Compliance

Following AVA OLO constitutional principles:

- **Principle 8**: No hardcoded values - all configuration via environment variables
- **Principle 12**: Central configuration management via CentralConfig
- **Principle 15**: Protection against breaking changes - validate before use

## 🔍 Debugging Commands

### Check ECS Task Definition
```bash
# See current environment variables in ECS
aws ecs describe-task-definition --task-definition ava-olo-agricultural-task --query 'taskDefinition.containerDefinitions[0].environment'
```

### Test Environment Access
```python
# Quick test script
from ava_olo_shared.environments.central_config import CentralConfig

print("=== ENVIRONMENT VARIABLE TEST ===")
CentralConfig.debug_environment()
print(f"All valid: {CentralConfig.validate_required_keys()}")
```

### Check Running Service
```bash
# See which task definition is currently running
aws ecs describe-services --cluster ava-olo-production --services ava-olo-agricultural-service --query 'services[0].taskDefinition'
```

## 🎯 Key Takeaways for Claude Code

1. **✅ Environment variables ARE set** in AWS ECS task definitions
2. **✅ Always use CentralConfig.py** to access them 
3. **✅ Run debug_environment()** if variables seem "missing"
4. **✅ They work in production** - if failing locally, check .env file
5. **✅ Never hardcode** API keys or database credentials

## 📚 Related Documentation

- [Central Configuration Implementation](/ava-olo-shared/environments/central_config.py)
- [AWS ECS Task Definitions](https://console.aws.amazon.com/ecs/home?region=us-east-1#/taskDefinitions)
- [Constitutional Principles](/ava-olo-shared/essentials/AVA_OLO_CONSTITUTION.md)

---

**🥭 Remember**: The Bulgarian mango farmer's environment variables are rock solid and always available! 🥭

**Last Updated**: 2025-07-27  
**Version**: v3.5.3  
**Status**: ✅ All variables confirmed present in AWS ECS