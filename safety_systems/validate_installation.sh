#!/bin/bash

# Installation Validation Script for AVA OLO Safety System
# Validates that all components are properly installed and ready for use

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}==================================================================${NC}"
echo -e "${BLUE}✅ AVA OLO Safety System Installation Validation${NC}"
echo -e "${BLUE}==================================================================${NC}"
echo ""

TOTAL_CHECKS=0
PASSED_CHECKS=0

# Function to run a check
run_check() {
    local description=$1
    local command=$2
    
    TOTAL_CHECKS=$((TOTAL_CHECKS + 1))
    echo -n "  $description... "
    
    if eval "$command" >/dev/null 2>&1; then
        echo -e "${GREEN}✅${NC}"
        PASSED_CHECKS=$((PASSED_CHECKS + 1))
        return 0
    else
        echo -e "${RED}❌${NC}"
        return 1
    fi
}

# 1. Check Documentation
echo -e "${YELLOW}📚 Documentation Checks${NC}"
run_check "Master implementation plan exists" "[ -f '../docs/SAFETY_SYSTEM_IMPLEMENTATION_PLAN.md' ]"
run_check "Usage guide exists" "[ -f '../docs/SAFETY_SYSTEM_USAGE_GUIDE.md' ]"
run_check "Safety system README exists" "[ -f 'README.md' ]"
echo ""

# 2. Check Core Scripts
echo -e "${YELLOW}🛡️ Core Safety Scripts${NC}"
run_check "Proactive deployment guard exists" "[ -f 'proactive_deployment_guard.py' ]"
run_check "Pre-deployment check script exists" "[ -f 'pre_deploy_check.sh' ]"
run_check "Emergency rollback script exists" "[ -f 'emergency_rollback.sh' ]"
run_check "Constitutional deploy script exists" "[ -f 'constitutional_deploy.sh' ]"
run_check "Enhanced version system exists" "[ -f 'enhanced_version_system.py' ]"
echo ""

# 3. Check Setup Scripts
echo -e "${YELLOW}🔧 Setup and Configuration Scripts${NC}"
run_check "Main setup script exists" "[ -f 'setup_safety_system.sh' ]"
run_check "Git hooks installer exists" "[ -f 'install_git_hooks.sh' ]"
run_check "Health dashboard enabler exists" "[ -f 'enable_health_dashboards.sh' ]"
run_check "Full system enabler exists" "[ -f 'enable_full_system.sh' ]"
echo ""

# 4. Check Dashboard Templates
echo -e "${YELLOW}📊 Dashboard Templates${NC}"
run_check "Comprehensive dashboard exists" "[ -f '../web_dashboard/comprehensive_health_dashboard.html' ]"
run_check "Monitoring dashboard template exists" "[ -f '../templates/health_dashboard_monitoring.html' ]"
run_check "Agricultural dashboard template exists" "[ -f '../templates/health_dashboard_agricultural.html' ]"
echo ""

# 5. Check Script Permissions
echo -e "${YELLOW}🔑 Script Permissions${NC}"
run_check "Setup script is executable" "[ -x 'setup_safety_system.sh' ]"
run_check "Emergency rollback is executable" "[ -x 'emergency_rollback.sh' ]"
run_check "Pre-deploy check is executable" "[ -x 'pre_deploy_check.sh' ]"
run_check "Constitutional deploy is executable" "[ -x 'constitutional_deploy.sh' ]"
run_check "Git hooks installer is executable" "[ -x 'install_git_hooks.sh' ]"
echo ""

# 6. Check Safety Flags
echo -e "${YELLOW}🏁 Safety Flag Tests${NC}"
run_check "Setup script has help flag" "./setup_safety_system.sh --help | grep -q 'Usage:'"
run_check "Git hooks has test mode" "./install_git_hooks.sh --help | grep -q 'test-mode'"
run_check "Health dashboards has dry-run" "./enable_health_dashboards.sh --help | grep -q 'dry-run'"
run_check "Emergency rollback has dry-run" "./emergency_rollback.sh monitoring_dashboards --help | grep -q 'dry-run'"
echo ""

# 7. Check Python Syntax
echo -e "${YELLOW}🐍 Python Script Validation${NC}"
if command -v python3 >/dev/null; then
    run_check "Proactive guard syntax is valid" "python3 -m py_compile proactive_deployment_guard.py"
    run_check "Version system syntax is valid" "python3 -m py_compile enhanced_version_system.py"
    run_check "Proactive guard dry-run works" "python3 proactive_deployment_guard.py monitoring_dashboards --dry-run | grep -q 'DRY-RUN MODE'"
else
    echo -e "  ${YELLOW}⚠️  Python3 not available - skipping Python validation${NC}"
fi
echo ""

# 8. Test Dry-Run Modes
echo -e "${YELLOW}🧪 Dry-Run Mode Tests${NC}"
run_check "Emergency rollback dry-run works" "./emergency_rollback.sh monitoring_dashboards --dry-run | grep -q 'DRY-RUN'"
run_check "Health dashboard dry-run works" "./enable_health_dashboards.sh --dry-run | grep -q 'DRY-RUN'"
run_check "Full system dry-run works" "./enable_full_system.sh --dry-run | grep -q 'DRY-RUN'"
echo ""

# 9. Check Directory Structure
echo -e "${YELLOW}📁 Directory Structure${NC}"
run_check "Safety systems directory exists" "[ -d '.' ]"
run_check "Web dashboard directory exists" "[ -d '../web_dashboard' ]"
run_check "Templates directory exists" "[ -d '../templates' ]"
run_check "Documentation directory exists" "[ -d '../docs' ]"
echo ""

# Summary
echo -e "${BLUE}==================================================================${NC}"
PERCENTAGE=$((PASSED_CHECKS * 100 / TOTAL_CHECKS))

if [ $PASSED_CHECKS -eq $TOTAL_CHECKS ]; then
    echo -e "${GREEN}🎉 Installation Validation Complete!${NC}"
    echo -e "${GREEN}All ${TOTAL_CHECKS} checks passed (100%)${NC}"
    echo ""
    echo -e "${YELLOW}📋 System Status: Ready for Review${NC}"
    echo -e "  ✅ All files installed correctly"
    echo -e "  ✅ All scripts have proper permissions"
    echo -e "  ✅ All safety flags working"
    echo -e "  ✅ Dry-run modes functional"
    echo ""
    echo -e "${BLUE}Next Steps:${NC}"
    echo -e "  1. Review documentation: cat ../docs/SAFETY_SYSTEM_USAGE_GUIDE.md"
    echo -e "  2. Test individual components with --dry-run flags"
    echo -e "  3. When ready, start with: ./setup_safety_system.sh"
elif [ $PERCENTAGE -ge 90 ]; then
    echo -e "${YELLOW}⚠️  Installation Mostly Complete${NC}"
    echo -e "${YELLOW}${PASSED_CHECKS} of ${TOTAL_CHECKS} checks passed (${PERCENTAGE}%)${NC}"
    echo ""
    echo -e "${BLUE}Review failed checks above and fix before proceeding${NC}"
elif [ $PERCENTAGE -ge 75 ]; then
    echo -e "${YELLOW}⚠️  Installation Partially Complete${NC}"
    echo -e "${YELLOW}${PASSED_CHECKS} of ${TOTAL_CHECKS} checks passed (${PERCENTAGE}%)${NC}"
    echo ""
    echo -e "${YELLOW}Several issues found - please review and fix before using${NC}"
else
    echo -e "${RED}❌ Installation Failed${NC}"
    echo -e "${RED}Only ${PASSED_CHECKS} of ${TOTAL_CHECKS} checks passed (${PERCENTAGE}%)${NC}"
    echo ""
    echo -e "${RED}Major issues found - please reinstall${NC}"
fi

echo -e "${BLUE}==================================================================${NC}"

exit 0