# ECS Deployment Visibility Crisis Investigation Report
Date: 2025-07-21
Investigator: Claude Code
Severity: CRITICAL
Status: ROOT CAUSE IDENTIFIED

## Executive Summary
Deployments are failing at multiple levels: CodeBuild builds fail, ECS deployments are stuck with 53+ failed tasks, and both services have deployments perpetually IN_PROGRESS. The v3.3.2 changes never made it to production because the entire deployment pipeline is broken.

## Critical Findings

### 1. Multiple ALB Confusion
- **ava-olo-farmers-alb**: Running v3.3.1-whatsapp-ui (July 20)
- **ava-olo-internal-alb**: Running v2.4.0-multi-dashboard (July 20)
- **ava-olo-alb**: Decommissioned/unreachable
- **Issue**: Different services on different ALBs with different versions

### 2. ECS Services Deployment Crisis
```
Agricultural-Core Service:
- Status: ACTIVE but deployment STUCK
- Failed Tasks: 53 (and counting)
- Current Deployment: IN_PROGRESS since July 20
- Running: Old task definition (ava-agricultural-task:5)
- Trying to deploy: ava-agricultural-task:6

Monitoring-Dashboards Service:
- Status: ACTIVE but deployment STUCK
- Failed Tasks: 27 (and counting)
- TWO deployments IN_PROGRESS simultaneously
- Both trying to deploy same task definition (ava-monitoring-task:9)
```

### 3. ECR Image Mismatch
```
Latest Images in ECR:
- agricultural-core: Tagged "latest" at 22:06:41 July 20
- monitoring-dashboards: NO "latest" tag, newest is v2.6.0-security
- v3.3.2 images: NEVER BUILT OR PUSHED
```

### 4. CodeBuild Failures
```
Manual Build (be9277f5-f6e7-4b6b-aaf2-355833b5fca6):
- Status: FAILED
- Error: docker push failed
- Last successful build: July 20 at 15:58
```

### 5. Task Launch Failures Pattern
```
Event Timeline (agricultural-core):
08:44 - Started task 646720344e174734b459628af8e3ea11
08:29 - "unable to consistently start tasks successfully"
08:16 - Started task 082cbf1123f3492bacdc56d6c19908fd
08:03 - "unable to consistently start tasks successfully"
07:50 - Started task a3e367c550ca412a98e5f5481833488e

Pattern: Tasks start, fail within ~13 minutes, retry endlessly
```

## Root Cause Analysis

### Primary Issues:
1. **ECS Task Definition Problem**: Task definitions likely have configuration issues causing immediate crashes
2. **No "latest" Tag Management**: ECR images don't have proper version tags
3. **Stuck Deployments**: ECS can't complete deployments due to failing tasks
4. **CodeBuild Permission Issues**: Docker push failing suggests ECR permission problems
5. **No Circuit Breaker**: Services keep trying failed deployments indefinitely

### Why Changes Aren't Visible:
- v3.3.2 was never successfully built or pushed to ECR
- ECS is running old containers because new ones fail to start
- Deployments are stuck in retry loops with failing tasks
- The "latest" tag points to July 20 images, not recent changes

## Evidence of Version Mismatches

```bash
# What's requested vs what's running:
Requested: v3.3.2 (from Git commits)
ECR Latest: July 20 builds (no v3.3.2 tag)
Running on farmers ALB: v3.3.1-whatsapp-ui
Running on internal ALB: v2.4.0-multi-dashboard
```

## Immediate Actions Required

### 1. Stop the Failing Deployments
```bash
# Force services to stop retrying
aws ecs update-service --cluster ava-olo-production \
  --service agricultural-core \
  --desired-count 0 --region us-east-1

aws ecs update-service --cluster ava-olo-production \
  --service monitoring-dashboards \
  --desired-count 0 --region us-east-1
```

### 2. Fix Task Definitions
- Check container health checks (likely too aggressive)
- Verify memory/CPU allocations
- Check environment variables
- Review startup commands

### 3. Fix CodeBuild
```bash
# Check ECR permissions for CodeBuild role
# Ensure docker login succeeds
# Fix IMAGE_TAG environment variable
```

### 4. Proper Version Management
```bash
# Tag images with actual versions, not just "latest"
docker tag image:latest $ECR_URI:v3.3.2
docker tag image:latest $ECR_URI:latest
```

## Comparison with ECS Issues
Similar pattern identified:
- ECS: Python bytecode caching prevented updates
- ECS: Failed deployments prevent updates
- Both: Changes deploy but old version keeps running
- Root similarity: Deployment completes but wrong code serves traffic

## Long-term Fix Recommendations

1. **Implement Deployment Circuit Breaker**
   ```bash
   aws ecs update-service --cluster ava-olo-production \
     --service agricultural-core \
     --deployment-configuration '{
       "deploymentCircuitBreaker": {
         "enable": true,
         "rollback": true
       }
     }'
   ```

2. **Proper Version Tagging Pipeline**
   - Never rely on "latest" tag alone
   - Tag with version AND latest
   - Include git commit hash in tags

3. **Health Check Configuration**
   - Increase initial delay (give containers time to start)
   - Adjust timeout and interval
   - Make health endpoints lightweight

4. **Monitoring and Alerts**
   - Alert on stuck deployments
   - Monitor failed task count
   - Track deployment duration

5. **Deployment Verification**
   - Add /deployment-canary endpoint
   - Check actual running version post-deployment
   - Automated rollback on version mismatch

## Deployment State Diagram
```
Git Push (v3.3.2) 
    ↓
GitHub Actions ✓
    ↓
CodeBuild Triggered ✓
    ↓
Docker Build (Success?)
    ↓
Docker Push ✗ FAILED
    ↓
ECR (No v3.3.2 image)
    ↓
ECS Update Service
    ↓
Task Definition (Revision 6)
    ↓
Launch Tasks ✗ FAILING (53+ times)
    ↓
Old Container Keeps Running (v3.3.1)
    ↓
ALB Shows Old Version
```

## Conclusion
The deployment pipeline is completely broken at multiple levels. The immediate issue is not caching but rather:
1. CodeBuild can't push images to ECR
2. ECS tasks fail to start with new task definitions
3. Services are stuck in endless retry loops
4. No proper version tagging strategy

The Bulgarian mango farmer sees old versions because new deployments never complete successfully. This requires immediate intervention to unstick the deployments and fix the underlying infrastructure issues.

## UPDATE: Root Cause Found
Task failure reason discovered:
```
ResourceInitializationError: unable to pull secrets or registry auth: 
execution resource retrieval failed: unable to retrieve secret from asm: 
service call has been retried 1 time(s): invalid character '!' in string escape code
```

The issue is with AWS Secrets Manager (ASM) - there's an invalid character '!' in a secret that's preventing ECS from pulling container images.

## Next Steps
1. Fix the AWS Secrets Manager secret with invalid character
2. Stop failing deployments immediately
3. Fix CodeBuild ECR permissions
4. Implement proper version tagging
5. Add deployment circuit breakers
6. Create deployment canary endpoint for verification