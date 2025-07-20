# AVA OLO Quick Start

## What We're Building
Agricultural CRM for global farmers. WhatsApp interface, AI-powered intelligence, works for any crop in any country.

## Current System Status
- **Version**: 3.0.0-forensic-cache-bust
- **Architecture**: Module-based, PostgreSQL-only, AWS deployed
- **Active Modules**: Core CRM, WhatsApp integration, LLM service
- **Core Intelligence**: CAVA (Conversation Architecture for AVA) - Four-database system powering all farmer interactions

## AWS Services Architecture
### **ava-olo-agricultural-core-fresh**
- **Purpose**: Main farmer application (registration, chat, WhatsApp integration)
- **Current Version**: v3.x.x series
- **Features**: CAVA-powered registration, agricultural chat, farmer authentication
- **URL**: https://ujvej9snpp.us-east-1.awsapprunner.com

### **ava-olo-monitoring-dashboards-fresh**
- **Purpose**: Business intelligence and monitoring dashboards
- **Current Version**: v2.x.x series  
- **Features**: Farmer statistics, field metrics, performance monitoring, database health
- **URL**: https://bcibj8ws3x.us-east-1.awsapprunner.com

## The MANGO RULE 🥭
**Supreme Test**: "Would this work for a Bulgarian mango farmer?"
- If NO → Redesign immediately
- Tests global scalability, no hardcoding, cultural neutrality

## Top 6 Constitutional Principles

1. **LLM-FIRST** - AI makes decisions, not hardcoded rules
2. **PRIVACY-FIRST** - Farmer data never exposed, encrypted always
3. **GLOBAL-FIRST** - Works for any crop, any country, any language
4. **WHATSAPP-FIRST** - Primary interface for all farmers
5. **DESIGN-FIRST** - Constitutional design system (brown/olive, 18px+, Enter key)
6. **POSTGRESQL-ONLY** - Single database technology, no exceptions

## Quick Links
- **Full Constitution**: [AVA_OLO_CONSTITUTION.md](AVA_OLO_CONSTITUTION.md)
- **Write Specs**: [SPECIFICATION_GUIDELINES.md](SPECIFICATION_GUIDELINES.md)
- **Implementation**: [IMPLEMENTATION_GUIDELINES.md](IMPLEMENTATION_GUIDELINES.md)
- **System Changelog**: [SYSTEM_CHANGELOG.md](SYSTEM_CHANGELOG.md) *(ALL changes - deployments + refactoring)*
- **CAVA Architecture**: [CAVA_TECHNICAL_SPECIFICATION.md](CAVA_TECHNICAL_SPECIFICATION.md)

## For New Chat Sessions
1. Read this file first
2. Check SYSTEM_CHANGELOG.md for recent changes
3. Use SPECIFICATION_GUIDELINES.md to write new features
4. Follow IMPLEMENTATION_GUIDELINES.md for Claude Code

## Success Metrics
- ✓ Passes MANGO RULE
- ✓ No hardcoded logic
- ✓ Works offline after sync
- ✓ Farmer understands without training
- ✓ Deploys with version verification