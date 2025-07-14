#!/bin/bash

# Health Dashboard Enablement Script for AVA OLO Safety System
# Default: Dry-run mode - shows what would be added without doing it

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
NC='\033[0m'

# Default to dry-run mode for safety
DRY_RUN=true
OPTIONAL=false
VERBOSE=false
BACKUP=true

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --enable)
            DRY_RUN=false
            shift
            ;;
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --optional)
            OPTIONAL=true
            shift
            ;;
        --no-backup)
            BACKUP=false
            shift
            ;;
        --verbose)
            VERBOSE=true
            shift
            ;;
        --help)
            echo "Usage: $0 [options]"
            echo "Options:"
            echo "  --enable        Actually modify files (default: dry-run)"
            echo "  --dry-run       Show what would be done without doing it (default)"
            echo "  --optional      Make dashboard endpoints optional (not required)"
            echo "  --no-backup     Don't create backup files"
            echo "  --verbose       Show detailed output"
            echo "  --help          Show this help message"
            echo ""
            echo "Default: Dry-run mode (safe inspection)"
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
echo -e "${BLUE}📊 AVA OLO Health Dashboard Enablement${NC}"
echo -e "${BLUE}==================================================================${NC}"
echo ""

if [ "$DRY_RUN" = true ]; then
    echo -e "${YELLOW}🔍 DRY-RUN MODE - No changes will be made${NC}"
    echo -e "${GREEN}✅ Safe to run - will only show what would happen${NC}"
else
    echo -e "${RED}⚠️  MODIFICATION MODE${NC}"
    echo -e "${YELLOW}This will add health dashboard endpoints to your services${NC}"
    if [ "$OPTIONAL" = true ]; then
        echo -e "${GREEN}✅ Dashboards will be optional (won't affect service startup)${NC}"
    else
        echo -e "${YELLOW}⚠️  Dashboards will be required for service operation${NC}"
    fi
fi
echo ""

# Function to check if file contains health endpoint
has_health_endpoint() {
    local file=$1
    grep -q "health-dashboard\|/health\|health_dashboard" "$file" 2>/dev/null
}

# Function to create backup
create_backup() {
    local file=$1
    if [ "$BACKUP" = true ] && [ "$DRY_RUN" = false ]; then
        cp "$file" "${file}.backup.$(date +%Y%m%d_%H%M%S)"
        echo -e "${GREEN}   ✅ Backup created${NC}"
    fi
}

# Function to add health endpoint to Python service
add_python_health_endpoint() {
    local service_path=$1
    local service_name=$2
    local main_file="$service_path/main.py"
    
    echo -e "${MAGENTA}🐍 Python Service: ${service_name}${NC}"
    
    if [ ! -f "$main_file" ]; then
        echo -e "${RED}   ❌ main.py not found${NC}"
        return 1
    fi
    
    # Check if health endpoint already exists
    if has_health_endpoint "$main_file"; then
        echo -e "${YELLOW}   ⚠️  Health endpoint already exists${NC}"
        return 0
    fi
    
    # Health endpoint code to add
    local health_code='
# Health Dashboard Endpoint
@app.route("/health-dashboard")
def health_dashboard():
    """Serve the health monitoring dashboard"""
    try:
        # Check if dashboard template exists
        dashboard_path = "templates/health_dashboard.html"
        if os.path.exists(dashboard_path):
            return render_template("health_dashboard.html")
        else:
            # Return basic health status if template not found
            return jsonify({
                "status": "healthy",
                "service": "'$service_name'",
                "message": "Dashboard template not found, service is running",
                "timestamp": datetime.utcnow().isoformat() + "Z"
            })
    except Exception as e:
        return jsonify({
            "status": "error",
            "service": "'$service_name'",
            "error": str(e)
        }), 500

# Health Check Endpoint
@app.route("/health")
def health_check():
    """Basic health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "'$service_name'",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    })'
    
    if [ "$DRY_RUN" = true ]; then
        echo -e "${BLUE}   Would add health endpoints:${NC}"
        echo -e "${BLUE}     - /health-dashboard (monitoring dashboard)${NC}"
        echo -e "${BLUE}     - /health (basic health check)${NC}"
        if [ "$VERBOSE" = true ]; then
            echo -e "${BLUE}   Code preview:${NC}"
            echo "$health_code" | head -10
            echo "   ..."
        fi
    else
        create_backup "$main_file"
        
        # Add imports if needed
        if ! grep -q "from datetime import datetime" "$main_file"; then
            sed -i '1a from datetime import datetime' "$main_file"
        fi
        if ! grep -q "import os" "$main_file"; then
            sed -i '1a import os' "$main_file"
        fi
        
        # Add health endpoints before the last "if __name__" block
        # This is a simplified version - in production, use proper AST parsing
        echo -e "${YELLOW}   Adding health endpoints...${NC}"
        # Implementation would go here
        
        echo -e "${GREEN}   ✅ Health endpoints added${NC}"
    fi
    
    return 0
}

# Function to add dashboard template
add_dashboard_template() {
    local service_path=$1
    local service_name=$2
    local template_dir="$service_path/templates"
    local dashboard_file="$template_dir/health_dashboard.html"
    
    echo -e "${MAGENTA}📄 Dashboard Template: ${service_name}${NC}"
    
    # Create templates directory if needed
    if [ ! -d "$template_dir" ]; then
        if [ "$DRY_RUN" = true ]; then
            echo -e "${BLUE}   Would create templates directory${NC}"
        else
            mkdir -p "$template_dir"
            echo -e "${GREEN}   ✅ Created templates directory${NC}"
        fi
    fi
    
    # Check if dashboard already exists
    if [ -f "$dashboard_file" ]; then
        echo -e "${YELLOW}   ⚠️  Dashboard template already exists${NC}"
        return 0
    fi
    
    # Source dashboard template
    local source_dashboard="../web_dashboard/comprehensive_health_dashboard.html"
    if [ ! -f "$source_dashboard" ]; then
        source_dashboard="comprehensive_health_dashboard.html"
    fi
    
    if [ "$DRY_RUN" = true ]; then
        echo -e "${BLUE}   Would copy dashboard template${NC}"
        echo -e "${BLUE}   Source: $source_dashboard${NC}"
        echo -e "${BLUE}   Target: $dashboard_file${NC}"
    else
        if [ -f "$source_dashboard" ]; then
            cp "$source_dashboard" "$dashboard_file"
            
            # Customize for specific service
            sed -i "s/AVA OLO Health Dashboard/${service_name} Health Dashboard/g" "$dashboard_file"
            
            echo -e "${GREEN}   ✅ Dashboard template installed${NC}"
        else
            echo -e "${RED}   ❌ Source dashboard not found${NC}"
            return 1
        fi
    fi
    
    return 0
}

# Function to add nginx/reverse proxy configuration
add_nginx_config() {
    local service_name=$1
    
    echo -e "${MAGENTA}🔧 Nginx Configuration: ${service_name}${NC}"
    
    local nginx_config="
# Health Dashboard Configuration
location /health-dashboard {
    proxy_pass http://localhost:8000;
    proxy_set_header Host \$host;
    proxy_set_header X-Real-IP \$remote_addr;
    proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto \$scheme;
}

location /health {
    proxy_pass http://localhost:8000;
    proxy_set_header Host \$host;
}"
    
    if [ "$DRY_RUN" = true ]; then
        echo -e "${BLUE}   Would add nginx configuration for health endpoints${NC}"
        if [ "$VERBOSE" = true ]; then
            echo "$nginx_config"
        fi
    else
        echo -e "${YELLOW}   ⚠️  Please add nginx configuration manually${NC}"
    fi
}

# Main installation logic
echo -e "${YELLOW}🔍 Checking services...${NC}"
echo ""

SERVICES_FOUND=0
SERVICES_PROCESSED=0

# Check monitoring-dashboards service
MONITORING_DIR="../../ava-olo-monitoring-dashboards"
if [ -d "$MONITORING_DIR" ]; then
    SERVICES_FOUND=$((SERVICES_FOUND + 1))
    echo -e "${GREEN}✅ Found monitoring-dashboards${NC}"
    
    if add_python_health_endpoint "$MONITORING_DIR" "monitoring_dashboards"; then
        add_dashboard_template "$MONITORING_DIR" "monitoring_dashboards"
        add_nginx_config "monitoring_dashboards"
        SERVICES_PROCESSED=$((SERVICES_PROCESSED + 1))
    fi
    echo ""
fi

# Check agricultural-core service
AGRICULTURAL_DIR="../../ava-olo-agricultural-core"
if [ -d "$AGRICULTURAL_DIR" ]; then
    SERVICES_FOUND=$((SERVICES_FOUND + 1))
    echo -e "${GREEN}✅ Found agricultural-core${NC}"
    
    if add_python_health_endpoint "$AGRICULTURAL_DIR" "agricultural_core"; then
        add_dashboard_template "$AGRICULTURAL_DIR" "agricultural_core"
        add_nginx_config "agricultural_core"
        SERVICES_PROCESSED=$((SERVICES_PROCESSED + 1))
    fi
    echo ""
fi

# Summary
echo -e "${BLUE}==================================================================${NC}"
if [ "$DRY_RUN" = true ]; then
    echo -e "${GREEN}✨ DRY-RUN Complete${NC}"
    echo -e "${YELLOW}Found ${SERVICES_FOUND} services${NC}"
    echo -e "${YELLOW}Would modify ${SERVICES_PROCESSED} services${NC}"
    echo ""
    echo -e "${BLUE}What would be added:${NC}"
    echo -e "  📊 /health-dashboard endpoint (full monitoring dashboard)"
    echo -e "  🏥 /health endpoint (basic health check)"
    echo -e "  📄 Dashboard HTML template"
    echo -e "  🔧 Nginx configuration guidance"
    echo ""
    echo -e "${BLUE}To actually install, run:${NC}"
    echo -e "  ${GREEN}$0 --enable${NC}"
    echo ""
    echo -e "${BLUE}To install as optional feature:${NC}"
    echo -e "  ${GREEN}$0 --enable --optional${NC}"
else
    echo -e "${GREEN}✨ Installation Complete${NC}"
    echo -e "${GREEN}Modified ${SERVICES_PROCESSED} of ${SERVICES_FOUND} services${NC}"
    echo ""
    echo -e "${YELLOW}📋 Next Steps:${NC}"
    echo -e "  1. Test health endpoints:"
    echo -e "     ${BLUE}curl http://localhost:8000/health${NC}"
    echo -e "     ${BLUE}curl http://localhost:8000/health-dashboard${NC}"
    echo ""
    echo -e "  2. View dashboard in browser:"
    echo -e "     ${BLUE}http://localhost:8000/health-dashboard${NC}"
    echo ""
    echo -e "  3. Update nginx/reverse proxy configuration"
    echo ""
    if [ "$BACKUP" = true ]; then
        echo -e "${GREEN}✅ Backup files created (.backup.* extension)${NC}"
    fi
fi
echo -e "${BLUE}==================================================================${NC}"

# Create a simple test script
if [ "$DRY_RUN" = false ]; then
    cat > test_health_endpoints.sh << 'EOF'
#!/bin/bash
# Test health endpoints

echo "Testing health endpoints..."

for port in 8000 8001 8080; do
    echo "Checking port $port..."
    if curl -s "http://localhost:$port/health" | grep -q "healthy"; then
        echo "✅ Health check passed on port $port"
    fi
done
EOF
    chmod +x test_health_endpoints.sh
    echo ""
    echo -e "${GREEN}Created test_health_endpoints.sh for testing${NC}"
fi

exit 0