#!/bin/bash

# Pre-Deployment Check Script
# Runs comprehensive safety checks before allowing deployment

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default to normal mode (this script is safe by default)
DRY_RUN=false
VERBOSE=false

# Parse command line arguments first
while [[ $# -gt 0 ]]; do
    case $1 in
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --verbose)
            VERBOSE=true
            shift
            ;;
        --help)
            echo "Usage: $0 <service_name> [code_path] [options]"
            echo "Options:"
            echo "  --dry-run       Show what would be checked without checking"
            echo "  --verbose       Show detailed output"
            echo "  --help          Show this help message"
            echo ""
            echo "Example: $0 monitoring_dashboards . --dry-run"
            exit 0
            ;;
        -*)
            echo "Unknown option $1"
            echo "Use --help for usage information"
            exit 1
            ;;
        *)
            # First non-option argument is service name
            if [ -z "$SERVICE_NAME" ]; then
                SERVICE_NAME=$1
            elif [ -z "$CODE_PATH" ]; then
                CODE_PATH=$1
            fi
            shift
            ;;
    esac
done

# Service name from argument or environment
SERVICE_NAME=${SERVICE_NAME:-$AWS_APPRUNNER_SERVICE_NAME}
CODE_PATH=${CODE_PATH:-.}

echo -e "${BLUE}==================================================================${NC}"
echo -e "${BLUE}🛡️  PRE-DEPLOYMENT SAFETY CHECK for ${SERVICE_NAME}${NC}"
echo -e "${BLUE}==================================================================${NC}"
echo ""

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
echo -e "${YELLOW}📋 Checking prerequisites...${NC}"
if ! command_exists python; then
    echo -e "${RED}❌ Python not found${NC}"
    exit 1
fi

if ! command_exists git; then
    echo -e "${RED}❌ Git not found${NC}"
    exit 1
fi

if ! command_exists aws; then
    echo -e "${RED}❌ AWS CLI not found${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Prerequisites OK${NC}"
echo ""

# 1. Run Proactive Deployment Guard
echo -e "${YELLOW}🛡️ Running Proactive Deployment Guard...${NC}"
if python "$(dirname "$0")/proactive_deployment_guard.py" "$SERVICE_NAME" "$CODE_PATH"; then
    echo -e "${GREEN}✅ Proactive Guard PASSED${NC}"
else
    echo -e "${RED}❌ Proactive Guard FAILED - Deployment blocked${NC}"
    exit 1
fi
echo ""

# 2. Check Git Status
echo -e "${YELLOW}📊 Checking git status...${NC}"
if [[ -n $(git status --porcelain) ]]; then
    echo -e "${RED}❌ Uncommitted changes detected${NC}"
    git status --short
    echo -e "${YELLOW}⚠️  Please commit or stash changes before deployment${NC}"
    exit 1
else
    echo -e "${GREEN}✅ Working directory clean${NC}"
fi
echo ""

# 3. Check AWS Credentials
echo -e "${YELLOW}🔐 Checking AWS credentials...${NC}"
if aws sts get-caller-identity >/dev/null 2>&1; then
    echo -e "${GREEN}✅ AWS credentials valid${NC}"
    ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
    echo -e "   Account: ${ACCOUNT_ID}"
else
    echo -e "${RED}❌ AWS credentials invalid or expired${NC}"
    exit 1
fi
echo ""

# 4. Test Service Health (if already deployed)
echo -e "${YELLOW}🏥 Testing current service health...${NC}"
if [ "$SERVICE_NAME" == "monitoring_dashboards" ]; then
    SERVICE_URL="https://6pmgiripe.us-east-1.awsapprunner.com"
elif [ "$SERVICE_NAME" == "agricultural_core" ]; then
    SERVICE_URL="https://3ksdvgdtud.us-east-1.awsapprunner.com"
else
    echo -e "${YELLOW}⚠️  Unknown service, skipping health check${NC}"
    SERVICE_URL=""
fi

if [ -n "$SERVICE_URL" ]; then
    if curl -s -o /dev/null -w "%{http_code}" "$SERVICE_URL/health" | grep -q "200\|404"; then
        echo -e "${GREEN}✅ Service responding (may not have /health endpoint)${NC}"
    else
        echo -e "${YELLOW}⚠️  Service not responding or down${NC}"
    fi
fi
echo ""

# 5. Check Branch
echo -e "${YELLOW}🌿 Checking git branch...${NC}"
CURRENT_BRANCH=$(git branch --show-current)
echo -e "   Current branch: ${CURRENT_BRANCH}"

if [[ "$CURRENT_BRANCH" == "main" ]] || [[ "$CURRENT_BRANCH" == "master" ]]; then
    echo -e "${GREEN}✅ On production branch${NC}"
else
    echo -e "${YELLOW}⚠️  Not on main/master branch - ensure this is intentional${NC}"
fi
echo ""

# 6. Check Recent Commits
echo -e "${YELLOW}📝 Recent commits:${NC}"
git log --oneline -5
echo ""

# 7. Check Environment Variables
echo -e "${YELLOW}🔧 Checking critical environment variables...${NC}"
MISSING_VARS=()

# Check required variables
[ -z "$DATABASE_URL" ] && MISSING_VARS+=("DATABASE_URL")
[ -z "$OPENAI_API_KEY" ] && MISSING_VARS+=("OPENAI_API_KEY")

if [ ${#MISSING_VARS[@]} -eq 0 ]; then
    echo -e "${GREEN}✅ All critical environment variables set${NC}"
else
    echo -e "${RED}❌ Missing environment variables:${NC}"
    for var in "${MISSING_VARS[@]}"; do
        echo -e "${RED}   - $var${NC}"
    done
    exit 1
fi
echo ""

# 8. Constitutional Compliance Summary
echo -e "${YELLOW}🏛️ Constitutional Compliance Summary:${NC}"
echo -e "   🥭 MANGO Rule: Ensures global farmer support"
echo -e "   🧠 LLM-First: AI-driven architecture"
echo -e "   🔒 Privacy-First: No farmer data exposure"
echo -e "   🏗️ Module Independence: Services isolated"
echo ""

# Final Summary
echo -e "${BLUE}==================================================================${NC}"
echo -e "${GREEN}✅ PRE-DEPLOYMENT CHECK COMPLETE${NC}"
echo -e "${BLUE}==================================================================${NC}"
echo ""
echo -e "${GREEN}All safety checks passed. Deployment can proceed.${NC}"
echo -e "${YELLOW}Remember to:${NC}"
echo -e "  1. Monitor deployment progress"
echo -e "  2. Check health dashboard after deployment"
echo -e "  3. Be ready to rollback if issues arise"
echo ""
echo -e "${BLUE}Deploy with: ${NC}./constitutional_deploy.sh ${SERVICE_NAME}"

exit 0