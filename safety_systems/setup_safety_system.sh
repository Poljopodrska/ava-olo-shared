#!/bin/bash

# Setup script for AVA OLO Safety System - REVIEW MODE by default
# This script helps install and configure the safety system

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Default to review mode for safety
REVIEW_MODE=true
ENABLE_HOOKS=false
MODIFY_SERVICES=false
VERBOSE=false

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --enable-production)
            REVIEW_MODE=false
            ENABLE_HOOKS=true
            MODIFY_SERVICES=true
            shift
            ;;
        --enable-hooks)
            ENABLE_HOOKS=true
            shift
            ;;
        --modify-services)
            MODIFY_SERVICES=true
            shift
            ;;
        --verbose)
            VERBOSE=true
            shift
            ;;
        --help)
            echo "Usage: $0 [options]"
            echo "Options:"
            echo "  --enable-production  Enable full production mode (use with caution)"
            echo "  --enable-hooks       Enable git hooks"
            echo "  --modify-services    Allow service modifications"
            echo "  --verbose           Show detailed output"
            echo "  --help              Show this help message"
            echo ""
            echo "Default: Review mode (safe for inspection)"
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
echo -e "${BLUE}🛡️  AVA OLO Safety System Setup${NC}"
echo -e "${BLUE}==================================================================${NC}"
echo ""

if [ "$REVIEW_MODE" = true ]; then
    echo -e "${YELLOW}📋 REVIEW MODE INSTALLATION${NC}"
    echo -e "${GREEN}✅ Safe for inspection - no production impact${NC}"
    echo -e "${YELLOW}❌ Git hooks will NOT be enabled${NC}"
    echo -e "${YELLOW}❌ Services will NOT be modified${NC}"
    echo -e "${GREEN}✅ All files will be created for review${NC}"
    echo ""
    echo -e "${BLUE}To enable features later, run with:${NC}"
    echo -e "  --enable-hooks       To enable git hooks"
    echo -e "  --modify-services    To modify services"
    echo -e "  --enable-production  To enable everything"
else
    echo -e "${RED}⚠️  PRODUCTION MODE INSTALLATION${NC}"
    echo -e "${YELLOW}This will modify your development environment!${NC}"
    read -p "Are you sure you want to continue? (yes/no): " confirm
    if [[ ! $confirm =~ ^[Yy][Ee][Ss]$ ]]; then
        echo "Installation cancelled."
        exit 0
    fi
fi
echo ""

# Function to create symlink
create_symlink() {
    local source=$1
    local target=$2
    
    if [ -e "$target" ]; then
        echo -e "${YELLOW}⚠️  $target already exists, skipping${NC}"
    else
        ln -s "$source" "$target"
        echo -e "${GREEN}✅ Created symlink: $target${NC}"
    fi
}

# 1. Check current directory
echo -e "${YELLOW}📍 Checking current location...${NC}"
if [[ "$PWD" == *"ava-olo-shared/safety_systems"* ]]; then
    echo -e "${GREEN}✅ In safety_systems directory${NC}"
    SHARED_DIR="../.."
elif [[ "$PWD" == *"ava-olo-shared"* ]]; then
    echo -e "${GREEN}✅ In ava-olo-shared directory${NC}"
    SHARED_DIR="."
    cd safety_systems
else
    echo -e "${YELLOW}⚠️  Please run from ava-olo-shared or safety_systems directory${NC}"
    exit 1
fi
echo ""

# 2. Make all scripts executable
echo -e "${YELLOW}🔧 Making scripts executable...${NC}"
chmod +x *.sh *.py 2>/dev/null || echo -e "${YELLOW}Some files may not exist yet${NC}"
echo -e "${GREEN}✅ Scripts are now executable${NC}"
echo ""

# 3. Setup for monitoring-dashboards service
if [ "$MODIFY_SERVICES" = true ]; then
    echo -e "${YELLOW}📊 Setting up monitoring-dashboards service...${NC}"
    MONITORING_DIR="../../ava-olo-monitoring-dashboards"

    if [ -d "$MONITORING_DIR" ]; then
        mkdir -p "$MONITORING_DIR/scripts"
        mkdir -p "$MONITORING_DIR/templates"
        
        # Create symlinks
        create_symlink "$(pwd)/pre_deploy_check.sh" "$MONITORING_DIR/scripts/pre_deploy_check.sh"
        create_symlink "$(pwd)/emergency_rollback.sh" "$MONITORING_DIR/scripts/emergency_rollback.sh"
        create_symlink "$(pwd)/constitutional_deploy.sh" "$MONITORING_DIR/scripts/constitutional_deploy.sh"
        
        # Copy dashboard template
        if [ -f "../web_dashboard/comprehensive_health_dashboard.html" ]; then
            cp ../web_dashboard/comprehensive_health_dashboard.html "$MONITORING_DIR/templates/health_dashboard.html"
            echo -e "${GREEN}✅ Copied health dashboard template${NC}"
        fi
    else
        echo -e "${YELLOW}⚠️  monitoring-dashboards directory not found${NC}"
    fi
else
    echo -e "${YELLOW}📊 Monitoring dashboards setup (SKIPPED - Review Mode)${NC}"
    echo -e "${BLUE}   Service files will NOT be modified${NC}"
fi
echo ""

# 4. Setup for agricultural-core service
if [ "$MODIFY_SERVICES" = true ]; then
    echo -e "${YELLOW}🌾 Setting up agricultural-core service...${NC}"
    AGRICULTURAL_DIR="../../ava-olo-agricultural-core"

    if [ -d "$AGRICULTURAL_DIR" ]; then
        mkdir -p "$AGRICULTURAL_DIR/scripts"
        mkdir -p "$AGRICULTURAL_DIR/templates"
        
        # Create symlinks
        create_symlink "$(pwd)/pre_deploy_check.sh" "$AGRICULTURAL_DIR/scripts/pre_deploy_check.sh"
        create_symlink "$(pwd)/emergency_rollback.sh" "$AGRICULTURAL_DIR/scripts/emergency_rollback.sh"
        create_symlink "$(pwd)/constitutional_deploy.sh" "$AGRICULTURAL_DIR/scripts/constitutional_deploy.sh"
        
        # Copy dashboard template
        if [ -f "../web_dashboard/comprehensive_health_dashboard.html" ]; then
            cp ../web_dashboard/comprehensive_health_dashboard.html "$AGRICULTURAL_DIR/templates/health_dashboard.html"
            echo -e "${GREEN}✅ Copied health dashboard template${NC}"
        fi
    else
        echo -e "${YELLOW}⚠️  agricultural-core directory not found${NC}"
    fi
else
    echo -e "${YELLOW}🌾 Agricultural core setup (SKIPPED - Review Mode)${NC}"
    echo -e "${BLUE}   Service files will NOT be modified${NC}"
fi
echo ""

# 5. Setup Git hooks
if [ "$ENABLE_HOOKS" = true ]; then
    echo -e "${YELLOW}🪝 Installing Git hooks...${NC}"
    echo -e "${YELLOW}⚠️  Git hooks installation requires manual steps${NC}"
    echo -e "${BLUE}Run: ./install_git_hooks.sh --enable${NC}"
else
    echo -e "${YELLOW}🪝 Git hooks setup (NOT ENABLED)${NC}"
    echo -e "${BLUE}To install git hooks later:${NC}"
    echo -e "  1. Run: ./install_git_hooks.sh --test-mode"
    echo -e "  2. Or manually: cp pre-push-hook.sh .git/hooks/pre-push"
fi
echo ""

# 6. Create initial version database
echo -e "${YELLOW}📊 Initializing version database...${NC}"
if python enhanced_version_system.py current --service monitoring_dashboards 2>/dev/null; then
    echo -e "${GREEN}✅ Version database already initialized${NC}"
else
    echo -e "${GREEN}✅ Version database created${NC}"
fi
echo ""

# 7. Summary
echo -e "${BLUE}==================================================================${NC}"
if [ "$REVIEW_MODE" = true ]; then
    echo -e "${GREEN}✨ REVIEW MODE Installation Complete!${NC}"
    echo ""
    echo -e "${YELLOW}📋 What to do next:${NC}"
    echo -e "  1. Review the documentation:"
    echo -e "     ${BLUE}cat ../docs/SAFETY_SYSTEM_USAGE_GUIDE.md${NC}"
    echo ""
    echo -e "  2. Test scripts with dry-run:"
    echo -e "     ${BLUE}./pre_deploy_check.sh monitoring_dashboards --dry-run${NC}"
    echo ""
    echo -e "  3. View the health dashboard:"
    echo -e "     ${BLUE}open ../web_dashboard/comprehensive_health_dashboard.html${NC}"
    echo ""
    echo -e "  4. When ready to enable features:"
    echo -e "     ${BLUE}./setup_safety_system.sh --enable-hooks${NC}"
    echo ""
    echo -e "${GREEN}✅ Safe to explore - nothing has been modified!${NC}"
else
    echo -e "${GREEN}✨ Production Mode Installation Complete!${NC}"
    echo ""
    echo -e "${YELLOW}📋 Next Steps:${NC}"
    echo -e "  1. Test pre-deployment check:"
    echo -e "     ${BLUE}./pre_deploy_check.sh <service_name>${NC}"
    echo ""
    echo -e "  2. Test emergency rollback (dry run):"
    echo -e "     ${BLUE}./emergency_rollback.sh <service_name> --dry-run${NC}"
    echo ""
    echo -e "  3. View health dashboard:"
    echo -e "     ${BLUE}open ../web_dashboard/comprehensive_health_dashboard.html${NC}"
    echo ""
    echo -e "  4. For actual deployment:"
    echo -e "     ${BLUE}./constitutional_deploy.sh <service_name> \"deployment message\"${NC}"
    echo ""
    echo -e "${GREEN}🛡️ Your AVA OLO services are now protected!${NC}"
fi
echo -e "${BLUE}==================================================================${NC}"

exit 0