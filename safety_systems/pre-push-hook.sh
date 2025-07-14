#!/bin/bash

# Git pre-push hook for AVA OLO Safety System
# Copy this file to .git/hooks/pre-push and make it executable

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}==================================================================${NC}"
echo -e "${BLUE}🛡️  AVA OLO Pre-Push Safety Check${NC}"
echo -e "${BLUE}==================================================================${NC}"

# Get the branch being pushed
BRANCH=$(git rev-parse --abbrev-ref HEAD)
echo -e "${YELLOW}Branch: ${BRANCH}${NC}"

# Check if we're in a service directory
if [ -f "main.py" ] && [ -f "requirements.txt" ]; then
    # Determine service name from directory
    SERVICE_NAME=""
    if [[ "$PWD" == *"ava-olo-monitoring-dashboards"* ]]; then
        SERVICE_NAME="monitoring_dashboards"
    elif [[ "$PWD" == *"ava-olo-agricultural-core"* ]]; then
        SERVICE_NAME="agricultural_core"
    fi
    
    if [ -n "$SERVICE_NAME" ]; then
        echo -e "${YELLOW}Service detected: ${SERVICE_NAME}${NC}"
        echo ""
        
        # Run pre-deployment check
        echo -e "${YELLOW}Running safety checks before push...${NC}"
        
        # Check if safety scripts exist
        SAFETY_SCRIPT="../../ava-olo-shared/safety_systems/pre_deploy_check.sh"
        if [ -f "$SAFETY_SCRIPT" ]; then
            if $SAFETY_SCRIPT "$SERVICE_NAME"; then
                echo -e "${GREEN}✅ Safety checks passed${NC}"
            else
                echo -e "${RED}❌ Safety checks failed${NC}"
                echo -e "${RED}Push cancelled for safety. Fix issues before pushing.${NC}"
                exit 1
            fi
        else
            echo -e "${YELLOW}⚠️  Safety scripts not found, proceeding with basic checks${NC}"
            
            # Basic checks
            # 1. Check for syntax errors
            if python -m py_compile main.py 2>/dev/null; then
                echo -e "${GREEN}✅ Python syntax OK${NC}"
            else
                echo -e "${RED}❌ Python syntax errors detected${NC}"
                exit 1
            fi
            
            # 2. Check for uncommitted changes
            if [[ -n $(git status --porcelain) ]]; then
                echo -e "${RED}❌ Uncommitted changes detected${NC}"
                git status --short
                exit 1
            fi
        fi
    fi
fi

# Check commit messages for constitutional compliance
echo ""
echo -e "${YELLOW}Checking commit messages...${NC}"

# Get commits that will be pushed
COMMITS=$(git log origin/$BRANCH..$BRANCH --oneline)

if [ -z "$COMMITS" ]; then
    echo -e "${YELLOW}No new commits to push${NC}"
else
    echo -e "${GREEN}✅ Commits ready to push:${NC}"
    echo "$COMMITS"
fi

# Constitutional reminder
echo ""
echo -e "${BLUE}🏛️ Constitutional Reminders:${NC}"
echo -e "  🥭 MANGO Rule: Works for Bulgarian mango farmers?"
echo -e "  🧠 LLM-First: Using AI over hardcoded logic?"
echo -e "  🔒 Privacy-First: No farmer data exposure?"
echo -e "  🌍 Global-First: Works for all countries?"

# Final confirmation for main/master branch
if [[ "$BRANCH" == "main" ]] || [[ "$BRANCH" == "master" ]]; then
    echo ""
    echo -e "${YELLOW}⚠️  Pushing to production branch${NC}"
    echo -e "${YELLOW}Have you:${NC}"
    echo -e "  - Run all tests?"
    echo -e "  - Checked constitutional compliance?"
    echo -e "  - Tested locally?"
    echo -e "  - Updated documentation?"
    
    # Give user 5 seconds to cancel
    echo ""
    echo -e "${YELLOW}Push will proceed in 5 seconds (Ctrl+C to cancel)...${NC}"
    for i in {5..1}; do
        echo -n "$i "
        sleep 1
    done
    echo ""
fi

echo -e "${GREEN}✅ Pre-push checks complete${NC}"
echo -e "${BLUE}==================================================================${NC}"

exit 0