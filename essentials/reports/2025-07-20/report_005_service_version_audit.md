# Service Version and Location Audit Report
Date: 2025-07-20 13:25:00 UTC

## Executive Summary
This report provides a complete inventory of all AVA OLO services running across App Runner and ECS, their versions, and recommendations for consolidation.

## Service Inventory

### Monitoring Dashboard Service
| Location | Version | URL | Status | Features Working | Last Deploy |
|----------|---------|-----|--------|------------------|-------------|
| App Runner | v2.2.6-restore-0aeff93f | https://bcibj8ws3x.us-east-1.awsapprunner.com | RUNNING | Yellow box ✓, 16 farmers ✓ | 2025-07-20 11:29:00 |
| ECS | v2.3.0-ecs-ready-a3d8affb | http://ava-olo-alb-65365776.us-east-1.elb.amazonaws.com/business-dashboard | RUNNING | Yellow box ✓, 16 farmers ✓ | 2025-07-19 21:24:20 |

### Agricultural Core Service  
| Location | Version | URL | Status | Features Working | Last Deploy |
|----------|---------|-----|--------|------------------|-------------|
| App Runner | v3.3.1-restore-d43734d6 | https://ujvej9snpp.us-east-1.awsapprunner.com | RUNNING | CAVA registration ✓ | 2025-07-20 11:29:00 |
| ECS | Unknown (using :latest tag) | http://ava-olo-alb-65365776.us-east-1.elb.amazonaws.com/ | FAILING | Service not found | N/A |

## Version History Reference
- **Monitoring Dashboard**:
  - Last stable tag: v2.2.6-restore
  - Current App Runner: v2.2.6-restore (matches tag) ✓
  - Current ECS: v2.3.0-ecs-ready (newer but not tagged)
  - Latest commit: 494a2c7 (Dockerfile fix for ECS)

- **Agricultural Core**:
  - Last stable tag: v3.3.1-restore  
  - Current App Runner: v3.3.1-restore (matches tag) ✓
  - Current ECS: Not properly deployed
  - Latest commit: 619d96c (restore v3.3.0 working registration)

## Infrastructure Details

### App Runner Configuration
Both services configured with:
- Auto-deployment from GitHub main branch
- 1 vCPU, 2 GB memory
- Build: `pip install -r requirements.txt`
- Monitoring uses VPC connector, Agricultural uses default egress

### ECS Configuration
- Cluster: ava-olo-production
- Both services attempting to run on Fargate
- ALB routing:
  - `/business-dashboard` → monitoring service (working)
  - `/` → agricultural service (failing)
- Issues: Agricultural service has health check failures

## Key Findings

1. **Duplication**: Monitoring dashboard running successfully in BOTH App Runner and ECS
2. **Working Versions**: 
   - App Runner has the correct tagged versions (v2.2.6-restore, v3.3.1-restore)
   - ECS monitoring works but uses untagged version
3. **Failed Migration**: Agricultural core exists in ECS but is not functioning
4. **Resource Waste**: Running duplicate monitoring services costs extra
5. **Version Mismatch**: ECS using `:latest` tags instead of specific versions

## Recommendations

### Immediate Actions (No Changes, Just Decisions)
1. **Choose deployment platform**: Either App Runner OR ECS, not both
2. **If choosing App Runner**: Delete ECS services to save costs
3. **If choosing ECS**: Need to properly deploy agricultural core first

### Recommended Approach
Based on the audit, I recommend **staying with App Runner** because:
- ✓ Both services already working perfectly
- ✓ Auto-deployment from GitHub configured
- ✓ Simpler infrastructure (no ALB, target groups, task definitions)
- ✓ Lower operational complexity
- ✓ Currently serving production traffic successfully

### Alternative: Complete ECS Migration
If you prefer ECS:
1. Fix agricultural core deployment (currently failing health checks)
2. Update task definitions to use specific version tags
3. Ensure both services healthy on ECS
4. Then remove App Runner services

## Cost Impact
Currently paying for:
- 2 App Runner services (working)
- 2 ECS services (1 working, 1 failing)
- 1 ALB
- Double the necessary resources

## Next Steps Decision Matrix

| Option | Pros | Cons | Effort |
|--------|------|------|--------|
| Stay with App Runner | Already working, Simple | Not using ECS investment | Low (just cleanup) |
| Move to ECS | More control, ALB features | Agricultural not working | High (fix deployment) |
| Keep Both | Redundancy | Double cost, Complexity | None (status quo) |

## Conclusion
The system is currently running duplicate services. App Runner has the working, properly tagged versions. ECS has a partially working deployment. A decision is needed on which platform to standardize on before making any changes.