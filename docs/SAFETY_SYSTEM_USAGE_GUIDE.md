# AVA OLO Safety System Usage Guide 🛡️

## 📋 Overview

This guide explains how to use the AVA OLO Safety System in REVIEW MODE and gradually enable features as you gain confidence. The system is designed with safety-first principles to prevent deployment failures while maintaining zero impact on existing workflows until explicitly enabled.

## 🚦 Operating Modes

### 1. Review Mode (DEFAULT - Safe)
- All files created for inspection
- No production impact
- No git hooks enabled
- No service modifications
- Full testing capability with dry-run flags

### 2. Test Mode
- Enables select features for testing
- Still no production impact
- Verbose logging
- Easy rollback

### 3. Production Mode
- Full system active
- All safety checks enforced
- Git hooks enabled
- Emergency procedures available

## 🛡️ Safety Flags

Every script supports these safety flags:

```bash
--dry-run          # Show what would happen without doing it
--test-mode        # Test functionality without production impact
--review-mode      # Install/run for review only (default)
--no-hooks         # Skip git hook operations
--no-modify        # Don't modify any existing files
--verbose          # Show detailed operation logs
--bypass           # Emergency bypass (requires confirmation)
```

## 📖 Step-by-Step Usage

### Phase 1: Initial Review (Current State)

1. **Review Documentation**
   ```bash
   # Read the master plan
   cat docs/SAFETY_SYSTEM_IMPLEMENTATION_PLAN.md
   
   # Check this usage guide
   cat docs/SAFETY_SYSTEM_USAGE_GUIDE.md
   ```

2. **Test Proactive Guards**
   ```bash
   # Test without any real checks
   cd safety_systems
   python proactive_deployment_guard.py monitoring_dashboards --dry-run
   
   # See what it would check
   python proactive_deployment_guard.py monitoring_dashboards --test-mode
   ```

3. **Test Emergency Rollback**
   ```bash
   # Dry run - shows what would happen
   ./emergency_rollback.sh monitoring_dashboards --dry-run
   
   # Test mode - runs checks but doesn't rollback
   ./emergency_rollback.sh monitoring_dashboards --test-mode
   ```

4. **View Health Dashboard**
   ```bash
   # Open in browser (read-only view)
   open ../web_dashboard/comprehensive_health_dashboard.html
   ```

### Phase 2: Local Testing

1. **Run Pre-Deployment Check**
   ```bash
   # Test mode - runs all checks but doesn't block
   ./pre_deploy_check.sh monitoring_dashboards --test-mode
   ```

2. **Test Constitutional Deploy**
   ```bash
   # Dry run - shows deployment steps
   ./constitutional_deploy.sh monitoring_dashboards "Test deployment" --dry-run
   ```

3. **Test Version System**
   ```bash
   # Check current version (safe - read only)
   python enhanced_version_system.py current --service monitoring_dashboards
   
   # View history (safe - read only)
   python enhanced_version_system.py history --service monitoring_dashboards
   ```

### Phase 3: Gradual Enablement

1. **Enable Git Hooks (When Ready)**
   ```bash
   # First, test what it would do
   ./install_git_hooks.sh --test-mode
   
   # Install but allow bypass
   ./install_git_hooks.sh --with-bypass
   
   # Full installation (later)
   ./install_git_hooks.sh --enable-production
   ```

2. **Enable Health Dashboards**
   ```bash
   # See what would be added
   ./enable_health_dashboards.sh --dry-run
   
   # Add endpoints but keep optional
   ./enable_health_dashboards.sh --optional
   
   # Full integration (later)
   ./enable_health_dashboards.sh --enable-production
   ```

3. **Enable Full System**
   ```bash
   # Final step - enable everything
   ./enable_full_system.sh --confirm
   ```

## 🚨 Emergency Procedures

### Bypass Safety Checks (Emergency Only)
```bash
# Bypass git hooks
git push --no-verify

# Bypass with environment variable
AVA_EMERGENCY=true git push

# Bypass deployment checks
AVA_EMERGENCY=true ./constitutional_deploy.sh service "Emergency fix"
```

### Emergency Rollback
```bash
# Requires typing confirmation
./emergency_rollback.sh monitoring_dashboards
# Type: EMERGENCY_ROLLBACK
```

### Disable System Temporarily
```bash
# Disable all checks for 1 hour
./safety_systems/disable_temporarily.sh --hours 1 --reason "Hotfix deployment"
```

## 🧪 Testing Commands

### Test Individual Components
```bash
# Test constitutional compliance
python -c "from proactive_deployment_guard import ProactiveDeploymentGuard; 
g = ProactiveDeploymentGuard(); 
print(g.check_constitutional_compliance('.'))"

# Test database connection
python -c "from proactive_deployment_guard import ProactiveDeploymentGuard;
g = ProactiveDeploymentGuard();
print(g.check_database_connections('.'))"

# Test version system
python enhanced_version_system.py record \
  --service test \
  --version v1.0.0 \
  --message "Test entry" \
  --dry-run
```

### Validate Installation
```bash
# Check all files exist
./validate_installation.sh

# Run system self-test
./run_safety_tests.sh

# Generate installation report
./generate_installation_report.sh > installation_report.txt
```

## 📊 Monitoring & Metrics

### Check System Status
```bash
# Overall system health
./safety_status.sh

# Deployment statistics
python enhanced_version_system.py stats --service monitoring_dashboards --days 30

# Safety check history
./check_history.sh --last 10
```

### Dashboard Access Points
- Local File: `file:///path/to/web_dashboard/comprehensive_health_dashboard.html`
- Monitoring Service: `https://<service-url>/health-dashboard` (when enabled)
- Agricultural Service: `https://<service-url>/health-dashboard` (when enabled)

## 🔧 Configuration

### Environment Variables
```bash
# Optional - override defaults
export AVA_SAFETY_MODE="review"           # review, test, production
export AVA_SAFETY_VERBOSE="true"          # Enable verbose logging
export AVA_SAFETY_COMPLIANCE_MIN="80"     # Minimum compliance score
export AVA_EMERGENCY="false"              # Emergency bypass flag
```

### Configuration Files
```bash
# Create local config (optional)
cat > .safety_config <<EOF
{
  "mode": "review",
  "enable_hooks": false,
  "compliance_threshold": 80,
  "rollback_timeout": 30
}
EOF
```

## 📈 Gradual Adoption Path

### Week 1: Review & Learn
- ✅ Read all documentation
- ✅ Test all scripts with --dry-run
- ✅ Understand emergency procedures
- ✅ Review health dashboard

### Week 2: Local Testing
- 🧪 Run pre-deployment checks locally
- 🧪 Test emergency rollback procedures
- 🧪 Practice with test deployments
- 🧪 Monitor version history

### Week 3: Soft Enable
- 🔧 Enable git hooks with bypass
- 🔧 Add health endpoints (optional)
- 🔧 Start tracking deployments
- 🔧 Review safety metrics

### Week 4: Full Production
- 🚀 Enable all safety checks
- 🚀 Remove bypass options
- 🚀 Enforce constitutional compliance
- 🚀 Celebrate improved reliability!

## ❓ Troubleshooting

### Common Issues

1. **Script Permission Denied**
   ```bash
   chmod +x safety_systems/*.sh
   ```

2. **Python Module Not Found**
   ```bash
   export PYTHONPATH="${PYTHONPATH}:$(pwd)/safety_systems"
   ```

3. **Git Hook Not Running**
   ```bash
   # Check hook is executable
   ls -la .git/hooks/pre-push
   chmod +x .git/hooks/pre-push
   ```

4. **Database Connection Failed**
   ```bash
   # Verify environment variable
   echo $DATABASE_URL
   # Test connection manually
   psql $DATABASE_URL -c "SELECT 1"
   ```

### Getting Help
1. Check this guide first
2. Review error messages carefully
3. Run with --verbose flag
4. Check system logs
5. Contact AVA OLO DevOps team

## 🎯 Best Practices

1. **Always Start with Dry Run**
   - Test every command with --dry-run first
   - Understand what will happen before doing it

2. **Enable Gradually**
   - Don't enable everything at once
   - Test each component thoroughly
   - Build confidence before full adoption

3. **Document Everything**
   - Log why you bypassed checks
   - Document emergency procedures used
   - Track all configuration changes

4. **Monitor Metrics**
   - Check deployment success rate weekly
   - Review rollback frequency
   - Track compliance scores

5. **Stay Constitutional**
   - Remember the MANGO rule 🥭
   - Maintain LLM-first approach 🧠
   - Protect farmer privacy 🔒

## 🏁 Next Steps

1. **Immediate**: Review all documentation
2. **Today**: Test scripts with --dry-run
3. **This Week**: Run local tests
4. **Next Week**: Enable first features
5. **This Month**: Full production enablement

---

Remember: The safety system is here to help, not hinder. Take your time to understand it, test thoroughly, and enable gradually. Your future self will thank you when deployments go smoothly! 🛡️