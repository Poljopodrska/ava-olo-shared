# 🏛️ Claude Code Master Constitutional Reference

**This document contains everything Claude Code needs to work with AVA OLO constitutional systems.**

> 📌 **IMPORTANT**: This document includes a complete file reference. Claude Code can access any listed file without needing them all uploaded. Simply reference the file path when you need specific information.

### 🚀 How to Use This Reference
1. **Start new chat**: Upload only this file (`CLAUDE_CODE_MASTER_CONSTITUTIONAL_REFERENCE.md`)
2. **Access any file**: Ask Claude Code to read specific files from the [Complete File Reference](#-complete-file-reference) section
3. **Example**: "Please read `docs/CONSTITUTIONAL_DESIGN_SYSTEM.md` to understand the design requirements"

## 🎯 System Overview

AVA OLO is a constitutional agricultural CRM serving farmers globally through WhatsApp integration. Built on AWS infrastructure with 100% LLM-first intelligence, supporting 50+ countries and languages, including minority farmers like Hungarian speakers in Croatia.

**Repository**: https://github.com/Poljopodrska/ava-olo-shared
**Working Directory**: `C:\Users\HP\ava-olo-constitutional\ava-olo-shared`

## 🏛️ The 13 Constitutional Principles

### 🥭 #1: THE MANGO RULE (Supreme Law)
**"Would this work for a Bulgarian mango farmer?"**
- Every feature must work for any crop in any country
- Test question: Can a Bulgarian farmer grow mangoes with this system?
- No geographic or crop discrimination allowed
- Universal compatibility required

### Core Principles:
2. **💾 POSTGRESQL-ONLY** - Single database technology
3. **🧠 LLM-FIRST** - AI intelligence over hardcoded logic
4. **🏗️ MODULE INDEPENDENCE** - Services work independently
5. **🔒 PRIVACY-FIRST** - Farmer data never leaves our infrastructure
6. **🌐 API-FIRST** - All communication via APIs
7. **🛡️ ERROR ISOLATION** - Failures don't cascade
8. **📊 TRANSPARENCY** - All actions logged and traceable
9. **👨‍🌾 FARMER-CENTRIC** - Designed for farmer needs
10. **⚡ PRODUCTION-READY** - AWS-deployed and scalable
11. **⚙️ CONFIGURATION-DRIVEN** - Settings over hardcoding
12. **🧪 TEST-DRIVEN** - Comprehensive testing
13. **🌍 COUNTRY-AWARE** - Smart detection with minority support
14. **🎨 DESIGN-FIRST** - Constitutional design system (ERROR-level enforcement)

## 📁 Repository Structure

```
ava-olo-shared/
├── 📜 constitutional/           # Supreme law documents
│   ├── AVA_OLO_CONSTITUTION.md      # The 13 principles
│   ├── CONSTITUTIONAL_AMENDMENT_13.md # Localization rules
│   └── CONSTITUTIONAL_COMPLIANCE.md   # Compliance guide
│
├── 📚 docs/                    # Developer documentation
│   ├── NEW_DEVELOPER_ONBOARDING.md   # Start here!
│   ├── QUICK_START_GUIDE.md          # 5-minute setup
│   ├── CONSTITUTIONAL_CHECKER_USAGE.md # Constitutional compliance
│   ├── VERSION_MANAGEMENT_GUIDE.md    # Version control
│   └── TROUBLESHOOTING_GUIDE.md      # Common issues
│
├── 🏗️ architecture/            # System design docs
│   ├── CURRENT_SYSTEM_ARCHITECTURE.md # How it all works
│   ├── AWS_DEPLOYMENT_ARCHITECTURE.md # AWS infrastructure
│   └── API_ENDPOINTS_REFERENCE.md     # All APIs documented
│
├── 💡 examples/                # Code examples
│   ├── CONSTITUTIONAL_CODE_EXAMPLES.md # Good vs bad code
│   ├── NEW_FEATURE_TEMPLATE.md        # Feature blueprint
│   └── database_dashboard_constitutional_example.py
│
├── 🔧 implementation/          # Core systems
│   ├── constitutional_checker.py              # Constitutional compliance
│   ├── constitutional_integration.py          # Integration helpers
│   ├── dashboard_constitutional_integration.py # Dashboard integration
│   ├── version_manager.py                     # Version management
│   ├── version_cli.py                         # CLI tools
│   ├── deployment_automation.py               # Automated deployment
│   ├── version_dashboard.py                   # Web dashboard
│   ├── config_manager.py                      # Configuration
│   └── smart_country_detector.py              # Smart localization
│
├── 🧪 tests/                   # Constitutional tests
└── 📖 README.md               # System overview
```

## 📚 Complete File Reference

### 🏛️ Constitutional Documents
- `constitutional/AVA_OLO_CONSTITUTION.md` - The 14 constitutional principles
- `constitutional/CONSTITUTIONAL_AMENDMENT_13.md` - Country localization rules
- `constitutional/CONSTITUTIONAL_COMPLIANCE.md` - How to stay compliant

### 📖 Developer Documentation
- `docs/QUICK_START_GUIDE.md` - Get running in 5 minutes
- `docs/NEW_DEVELOPER_ONBOARDING.md` - Complete onboarding guide
- `docs/ENVIRONMENT_CONFIGURATION.md` - .env setup and management
- `docs/CONSTITUTIONAL_DESIGN_SYSTEM.md` - Design system with enforcement
- `docs/CONSTITUTIONAL_CHECKER_USAGE.md` - How to use compliance checker
- `docs/VERSION_MANAGEMENT_GUIDE.md` - Version control system
- `docs/TROUBLESHOOTING_GUIDE.md` - Common issues and solutions
- `docs/TESTING_PROCEDURES.md` - How to test properly
- `docs/DEVELOPMENT_CHECKLIST.md` - Pre-deployment checklist
- `docs/STARTUP_CHECKLIST.md` - System startup procedures
- `docs/EMERGENCY_DEVELOPER_RECOVERY.md` - When things go wrong
- `docs/GIT_COMMANDS_CONSTITUTIONAL.md` - Git workflow guide
- `docs/INTEGRATION_GUIDE_AMENDMENT_13.md` - Localization integration

### 🏗️ Architecture & System Design
- `architecture/CURRENT_SYSTEM_ARCHITECTURE.md` - How everything connects
- `architecture/AWS_DEPLOYMENT_ARCHITECTURE.md` - AWS infrastructure details
- `architecture/API_ENDPOINTS_REFERENCE.md` - All API endpoints documented

### 🐍 Core Implementation (Python)
- `implementation/constitutional_checker.py` - Validates 14 principles compliance
- `implementation/version_manager.py` - Manages versions with compliance
- `implementation/config_manager.py` - Configuration management
- `implementation/constitutional_integration.py` - Easy integration helpers
- `implementation/dashboard_constitutional_integration.py` - Dashboard decorators
- `implementation/deployment_automation.py` - Auto-deploy with compliance
- `implementation/smart_country_detector.py` - Detects minority languages
- `implementation/version_cli.py` - CLI for version management
- `implementation/version_dashboard.py` - Web dashboard for versions

### 🎨 Design System Files
- `templates/constitutional-design-template.html` - **Complete HTML example**
- `src/styles/constitutional-design-system.css` - Core CSS framework
- `src/styles/mobile-constitutional.css` - Mobile-specific styles
- `scripts/constitutional-build-check.js` - Build-time enforcement
- `src/utils/constitutional-design-checker.js` - Design validation

### ⚛️ React Components
- `src/components/constitutional/ConstitutionalHeader.jsx` - Header with atomic logo
- `src/components/constitutional/ConstitutionalCard.jsx` - Card component
- `src/components/constitutional/ConstitutionalInput.jsx` - Input with Enter key
- `src/components/constitutional/ConstitutionalButton.jsx` - Accessible buttons
- `src/components/constitutional/DesignComplianceDashboard.jsx` - Compliance monitor

### 📊 Examples & Templates
- `examples/CONSTITUTIONAL_CODE_EXAMPLES.md` - Good vs bad code examples
- `examples/NEW_FEATURE_TEMPLATE.md` - Template for new features
- `examples/database_dashboard_constitutional_example.py` - Full example

### 🧪 Tests
- `tests/test_constitutional_checker.py` - Compliance checker tests
- `tests/test_constitutional_amendment_13.py` - Localization tests

### 💾 Database
- `database/database_schema_amendment_13.sql` - Schema with localization

### ⚙️ Configuration Files
- `version_config.json` - Version management config
- `version_history.json` - Version history tracking
- `deployment_status.json` - AWS deployment status
- `.env.example` - Environment template (root directory)

### 📝 Master References
- `CLAUDE_CODE_MASTER_CONSTITUTIONAL_REFERENCE.md` - **This file** (use for all chats)
- `README.md` - Project overview

## 🎯 Essential Files for Common Tasks

### For New Feature Development:
1. Read `constitutional/AVA_OLO_CONSTITUTION.md` - Understand the 14 principles
2. Use `templates/constitutional-design-template.html` - Start with compliant design
3. Check `examples/NEW_FEATURE_TEMPLATE.md` - Feature development blueprint
4. Run `implementation/constitutional_checker.py` - Validate compliance

### For Frontend Development:
1. View `templates/constitutional-design-template.html` - See all design patterns
2. Import `src/styles/constitutional-design-system.css` - Use the CSS framework
3. Use components from `src/components/constitutional/` - Pre-built React components
4. Check with `scripts/constitutional-build-check.js` - Ensure design compliance

### For Backend Integration:
1. Read `docs/QUICK_START_GUIDE.md` - Get up and running
2. Use `implementation/constitutional_integration.py` - Integration helpers
3. Check `architecture/API_ENDPOINTS_REFERENCE.md` - API documentation
4. Follow `examples/database_dashboard_constitutional_example.py` - Full example

### For Deployment:
1. Read `docs/ENVIRONMENT_CONFIGURATION.md` - Configure .env properly
2. Use `implementation/deployment_automation.py` - Automated deployment
3. Check `architecture/AWS_DEPLOYMENT_ARCHITECTURE.md` - AWS setup
4. Monitor with `implementation/version_dashboard.py` - Version tracking

### For Troubleshooting:
1. Start with `docs/TROUBLESHOOTING_GUIDE.md` - Common issues
2. Check `docs/EMERGENCY_DEVELOPER_RECOVERY.md` - Recovery procedures
3. Review logs using guidance from `docs/SYSTEM_CONFIG.md`

## 🚀 AWS Infrastructure

### Live Services:
- **Monitoring Dashboards**: `https://6pmgiripe.us-east-1.awsapprunner.com`
- **Agricultural Core**: `https://3ksdvgdtud.us-east-1.awsapprunner.com`
- **Database**: Aurora PostgreSQL (`farmer-crm-production`)

### Service Status:
- ✅ **Monitoring Dashboards**: Operational
- ✅ **Agricultural Core**: Operational  
- ✅ **Database**: Multi-AZ, Encrypted, Backed up
- ✅ **Constitutional Compliance**: 100%

## 🏛️ Constitutional Compliance System

### Usage:
```python
from implementation.constitutional_checker import ConstitutionalChecker

# Check code compliance
checker = ConstitutionalChecker()
result = await checker.check_compliance(code_or_file, "auto")

# Integration with FastAPI
from implementation.dashboard_constitutional_integration import constitutional_endpoint

@app.post("/api/query")
@constitutional_endpoint()
async def protected_endpoint(query: str):
    # Automatically validated for constitutional compliance
    return {"response": "Constitutional response"}
```

### Compliance Thresholds:
- **✅ Compliant**: 80%+ score across all principles
- **⚠️ Warning**: 60-79% score (version created with warnings)
- **❌ Blocked**: <60% score (version creation blocked)

## 🎨 Constitutional Design System (Principle #14)

### Design Template Available
A complete HTML template demonstrating all constitutional design requirements is available at:
```
templates/constitutional-design-template.html
```

### Key Design Requirements:
- **🎨 Colors**: Brown & olive agricultural palette (use CSS variables)
- **📝 Typography**: 18px+ minimum for older farmers
- **⌨️ Enter Key**: Mandatory on ALL inputs
- **📱 Mobile**: Responsive design required
- **⚛️ Logo**: Atomic structure branding

### Design Resources:
```
├── templates/
│   └── constitutional-design-template.html    # ← Complete HTML example
├── src/styles/
│   ├── constitutional-design-system.css       # Core CSS framework
│   └── mobile-constitutional.css              # Mobile-specific styles
├── src/components/constitutional/
│   ├── ConstitutionalHeader.jsx               # Header with atomic logo
│   ├── ConstitutionalCard.jsx                 # Card component
│   ├── ConstitutionalInput.jsx                # Input with Enter key
│   └── ConstitutionalButton.jsx               # Accessible buttons
└── docs/
    └── CONSTITUTIONAL_DESIGN_SYSTEM.md        # Complete design guide
```

### Quick Start with Design:
```bash
# View the design template
open templates/constitutional-design-template.html

# Import CSS in your project
@import '../src/styles/constitutional-design-system.css';

# Check design compliance
npm run check-design
```

### Build-Time Enforcement:
```json
{
  "scripts": {
    "build": "npm run check-design && webpack build",
    "check-design": "node scripts/constitutional-build-check.js"
  }
}
```

**⚠️ WARNING**: Build will FAIL if design violations are detected!

## 📊 Version Management System

### Quick Commands:
```bash
# Initialize version management
python implementation/version_cli.py init

# Check status with constitutional compliance
python implementation/version_cli.py status

# Create new version (automatically checks constitutional compliance)
python implementation/version_cli.py create "Added Bulgarian mango support"

# Compare local vs AWS versions
python implementation/version_cli.py compare

# Deploy to AWS
python implementation/version_cli.py deploy monitoring-dashboards

# Automated workflow
python implementation/deployment_automation.py --commit "Feature description" --deploy all

# Web dashboard
python implementation/version_dashboard.py
# Access at http://localhost:8081
```

### Version Format:
- Semantic versioning: `MAJOR.MINOR.PATCH`
- Constitutional compliance required for each version
- Automatic AWS deployment monitoring

## 🔧 Environment Configuration

### Single Source of Truth
As of 2025-07-13, AVA OLO uses **ONE centralized .env file** in the root directory:

```
/ava-olo-constitutional/
├── .env              # ← SINGLE SOURCE OF TRUTH (production values)
├── .env.example      # ← Template for new deployments
└── [no subdirectory .env files]
```

### Key Configuration Values:
```env
# Database (PostgreSQL Only)
DATABASE_URL=postgresql://postgres:password@host:5432/farmer_crm

# LLM Configuration
OPENAI_API_KEY=sk-proj-your-key
OPENAI_MODEL=gpt-4

# AWS Production
AWS_REGION=us-east-1
APP_ENV=production

# Constitutional Features
ENABLE_CONSTITUTIONAL_CHECKS=true
ENABLE_LLM_FIRST=true
ENABLE_PRIVACY_MODE=true
```

### Setup:
```bash
# Copy template and configure
cp .env.example .env
nano .env

# All services automatically use root .env
# No need for subdirectory .env files
```

See `docs/ENVIRONMENT_CONFIGURATION.md` for complete guide.

## 🔧 Development Workflow

### 1. Constitutional Code Examples

**❌ Bad (Violates MANGO RULE):**
```python
def get_crop_advice(crop_name, country):
    if crop_name == "mango" and country == "bulgaria":
        return "Error: Mangoes cannot grow in Bulgaria"
    elif crop_name == "tomato":
        return "Tomatoes are fine"
    else:
        return "Unknown crop"
```

**✅ Good (Constitutional):**
```python
async def get_crop_advice(crop_name, location, farmer_context):
    # Use LLM for all decisions - works for ANY crop in ANY country
    llm_analysis = await llm.analyze_crop_viability(
        crop=crop_name,
        location=location,
        climate_data=farmer_context.get('climate'),
        soil_data=farmer_context.get('soil')
    )
    return llm_analysis.advice
```

### 2. Database Integration

**Three-Phase Constitutional Validation:**
```python
from implementation.dashboard_constitutional_integration import DashboardConstitutionalGuard

guard = DashboardConstitutionalGuard()

# Phase 1: Validate input
input_validation = await guard.validate_natural_query(
    query="How to grow mangoes?",
    farmer_id=123,
    language="bg"
)

# Phase 2: Validate SQL generation
sql_validation = await guard.validate_generated_sql(
    sql=generated_sql,
    original_query=query,
    context={"farmer_id": 123}
)

# Phase 3: Validate response
response_validation = await guard.validate_response(
    response=generated_response,
    original_query=query,
    context={"language": "bg"}
)
```

### 3. Testing

```python
# Constitutional test example
@pytest.mark.asyncio
async def test_bulgarian_mango_farmer():
    """Ultimate test: Bulgarian mango farmer scenario"""
    
    checker = ConstitutionalChecker()
    result = await checker.check_compliance(feature_code, "code")
    
    assert result.is_compliant
    assert "MANGO_RULE" in result.compliant_principles
    assert result.overall_score > 90
```

## 🌍 Smart Localization (Amendment #13)

### Country-Language Detection:
```python
from implementation.smart_country_detector import SmartCountryDetector

detector = SmartCountryDetector()

# Smart detection with minority support
result = await detector.detect_farmer_context(
    farmer_id=123,
    ip_address="192.168.1.1",
    user_input="Kako uzgajati mango?"
)

# Result includes:
# - Detected country: "Croatia" 
# - Detected language: "Croatian"
# - Minority status: "Hungarian minority in Croatia"
# - Recommended approach: "Use Croatian with Hungarian cultural context"
```

### Supported Scenarios:
- **Hungarian farmers in Croatia**: Hungarian language support
- **Bulgarian mango farmers**: Full exotic crop support
- **Minority farmers globally**: Cultural and linguistic accommodation
- **50+ countries and languages**: Universal coverage

## 🚨 Common Constitutional Violations

### 1. MANGO RULE Violations:
```python
# ❌ Geographic discrimination
if country == "bulgaria":
    return "Not supported"

# ❌ Crop discrimination  
if crop == "mango":
    return "Cannot grow here"

# ✅ Constitutional approach
advice = await llm.get_agricultural_advice(crop, location, context)
```

### 2. LLM-FIRST Violations:
```python
# ❌ Hardcoded translations
TRANSLATIONS = {"en": "Hello", "es": "Hola"}

# ✅ Constitutional approach
translation = await llm.translate(text, target_language)
```

### 3. PRIVACY-FIRST Violations:
```python
# ❌ Sending personal data to external APIs
openai_response = await openai.complete(f"Advice for farmer {farmer_name}")

# ✅ Constitutional approach
openai_response = await openai.complete(f"Advice for farmer_id {anonymize(farmer_id)}")
```

## 📋 Quick Constitutional Checklist

Before any code deployment, verify:

- [ ] ✅ **MANGO RULE**: Works for Bulgarian mango farmers?
- [ ] 🧠 **LLM-FIRST**: Using AI decisions, not hardcoded logic?
- [ ] 🔒 **PRIVACY-FIRST**: No personal data in external APIs?
- [ ] 🌍 **GLOBAL**: No country/crop discrimination?
- [ ] 📊 **Constitutional compliance score**: ≥80%?
- [ ] 🧪 **Tests passing**: All constitutional tests green?

## 🛠️ Emergency Procedures

### Constitutional Crisis Recovery:
```bash
# Check current compliance
python implementation/version_cli.py status

# Force create emergency version (if compliance <80%)
python implementation/version_cli.py create "Emergency constitutional fix" --force

# Run constitutional checker
python -c "
from implementation.constitutional_checker import ConstitutionalChecker
import asyncio

async def emergency_check():
    checker = ConstitutionalChecker()
    result = await checker.check_compliance('.', 'auto')
    print(checker.generate_report(result))

asyncio.run(emergency_check())
"
```

### System Recovery:
```bash
# If system is broken
git status
git pull origin main
python implementation/version_cli.py init
python implementation/version_cli.py status
```

## 🎯 Integration Instructions for New Features

### 1. Add Constitutional Protection:
```python
# For any new endpoint
@constitutional_endpoint()
async def new_feature():
    # Your code here
    pass
```

### 2. Create Constitutional Version:
```bash
python implementation/version_cli.py create "Added [feature] with Bulgarian mango farmer support"
```

### 3. Deploy with Monitoring:
```bash
python implementation/deployment_automation.py --commit "Constitutional [feature]" --deploy all
```

### 4. Verify Compliance:
```bash
# Check dashboard
python implementation/version_dashboard.py
# Visit http://localhost:8081

# Verify constitutional compliance
python implementation/version_cli.py status
```

## 📊 Key Metrics to Monitor

- **Constitutional Compliance Score**: Should be ≥80%
- **MANGO RULE Status**: Must be PASS
- **Version Synchronization**: Local vs AWS alignment
- **Service Health**: All AWS services online
- **Deployment Success Rate**: Successful deployments

## 🌾 The Bulgarian Mango Farmer Test

**Ultimate validation question**: *"Would this work for a Bulgarian farmer trying to grow mangoes?"*

If the answer is NO to any of these, it violates the constitution:
- Can they get crop advice? ✅
- In their language? ✅  
- For their exotic crop? ✅
- Without discrimination? ✅
- With helpful guidance? ✅

## 🎉 Success Indicators

Your system is constitutionally compliant when:
- ✅ Constitutional compliance score ≥80%
- ✅ MANGO RULE status: PASS
- ✅ All services synchronized with AWS
- ✅ No critical constitutional violations
- ✅ Bulgarian mango farmer scenario works
- ✅ All 13 principles validated

## 🚀 Repository Status

**Current Status**: All constitutional systems deployed and operational
**Last Major Update**: Constitutional Compliance & Version Management Systems
**Git Status**: Pushed to main branch
**Production Ready**: ✅ Yes

---

## 📞 Quick Reference Commands

```bash
# Status check
python implementation/version_cli.py status

# Constitutional compliance
python -c "from implementation.constitutional_checker import *; import asyncio; asyncio.run(check_code_compliance('your_code.py'))"

# Version management
python implementation/version_cli.py create "Description"
python implementation/version_cli.py compare
python implementation/version_cli.py deploy monitoring-dashboards

# Dashboard
python implementation/version_dashboard.py

# Emergency
git pull origin main && python implementation/version_cli.py init
```

---

**Remember: The MANGO RULE is supreme. If it doesn't work for a Bulgarian mango farmer, it doesn't work at all!** 🥭🏛️

*This document contains everything Claude Code needs to work with AVA OLO constitutional systems. No additional uploads required.*