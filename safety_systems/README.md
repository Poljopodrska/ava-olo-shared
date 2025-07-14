# AVA OLO Safety System 🛡️

A comprehensive proactive + monitoring safety system that prevents deployment failures and ensures constitutional compliance for AVA OLO services.

## 🎯 Purpose

This system was created to prevent deployment failures like the 2-hour debugging session that prompted its creation. It provides:

1. **Proactive Protection**: Blocks risky deployments before they happen
2. **Real-time Monitoring**: Tracks service health and version history
3. **Emergency Recovery**: 30-second rollback capability
4. **Constitutional Compliance**: Ensures all deployments follow AVA OLO principles

## 📁 Components

### Proactive System
- `proactive_deployment_guard.py` - Main validation engine
- `pre_deploy_check.sh` - Pre-deployment validation wrapper
- `constitutional_deploy.sh` - Safe deployment protocol
- `pre-push-hook.sh` - Git hook for early validation

### Monitoring System
- `comprehensive_health_dashboard.html` - Real-time monitoring dashboard
- `enhanced_version_system.py` - Version tracking with Git integration

### Emergency Response
- `emergency_rollback.sh` - 30-second emergency rollback
- Automatic rollback on deployment failure

## 🚀 Quick Start

### Initial Setup
```bash
# Run the setup script
./setup_safety_system.sh
```

### Pre-Deployment Check
```bash
# Run safety checks before deployment
./pre_deploy_check.sh monitoring_dashboards
```

### Safe Deployment
```bash
# Deploy with full safety protocol
./constitutional_deploy.sh monitoring_dashboards "Fix dashboard routing"
```

### Emergency Rollback
```bash
# Rollback to previous stable version
./emergency_rollback.sh monitoring_dashboards
```

### Version Management
```bash
# Check current version
python enhanced_version_system.py current --service monitoring_dashboards

# View deployment history
python enhanced_version_system.py history --service monitoring_dashboards

# Get deployment statistics
python enhanced_version_system.py stats --service monitoring_dashboards --days 30
```

## 🏛️ Constitutional Compliance

All components follow AVA OLO constitutional principles:
- 🥭 **MANGO Rule**: Works for any farmer, any crop, any country
- 🧠 **LLM-First**: AI-driven decision making
- 🔒 **Privacy-First**: No farmer data exposure
- 🌍 **Global-First**: Works globally
- 🏗️ **Module Independence**: Services work independently

## 📊 Monitoring Dashboard

Open `../web_dashboard/comprehensive_health_dashboard.html` to view:
- Real-time service health
- Version history with rollback tracking
- Constitutional compliance scores
- Database connection status
- Quick action buttons for emergency procedures

## 🔧 Configuration

### Environment Variables Required
- `DATABASE_URL` - PostgreSQL connection string
- `OPENAI_API_KEY` - For LLM-first operations
- `AWS_APPRUNNER_SERVICE_NAME` - Service identifier (optional)

### Service URLs
- Monitoring Dashboards: `https://6pmgiripe.us-east-1.awsapprunner.com`
- Agricultural Core: `https://3ksdvgdtud.us-east-1.awsapprunner.com`

## 🚨 Emergency Procedures

### Deployment Failure
1. System automatically initiates rollback
2. Check health dashboard for status
3. Review deployment logs
4. Fix issues before re-deployment

### Manual Emergency Rollback
```bash
./emergency_rollback.sh <service_name>
```

### Service Degradation
1. Check dashboard for affected services
2. Review version history for problematic deployment
3. Execute rollback if needed
4. Notify team through configured channels

## 📋 Deployment Rules

The system enforces these safety rules:
- Any critical failure = BLOCK deployment
- More than 1 high-risk failure = BLOCK
- More than 3 medium-risk failures = BLOCK
- Constitutional compliance must be ≥ 80%
- Database connections must be verified
- Working systems must be protected

## 🧪 Testing

Test the system without affecting production:
```bash
# Test proactive guard
python proactive_deployment_guard.py monitoring_dashboards .

# Test emergency rollback (dry run - answer 'no' when prompted)
./emergency_rollback.sh monitoring_dashboards

# Test version tracking
python enhanced_version_system.py record --service test --version v1.0.0 --message "Test deployment"
```

## 📈 Success Metrics

When properly implemented, this system provides:
- ✅ Zero unplanned downtime
- ✅ 30-second rollback capability
- ✅ 95%+ deployment success rate
- ✅ Full constitutional compliance
- ✅ Complete deployment audit trail

## 🤝 Contributing

When modifying the safety system:
1. Test all changes locally first
2. Ensure constitutional compliance
3. Update documentation
4. Run full validation suite
5. Get team review before deployment

## 📞 Support

For issues or questions:
- Check health dashboard first
- Review deployment logs
- Contact AVA OLO DevOps team
- Emergency: Use emergency rollback procedure

---

**Remember**: This system is your safety net. Use it for every deployment to ensure the continued reliability of AVA OLO services. 🛡️