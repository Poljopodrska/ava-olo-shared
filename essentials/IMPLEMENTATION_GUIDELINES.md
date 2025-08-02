# AVA OLO Implementation Guidelines
*For Claude Code to implement features*

## 📌 CRITICAL ABBREVIATION
**TS = TASK SPECIFICATION FOR CLAUDE CODE**
- When user writes "TS", it means they're providing a TASK SPECIFICATION FOR CLAUDE CODE
- These are formal specifications following the template in SPECIFICATION_GUIDELINES.md
- Immediately recognize "TS" as a signal to expect implementation requirements

## 📝 MANDATORY COMMIT STANDARDS

### 🔴 EVERY COMMIT MUST INCLUDE VERSION NUMBER
- Format: `vX.X.X - Description`
- See [COMMIT_MESSAGE_STANDARD.md](./COMMIT_MESSAGE_STANDARD.md) for full details
- Git hooks will REJECT commits without proper format

## 🛡️ MANDATORY DEPLOYMENT PROTECTION

### ⚠️ ZERO TOLERANCE FOR REGRESSION
Before ANY deployment, the following protection gates MUST be passed:

#### Pre-Deployment Checklist
1. **Capture Current Working State**
   ```bash
   cd protection_system
   ./capture_working_state.sh
   ```

2. **Run Protection Gate** (MANDATORY)
   ```bash
   ./pre_deployment_gate.sh
   ```
   **MUST EXIT 0** - deployment rejected if any failures

3. **Document Protection Results**
   Add protection gate status to SYSTEM_CHANGELOG.md

4. **Verify Constitutional Compliance**
   ```bash
   python3 scripts/module_health_monitor.py
   ```

#### Emergency Procedures
If deployment breaks working features:
```bash
./emergency_rollback.sh both [working-state-tag]
./pre_deployment_gate.sh  # Verify rollback success
```

#### MANGO RULE Protection 🥭
Every deployment MUST preserve:
- Yellow debug box (#FFD700) 
- Farmer count display
- Bulgarian mango farmer scenario functionality
- No hardcoded country/crop limitations

#### URL Permanence Protection 🔗
Constitutional Amendment #16 enforcement:
- URLs MUST NEVER change after deployment
- Feature URLs are permanent contracts
- URL structure validation before deployment
- Deployment blocked if URL changes detected

## 🚨 CRITICAL: Git Commit & Push MANDATORY

**EVERY task MUST end with:**
```bash
git add -A
git commit -m "feat: [description]"
git push origin main

# MANDATORY VERSION TAG: v[VERSION]-[feature-name]
git tag v[VERSION]-[feature-name]  # Example: v3.5.5-deployment-verification-tools
git push origin v[VERSION]-[feature-name]
```

**Tasks are INCOMPLETE without git push!**

## 🚨 CRITICAL: Version & Deployment Rules

### ⚠️ INFRASTRUCTURE MANDATE: ECS ONLY
- **ECS is OBSOLETE** - DO NOT deploy or reference ECS
- **All deployments MUST use ECS** infrastructure only
- **Production URL**: http://ava-olo-alb-65365776.us-east-1.elb.amazonaws.com
- **Services**: ava-monitoring-task and ava-agricultural-task on ECS

### Every Deployment MUST:
1. **Target ECS only** (ECS is decommissioned)
2. **Run protection gate** (./pre_deployment_gate.sh MUST PASS)
3. **Increment version** (MAJOR.MINOR.PATCH)
4. **Deploy to ECS and verify** version matches
5. **Update SYSTEM_CHANGELOG.md** with dual timestamps (YYYY-MM-DD HH:MM:SS UTC | HH:MM:SS CET)
6. **Run post-deployment verification** (./pre_deployment_gate.sh again)
7. **Only then** mark task complete

### Version Verification Process
```bash
# 1. Deploy (use forensic naming for critical fixes)
git tag v3.0.0-forensic-cache-bust && git push origin v3.0.0-forensic-cache-bust

# 2. Verify (MANDATORY)
curl https://api.ava-olo.com/version
# Must return: {"version": "3.0.0-forensic-cache-bust"}

# 3. Check ECS task definition version
# Verify ECS service is running latest task definition

# 4. Update diary
# 5. Task complete ✓
```

**NO TASK IS COMPLETE WITHOUT VERSION VERIFICATION!**

## 🚀 MANDATORY DEPLOYMENT STEPS

**EVERY implementation MUST end with:**

1. **Git Commit & Push:**
```bash
git add -A
git commit -m "feat/fix/chore: descriptive message"
git push origin main
```

2. **Verify GitHub Actions:**
   - Check deployment triggered
   - Wait for green checkmark  
   - Verify version updated on ALB

3. **NO TASK IS COMPLETE WITHOUT:**
   - ✅ Code pushed to Git
   - ✅ GitHub Actions successful
   - ✅ Feature accessible on production
   - ✅ SYSTEM_CHANGELOG.md updated

### 🚨 CRITICAL: Task Completion Rules
1. Deploy your version (e.g., v2.1.7)
2. Check deployed version matches YOUR version
3. If mismatch → Task is NOT complete
4. Only report "Task Complete" when:
   - Version endpoint returns YOUR exact version
   - All features work as specified
   - SYSTEM_CHANGELOG.md updated with dual timestamps (UTC | CET)
   
**Example:**
```bash
# You deployed v2.1.7 to ECS
curl http://ava-olo-alb-65365776.us-east-1.elb.amazonaws.com/version
# Returns: {"version": "2.1.4"} → TASK NOT COMPLETE! 
# Returns: {"version": "2.1.7"} → Task complete ✓
```

## Implementation Workflow

### 1. Receive Specification (TS)
- When you see "TS" or "TASK SPECIFICATION FOR CLAUDE CODE", expect formal requirements
- Check MANGO RULE compliance
- Verify constitutional alignment
- Review implementation approach provided
- **TRY to implement as specified first**
- **If challenges arise, communicate clearly:**
  - "I tried X but encountered Y because Z"
  - "The specified approach would cause [specific issue]"
  - "Here's an alternative that achieves the same goal"

### Collaborative Implementation Principle
- Specifications provide concrete guidance to follow
- **If you can't implement as specified, explain WHY:**
  - Technical constraints (e.g., "API doesn't support that")
  - Performance concerns (e.g., "Would cause 30s delays")
  - Security issues (e.g., "Would expose farmer data")
  - Better alternative exists (e.g., "CAVA already handles this")
- Provide evidence for your concerns
- Suggest alternative approaches that achieve the same goal
- Document implementation decisions in code comments

### 2. Code Patterns

#### ❌ NEVER DO THIS:
```python
if country == "Bulgaria":
    return "Use NPK 15-15-15"
```

#### ✅ ALWAYS DO THIS:
```python
# Use CAVA for conversation flows
response = cava_service.process_farmer_query(
    farmer_id=farmer.id,
    message=message,
    context={'crop': crop, 'country': country, 'soil': data}
)
return response

# Or direct LLM for non-conversation tasks
prompt = f"Recommend fertilizer for {crop} in {country} with soil: {data}"
return llm.generate(prompt)
```

### 3. Module Independence
```python
# Each feature = separate module
# No cross-dependencies
# API communication only

class SoilAnalysisModule:
    def __init__(self):
        self.cava = CAVAService()  # For conversation flows
        self.llm = LLMService()    # For direct LLM tasks
        self.db = PostgreSQL()     # Only database
    
    # Module is self-contained
```

### 4. Database Rules
- PostgreSQL ONLY
- Proper migrations
- Encrypt farmer data
- Version in schema
- Check DATABASE_SCHEMA.md for current structure
- NEVER manually edit DATABASE_SCHEMA.md (auto-updated)

### 5. Report Storage Guidelines

#### 📁 Report Organization Rules
All reports MUST be stored in the centralized location with proper naming:

**Mandatory Structure:**
```
/ava-olo-shared/essentials/reports/YYYY-MM-DD/report_XXX_description.md
```

**Examples:**
- `/reports/2025-07-26/report_001_aws_aurora_verification.md`
- `/reports/2025-07-26/report_002_database_analysis.md`
- `/reports/2025-07-26/report_003_deployment_success.md`

**Rules:**
- 📅 **Date Folder**: Always use `YYYY-MM-DD` format
- 🔢 **Sequential Numbering**: Use `report_XXX` with zero-padded numbers
- 📝 **Descriptive Names**: Clear, lowercase, underscore-separated descriptions
- 🚫 **No Root Reports**: Never store reports in module root directories
- 📚 **Index Update**: Update `/reports/README.md` when adding new reports

**Bulgarian Mango Test for Reports:** 
"Can a Bulgarian mango farmer easily find and understand this report's purpose from its filename and location?"

### 6. Version Naming Standards

#### 🏷️ Git Tag Format (MANDATORY)
All git tags MUST follow this format:
```
v[VERSION]-[description]
```

**Examples:**
- ✅ `v3.2.0-schema-button-aurora`
- ✅ `v2.5.4-db-fixed`
- ✅ `v3.3.0-schema-viewer`
- ❌ `backup-20250717-210831` (no version prefix)
- ❌ `pre-web-interface-v1.0` (version not at start)

**Rules:**
- 🔢 **Version First**: Always start with `v` followed by semantic version
- 📝 **Descriptive Suffix**: Brief description after hyphen
- 🚫 **No Spaces**: Use hyphens for separation
- 📊 **Semantic Versioning**: Major.Minor.Patch format

### 7. Changelog Maintenance Rules

#### 📋 SYSTEM_CHANGELOG.md Updates (MANDATORY)
Every deployment MUST have a changelog entry with:

**Required Format:**
```markdown
## [YYYY-MM-DD] Feature Description - v[VERSION]
**Status**: DEPLOYED ✅ / READY FOR DEPLOYMENT ✅
**Service**: [Service-name] (ECS)
**Version**: v[VERSION]
**Feature**: [Brief Description]

**Changes**:
- 📊 **Feature 1**: Description
- 🔧 **Feature 2**: Description

**Technical Updates**:
- File changes
- New endpoints
- Configuration updates
```

**Rules:**
- 📅 **Timestamp**: Include both UTC and CET when possible
- ✅ **Status**: Clear deployment status indicator  
- 🏷️ **Version Match**: Version must match git tag exactly
- 📝 **Complete**: Never leave "TODO" or incomplete entries

### 8. Version Management Rules

#### ❌ NO HARDCODING OF VERSIONS - EVER!
**Problem**: Hardcoded versions cause deployments to always show the same version, breaking version tracking and deployment verification.

**📚 See [BEST_PRACTICES.md](./BEST_PRACTICES.md) for complete deployment guidelines and real-world scenarios**

**Examples of what NOT to do:**
```python
# ❌ NEVER DO THIS
VERSION = "2.1.4"  # Hardcoded - will never update!

# ❌ NEVER DO THIS
def get_version():
    return "2.1.4"  # Hardcoded!

# ❌ NEVER DO THIS
response = {"version": "2.1.4", "status": "ok"}  # Hardcoded!
```

**✅ CORRECT Approach:**
```python
# ✅ Always use dynamic version from config/environment
from config import VERSION  # Imported from central config

# ✅ Or from environment variable
VERSION = os.getenv('APP_VERSION', 'development')

# ✅ Or from a version file that gets updated
with open('version.txt', 'r') as f:
    VERSION = f.read().strip()

# ✅ Or from git tags
VERSION = subprocess.check_output(['git', 'describe', '--tags']).decode().strip()
```

**Version Update Process:**
1. Update version in ONE central location (config.py, version.txt, or environment)
2. All modules import/read from that single source
3. Deploy scripts update the central version
4. Verification confirms the new version is live

### 6. Testing Requirements
```python
def test_mango_rule():
    # Every feature must pass
    result = feature.process(
        crop="mango",
        country="Bulgaria",
        language="bg"
    )
    assert result.success
```

## Deployment Checklist

- [ ] All tests pass
- [ ] Constitutional compliance ≥90%
- [ ] Version incremented (use forensic naming if critical)
- [ ] Code follows LLM-first
- [ ] Module independent
- [ ] Privacy maintained
- [ ] Run deployment verification script (creates manifest)
- [ ] Deployed to ECS (ECS is OBSOLETE)
- [ ] Version endpoint verified on ALB
- [ ] Deployment integrity checked (/api/deployment/verify)
- [ ] Visual health confirmed (/api/deployment/health shows GREEN)
- [ ] ECS task definition updated and running
- [ ] SYSTEM_CHANGELOG.md updated with dual timestamps (YYYY-MM-DD HH:MM:SS UTC | HH:MM:SS CET)
- [ ] Rollback ready

## Error Handling

### Deployment Failure:
1. DO NOT mark complete
2. Rollback to previous
3. Document in SYSTEM_CHANGELOG.md
4. Fix and re-deploy with new version

### Version Mismatch:
1. Investigation required
2. Check ECS task definition version
3. Update ECS service to latest task
4. Never proceed if versions don't match
5. Re-deploy with incremented version (forensic naming for critical)

### Partial Deployment (NEW):
1. Check /api/deployment/verify endpoint
2. If "valid": false, AWS did partial deployment
3. Look for specific mismatches in response
4. Update DEPLOYMENT_TIMESTAMP to force rebuild
5. Regenerate manifest and redeploy
6. Visual confirmation: Check for yellow debug box (monitoring)
7. Never mark task complete without GREEN health status

## UI/UX Requirements

### Version Visibility (MANDATORY)
- Version number MUST appear on every page
- Position: Top right corner
- Format: "v{VERSION}" (e.g., "v2.1.7")
- Style: Muted text color (#666 or similar)
- Purpose: Farmers/support can verify latest features
- Implementation example:
```html
<div class="version-display">v2.1.7</div>
<!-- CSS: position: fixed; top: 10px; right: 10px; -->
```

## Quick Implementation Example

```python
# Feature: Soil Test Interpreter v2.1.0

# 1. Module structure
soil_module/
├── __init__.py
├── interpreter.py
├── routes.py
└── tests.py

# 2. LLM-first implementation
def interpret_soil_test(lab_data, farmer_context):
    prompt = build_soil_prompt(lab_data, farmer_context)
    interpretation = llm.generate(prompt)
    
    # 3. Store with privacy
    encrypted = encrypt_data(interpretation)
    db.store(farmer_context.id, encrypted)
    
    # 4. Return with version
    return {
        "interpretation": interpretation,
        "version": "2.1.0",
        "language": farmer_context.language
    }

# 5. Deploy and verify
# git tag v2.1.0
# deploy_to_aws()
# verify_version("2.1.0")
# update_diary()
```

## Autonomous Deployment Instructions

When given FULL AUTONOMY for urgent deployment fixes:

### 1. Take Complete Ownership
```bash
# You are responsible for EVERYTHING:
# - Diagnosis
# - Implementation
# - Deployment
# - Verification
# - Documentation
```

### 2. Critical ECS Deployment Fixes
When fixing container/configuration issues:
```python
# 1. Identify wrong import (e.g., main.py)
# OLD: from api_gateway_minimal import app
# NEW: from api_gateway_constitutional_ui import app

# 2. Update version in affected files
VERSION = "3.1.1-main-py-fix"

# 3. Force ECS task update if needed
# Update task definition and redeploy service
```

### 3. Deployment Verification Protocol
```bash
# Deploy
git add -A && git commit -m "fix: v3.1.1-main-py-fix"
git push origin main

# Deploy to ECS
aws ecs update-service --cluster ava-olo-production --service [service-name] --force-new-deployment

# Verify
curl http://ava-olo-alb-65365776.us-east-1.elb.amazonaws.com/version
curl http://ava-olo-alb-65365776.us-east-1.elb.amazonaws.com/  # Check UI loads

# Check ECS service status
aws ecs describe-services --cluster ava-olo-production --services [service-name]
```

### 4. Success Criteria Checklist
- [ ] Root cause identified
- [ ] Fix implemented and committed
- [ ] Version incremented with forensic naming
- [ ] AWS deployment triggered
- [ ] Service URL verified working
- [ ] Constitutional compliance confirmed
- [ ] SYSTEM_CHANGELOG.md updated with dual timestamps (YYYY-MM-DD HH:MM:SS UTC | HH:MM:SS CET)
- [ ] Farmer can use feature (MANGO RULE)

### 5. Emergency Escalation
If ECS deployment fails:
1. Check ECS task logs in CloudWatch
2. Verify task definition is valid
3. Check ALB target group health
4. Document exact issue in SYSTEM_CHANGELOG.md
5. Roll back to previous task definition if needed

## AWS SERVICE CREATION RULES

### 🚨 CRITICAL: AWS Service Creation/Deletion Approval
- **MANDATORY**: Admin written approval required BEFORE creating OR deleting any AWS service
- **NO AUTONOMOUS CHANGES**: Claude Code must NEVER create/delete AWS services independently
- **Creation Approval Format**:
  ```
  APPROVED: Create [service-name] for [specific-purpose]
  Budget: $[amount]/month
  Justification: [why existing services insufficient]
  Signed: [Admin name/date]
  ```
- **Deletion Approval Format**:
  ```
  APPROVED: Delete [service-name]
  Data Backup: [confirmation of data backup/migration]
  Cost Savings: $[amount]/month
  Impact Analysis: [what stops working]
  Signed: [Admin name/date]
  ```
- **NOT VALID**: Simple "yes", "ok", "delete it" without details

### When Service Changes Need Approval
**Creation:**
- ✅ New ECS services/tasks
- ✅ New RDS instances
- ✅ New Lambda functions
- ✅ New S3 buckets
- ✅ ANY service that incurs costs

**Deletion:**
- ✅ ANY service deletion (even if saving costs)
- ✅ Database deletions (EXTREME CAUTION)
- ✅ Storage deletions (data loss risk)
- ✅ Inactive/unused services

### Use Existing Services First
- Check if existing services can handle the feature
- Document why new service is necessary
- Consider cost implications
- Propose alternatives before requesting new service

## DEPLOYMENT CONFIGURATION CHANGES

### Container/Task Definition Change Tracking Rule
- **MANDATORY**: All ECS task definition modifications must be explicitly documented in SYSTEM_CHANGELOG.md
- **Required fields**: 
  - What changed (build/run/env/network)
  - Why the infrastructure change was needed
  - Impact assessment (breaking/non-breaking)
  - Rollback plan if deployment fails

### When YAML Changes Are Needed
- ✅ New environment variables
- ✅ Resource scaling (CPU/memory)
- ✅ Runtime version updates
- ✅ Build process modifications
- ✅ Network configuration changes
- ✅ Health check adjustments

### When YAML Should NOT Change
- ❌ Adding business features
- ❌ UI/UX improvements  
- ❌ Bug fixes
- ❌ Database schema changes
- ❌ Code-only updates
- ❌ Version bumps alone

### ECS Task Definition Change Documentation Example
```markdown
## Version X.X.X - YYYY-MM-DD HH:MM:SS UTC | HH:MM:SS CET
**Infrastructure Change**: Modified ECS task definition
**What Changed**: 
- Increased CPU from 1 to 2 vCPUs
- Added DB_CONNECTION_POOL_SIZE=20 env variable
**Why**: Performance degradation with 50+ concurrent farmers
**Impact**: Non-breaking - resource increase only
**Rollback**: Revert to previous CPU/env settings if issues
```

## Database Schema Documentation
- **DATABASE_SCHEMA.md** in /essentials/ is auto-updated every 15 minutes
- ALWAYS consult before writing database queries
- Contains current tables, columns, types, constraints
- Schema changes appear automatically within 15 minutes
- For immediate schema needs, query information_schema directly

## Bulletproof Deployment System (v2.2.5+)

### Purpose
Prevents AWS partial deployments where only VERSION updates but functions don't deploy.

### Key Components
1. **deployment_manager.py** - Generates SHA-256 manifest of all files
2. **DEPLOYMENT_TIMESTAMP** - Forces AWS rebuild on every deploy
3. **/api/deployment/verify** - Checks if deployment matches manifest
4. **/api/deployment/health** - Visual GREEN/RED status box

### Deployment Process
```bash
# 1. Update timestamp (automated in deploy script)
DEPLOYMENT_TIMESTAMP = '20250719210000'

# 2. Generate manifest
python3 deployment_manager.py

# 3. Deploy and wait 90 seconds
git push && sleep 90

# 4. Verify deployment
curl https://service-url/api/deployment/verify
# Must return: {"valid": true}

# 5. Visual check
# Monitoring: Yellow debug box with data
# Agricultural: GREEN health status
```

### Visual Indicators
- **Monitoring Dashboard**: Unmissable yellow box with red border showing real data
- **Agricultural Core**: GREEN/RED health box at /api/deployment/health
- **Both Services**: Version with BUILD_ID hash for verification

### When Deployment Fails
- manifest shows mismatched files
- No yellow debug box on dashboard
- Health endpoint shows RED
- Fix: Update DEPLOYMENT_TIMESTAMP and redeploy

## Report Creation Rules

### When to Create Reports
Create a report in `/essentials/reports/YYYY-MM-DD/` when:
- 🔍 **Investigations**: Root cause analysis, debugging complex issues
- 🏗️ **Infrastructure Changes**: Migration status, architectural decisions
- 📊 **Performance Analysis**: Bottlenecks, optimization findings
- 🚨 **Incidents**: Production issues, post-mortems
- 💰 **Cost Analysis**: AWS resource optimization
- 🔒 **Security Audits**: Vulnerability assessments, compliance checks

### Report Format
```markdown
# Report Title
**Date**: YYYY-MM-DD HH:MM:SS UTC | HH:MM:SS CET
**Type**: Investigation/Migration/Performance/Incident/Cost/Security
**Author**: Claude Code
**Related Services**: [service names]

## Executive Summary
[2-3 sentence summary]

## Details
[Main content]

## Findings
[Key discoveries]

## Recommendations
[Actionable next steps]

## References
- Related code: [file paths]
- Related logs: [log locations]
- Related issues: [issue numbers]
```

### Report Workflow
1. **Create Report File**:
   ```bash
   # Format: report_XXX_descriptive_name.md
   # XXX = sequential number for that day (001, 002, etc.)
   reports/2025-07-20/report_001_ecs_migration_analysis.md
   ```

2. **Update SYSTEM_CHANGELOG.md**:
   ```markdown
   ## YYYY-MM-DD HH:MM:SS UTC | HH:MM:SS CET - Title [🔍 INVESTIGATION]
   **Report**: reports/YYYY-MM-DD/report_XXX_name.md
   **Summary**: Brief description of findings
   ```

3. **Reference in Code Comments** (if applicable):
   ```python
   # See detailed analysis: reports/2025-07-20/report_001_ecs_migration_analysis.md
   ```

### Report Storage Rules
- Reports are **permanent documentation** - never delete
- Organize by date: `/reports/YYYY-MM-DD/`
- Sequential numbering per day: 001, 002, 003...
- Use descriptive names with underscores
- Always create in markdown format (.md)

## Remember
- LLM makes decisions, not code
- CAVA handles all conversation flows
- Every deployment needs version
- Module independence is key
- MANGO RULE guides everything
- Task incomplete until verified
- FULL AUTONOMY = Complete responsibility
- DATABASE_SCHEMA.md is your source of truth
- **Constructive dialogue is encouraged - explain implementation challenges**
- **Provide evidence when suggesting alternatives**
- **Deployment verification is MANDATORY - no exceptions**
- **Partial deployments waste 12+ hours - verify everything**
- **Reports document important findings - create them proactively**