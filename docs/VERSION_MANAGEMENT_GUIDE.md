# Constitutional Version Management Guide

## 🎯 Overview

The Constitutional Version Management system provides comprehensive version control for AVA OLO with:

- **🔢 Automatic version numbering** with semantic versioning
- **🏛️ Constitutional compliance checking** for each version
- **☁️ AWS deployment tracking** and monitoring
- **⚖️ Local vs AWS version comparison**
- **🖥️ Simple CLI and web interfaces**
- **🥭 MANGO RULE enforcement** - ensures every version works for Bulgarian mango farmers

## 🚀 Quick Start

### 1. Initialize Version Management

```bash
# Navigate to your project directory
cd /path/to/ava-olo-shared

# Initialize version management
python implementation/version_cli.py init

# Check current status
python implementation/version_cli.py status
```

### 2. Create Your First Version

```bash
# Create patch version with description
python implementation/version_cli.py create "Added Bulgarian mango farmer support"

# Create minor version for new features
python implementation/version_cli.py create "New localization features" --type minor

# Create major version for breaking changes
python implementation/version_cli.py create "Constitutional framework 2.0" --type major
```

### 3. Compare Local vs AWS Versions

```bash
# Check if local and AWS versions are synchronized
python implementation/version_cli.py compare
```

### 4. Deploy to AWS

```bash
# Deploy specific service
python implementation/version_cli.py deploy monitoring-dashboards

# Or use automated deployment with git commit
python implementation/deployment_automation.py --commit "Added mango support" --deploy all
```

### 5. Monitor with Web Dashboard

```bash
# Start web dashboard
python implementation/version_dashboard.py

# Access at http://localhost:8081
# Dashboard auto-refreshes every 30 seconds
```

## 📋 Detailed Commands Reference

### Status Commands

```bash
# Show current version and git status
python implementation/version_cli.py status

# Show version history (last 10)
python implementation/version_cli.py history

# Show more versions
python implementation/version_cli.py history --limit 20
```

### Version Creation

```bash
# Basic version creation (patch increment)
python implementation/version_cli.py create "Description of changes"

# Specify version type
python implementation/version_cli.py create "New feature" --type minor
python implementation/version_cli.py create "Breaking change" --type major
python implementation/version_cli.py create "Bug fix" --type patch
```

### Deployment Commands

```bash
# Compare local and AWS versions
python implementation/version_cli.py compare

# Deploy to specific service
python implementation/version_cli.py deploy monitoring-dashboards
python implementation/version_cli.py deploy agricultural-core

# Automated workflow (commit + version + deploy)
python implementation/deployment_automation.py --commit "Feature description" --deploy all
python implementation/deployment_automation.py --commit "Bug fix" --deploy monitoring-dashboards --type patch
```

## 🏗️ Version Numbering System

AVA OLO uses **semantic versioning**: `MAJOR.MINOR.PATCH`

### Version Types

- **🔴 MAJOR (X.0.0)**: Breaking changes, constitutional amendments, major system overhauls
  - Example: `1.0.0 → 2.0.0`
  - Use cases: New constitutional principles, API breaking changes

- **🟡 MINOR (0.X.0)**: New features, backward compatible changes
  - Example: `1.2.0 → 1.3.0` 
  - Use cases: New farmer features, additional crops support

- **🟢 PATCH (0.0.X)**: Bug fixes, small improvements, documentation
  - Example: `1.2.3 → 1.2.4`
  - Use cases: Bug fixes, performance improvements, text corrections

### Examples

```bash
# Bug fix: 1.2.3 → 1.2.4
python implementation/version_cli.py create "Fixed mango growth calculation" --type patch

# New feature: 1.2.4 → 1.3.0  
python implementation/version_cli.py create "Added Dragon fruit support" --type minor

# Breaking change: 1.3.0 → 2.0.0
python implementation/version_cli.py create "New constitutional framework" --type major
```

## 🏛️ Constitutional Compliance System

Every version automatically checks **all 13 constitutional principles**:

### Core Principles Checked

1. **🥭 MANGO RULE** - Works for any crop in any country
2. **🧠 LLM-FIRST** - AI-driven decisions over hardcoded logic  
3. **🔒 PRIVACY-FIRST** - Farmer data protection
4. **🐘 POSTGRESQL-ONLY** - Single database technology
5. **🏗️ MODULE INDEPENDENCE** - Services work independently
6. **📡 API-FIRST** - All communication via APIs
7. **🛡️ ERROR ISOLATION** - Graceful failure handling
8. **📊 TRANSPARENCY** - Complete logging and traceability
9. **👨‍🌾 FARMER-CENTRIC** - Professional agricultural tone
10. **⚡ PRODUCTION-READY** - AWS deployment ready
11. **⚙️ CONFIGURATION** - No hardcoded values
12. **🧪 TEST-DRIVEN** - Comprehensive testing
13. **🌍 COUNTRY-AWARE** - Smart localization

### Compliance Thresholds

- **✅ Compliant**: 80%+ score across all principles
- **⚠️ Warning**: 60-79% score (version created with warnings)
- **❌ Blocked**: <60% score (version creation blocked)

### Override Compliance

```bash
# Force create version despite compliance issues (emergency only)
python implementation/version_cli.py create "Emergency fix" --force

# In Python code
version = await manager.create_version("Emergency fix", force=True)
```

## 📁 Files Created by Version Management

### Version Tracking Files

```
ava-olo-shared/
├── version_history.json      # Complete version history
├── version_config.json       # System configuration
└── deployment_status.json    # AWS deployment tracking
```

### version_history.json Structure

```json
{
  "current_version": "1.2.3",
  "versions": [
    {
      "version_number": "1.2.3",
      "timestamp": "2024-01-15T10:30:00",
      "description": "Added Bulgarian mango support",
      "git_commit": "abc123...",
      "git_branch": "main",
      "files_changed": ["src/crops.py", "docs/README.md"],
      "constitutional_compliance": true,
      "compliance_score": 95.2,
      "deployment_status": "deployed"
    }
  ]
}
```

### version_config.json Configuration

```json
{
  "version_format": "semantic",
  "auto_increment": true,
  "require_description": true,
  "require_constitutional_check": true,
  "aws_services": {
    "monitoring-dashboards": {
      "name": "ava-olo-monitoring-dashboards",
      "url": "https://6pmgiripe.us-east-1.awsapprunner.com",
      "health_endpoint": "/health"
    }
  }
}
```

## 🔧 Advanced Usage

### Programmatic API

```python
from implementation.version_manager import ConstitutionalVersionManager

# Initialize manager
manager = ConstitutionalVersionManager()

# Check current version
current = manager.get_current_version()
print(f"Current version: {current}")

# Create new version
version = await manager.create_version(
    description="Added new feature",
    increment_type="minor"
)

# Check AWS deployment status
comparison = await manager.compare_versions()
print(f"All synced: {comparison['all_synced']}")

# Check constitutional compliance
compliance = await manager.check_constitutional_compliance()
print(f"Compliance score: {compliance['average_score']:.1f}%")
```

### Custom Configuration

```python
# Modify configuration
manager.config["require_constitutional_check"] = False  # Disable compliance checking
manager.config["version_format"] = "timestamp"  # Use timestamp versioning
manager._save_config()
```

### Batch Operations

```bash
# Create multiple versions quickly
for feature in "feature1" "feature2" "feature3"; do
    python implementation/version_cli.py create "Added $feature" --type patch
done

# Deploy all services in sequence
python implementation/deployment_automation.py --commit "Batch deployment" --deploy all
```

## 🌐 Web Dashboard Features

Access the dashboard at `http://localhost:8081`

### Dashboard Sections

1. **📊 Current Version Status**
   - Current version number
   - Synchronization status with AWS
   - Quick statistics

2. **☁️ AWS Service Status**  
   - Real-time service health
   - Version comparison per service
   - Status indicators (online/offline)

3. **📚 Version History**
   - Last 10 versions with details
   - Constitutional compliance scores
   - Deployment status indicators

4. **🚀 Deployment Status**
   - Complete deployment tracking
   - Service URLs and health
   - Deployment timestamps

### Dashboard Features

- **🔄 Auto-refresh** every 30 seconds
- **📱 Responsive design** for mobile/desktop  
- **🎨 Constitutional theme** with MANGO RULE emphasis
- **⚡ Real-time AWS status** checking

## 🚀 Deployment Workflows

### Simple Workflow

```bash
# 1. Make changes to code
echo "new feature" >> src/feature.py

# 2. Create version
python implementation/version_cli.py create "Added new feature"

# 3. Commit to git
git add .
git commit -m "Added new feature (v1.2.4)"

# 4. Deploy
python implementation/version_cli.py deploy monitoring-dashboards
```

### Automated Workflow

```bash
# Single command: commit + version + deploy
python implementation/deployment_automation.py \
  --commit "Added Bulgarian mango farmer dashboard" \
  --deploy all \
  --type minor
```

### CI/CD Integration

```yaml
# .github/workflows/deploy.yml
name: Constitutional Deployment

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Check Constitutional Compliance
        run: |
          python implementation/version_cli.py status
          
      - name: Create Version
        run: |
          python implementation/version_cli.py create "Automated deployment"
          
      - name: Deploy to AWS
        run: |
          python implementation/deployment_automation.py --commit "CI/CD deployment" --deploy all
```

## 🛠️ Best Practices

### 1. Version Description Guidelines

```bash
# ✅ Good descriptions
python implementation/version_cli.py create "Added Bulgarian mango farmer support with smart localization"
python implementation/version_cli.py create "Fixed constitutional compliance in crop detection module"
python implementation/version_cli.py create "Improved LLM response time for minority farmers"

# ❌ Poor descriptions  
python implementation/version_cli.py create "fix"
python implementation/version_cli.py create "changes"
python implementation/version_cli.py create "update"
```

### 2. Constitutional Compliance

```bash
# Always check compliance before major versions
python implementation/version_cli.py status

# Review compliance score in version history
python implementation/version_cli.py history

# Use web dashboard for detailed compliance tracking
python implementation/version_dashboard.py
```

### 3. Deployment Strategy

```bash
# Test locally first
python implementation/version_cli.py compare

# Deploy one service at a time for critical changes
python implementation/version_cli.py deploy monitoring-dashboards
# Wait and verify, then:
python implementation/version_cli.py deploy agricultural-core

# Use automated deployment for routine updates
python implementation/deployment_automation.py --commit "Routine update" --deploy all
```

### 4. Git Integration

```bash
# Keep git and versions synchronized
git status  # Check git status
python implementation/version_cli.py status  # Check version status

# Use meaningful commit messages
git commit -m "Add Bulgarian mango support (v1.3.0)"

# Tag major releases
git tag -a v1.3.0 -m "Major release: Bulgarian mango farmer support"
```

## 🚨 Troubleshooting

### Common Issues

#### 1. Constitutional Compliance Failures

```bash
# Problem: Version creation blocked due to compliance
❌ Error: Constitutional compliance failed: 65.2% (3 critical violations)

# Solution: Check specific violations
python implementation/version_cli.py status

# Fix violations or use force override (emergency only)
python implementation/version_cli.py create "Emergency fix" --force
```

#### 2. AWS Connection Issues

```bash
# Problem: Cannot connect to AWS services
🔴 Status: offline, error: Connection timeout

# Solution: Check AWS service URLs in config
# Edit version_config.json to update service URLs
```

#### 3. Git Integration Problems

```bash
# Problem: No git repository found
❌ Error: Git information unavailable

# Solution: Initialize git repository
git init
git add .
git commit -m "Initial commit"
```

#### 4. Version File Corruption

```bash
# Problem: Cannot read version history
❌ Error: JSON decode error in version_history.json

# Solution: Reinitialize version management
mv version_history.json version_history.json.backup
python implementation/version_cli.py init
```

### Debug Mode

```bash
# Enable detailed logging
export CONSTITUTIONAL_DEBUG=1
python implementation/version_cli.py status

# Check dashboard logs
python implementation/version_dashboard.py
# Look for error messages in console
```

### Reset Version Management

```bash
# Complete reset (WARNING: Loses history)
rm version_history.json version_config.json deployment_status.json
python implementation/version_cli.py init
```

## 📊 Monitoring and Metrics

### Key Metrics to Track

1. **Version Velocity**: Versions created per week
2. **Compliance Score Trend**: Average compliance over time  
3. **Deployment Success Rate**: Successful deployments vs failures
4. **AWS Sync Status**: Percentage of time services are synchronized

### Dashboard Monitoring

```bash
# Start dashboard for continuous monitoring
python implementation/version_dashboard.py &

# Set up monitoring alerts (example)
while true; do
  python implementation/version_cli.py compare | grep "❌" && echo "ALERT: Version mismatch detected"
  sleep 300
done
```

## 🎯 Production Deployment Checklist

Before deploying to production:

- [ ] ✅ Constitutional compliance score ≥ 80%
- [ ] ✅ All tests passing
- [ ] ✅ Git repository clean and committed
- [ ] ✅ Version description is meaningful
- [ ] ✅ AWS services healthy
- [ ] ✅ Local and AWS versions compared
- [ ] ✅ MANGO RULE compliance verified
- [ ] ✅ Deployment plan documented

## 🤝 Contributing to Version Management

### Extending the System

```python
# Add new AWS service
manager.config["aws_services"]["new-service"] = {
    "name": "ava-olo-new-service",
    "url": "https://new-service.aws.com",
    "health_endpoint": "/health"
}
manager._save_config()

# Add custom compliance checks
class ExtendedVersionManager(ConstitutionalVersionManager):
    async def check_custom_compliance(self):
        # Your custom compliance logic
        pass
```

### Configuration Options

All configuration options in `version_config.json`:

```json
{
  "version_format": "semantic",           // "semantic" or "timestamp"
  "auto_increment": true,                 // Auto-increment version numbers
  "require_description": true,            // Require version descriptions
  "require_constitutional_check": true,   // Require compliance checking
  "excluded_files": [                     // Files to ignore in version tracking
    "*.pyc", "__pycache__", ".git", "*.log"
  ]
}
```

## 📚 Additional Resources

### Documentation Links

- [Constitutional Principles](../constitutional/AVA_OLO_CONSTITUTION.md)
- [Constitutional Checker Guide](CONSTITUTIONAL_CHECKER_USAGE.md)
- [AWS Deployment Architecture](../architecture/AWS_DEPLOYMENT_ARCHITECTURE.md)
- [System Architecture](../architecture/CURRENT_SYSTEM_ARCHITECTURE.md)

### Support

For issues with version management:

1. Check this guide for solutions
2. Review constitutional compliance requirements
3. Verify AWS service configuration
4. Check git repository status

## 🥭 Remember the MANGO RULE!

**Every version must work for a Bulgarian mango farmer!**

The Constitutional Version Management system ensures that every code change maintains universal compatibility and constitutional compliance.

---

*"Version constitutionally, deploy confidently, serve farmers globally!"* 🌾🏛️