# ECS Database Access Solutions
**Date**: 2025-07-20 11:54:00 UTC | 13:54:00 CET
**Type**: Infrastructure
**Author**: Claude Code
**Related Services**: ECS Tasks and RDS Access

## Executive Summary
With App Runner being decommissioned and ECS now in production, we need alternative methods to access the private RDS database for analysis and maintenance. This report provides practical solutions for the ECS architecture.

## Current Infrastructure Status
- **Production**: ECS (http://ava-olo-alb-65365776.us-east-1.elb.amazonaws.com)
- **App Runner**: To be decommissioned (temporary backup)
- **RDS**: Private subnet (172.31.0.55)
- **ECS Tasks**: ava-monitoring-task:5, ava-agricultural-task:4

## Database Access Solutions for ECS

### Solution 1: ECS Exec (RECOMMENDED)
AWS ECS Exec allows you to run commands directly in running containers:

```bash
# Enable ECS Exec on your service
aws ecs update-service \
  --cluster ava-olo-production \
  --service monitoring-service \
  --enable-execute-command

# Execute into container
aws ecs execute-command \
  --cluster ava-olo-production \
  --task <task-id> \
  --container monitoring \
  --interactive \
  --command "/bin/bash"

# Once inside, use psql
psql -h farmer-crm-production.cifgmm0mqg5q.us-east-1.rds.amazonaws.com -U postgres -d farmer_crm
```

**Advantages**:
- Direct access through existing ECS tasks
- No additional infrastructure needed
- Uses existing VPC connectivity

### Solution 2: Database API Endpoint in ECS
Add a temporary admin endpoint to your ECS service:

```python
# In monitoring service
@app.route('/api/admin/database-analysis', methods=['POST'])
def database_analysis():
    # Require special header for security
    if request.headers.get('X-Admin-Token') != os.environ.get('ADMIN_TOKEN'):
        return jsonify({'error': 'Unauthorized'}), 401
    
    query = request.json.get('query')
    # Run analysis queries
    results = db.execute(query)
    return jsonify(results)
```

Deploy temporarily, use, then remove.

### Solution 3: Lambda Function in VPC
Create a temporary Lambda for database access:

```python
import json
import psycopg2
import os

def lambda_handler(event, context):
    conn = psycopg2.connect(
        host=os.environ['DB_HOST'],
        database=os.environ['DB_NAME'],
        user=os.environ['DB_USER'],
        password=os.environ['DB_PASSWORD']
    )
    
    cur = conn.cursor()
    cur.execute(event['query'])
    results = cur.fetchall()
    
    return {
        'statusCode': 200,
        'body': json.dumps(results, default=str)
    }
```

### Solution 4: AWS Systems Manager with ECS
Create an ECS task specifically for administration:

```yaml
# admin-task-definition.json
{
  "family": "ava-admin-tools",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "256",
  "memory": "512",
  "containerDefinitions": [{
    "name": "admin-tools",
    "image": "postgres:14-alpine",
    "command": ["sleep", "3600"],
    "environment": [
      {"name": "PGHOST", "value": "farmer-crm-production.cifgmm0mqg5q.us-east-1.rds.amazonaws.com"},
      {"name": "PGUSER", "value": "postgres"},
      {"name": "PGDATABASE", "value": "farmer_crm"}
    ],
    "secrets": [
      {"name": "PGPASSWORD", "valueFrom": "arn:aws:secretsmanager:us-east-1:127679825789:secret:ava-olo/db-password"}
    ]
  }]
}
```

Run on-demand for database work.

### Solution 5: RDS Query Editor (Simplest)
Use AWS Console's built-in query editor:

1. AWS Console → RDS → Query Editor
2. Connect to farmer-crm-production
3. Run analysis queries
4. Export results

**Note**: Requires RDS Data API to be enabled.

## Recommended Approach for Database Analysis

Given your current task needs:

1. **Immediate**: Use RDS Query Editor in AWS Console
2. **Short-term**: Enable ECS Exec on existing tasks
3. **For automation**: Create Lambda function
4. **For regular access**: Admin ECS task

## Implementation Priority

### Phase 1: Complete Current Analysis (Today)
```bash
# Option A: RDS Query Editor
# Run these queries in AWS Console:

-- Table count
SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public';

-- Table sizes
SELECT 
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
```

### Phase 2: Setup Permanent Access (This Week)
1. Enable ECS Exec on services
2. Create admin Lambda function
3. Document access procedures

## Security Considerations

1. **ECS Exec**: Audit logs in CloudTrail
2. **API Endpoints**: Use strong authentication
3. **Lambda**: Restrict IAM permissions
4. **Admin Tasks**: Run only when needed

## Cost Impact

- **ECS Exec**: No additional cost
- **Lambda**: ~$0.01 per 1000 queries
- **Admin ECS Task**: ~$0.01/hour when running
- **RDS Query Editor**: No cost

## Next Steps

1. Use RDS Query Editor for immediate analysis
2. Update IMPLEMENTATION_GUIDELINES.md with ECS access methods
3. Remove App Runner references from documentation
4. Setup ECS Exec for future access

The transition from App Runner to ECS actually provides MORE flexibility for database access through ECS Exec and task-based administration.