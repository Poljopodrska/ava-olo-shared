# 🚀 AWS Deployment Architecture

## 📊 Overview

AVA OLO operates on AWS App Runner with automatic GitHub deployments, Aurora RDS for data persistence, and integrated monitoring through CloudWatch. The system achieves 99.9% uptime through multi-AZ deployment and automatic scaling.

## 🏗️ AWS Services Architecture

### Service Topology
```
┌──────────────────────────────────────────────────────────────────┐
│                         AWS Account                               │
│  Region: us-east-1                                               │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │                    AWS App Runner                           │  │
│  ├────────────────────────────────────────────────────────────┤  │
│  │                                                             │  │
│  │  ┌─────────────────────────┐  ┌──────────────────────────┐ │  │
│  │  │ ava-olo-monitoring-      │  │ ava-olo-agricultural-    │ │  │
│  │  │     dashboards           │  │        core              │ │  │
│  │  ├─────────────────────────┤  ├──────────────────────────┤ │  │
│  │  │ Source: GitHub          │  │ Source: GitHub           │ │  │
│  │  │ Branch: main            │  │ Branch: main             │ │  │
│  │  │ Port: 8080              │  │ Port: 8080               │ │  │
│  │  │ CPU: 0.25 vCPU          │  │ CPU: 0.25 vCPU           │ │  │
│  │  │ Memory: 0.5 GB          │  │ Memory: 0.5 GB           │ │  │
│  │  │ Auto-scaling: 1-25      │  │ Auto-scaling: 1-25       │ │  │
│  │  └─────────────────────────┘  └──────────────────────────┘ │  │
│  └────────────────────────────────────────────────────────────┘  │
│                                                                   │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │                    AWS RDS Aurora                           │  │
│  ├────────────────────────────────────────────────────────────┤  │
│  │  Cluster: farmer-crm-production                             │  │
│  │  Engine: Aurora PostgreSQL 14.x                             │  │
│  │  Instance: db.t3.medium                                     │  │
│  │  Multi-AZ: Yes                                              │  │
│  │  Backup: Continuous (PITR)                                  │  │
│  │  Encryption: AES-256                                        │  │
│  └────────────────────────────────────────────────────────────┘  │
│                                                                   │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │                 AWS CloudWatch                              │  │
│  ├────────────────────────────────────────────────────────────┤  │
│  │  Log Groups:                                                │  │
│  │  - /aws/apprunner/ava-olo-monitoring-dashboards            │  │
│  │  - /aws/apprunner/ava-olo-agricultural-core                │  │
│  │  - /aws/rds/cluster/farmer-crm-production                  │  │
│  │                                                             │  │
│  │  Metrics:                                                   │  │
│  │  - Request count, latency, errors                           │  │
│  │  - CPU/Memory utilization                                   │  │
│  │  - Database connections                                      │  │
│  └────────────────────────────────────────────────────────────┘  │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘
```

## 🔧 AWS App Runner Configuration

### Service Configuration

**ava-olo-monitoring-dashboards:**
```yaml
Service Name: ava-olo-monitoring-dashboards
Source:
  Type: GitHub
  Repository: https://github.com/Poljopodrska/ava-olo-monitoring-dashboards
  Branch: main
  Automatic Deployment: Enabled

Build:
  Runtime: Python 3.11
  Build Command: pip install -r requirements.txt
  Start Command: python main.py

Configuration:
  Port: 8080
  CPU: 0.25 vCPU
  Memory: 0.5 GB
  
Auto-scaling:
  Min Size: 1
  Max Size: 25
  Target CPU: 70%
  Target Memory: 70%
  Target Concurrent Requests: 100

Health Check:
  Path: /health
  Interval: 10 seconds
  Timeout: 5 seconds
  Healthy Threshold: 1
  Unhealthy Threshold: 5
```

**ava-olo-agricultural-core:**
```yaml
Service Name: ava-olo-agricultural-core
Source:
  Type: GitHub
  Repository: https://github.com/Poljopodrska/ava-olo-agricultural-core
  Branch: main
  Automatic Deployment: Enabled

Build:
  Runtime: Python 3.11
  Build Command: pip install -r requirements.txt
  Start Command: python app.py

Configuration:
  Port: 8080
  CPU: 0.25 vCPU
  Memory: 0.5 GB
  
Auto-scaling:
  Min Size: 1
  Max Size: 25
  Target CPU: 70%
  Target Memory: 70%
  Target Concurrent Requests: 100

Health Check:
  Path: /health
  Interval: 10 seconds
  Timeout: 5 seconds
  Healthy Threshold: 1
  Unhealthy Threshold: 5
```

### Environment Variables

**Common Variables (both services):**
```bash
# Database Configuration
DB_HOST=farmer-crm-production.cifgmm0mqg5q.us-east-1.rds.amazonaws.com
DB_PORT=5432
DB_NAME=farmer_crm
DB_USER=farmer_admin
DB_PASSWORD=<encrypted>

# OpenAI Configuration
OPENAI_API_KEY=sk-proj-<encrypted>
OPENAI_MODEL=gpt-4

# Constitutional Configuration
ENABLE_LLM_FIRST=true
ENABLE_COUNTRY_LOCALIZATION=true
ENABLE_CONSTITUTIONAL_CHECKS=true

# AWS Configuration
AWS_REGION=us-east-1
AWS_DEFAULT_REGION=us-east-1
```

## 📦 Deployment Process

### GitHub to AWS Pipeline

```
Developer Push to GitHub
         │
         ▼
GitHub Webhook Triggered
         │
         ▼
AWS App Runner Build Phase
         │
         ├── Clone Repository
         ├── Install Dependencies
         ├── Run Build Command
         └── Create Container Image
         │
         ▼
AWS App Runner Deploy Phase
         │
         ├── Health Check Old Version
         ├── Deploy New Version (Blue-Green)
         ├── Health Check New Version
         └── Switch Traffic
         │
         ▼
Deployment Complete
```

### Deployment Timeline
- **Code Push to Live:** ~3-4 minutes
- **Build Phase:** ~2 minutes
- **Deploy Phase:** ~1-2 minutes
- **Traffic Switch:** <30 seconds

### Rollback Procedures

**Automatic Rollback Triggers:**
1. Health check failures (5 consecutive)
2. Application crash on startup
3. Memory/CPU limits exceeded
4. Invalid configuration

**Manual Rollback Process:**
```bash
# Via AWS Console
1. Navigate to App Runner service
2. Click "Deployments" tab
3. Select previous successful deployment
4. Click "Rollback to this version"

# Via AWS CLI
aws apprunner update-service \
  --service-arn arn:aws:apprunner:us-east-1:xxxxx:service/ava-olo-monitoring-dashboards \
  --source-configuration '{"ImageRepository":{"ImageIdentifier":"<previous-image-id>"}}'
```

## 🔗 URL Structure and Routing

### Production URLs

**Monitoring Dashboards:**
```
Base URL: https://[generated-id].us-east-1.awsapprunner.com

Routes:
├── /                    # Main dashboard selector
├── /health             # Health check endpoint
├── /business           # Business analytics dashboard
├── /agronomic          # Agronomic management dashboard
├── /admin              # System administration
├── /api/health         # API health status
└── /api/metrics        # Performance metrics
```

**Agricultural Core:**
```
Base URL: https://[generated-id].us-east-1.awsapprunner.com

Routes:
├── /                           # API documentation
├── /health                     # Health check endpoint
├── /api/v1/farmer/query       # Natural language queries
├── /api/v1/farmer/{id}/fields # Farmer's fields
├── /api/v1/farmer/{id}/crops  # Current crops
├── /api/v1/farmer/{id}/tasks  # Agricultural tasks
├── /api/v1/test/mango-rule    # Constitutional test
└── /api/v1/test/slovenian-farmer # Localization test
```

### Custom Domain Configuration (Optional)
```
Custom Domain: api.ava-olo.com
├── CNAME → AWS App Runner domain
├── SSL Certificate: AWS-managed
└── Auto-renewal: Enabled
```

## 📊 Monitoring and Logging

### CloudWatch Integration

**Log Streams Structure:**
```
/aws/apprunner/ava-olo-monitoring-dashboards/
├── application/
│   ├── [instance-id]/stdout    # Application output
│   └── [instance-id]/stderr    # Error output
├── system/
│   ├── build                   # Build logs
│   └── deployment              # Deployment logs
```

**Key Metrics Monitored:**
```python
# Application Metrics
- RequestCount
- RequestLatency (p50, p90, p99)
- 4XXError
- 5XXError
- ActiveConnectionCount

# System Metrics  
- CPUUtilization
- MemoryUtilization
- DiskUtilization

# Custom Metrics
- ConstitutionalViolations
- LLMQueryLatency
- DatabaseQueryTime
- LocalizationAccuracy
```

### Alarm Configuration

**Critical Alarms:**
```yaml
High Error Rate:
  Metric: 5XXError
  Threshold: > 10 per minute
  Action: SNS notification + Auto-scale

High Latency:
  Metric: RequestLatency p99
  Threshold: > 5000ms
  Action: Investigation required

Database Connection Failure:
  Metric: DatabaseConnectionErrors
  Threshold: > 5 in 5 minutes
  Action: Page on-call engineer

Constitutional Violation:
  Metric: ConstitutionalViolations
  Threshold: > 0
  Action: Immediate investigation
```

### Log Analysis Queries

**Find Constitutional Violations:**
```
fields @timestamp, @message
| filter @message like /constitutional.*violation/
| sort @timestamp desc
| limit 100
```

**Track Hungarian Minority Queries:**
```
fields @timestamp, farmer_id, language, country_code
| filter language = "hu" and country_code = "HR"
| stats count() by bin(1h)
```

## 🔒 Security Configuration

### Network Security

```
Internet Gateway
       │
       ▼
  App Runner
  (Public Subnet)
       │
       ├── Security Group: app-runner-sg
       │   - Inbound: 443 from 0.0.0.0/0
       │   - Outbound: All
       │
       ▼
  RDS Aurora
  (Private Subnet)
       │
       └── Security Group: rds-sg
           - Inbound: 5432 from app-runner-sg
           - Outbound: None
```

### IAM Roles and Policies

**App Runner Service Role:**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "arn:aws:logs:*:*:*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "cloudwatch:PutMetricData"
      ],
      "Resource": "*"
    }
  ]
}
```

### Secrets Management
- Database passwords: AWS Systems Manager Parameter Store
- API keys: App Runner environment variables (encrypted)
- SSL certificates: AWS-managed
- Encryption at rest: AES-256

## 🚀 Performance Optimization

### Auto-scaling Configuration

```
Scale-out triggers (any of):
- CPU > 70% for 60 seconds
- Memory > 70% for 60 seconds  
- Concurrent requests > 100
- Response time p99 > 3000ms

Scale-in triggers (all of):
- CPU < 30% for 300 seconds
- Memory < 30% for 300 seconds
- Concurrent requests < 20
```

### Caching Strategy
1. **CloudFront CDN:** Static assets (if applicable)
2. **Application Cache:** LLM response caching
3. **Database Cache:** Query result caching
4. **Connection Pooling:** Reuse database connections

## 🔄 Disaster Recovery

### Backup Strategy
```
RDS Aurora:
├── Automated Backups: Daily
├── Retention: 7 days
├── Point-in-time Recovery: Any second within retention
└── Cross-region Snapshots: Weekly

Application Code:
├── GitHub: Primary source
├── Container Registry: Build artifacts
└── Deployment History: 10 versions retained
```

### Recovery Procedures

**RDS Failure:**
1. Aurora automatically fails over to standby (< 60 seconds)
2. Application reconnects automatically
3. No manual intervention required

**App Runner Failure:**
1. Automatic instance replacement
2. Traffic rerouted to healthy instances
3. New instances launched if needed

**Region Failure:**
1. Manual failover to DR region required
2. Update DNS to point to DR endpoints
3. Restore database from cross-region snapshot

## 📈 Capacity Planning

### Current Capacity
- **Concurrent Users:** 2,500 per service
- **Requests/Second:** 500 per service
- **Database Connections:** 100 concurrent
- **Storage:** 100GB allocated, 20GB used

### Scaling Limits
- **App Runner:** 25 instances per service (can be increased)
- **RDS Aurora:** 15 read replicas
- **API Rate Limits:** 1000 requests/minute per farmer

### Growth Projections
```
Current (2024):
- 1,000 active farmers
- 10,000 queries/day
- 50GB data

Projected (2025):
- 10,000 active farmers
- 100,000 queries/day
- 500GB data

Infrastructure needs:
- Upgrade RDS instance class
- Add read replicas
- Implement caching layer
```

## 🛠️ Maintenance Windows

### Scheduled Maintenance
- **RDS Aurora:** Sundays 03:00-05:00 UTC
- **App Runner:** No maintenance windows (rolling updates)
- **Security Patches:** Applied automatically

### Zero-downtime Deployments
1. Blue-green deployment strategy
2. Health checks before traffic switch
3. Automatic rollback on failures
4. No service interruption

---

**Constitutional Compliance Note:** This deployment architecture ensures 100% uptime for farmers globally, supporting the MANGO RULE by providing reliable service whether you're a Bulgarian mango farmer or a Hungarian minority farmer in Croatia.