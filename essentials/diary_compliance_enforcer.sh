#!/bin/bash

# AVA OLO Diary Compliance Enforcer
# Enforces diary reporting protocol across all development activities

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
REPORTS_DIR="$(dirname "$0")/reports"
TODAY=$(date +%Y-%m-%d)
TODAY_DIR="$REPORTS_DIR/$TODAY"
PROTOCOL_FILE="$(dirname "$0")/DIARY_REPORTING_PROTOCOL.md"
CHANGELOG_FILE="$(dirname "$0")/SYSTEM_CHANGELOG.md"

# Function to print colored messages
print_color() {
    color=$1
    message=$2
    echo -e "${color}${message}${NC}"
}

# Function to check if reports exist for today
check_daily_reports() {
    if [ ! -d "$TODAY_DIR" ]; then
        print_color "$RED" "❌ No reports directory for today ($TODAY)"
        return 1
    fi
    
    report_count=$(find "$TODAY_DIR" -name "report_*.md" 2>/dev/null | wc -l)
    
    if [ "$report_count" -eq 0 ]; then
        print_color "$RED" "❌ No reports found for today"
        return 1
    else
        print_color "$GREEN" "✅ Found $report_count report(s) for today"
        return 0
    fi
}

# Function to check if daily summary exists
check_daily_summary() {
    if [ -f "$TODAY_DIR/DAILY_SUMMARY.md" ]; then
        print_color "$GREEN" "✅ Daily summary exists"
        return 0
    else
        print_color "$YELLOW" "⚠️  Daily summary not yet created"
        return 1
    fi
}

# Function to validate report format
validate_report() {
    report_file=$1
    
    if [ ! -f "$report_file" ]; then
        echo "Report file not found: $report_file"
        return 1
    fi
    
    # Check for required sections
    required_sections=(
        "## 📊 Summary"
        "## 🔄 Work Performed"
        "## 📈 Progress Metrics"
        "## 🐛 Issues Encountered"
        "## 💡 Decisions Made"
        "## 🔮 Next Steps"
        "## 📎 References"
        "## ✅ Compliance Check"
    )
    
    missing_sections=()
    
    for section in "${required_sections[@]}"; do
        if ! grep -q "^$section" "$report_file"; then
            missing_sections+=("$section")
        fi
    done
    
    if [ ${#missing_sections[@]} -eq 0 ]; then
        print_color "$GREEN" "✅ Report format is valid"
        return 0
    else
        print_color "$RED" "❌ Report is missing sections:"
        for section in "${missing_sections[@]}"; do
            echo "   - $section"
        done
        return 1
    fi
}

# Function to check if report is in CHANGELOG
check_changelog_entry() {
    report_name=$(basename "$1")
    
    if grep -q "$report_name" "$CHANGELOG_FILE"; then
        print_color "$GREEN" "✅ Report is referenced in SYSTEM_CHANGELOG.md"
        return 0
    else
        print_color "$YELLOW" "⚠️  Report not yet in SYSTEM_CHANGELOG.md"
        return 1
    fi
}

# Function to calculate compliance score
calculate_compliance_score() {
    score=0
    max_score=100
    
    # Check for reports today (40 points)
    if check_daily_reports >/dev/null 2>&1; then
        score=$((score + 40))
    fi
    
    # Check for daily summary (20 points)
    if check_daily_summary >/dev/null 2>&1; then
        score=$((score + 20))
    fi
    
    # Check report count (20 points for 1+, 20 more for 3+)
    if [ -d "$TODAY_DIR" ]; then
        report_count=$(find "$TODAY_DIR" -name "report_*.md" 2>/dev/null | wc -l)
        if [ "$report_count" -ge 1 ]; then
            score=$((score + 10))
        fi
        if [ "$report_count" -ge 3 ]; then
            score=$((score + 10))
        fi
    fi
    
    # Check if latest report is properly formatted (20 points)
    if [ -d "$TODAY_DIR" ]; then
        latest_report=$(find "$TODAY_DIR" -name "report_*.md" 2>/dev/null | sort | tail -n1)
        if [ -n "$latest_report" ] && validate_report "$latest_report" >/dev/null 2>&1; then
            score=$((score + 20))
        fi
    fi
    
    echo "$score"
}

# Function to enforce pre-commit check
pre_commit_check() {
    print_color "$BLUE" "🔍 Running Pre-Commit Diary Compliance Check..."
    
    if ! check_daily_reports; then
        print_color "$RED" "❌ COMMIT BLOCKED: No diary report for today!"
        print_color "$YELLOW" "Please create a report using:"
        echo "  python diary_report_generator.py create --title 'Your Title' --summary 'Your Summary'"
        exit 1
    fi
    
    print_color "$GREEN" "✅ Pre-commit check passed"
}

# Function to enforce pre-deployment check
pre_deployment_check() {
    print_color "$BLUE" "🚀 Running Pre-Deployment Diary Compliance Check..."
    
    # Must have deployment report
    deployment_report=$(find "$TODAY_DIR" -name "*deployment*.md" 2>/dev/null | head -n1)
    
    if [ -z "$deployment_report" ]; then
        print_color "$RED" "❌ DEPLOYMENT BLOCKED: No deployment report found!"
        print_color "$YELLOW" "Please create a deployment report first"
        exit 1
    fi
    
    # Validate the deployment report
    if ! validate_report "$deployment_report"; then
        print_color "$RED" "❌ DEPLOYMENT BLOCKED: Deployment report is incomplete!"
        exit 1
    fi
    
    print_color "$GREEN" "✅ Pre-deployment check passed"
}

# Function to show compliance dashboard
show_dashboard() {
    clear
    print_color "$BLUE" "═══════════════════════════════════════════════════════"
    print_color "$BLUE" "         📔 AVA OLO DIARY COMPLIANCE DASHBOARD"
    print_color "$BLUE" "═══════════════════════════════════════════════════════"
    echo ""
    
    # Date and time
    echo "📅 Date: $(date '+%Y-%m-%d %H:%M:%S')"
    echo ""
    
    # Reports status
    print_color "$YELLOW" "📊 Today's Reports Status:"
    check_daily_reports
    check_daily_summary
    echo ""
    
    # List today's reports
    if [ -d "$TODAY_DIR" ]; then
        print_color "$YELLOW" "📝 Reports Created Today:"
        for report in "$TODAY_DIR"/report_*.md; do
            if [ -f "$report" ]; then
                echo "   - $(basename "$report")"
            fi
        done
    fi
    echo ""
    
    # Compliance score
    score=$(calculate_compliance_score)
    print_color "$YELLOW" "🏆 Compliance Score: $score%"
    
    if [ "$score" -ge 90 ]; then
        print_color "$GREEN" "   Status: Excellent 🟢"
    elif [ "$score" -ge 70 ]; then
        print_color "$YELLOW" "   Status: Good 🟡"
    elif [ "$score" -ge 50 ]; then
        print_color "$YELLOW" "   Status: Needs Improvement 🟠"
    else
        print_color "$RED" "   Status: Non-Compliant 🔴"
    fi
    
    echo ""
    print_color "$BLUE" "═══════════════════════════════════════════════════════"
}

# Function to create reminder
create_reminder() {
    print_color "$YELLOW" "⏰ DIARY REMINDER:"
    echo ""
    
    if ! check_daily_reports >/dev/null 2>&1; then
        print_color "$RED" "❗ You haven't created any reports today!"
        echo "   Start with: python diary_report_generator.py create --title 'Daily Work' --summary 'Summary here'"
    else
        report_count=$(find "$TODAY_DIR" -name "report_*.md" 2>/dev/null | wc -l)
        hours_since_last=$(find "$TODAY_DIR" -name "report_*.md" -exec stat -c %Y {} \; 2>/dev/null | sort -n | tail -1 | xargs -I {} date -d @{} +%s | xargs -I {} echo $(( ($(date +%s) - {}) / 3600 )))
        
        if [ "$hours_since_last" -gt 4 ]; then
            print_color "$YELLOW" "⚠️  It's been $hours_since_last hours since your last report"
            echo "   Consider creating an update report"
        fi
    fi
    
    if ! check_daily_summary >/dev/null 2>&1; then
        current_hour=$(date +%H)
        if [ "$current_hour" -ge 16 ]; then
            print_color "$YELLOW" "📝 Don't forget to create your daily summary!"
            echo "   Run: python diary_report_generator.py daily"
        fi
    fi
}

# Main execution
main() {
    action=${1:-dashboard}
    
    case "$action" in
        dashboard)
            show_dashboard
            ;;
        check)
            check_daily_reports
            check_daily_summary
            ;;
        validate)
            if [ -z "$2" ]; then
                echo "Usage: $0 validate <report_file>"
                exit 1
            fi
            validate_report "$2"
            check_changelog_entry "$2"
            ;;
        pre-commit)
            pre_commit_check
            ;;
        pre-deploy)
            pre_deployment_check
            ;;
        reminder)
            create_reminder
            ;;
        score)
            score=$(calculate_compliance_score)
            echo "Compliance Score: $score%"
            ;;
        help)
            echo "AVA OLO Diary Compliance Enforcer"
            echo ""
            echo "Usage: $0 [action]"
            echo ""
            echo "Actions:"
            echo "  dashboard    - Show compliance dashboard (default)"
            echo "  check        - Check if reports exist for today"
            echo "  validate     - Validate a specific report file"
            echo "  pre-commit   - Run pre-commit compliance check"
            echo "  pre-deploy   - Run pre-deployment compliance check"
            echo "  reminder     - Show diary reminders"
            echo "  score        - Calculate compliance score"
            echo "  help         - Show this help message"
            ;;
        *)
            echo "Unknown action: $action"
            echo "Run '$0 help' for usage information"
            exit 1
            ;;
    esac
}

main "$@"