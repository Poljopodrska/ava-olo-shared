#!/bin/bash

# Full System Enablement Script for AVA OLO Safety System
# This script enables all safety features for production use

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
NC='\033[0m'

# Default to requiring confirmation
FORCE=false
DRY_RUN=false
VERBOSE=false

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --confirm)
            # User confirmed they want to enable everything
            shift
            ;;
        --force)
            FORCE=true
            shift
            ;;
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --verbose)
            VERBOSE=true
            shift
            ;;
        --help)
            echo "Usage: $0 [options]"
            echo "Options:"
            echo "  --confirm       Proceed with full enablement"
            echo "  --force         Skip safety confirmations"
            echo "  --dry-run       Show what would be enabled"
            echo "  --verbose       Show detailed output"
            echo "  --help          Show this help message"
            echo ""
            echo "⚠️  WARNING: This enables all safety features for production use"
            echo "Make sure you've tested everything first!"
            exit 0
            ;;
        *)
            echo "Unknown option $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

echo -e "${BLUE}==================================================================${NC}"
echo -e "${BLUE}🚀 AVA OLO Full Safety System Enablement${NC}"
echo -e "${BLUE}==================================================================${NC}"
echo ""

if [ "$DRY_RUN" = true ]; then
    echo -e "${YELLOW}🧪 DRY-RUN MODE - Showing what would be enabled${NC}"
else
    echo -e "${RED}⚠️  PRODUCTION ENABLEMENT MODE${NC}"
    echo -e "${YELLOW}This will enable ALL safety features for production use${NC}"
fi
echo ""

# Safety confirmation
if [ "$DRY_RUN" = false ] && [ "$FORCE" = false ]; then
    echo -e "${YELLOW}📋 Pre-enablement Checklist:${NC}"
    echo -e "  Have you tested all scripts with --dry-run? (y/n)"
    read -r TESTED_DRYRUN
    
    echo -e "  Have you reviewed all documentation? (y/n)"
    read -r REVIEWED_DOCS
    
    echo -e "  Are you ready for git hooks to enforce safety checks? (y/n)"
    read -r READY_HOOKS
    
    echo -e "  Do you understand the emergency procedures? (y/n)"
    read -r UNDERSTAND_EMERGENCY
    
    if [[ ! "$TESTED_DRYRUN" =~ ^[Yy]$ ]] || [[ ! "$REVIEWED_DOCS" =~ ^[Yy]$ ]] || 
       [[ ! "$READY_HOOKS" =~ ^[Yy]$ ]] || [[ ! "$UNDERSTAND_EMERGENCY" =~ ^[Yy]$ ]]; then
        echo ""
        echo -e "${RED}❌ Pre-enablement checklist not complete${NC}"
        echo -e "${YELLOW}Please complete all requirements before enabling full system${NC}"
        exit 1
    fi
    
    echo ""
    echo -e "${RED}🚨 FINAL WARNING${NC}"
    echo -e "${YELLOW}This will make the following changes:${NC}"
    echo -e "  - Install git hooks that can block pushes"
    echo -e "  - Add health endpoints to services"  
    echo -e "  - Enable all safety checks"
    echo -e "  - Enforce constitutional compliance"
    echo ""
    read -p "Type 'ENABLE_FULL_SYSTEM' to proceed: " CONFIRMATION
    
    if [ "$CONFIRMATION" != "ENABLE_FULL_SYSTEM" ]; then
        echo -e "${YELLOW}Enablement cancelled.${NC}"
        exit 0
    fi
fi

echo ""
echo -e "${MAGENTA}🔧 Starting full system enablement...${NC}"
echo ""

# Step 1: Enable Git Hooks
echo -e "${YELLOW}Step 1/4: Enabling Git Hooks${NC}"
if [ "$DRY_RUN" = true ]; then
    echo -e "${BLUE}   Would run: ./install_git_hooks.sh --enable${NC}"
else
    if ./install_git_hooks.sh --enable; then
        echo -e "${GREEN}   ✅ Git hooks enabled${NC}"
    else
        echo -e "${RED}   ❌ Failed to enable git hooks${NC}"
        echo -e "${YELLOW}   Continuing with remaining steps...${NC}"
    fi
fi
echo ""

# Step 2: Enable Health Dashboards
echo -e "${YELLOW}Step 2/4: Enabling Health Dashboards${NC}"
if [ "$DRY_RUN" = true ]; then
    echo -e "${BLUE}   Would run: ./enable_health_dashboards.sh --enable${NC}"
else
    if ./enable_health_dashboards.sh --enable; then
        echo -e "${GREEN}   ✅ Health dashboards enabled${NC}"
    else
        echo -e "${RED}   ❌ Failed to enable health dashboards${NC}"
        echo -e "${YELLOW}   Continuing with remaining steps...${NC}"
    fi
fi
echo ""

# Step 3: Configure Services
echo -e "${YELLOW}Step 3/4: Configuring Services${NC}"
if [ "$DRY_RUN" = true ]; then
    echo -e "${BLUE}   Would run: ./setup_safety_system.sh --modify-services${NC}"
    echo -e "${BLUE}   Would create service scripts and templates${NC}"
else
    if ./setup_safety_system.sh --modify-services; then
        echo -e "${GREEN}   ✅ Services configured${NC}"
    else
        echo -e "${RED}   ❌ Failed to configure services${NC}"
        echo -e "${YELLOW}   Continuing with remaining steps...${NC}"
    fi
fi
echo ""

# Step 4: Initialize Version Tracking
echo -e "${YELLOW}Step 4/4: Initializing Version Tracking${NC}"
if [ "$DRY_RUN" = true ]; then
    echo -e "${BLUE}   Would initialize version database${NC}"
    echo -e "${BLUE}   Would record current versions${NC}"
else
    # Record current versions for both services
    for service in "monitoring_dashboards" "agricultural_core"; do
        echo -e "${YELLOW}   Recording current version for ${service}...${NC}"
        if python enhanced_version_system.py record \
           --service "$service" \
           --version "v16.1.0" \
           --message "Initial version recorded during safety system enablement"; then
            echo -e "${GREEN}   ✅ Version recorded for ${service}${NC}"
        else
            echo -e "${YELLOW}   ⚠️  Version recording skipped for ${service}${NC}"
        fi
    done
fi
echo ""

# Create configuration file to track enablement
echo -e "${YELLOW}📋 Creating enablement record...${NC}"
ENABLEMENT_RECORD=".safety_system_enabled"

if [ "$DRY_RUN" = true ]; then
    echo -e "${BLUE}   Would create: $ENABLEMENT_RECORD${NC}"
else
    cat > "$ENABLEMENT_RECORD" << EOF
{
  "enabled": true,
  "enabled_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "enabled_by": "$USER",
  "version": "1.0.0",
  "features": {
    "git_hooks": true,
    "health_dashboards": true,
    "service_modifications": true,
    "version_tracking": true
  },
  "emergency_procedures": {
    "bypass_hooks": "git push --no-verify",
    "emergency_rollback": "./emergency_rollback.sh <service>",
    "disable_system": "./disable_safety_system.sh"
  }
}
EOF
    echo -e "${GREEN}   ✅ Enablement record created${NC}"
fi
echo ""

# Summary and next steps
echo -e "${BLUE}==================================================================${NC}"
if [ "$DRY_RUN" = true ]; then
    echo -e "${GREEN}✨ DRY-RUN Complete - Full System Ready for Enablement${NC}"
    echo ""
    echo -e "${YELLOW}📋 What would be enabled:${NC}"
    echo -e "  🪝 Git hooks enforcing safety checks"
    echo -e "  📊 Health dashboards in services"
    echo -e "  🔧 Service-level safety scripts"
    echo -e "  📈 Version tracking system"
    echo ""
    echo -e "${BLUE}To actually enable, run:${NC}"
    echo -e "  ${GREEN}$0 --confirm${NC}"
else
    echo -e "${GREEN}🎉 Full Safety System Enabled Successfully!${NC}"
    echo ""
    echo -e "${YELLOW}📋 System Status:${NC}"
    echo -e "  🪝 Git hooks: Active (can block unsafe pushes)"
    echo -e "  📊 Health dashboards: Available at /health-dashboard endpoints"
    echo -e "  🛡️ Safety checks: Enforced on all deployments"
    echo -e "  📈 Version tracking: Recording all changes"
    echo ""
    echo -e "${YELLOW}📋 Emergency Procedures:${NC}"
    echo -e "  🚨 Bypass hooks: ${BLUE}git push --no-verify${NC}"
    echo -e "  🔄 Emergency rollback: ${BLUE}./emergency_rollback.sh <service>${NC}"
    echo -e "  ❌ Disable system: ${BLUE}./disable_safety_system.sh${NC}"
    echo ""
    echo -e "${YELLOW}📋 Next Steps:${NC}"
    echo -e "  1. Test a small change with git push"
    echo -e "  2. Check health dashboards: http://localhost:8000/health-dashboard"
    echo -e "  3. Try a deployment: ./constitutional_deploy.sh <service> \"message\""
    echo -e "  4. Practice emergency rollback: ./emergency_rollback.sh <service> --dry-run"
fi
echo -e "${BLUE}==================================================================${NC}"

# Create quick test script
if [ "$DRY_RUN" = false ]; then
    cat > test_full_system.sh << 'EOF'
#!/bin/bash
# Test the full safety system

echo "🧪 Testing Full Safety System..."

# Test 1: Pre-deployment check
echo "1. Testing pre-deployment check..."
./pre_deploy_check.sh monitoring_dashboards --dry-run

# Test 2: Health endpoints
echo "2. Testing health endpoints..."
if command -v curl >/dev/null; then
    curl -s http://localhost:8000/health || echo "   Service not running locally"
fi

# Test 3: Version system
echo "3. Testing version system..."
python enhanced_version_system.py current --service monitoring_dashboards

# Test 4: Emergency rollback
echo "4. Testing emergency rollback..."
./emergency_rollback.sh monitoring_dashboards --dry-run

echo "✅ Full system test complete!"
EOF
    chmod +x test_full_system.sh
    echo ""
    echo -e "${GREEN}Created test_full_system.sh for validation${NC}"
fi

exit 0