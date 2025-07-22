#!/bin/bash
# Pre-deployment validation script
# Prevents common deployment failures before they happen

set -e  # Exit on any error

echo "================================================"
echo "🔍 AVA OLO Pre-Deployment Validation"
echo "================================================"
echo "Time: $(date)"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if we're in the right directory
if [[ ! -f "Dockerfile" ]]; then
    echo -e "${RED}ERROR: No Dockerfile found in current directory${NC}"
    echo "Please run this script from the service root directory"
    exit 1
fi

# Detect which service we're checking
SERVICE_NAME=""
if [[ -d "modules/dashboards" ]]; then
    SERVICE_NAME="monitoring-dashboards"
elif [[ -f "modules/core/config.py" ]]; then
    SERVICE_NAME="agricultural-core"
else
    echo -e "${YELLOW}WARNING: Could not detect service type${NC}"
    SERVICE_NAME="unknown"
fi

echo "Service detected: $SERVICE_NAME"
echo ""

# 1. Validate Dockerfile
echo "1. Validating Dockerfile..."
if grep -q "main.py" Dockerfile && grep -q "main:app" Dockerfile; then
    echo -e "${GREEN}✓ Dockerfile references correct entry point${NC}"
else
    echo -e "${RED}✗ Dockerfile may have incorrect entry point${NC}"
    echo "  Expected: main.py and main:app"
    exit 1
fi

if grep -q "gcc" Dockerfile && grep -q "python3-dev" Dockerfile; then
    echo -e "${GREEN}✓ Dockerfile includes required build dependencies${NC}"
else
    echo -e "${YELLOW}⚠ Dockerfile may be missing gcc/python3-dev for psutil${NC}"
fi

# 2. Test Docker build
echo ""
echo "2. Testing Docker build..."
if docker build --no-cache -t pre-deployment-test . > /tmp/docker-build.log 2>&1; then
    echo -e "${GREEN}✓ Docker build succeeded${NC}"
    docker rmi pre-deployment-test > /dev/null 2>&1
else
    echo -e "${RED}✗ Docker build failed${NC}"
    echo "Error details:"
    tail -20 /tmp/docker-build.log
    exit 1
fi

# 3. Check required files exist
echo ""
echo "3. Checking required files..."
REQUIRED_FILES=("main.py" "requirements.txt" "Dockerfile")
for file in "${REQUIRED_FILES[@]}"; do
    if [[ -f "$file" ]]; then
        echo -e "${GREEN}✓ $file exists${NC}"
    else
        echo -e "${RED}✗ $file is missing${NC}"
        exit 1
    fi
done

# 4. Validate secrets format (if AWS CLI is available)
echo ""
echo "4. Checking AWS secrets..."
if command -v aws &> /dev/null; then
    # Check if admin secret exists and is valid JSON
    SECRET_VALUE=$(aws secretsmanager get-secret-value --secret-id ava-olo/admin --region us-east-1 --query SecretString --output text 2>/dev/null || echo "NOT_FOUND")
    
    if [[ "$SECRET_VALUE" == "NOT_FOUND" ]]; then
        echo -e "${YELLOW}⚠ Admin secret not found (may be deleted)${NC}"
    elif echo "$SECRET_VALUE" | jq . > /dev/null 2>&1; then
        # Check for escape sequences
        if echo "$SECRET_VALUE" | grep -q '\\!'; then
            echo -e "${RED}✗ Admin secret contains invalid escape sequence \\!${NC}"
            echo "  This will cause ECS tasks to fail"
            exit 1
        else
            echo -e "${GREEN}✓ Admin secret format is valid${NC}"
        fi
    else
        echo -e "${RED}✗ Admin secret is not valid JSON${NC}"
        exit 1
    fi
else
    echo -e "${YELLOW}⚠ AWS CLI not available, skipping secrets check${NC}"
fi

# 5. Check current ECS service health
echo ""
echo "5. Checking current ECS service health..."
if command -v aws &> /dev/null && [[ "$SERVICE_NAME" != "unknown" ]]; then
    RUNNING_TASKS=$(aws ecs list-tasks --cluster ava-olo-production --service-name $SERVICE_NAME --desired-status RUNNING --region us-east-1 --query 'length(taskArns)' --output text 2>/dev/null || echo "0")
    
    if [[ "$RUNNING_TASKS" -gt "0" ]]; then
        echo -e "${GREEN}✓ Service has $RUNNING_TASKS running task(s)${NC}"
    else
        echo -e "${YELLOW}⚠ Service has no running tasks${NC}"
    fi
    
    # Check for recent failures
    FAILED_TASKS=$(aws ecs list-tasks --cluster ava-olo-production --service-name $SERVICE_NAME --desired-status STOPPED --region us-east-1 --query 'taskArns[:10]' --output json 2>/dev/null | jq length)
    
    if [[ "$FAILED_TASKS" -gt "5" ]]; then
        echo -e "${YELLOW}⚠ High number of recently stopped tasks: $FAILED_TASKS${NC}"
        echo "  This may indicate deployment issues"
    fi
fi

# 6. Check version consistency
echo ""
echo "6. Checking version consistency..."
if [[ "$SERVICE_NAME" == "agricultural-core" ]]; then
    VERSION_IN_CONFIG=$(grep "VERSION.*=" modules/core/config.py 2>/dev/null | grep -oE "v[0-9]+\.[0-9]+\.[0-9]+" | head -1)
    if [[ -n "$VERSION_IN_CONFIG" ]]; then
        echo -e "${GREEN}✓ Version found in config: $VERSION_IN_CONFIG${NC}"
    else
        echo -e "${YELLOW}⚠ Could not find version in config.py${NC}"
    fi
fi

# 7. Check Git status
echo ""
echo "7. Checking Git status..."
if [[ -n $(git status --porcelain) ]]; then
    echo -e "${YELLOW}⚠ Uncommitted changes detected:${NC}"
    git status --short
else
    echo -e "${GREEN}✓ Working directory clean${NC}"
fi

# Get current branch
CURRENT_BRANCH=$(git branch --show-current)
if [[ "$CURRENT_BRANCH" == "main" ]] || [[ "$CURRENT_BRANCH" == "master" ]]; then
    echo -e "${GREEN}✓ On deployment branch: $CURRENT_BRANCH${NC}"
else
    echo -e "${YELLOW}⚠ Not on main/master branch: $CURRENT_BRANCH${NC}"
fi

# 8. Memory check (optional)
echo ""
echo "8. System resources check..."
AVAILABLE_MEM=$(free -m | awk 'NR==2{printf "%.0f", $7}')
if [[ "$AVAILABLE_MEM" -lt "500" ]]; then
    echo -e "${YELLOW}⚠ Low available memory: ${AVAILABLE_MEM}MB${NC}"
    echo "  Docker build may fail"
else
    echo -e "${GREEN}✓ Sufficient memory available: ${AVAILABLE_MEM}MB${NC}"
fi

# Summary
echo ""
echo "================================================"
echo "Pre-deployment check complete!"
echo ""

# Create deployment readiness file
cat > /tmp/deployment-readiness.json <<EOF
{
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "service": "$SERVICE_NAME",
  "branch": "$CURRENT_BRANCH",
  "checks_passed": true,
  "version": "${VERSION_IN_CONFIG:-unknown}"
}
EOF

echo -e "${GREEN}✅ All critical checks passed - ready to deploy!${NC}"
echo ""
echo "Next steps:"
echo "1. git add . && git commit -m 'your message'"
echo "2. git push origin $CURRENT_BRANCH"
echo "3. Monitor deployment at: http://ava-olo-internal-alb-426050720.us-east-1.elb.amazonaws.com/dashboards/deployment"

exit 0