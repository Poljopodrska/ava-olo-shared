# 🚀 AVA OLO DEPLOYMENT STANDARD

## ONE WAY TO DEPLOY - NO EXCEPTIONS

This is the **ONLY** approved method for deploying AVA OLO services. Any deviation is a constitutional violation.

## Step 1: Pre-deployment Verification

### 1.1 Check Feature Protection
```bash
# Capture current working state
python modules/core/feature_protection.py capture

# Verify all features still work
python modules/core/feature_protection.py verify
```

### 1.2 Constitutional Compliance Check
```bash
# Run constitutional guard
python modules/core/constitutional_guard.py check
```

### 1.3 Version Check
Ensure your version follows the format: `vX.X.X`
- Major (X.0.0): Breaking changes or major features
- Minor (0.X.0): New features or significant improvements  
- Patch (0.0.X): Bug fixes or small improvements

## Step 2: Update Version

### 2.1 Set Version Environment Variable
```bash
export APP_VERSION="3.5.0"
```

### 2.2 Update Version in Code
The version is centrally managed in:
- `/ava-olo-shared/version_config.py`
- Service-specific `config.py` files

## Step 3: Run All Tests

### 3.1 Feature Protection Tests
```bash
python modules/core/feature_protection.py verify --all
```

### 3.2 Unit Tests
```bash
python -m pytest tests/ -v
```

### 3.3 Integration Tests
```bash
python tests/integration/test_all_endpoints.py
```

## Step 4: Commit with Proper Format

### 4.1 Stage Changes
```bash
git add -A
```

### 4.2 Commit with Version
```bash
git commit -m "v3.5.0 - Your description here"
```

**IMPORTANT**: The commit MUST start with `vX.X.X - `. The git hook will reject any other format.

## Step 5: Push to Trigger Deployment

### 5.1 Push to Main Branch
```bash
git push origin main
```

This will trigger:
- AWS CodeBuild (builds Docker image)
- AWS ECR (stores image)
- AWS ECS (deploys new version)

## Step 6: Verify Deployment

### 6.1 Run Deployment Verification
```bash
./verify_deployment.sh
```

### 6.2 Check Version Endpoints
```bash
# Agricultural Core Service
curl http://ava-olo-farmers-alb-82735690.us-east-1.elb.amazonaws.com/health

# Monitoring Dashboards Service  
curl http://ava-olo-alb-65365776.us-east-1.elb.amazonaws.com/health
```

### 6.3 Verify Features Still Work
```bash
python modules/core/feature_protection.py test farmer_registration
python modules/core/feature_protection.py test dashboard_display
python modules/core/feature_protection.py test version_display
```

## 🚨 DEPLOYMENT GATES

The deployment will be **BLOCKED** if:

1. **Feature Protection Fails**: Any working feature is broken
2. **Commit Format Wrong**: Not in `vX.X.X - Description` format
3. **Version Badge Missing**: Any page without version badge
4. **Constitutional Violation**: Hardcoded countries/crops detected
5. **Environment Variables Missing**: Required keys not set
6. **Tests Failing**: Any test fails

## 📋 Environment Variables Required

These MUST be set in ECS task definition:

```json
{
    "name": "APP_VERSION",
    "value": "3.5.0"
},
{
    "name": "ENVIRONMENT",
    "value": "production"
},
{
    "name": "DB_HOST",
    "value": "farmer-crm-production.cifgmm0mqg5q.us-east-1.rds.amazonaws.com"
},
{
    "name": "DB_NAME",
    "value": "farmer_crm"
},
{
    "name": "DB_USER",
    "value": "postgres"
},
{
    "name": "DB_PASSWORD",
    "value": "from-aws-secrets"
},
{
    "name": "OPENAI_API_KEY",
    "value": "from-aws-secrets"
}
```

## 🔄 Rollback Procedure

If deployment fails:

### Immediate Rollback
```bash
# Revert to previous task definition
aws ecs update-service \
    --cluster ava-olo-production \
    --service ava-olo-agricultural-service \
    --task-definition ava-agricultural-task:PREVIOUS_VERSION
```

### Verify Rollback
```bash
./verify_deployment.sh --version PREVIOUS_VERSION
```

## ⚠️ NEVER DO THIS

1. **Manual deployment** - Always use git push
2. **Skip tests** - All tests must pass
3. **Hardcode versions** - Use environment variables
4. **Direct ECS updates** - Use git workflow
5. **Ignore feature protection** - Never break working features

## 📊 Deployment Checklist

Before EVERY deployment:

- [ ] Feature protection captured
- [ ] All tests passing
- [ ] Version updated correctly
- [ ] Commit message format correct
- [ ] Environment variables set
- [ ] Constitutional compliance verified
- [ ] Documentation updated

After deployment:

- [ ] Version visible on all pages
- [ ] All features still working
- [ ] No errors in CloudWatch logs
- [ ] Farmer registration works
- [ ] Dashboard data displays
- [ ] Google Maps loads

## 🎯 Success Criteria

A successful deployment means:
- ✅ Zero broken features
- ✅ Version badge on every page
- ✅ All endpoints responding
- ✅ Database connections stable
- ✅ No constitutional violations

## 🆘 TROUBLESHOOTING

### Common Deployment Issues

#### ECS Tasks Failing to Start
If ECS tasks fail to start immediately after deployment:

1. **Check CloudWatch Logs**:
   ```bash
   aws logs describe-log-streams --log-group-name /ecs/ava-agricultural --order-by LastEventTime --descending --limit 5
   ```

2. **Look for Secrets Manager Errors**:
   Common error pattern:
   ```
   ResourceInitializationError: unable to pull secrets or registry auth: 
   execution resource retrieval failed: unable to retrieve secret from asm: 
   AccessDeniedException: User: arn:aws:sts::127679825789:assumed-role/ecsTaskExecutionRole/[task] 
   is not authorized to perform: secretsmanager:GetSecretValue
   ```

#### IAM Permission Issues (CRITICAL)
If you see `AccessDeniedException` for secrets:

1. **Verify IAM Policies Attached**:
   ```bash
   aws iam list-attached-role-policies --role-name ecsTaskExecutionRole
   ```
   
   Should show:
   - `AmazonECSTaskExecutionRolePolicy`
   - `AVA-OLO-SecretsManagerAccess`

2. **If Missing AVA-OLO-SecretsManagerAccess**:
   ```bash
   # Check if policy exists
   aws iam get-policy --policy-arn arn:aws:iam::127679825789:policy/AVA-OLO-SecretsManagerAccess
   
   # If exists, attach to role
   aws iam attach-role-policy --role-name ecsTaskExecutionRole --policy-arn arn:aws:iam::127679825789:policy/AVA-OLO-SecretsManagerAccess
   
   # Force new deployment
   aws ecs update-service --cluster ava-olo-production --service agricultural-core --force-new-deployment
   ```

3. **If Policy Doesn't Exist**:
   See `AWS_IAM_REQUIREMENTS.md` for complete setup instructions.

#### Service Health Check Failures
1. **Check ALB Target Groups**:
   ```bash
   aws elbv2 describe-target-health --target-group-arn arn:aws:elasticloadbalancing:us-east-1:127679825789:targetgroup/ava-farmers-tg/d1394d67a8492b35
   ```

2. **Verify Health Endpoint**:
   ```bash
   curl -v http://ava-olo-farmers-alb-82735690.us-east-1.elb.amazonaws.com/health
   ```

#### Database Connection Issues
1. **Test Database Connectivity**:
   ```bash
   # From ECS task or local environment with same credentials
   psql -h farmer-crm-production.cifgmm0mqg5q.us-east-1.rds.amazonaws.com -U [username] -d postgres
   ```

2. **Check Security Groups**:
   Ensure ECS security group can access RDS on port 5432.

#### Version Not Updating
1. **Check ECR Image Tags**:
   ```bash
   aws ecr describe-images --repository-name ava-olo-agricultural-core --region us-east-1
   ```

2. **Verify Task Definition**:
   ```bash
   aws ecs describe-task-definition --task-definition ava-agricultural-task:latest
   ```

### Emergency Recovery
For critical service outages:

1. **Immediate Actions**:
   - Check CloudWatch logs first
   - Verify IAM permissions (most common cause)
   - Check ECS service events
   - Test health endpoints

2. **Historic Issues Resolved**:
   - **2025-07-27**: IAM permissions for Secrets Manager (17+ failed deployments)
   - See `SYSTEM_CHANGELOG.md` for complete incident history

3. **Documentation References**:
   - `AWS_IAM_REQUIREMENTS.md` - Complete IAM setup
   - `SYSTEM_CHANGELOG.md` - Full deployment history
   - `DEPLOYMENT_STATUS_*.md` - Current service status

---

**NO OTHER METHOD IS ALLOWED!**

This standard ensures consistency, reliability, and constitutional compliance across all AVA OLO deployments.