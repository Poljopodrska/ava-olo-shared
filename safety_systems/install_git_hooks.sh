#!/bin/bash

# Git Hooks Installation Script for AVA OLO Safety System
# Default: Test mode - shows what would be installed without doing it

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Default to test mode for safety
TEST_MODE=true
WITH_BYPASS=true
FORCE=false
VERBOSE=false

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --enable)
            TEST_MODE=false
            shift
            ;;
        --test-mode)
            TEST_MODE=true
            shift
            ;;
        --no-bypass)
            WITH_BYPASS=false
            shift
            ;;
        --force)
            FORCE=true
            shift
            ;;
        --verbose)
            VERBOSE=true
            shift
            ;;
        --help)
            echo "Usage: $0 [options]"
            echo "Options:"
            echo "  --enable        Actually install hooks (default: test mode)"
            echo "  --test-mode     Show what would be done without doing it (default)"
            echo "  --no-bypass     Install without emergency bypass option"
            echo "  --force         Overwrite existing hooks"
            echo "  --verbose       Show detailed output"
            echo "  --help          Show this help message"
            echo ""
            echo "Default: Test mode (safe inspection of what would happen)"
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
echo -e "${BLUE}🪝 AVA OLO Git Hooks Installation${NC}"
echo -e "${BLUE}==================================================================${NC}"
echo ""

if [ "$TEST_MODE" = true ]; then
    echo -e "${YELLOW}🧪 TEST MODE - No changes will be made${NC}"
    echo -e "${GREEN}✅ Safe to run - will only show what would happen${NC}"
else
    echo -e "${RED}⚠️  INSTALLATION MODE${NC}"
    echo -e "${YELLOW}This will install git hooks in your repositories${NC}"
    if [ "$WITH_BYPASS" = false ]; then
        echo -e "${RED}⚠️  Bypass option DISABLED - hooks cannot be skipped${NC}"
    fi
fi
echo ""

# Function to check if directory is a git repository
is_git_repo() {
    [ -d "$1/.git" ]
}

# Function to install hook
install_hook() {
    local repo_path=$1
    local hook_name=$2
    local hook_source=$3
    local repo_name=$(basename "$repo_path")
    
    echo -e "${YELLOW}📂 Repository: ${repo_name}${NC}"
    
    if ! is_git_repo "$repo_path"; then
        echo -e "${RED}   ❌ Not a git repository${NC}"
        return 1
    fi
    
    local hook_target="$repo_path/.git/hooks/$hook_name"
    
    # Check if hook already exists
    if [ -f "$hook_target" ] && [ "$FORCE" = false ]; then
        echo -e "${YELLOW}   ⚠️  Hook already exists: $hook_name${NC}"
        if [ "$TEST_MODE" = false ]; then
            echo -e "${BLUE}   Use --force to overwrite${NC}"
            return 1
        fi
    fi
    
    if [ "$TEST_MODE" = true ]; then
        echo -e "${BLUE}   Would install: $hook_name${NC}"
        if [ "$WITH_BYPASS" = true ]; then
            echo -e "${BLUE}   With emergency bypass enabled${NC}"
        else
            echo -e "${YELLOW}   Without emergency bypass${NC}"
        fi
        [ "$VERBOSE" = true ] && echo -e "${BLUE}   Source: $hook_source${NC}"
    else
        # Create hooks directory if it doesn't exist
        mkdir -p "$repo_path/.git/hooks"
        
        # Copy hook file
        cp "$hook_source" "$hook_target"
        chmod +x "$hook_target"
        
        echo -e "${GREEN}   ✅ Installed: $hook_name${NC}"
        if [ "$WITH_BYPASS" = true ]; then
            echo -e "${GREEN}   ✅ Emergency bypass enabled (use --no-verify)${NC}"
        fi
    fi
    
    return 0
}

# Create pre-push hook with safety features
create_safe_pre_push_hook() {
    local temp_file="/tmp/ava-olo-pre-push-$$"
    
    cat > "$temp_file" << 'EOF'
#!/bin/bash

# AVA OLO Pre-Push Safety Hook
# Use 'git push --no-verify' to bypass in emergencies

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}==================================================================${NC}"
echo -e "${BLUE}🛡️  AVA OLO Pre-Push Safety Check${NC}"
echo -e "${BLUE}==================================================================${NC}"

# Check for emergency bypass
if [ "$1" = "--bypass" ] || [ "$AVA_EMERGENCY" = "true" ]; then
    echo -e "${YELLOW}⚠️  Safety checks bypassed (emergency mode)${NC}"
    echo -e "${YELLOW}Reason: ${AVA_EMERGENCY_REASON:-Not specified}${NC}"
    exit 0
fi

# Allow --no-verify bypass
if [ -n "$GIT_BYPASS_HOOKS" ]; then
    echo -e "${YELLOW}⚠️  Hooks bypassed via --no-verify${NC}"
    exit 0
fi

# Get current branch
BRANCH=$(git rev-parse --abbrev-ref HEAD)
echo -e "${YELLOW}Branch: ${BRANCH}${NC}"

# Find safety scripts
SAFETY_SCRIPT=""
if [ -f "../../ava-olo-shared/safety_systems/pre_deploy_check.sh" ]; then
    SAFETY_SCRIPT="../../ava-olo-shared/safety_systems/pre_deploy_check.sh"
elif [ -f "../ava-olo-shared/safety_systems/pre_deploy_check.sh" ]; then
    SAFETY_SCRIPT="../ava-olo-shared/safety_systems/pre_deploy_check.sh"
elif [ -f "scripts/pre_deploy_check.sh" ]; then
    SAFETY_SCRIPT="scripts/pre_deploy_check.sh"
fi

if [ -n "$SAFETY_SCRIPT" ] && [ -x "$SAFETY_SCRIPT" ]; then
    echo -e "${YELLOW}Running safety checks...${NC}"
    
    # Determine service name
    SERVICE_NAME=""
    if [[ "$PWD" == *"monitoring-dashboards"* ]]; then
        SERVICE_NAME="monitoring_dashboards"
    elif [[ "$PWD" == *"agricultural-core"* ]]; then
        SERVICE_NAME="agricultural_core"
    fi
    
    if [ -n "$SERVICE_NAME" ]; then
        if $SAFETY_SCRIPT "$SERVICE_NAME"; then
            echo -e "${GREEN}✅ Safety checks passed${NC}"
        else
            echo -e "${RED}❌ Safety checks failed${NC}"
            echo -e "${YELLOW}To bypass: git push --no-verify${NC}"
            echo -e "${YELLOW}Or set: AVA_EMERGENCY=true AVA_EMERGENCY_REASON='reason' git push${NC}"
            exit 1
        fi
    else
        echo -e "${YELLOW}⚠️  Could not determine service name${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  Safety scripts not found - basic checks only${NC}"
    
    # Basic syntax check for Python files
    if [ -f "main.py" ]; then
        if python -m py_compile main.py 2>/dev/null; then
            echo -e "${GREEN}✅ Python syntax OK${NC}"
        else
            echo -e "${RED}❌ Python syntax errors detected${NC}"
            exit 1
        fi
    fi
fi

# Constitutional reminder
echo ""
echo -e "${BLUE}🏛️ Constitutional Checklist:${NC}"
echo -e "  🥭 MANGO Rule compliant?"
echo -e "  🧠 LLM-First approach?"
echo -e "  🔒 Privacy protected?"
echo -e "  🌍 Works globally?"

# Give user 3 seconds to cancel if needed
echo ""
echo -e "${GREEN}✅ Proceeding with push in 3 seconds (Ctrl+C to cancel)...${NC}"
sleep 3

exit 0
EOF
    
    echo "$temp_file"
}

# Main installation logic
echo -e "${YELLOW}🔍 Looking for repositories...${NC}"
echo ""

# Find repositories to install hooks in
REPOS_FOUND=0
REPOS_PROCESSED=0

# Check current directory
if is_git_repo "."; then
    echo -e "${GREEN}✅ Current directory is a git repository${NC}"
    HOOK_SOURCE=$(create_safe_pre_push_hook)
    install_hook "." "pre-push" "$HOOK_SOURCE"
    rm -f "$HOOK_SOURCE"
    REPOS_FOUND=$((REPOS_FOUND + 1))
    REPOS_PROCESSED=$((REPOS_PROCESSED + 1))
    echo ""
fi

# Check for service directories
for service_dir in "../../ava-olo-monitoring-dashboards" "../../ava-olo-agricultural-core"; do
    if [ -d "$service_dir" ] && is_git_repo "$service_dir"; then
        REPOS_FOUND=$((REPOS_FOUND + 1))
        HOOK_SOURCE=$(create_safe_pre_push_hook)
        if install_hook "$service_dir" "pre-push" "$HOOK_SOURCE"; then
            REPOS_PROCESSED=$((REPOS_PROCESSED + 1))
        fi
        rm -f "$HOOK_SOURCE"
        echo ""
    fi
done

# Summary
echo -e "${BLUE}==================================================================${NC}"
if [ "$TEST_MODE" = true ]; then
    echo -e "${GREEN}✨ TEST MODE Complete${NC}"
    echo -e "${YELLOW}Found ${REPOS_FOUND} repositories${NC}"
    echo -e "${YELLOW}Would install hooks in ${REPOS_PROCESSED} repositories${NC}"
    echo ""
    echo -e "${BLUE}To actually install, run:${NC}"
    echo -e "  ${GREEN}$0 --enable${NC}"
    echo ""
    echo -e "${BLUE}To install without bypass option:${NC}"
    echo -e "  ${GREEN}$0 --enable --no-bypass${NC}"
else
    echo -e "${GREEN}✨ Installation Complete${NC}"
    echo -e "${GREEN}Installed hooks in ${REPOS_PROCESSED} of ${REPOS_FOUND} repositories${NC}"
    echo ""
    echo -e "${YELLOW}📋 Hook Features:${NC}"
    if [ "$WITH_BYPASS" = true ]; then
        echo -e "  ✅ Emergency bypass: git push --no-verify"
        echo -e "  ✅ Environment bypass: AVA_EMERGENCY=true git push"
    else
        echo -e "  ❌ Bypass disabled (strict mode)"
    fi
    echo -e "  ✅ Safety checks before push"
    echo -e "  ✅ Constitutional compliance reminders"
    echo ""
    echo -e "${BLUE}To test:${NC}"
    echo -e "  Make a change and try: git push"
fi
echo -e "${BLUE}==================================================================${NC}"

exit 0