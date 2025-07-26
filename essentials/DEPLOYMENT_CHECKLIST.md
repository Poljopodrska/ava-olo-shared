# AVA OLO Deployment Checklist
**Constitutional Compliance Required Before ANY Deployment**

## 🥭 MANGO RULE Pre-Flight Check
> **Critical Question**: "Would this work for a Bulgarian mango farmer?"
- [ ] No hardcoded country/crop logic
- [ ] Universal database approach (PostgreSQL only)
- [ ] LLM/CAVA handles variations, not code
- [ ] Functionality works regardless of location

## 📋 Pre-Deployment Checklist

### 1. Code Quality & Testing
- [ ] All tests pass locally
- [ ] No console errors in browser
- [ ] Database migrations tested
- [ ] API endpoints return expected responses
- [ ] MANGO RULE compliance verified

### 2. Documentation Updates
- [ ] **SYSTEM_CHANGELOG.md updated** with:
  - [ ] Correct version number (v[X.Y.Z]-[description])
  - [ ] Deployment status (READY FOR DEPLOYMENT ✅)
  - [ ] Complete feature description
  - [ ] Technical changes listed
  - [ ] No TODO/TBD entries
- [ ] Version bumped in config files
- [ ] README.md updated if needed

### 3. File Organization
- [ ] **Reports in correct location**: `/essentials/reports/YYYY-MM-DD/report_XXX_description.md`
- [ ] No reports in module root directories
- [ ] All new reports follow naming convention
- [ ] No temporary/debug files committed

### 4. Version Management
- [ ] **Git tag created**: `v[VERSION]-[description]` format
- [ ] Tag matches SYSTEM_CHANGELOG.md version exactly
- [ ] No hardcoded versions in code
- [ ] Version endpoint will return correct version

### 5. Git & Repository
- [ ] All changes committed and pushed
- [ ] Git tags pushed (`git push origin --tags`)
- [ ] Branch protection rules respected
- [ ] No merge conflicts

## 🚀 Deployment Process

### Step 1: Pre-Deployment Validation
```bash
# Run compliance check
./.pre-commit-compliance.sh

# Verify version consistency
git tag -l | tail -5
grep "## \[$(date +%Y-%m-%d)\]" SYSTEM_CHANGELOG.md
```

### Step 2: Trigger Deployment
```bash
# Commit final changes
git add -A
git commit -m "feat: [DESCRIPTION] v[VERSION]

🤖 Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>"

# Create and push tag
git tag v[VERSION]-[description]
git push origin main --tags
```

### Step 3: Verify Deployment
- [ ] GitHub Actions successful
- [ ] Service deployed to ECS
- [ ] Version endpoint returns correct version
- [ ] Key features working in production
- [ ] No error logs in CloudWatch

### Step 4: Post-Deployment
- [ ] Update changelog status to "DEPLOYED ✅"
- [ ] Test critical user flows
- [ ] Monitor for 15 minutes
- [ ] Document any issues found

## 🆘 Emergency Rollback

If deployment fails or breaks functionality:

```bash
# 1. Identify last working version
git tag -l | grep v | sort -V | tail -10

# 2. Rollback to working version
git checkout [WORKING_TAG]
git push origin main --force

# 3. Update changelog
# Mark failed deployment in SYSTEM_CHANGELOG.md
# Document rollback reason and resolution plan

# 4. Verify rollback success
curl [PRODUCTION_URL]/version
```

## 🎯 Success Criteria

Deployment is considered successful when:
- [ ] Version endpoint returns deployed version
- [ ] All primary user flows functional
- [ ] No increase in error rates
- [ ] Bulgarian mango farmer can use the system ✅
- [ ] SYSTEM_CHANGELOG.md marked as "DEPLOYED ✅"

## 🔍 Common Issues & Solutions

### Issue: Wrong Version Displayed
**Cause**: Hardcoded version in code  
**Fix**: Use environment variables or dynamic version loading  
**Prevention**: Run `.pre-commit-compliance.sh` before commit

### Issue: Reports in Wrong Location
**Cause**: Created in module root instead of `/essentials/reports/`  
**Fix**: Move to `/essentials/reports/YYYY-MM-DD/report_XXX_description.md`  
**Prevention**: Follow report storage guidelines

### Issue: Missing Changelog Entry
**Cause**: Forgot to update SYSTEM_CHANGELOG.md  
**Fix**: Add complete entry with version, features, and status  
**Prevention**: Include in deployment checklist

### Issue: Git Tag Mismatch
**Cause**: Tag version doesn't match changelog  
**Fix**: Create new tag with correct version  
**Prevention**: Verify tag matches changelog before push

## 📚 Reference Links

- **Implementation Guidelines**: `/essentials/IMPLEMENTATION_GUIDELINES.md`
- **Constitution**: `/essentials/AVA_OLO_CONSTITUTION.md`
- **Report Examples**: `/essentials/reports/`
- **Version History**: `SYSTEM_CHANGELOG.md`

---
**Remember**: Every deployment affects farmers globally. From Croatian wheat to Bulgarian mangoes, quality and compliance matter! 🥭✅