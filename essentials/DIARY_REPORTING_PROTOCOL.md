# 📔 AVA OLO DIARY REPORTING PROTOCOL
*Mandatory Daily Development Documentation System*

## 🚨 CRITICAL: This Protocol is MANDATORY

Starting from **2025-08-16**, all development work MUST include diary reports. This is not optional.

---

## 📋 REPORTING REQUIREMENTS

### When to Write Reports (MANDATORY):

1. **Daily Summary Report** - At the end of each working day
2. **Deployment Report** - Before AND after each deployment
3. **Error Investigation Report** - When any error occurs
4. **Feature Implementation Report** - When adding new features
5. **Bug Fix Report** - When fixing any bug
6. **Configuration Change Report** - When changing any configuration

### Report Frequency Rules:

- **Minimum**: 1 report per working session
- **Maximum**: No limit (more documentation is always better)
- **Critical Changes**: IMMEDIATE report required

---

## 📝 REPORT TEMPLATE (STRICT FORMAT)

```markdown
# Report XXX: [Descriptive Title]

**Date**: YYYY-MM-DD HH:MM:SS UTC | HH:MM:SS CET  
**Author**: Claude Code / [Developer Name]  
**Type**: [Daily|Deployment|Investigation|Feature|BugFix|Configuration|Emergency]  
**Version**: [Current version being worked on]  
**Priority**: [Low|Medium|High|Critical]  

## 📊 Summary
[2-3 sentences maximum - what happened today/in this session]

## 🔄 Work Performed
- [ ] Task 1 completed
- [ ] Task 2 completed  
- [ ] Task 3 in progress
- [ ] Task 4 blocked

## 📈 Progress Metrics
- Lines of Code: Added [X] / Modified [Y] / Deleted [Z]
- Files Changed: [Number]
- Tests: Passed [X] / Failed [Y]
- Deployment Status: [Not Started|In Progress|Completed|Failed]

## 🐛 Issues Encountered
1. **Issue**: [Description]
   - **Severity**: [Low|Medium|High|Critical]
   - **Resolution**: [Fixed|Workaround|Pending]
   - **Time Spent**: [X hours]

## 💡 Decisions Made
- **Decision 1**: [What was decided and why]
- **Rationale**: [Reasoning behind the decision]
- **Impact**: [How this affects the system]

## 🔮 Next Steps
1. [What needs to be done next]
2. [Priority tasks for next session]
3. [Blockers that need resolution]

## 📎 References
- Commits: [List commit hashes]
- Files Modified: [List key files]
- Related Reports: [Link to related reports]
- External Docs: [Any external references]

## ✅ Compliance Check
- [ ] Report follows template format
- [ ] All sections completed
- [ ] Added to SYSTEM_CHANGELOG.md
- [ ] Saved in correct date folder
- [ ] Report number is sequential
```

---

## 🗂️ FILE ORGANIZATION RULES

### Directory Structure:
```
/ava-olo-shared/essentials/reports/
├── YYYY-MM-DD/
│   ├── report_001_[description].md
│   ├── report_002_[description].md
│   └── DAILY_SUMMARY.md
```

### Naming Convention:
- Format: `report_XXX_descriptive_name.md`
- XXX: Three-digit sequential number (001, 002, 003...)
- descriptive_name: lowercase with underscores
- Daily summary: `DAILY_SUMMARY.md` (one per day)

---

## 🔐 ENFORCEMENT MECHANISMS

### 1. Pre-Commit Hook
Every commit will check:
- Is there a report for today?
- Does the report reference this commit?
- Is the report properly formatted?

### 2. Deployment Gate
Deployments will be BLOCKED unless:
- Deployment report exists
- Version matches in report
- All compliance checks pass

### 3. Daily Reminder
At the start of each session:
- System checks for yesterday's summary
- Prompts for today's first report
- Shows incomplete reports

---

## 📊 REPORT TYPES EXPLAINED

### 1. Daily Summary Report
- **When**: End of each working day
- **Purpose**: Summarize all work done
- **Required Sections**: All

### 2. Deployment Report  
- **When**: Before and after deployment
- **Purpose**: Document deployment process
- **Extra Fields**: 
  - Previous Version
  - New Version
  - Rollback Plan
  - Verification Steps

### 3. Error Investigation Report
- **When**: Any error occurs
- **Purpose**: Document root cause and fix
- **Extra Fields**:
  - Error Message
  - Stack Trace
  - Root Cause
  - Prevention Measures

### 4. Feature Implementation Report
- **When**: New feature added
- **Purpose**: Document design decisions
- **Extra Fields**:
  - Feature Specification
  - Implementation Approach
  - Testing Strategy
  - User Impact

### 5. Bug Fix Report
- **When**: Bug fixed
- **Purpose**: Document bug and solution
- **Extra Fields**:
  - Bug Description
  - Steps to Reproduce
  - Fix Applied
  - Regression Testing

### 6. Configuration Change Report
- **When**: Any config changed
- **Purpose**: Track configuration evolution
- **Extra Fields**:
  - Old Configuration
  - New Configuration
  - Reason for Change
  - Rollback Instructions

---

## 🏆 COMPLIANCE SCORING

Each report is scored on:
- **Completeness** (25%): All sections filled
- **Clarity** (25%): Clear, concise writing
- **Accuracy** (25%): Correct information
- **Timeliness** (25%): Submitted on time

### Score Thresholds:
- 90-100%: Excellent 🟢
- 70-89%: Good 🟡
- 50-69%: Needs Improvement 🟠
- Below 50%: Non-Compliant 🔴

---

## 🚀 INTEGRATION WITH SYSTEM_CHANGELOG

Every report MUST have an entry in SYSTEM_CHANGELOG.md:

```markdown
## YYYY-MM-DD HH:MM:SS UTC | HH:MM:SS CET - [Title] [📔 REPORT]
**Report**: reports/YYYY-MM-DD/report_XXX_[name].md
**Type**: [Report Type]
**Summary**: [One line summary]
**Version**: [Version working on]
```

---

## 🎯 BENEFITS OF DIARY REPORTING

1. **Accountability**: Clear record of all work
2. **Knowledge Transfer**: Easy onboarding for new developers
3. **Debugging**: Historical context for issues
4. **Compliance**: Audit trail for all changes
5. **Progress Tracking**: Measure velocity and productivity
6. **Decision History**: Understand why choices were made

---

## ⚠️ NON-COMPLIANCE CONSEQUENCES

Failure to maintain diary reports will result in:
1. Commit rejection
2. Deployment blocking
3. Automated alerts
4. Compliance score reduction
5. Required remediation reports

---

## 📚 EXAMPLES OF GOOD REPORTS

See these exemplary reports:
- `/reports/2025-07-26/report_004_deployment_success.md`
- `/reports/2025-07-20/report_005_service_version_audit.md`
- `/reports/2025-07-21/report_002_ecs_deployment_visibility_crisis.md`

---

## 🔄 PROTOCOL VERSION

- **Version**: 1.0.0
- **Effective Date**: 2025-08-16
- **Last Updated**: 2025-08-16
- **Review Schedule**: Monthly

---

*"Documentation is not optional - it's the foundation of professional development"*