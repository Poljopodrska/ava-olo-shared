#!/usr/bin/env python3
"""
AVA OLO Diary Report Generator
Automated tool to create and validate diary reports
"""

import os
import sys
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import argparse

class DiaryReportGenerator:
    """Generate and manage diary reports for AVA OLO development"""
    
    def __init__(self):
        self.reports_dir = Path(__file__).parent / "reports"
        self.changelog_path = Path(__file__).parent / "SYSTEM_CHANGELOG.md"
        self.protocol_path = Path(__file__).parent / "DIARY_REPORTING_PROTOCOL.md"
        
    def get_current_datetime(self) -> Tuple[str, str]:
        """Get current UTC and CET timestamps"""
        now_utc = datetime.now(timezone.utc)
        # CET is UTC+1 (or UTC+2 in summer)
        cet_offset = 2 if self._is_summer_time() else 1
        now_cet = now_utc.replace(tzinfo=None) + timezone(hours=cet_offset)
        
        utc_str = now_utc.strftime("%Y-%m-%d %H:%M:%S UTC")
        cet_str = now_cet.strftime("%H:%M:%S CET")
        
        return utc_str, cet_str
    
    def _is_summer_time(self) -> bool:
        """Check if we're in summer time (rough approximation)"""
        month = datetime.now().month
        return 4 <= month <= 10
    
    def get_current_version(self) -> str:
        """Get current version from git or config files"""
        try:
            # Try to get from agricultural-core config
            config_path = Path(__file__).parent.parent.parent / "ava-olo-agricultural-core" / "modules" / "core" / "config.py"
            if config_path.exists():
                with open(config_path, 'r') as f:
                    for line in f:
                        if 'VERSION = ' in line:
                            return line.split('"')[1]
        except:
            pass
        
        # Fallback to git tag
        try:
            result = subprocess.run(['git', 'describe', '--tags', '--abbrev=0'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout.strip()
        except:
            pass
            
        return "unknown"
    
    def get_next_report_number(self, date_str: str) -> str:
        """Get the next sequential report number for today"""
        date_dir = self.reports_dir / date_str
        if not date_dir.exists():
            return "001"
        
        existing_reports = list(date_dir.glob("report_*.md"))
        if not existing_reports:
            return "001"
        
        # Extract numbers from existing reports
        numbers = []
        for report in existing_reports:
            try:
                num = report.stem.split('_')[1]
                numbers.append(int(num))
            except:
                continue
        
        next_num = max(numbers) + 1 if numbers else 1
        return f"{next_num:03d}"
    
    def get_git_stats(self) -> Dict[str, int]:
        """Get git statistics for current work"""
        stats = {
            "lines_added": 0,
            "lines_modified": 0,
            "lines_deleted": 0,
            "files_changed": 0
        }
        
        try:
            # Get diff stats
            result = subprocess.run(['git', 'diff', '--stat'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                if lines and 'changed' in lines[-1]:
                    # Parse the summary line
                    summary = lines[-1]
                    if 'insertion' in summary:
                        stats["lines_added"] = int(summary.split('insertion')[0].split()[-1])
                    if 'deletion' in summary:
                        stats["lines_deleted"] = int(summary.split('deletion')[0].split()[-1])
                    if 'file' in summary:
                        stats["files_changed"] = int(summary.split('file')[0].strip().split()[-1])
        except:
            pass
        
        return stats
    
    def get_recent_commits(self, limit: int = 5) -> List[str]:
        """Get recent commit hashes"""
        commits = []
        try:
            result = subprocess.run(['git', 'log', '--oneline', f'-{limit}'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                for line in result.stdout.strip().split('\n'):
                    if line:
                        commits.append(line.split()[0])
        except:
            pass
        
        return commits
    
    def create_report(self, 
                     report_type: str,
                     title: str,
                     summary: str,
                     work_performed: List[str],
                     issues: List[Dict],
                     decisions: List[Dict],
                     next_steps: List[str],
                     priority: str = "Medium") -> str:
        """Create a new diary report"""
        
        utc_time, cet_time = self.get_current_datetime()
        date_str = datetime.now().strftime("%Y-%m-%d")
        report_num = self.get_next_report_number(date_str)
        version = self.get_current_version()
        git_stats = self.get_git_stats()
        commits = self.get_recent_commits()
        
        # Create report content
        report_content = f"""# Report {report_num}: {title}

**Date**: {utc_time} | {cet_time}  
**Author**: Claude Code  
**Type**: {report_type}  
**Version**: {version}  
**Priority**: {priority}  

## 📊 Summary
{summary}

## 🔄 Work Performed
"""
        
        for task in work_performed:
            status = "x" if task.get("completed", False) else " "
            report_content += f"- [{status}] {task.get('description', task)}\n"
        
        report_content += f"""
## 📈 Progress Metrics
- Lines of Code: Added [{git_stats['lines_added']}] / Modified [{git_stats['lines_modified']}] / Deleted [{git_stats['lines_deleted']}]
- Files Changed: {git_stats['files_changed']}
- Tests: Passed [X] / Failed [Y]
- Deployment Status: [In Progress]

## 🐛 Issues Encountered
"""
        
        if issues:
            for i, issue in enumerate(issues, 1):
                report_content += f"""
{i}. **Issue**: {issue.get('description', 'Unknown')}
   - **Severity**: {issue.get('severity', 'Medium')}
   - **Resolution**: {issue.get('resolution', 'Pending')}
   - **Time Spent**: {issue.get('time_spent', '0 hours')}
"""
        else:
            report_content += "No significant issues encountered.\n"
        
        report_content += "\n## 💡 Decisions Made\n"
        
        if decisions:
            for decision in decisions:
                report_content += f"""
- **Decision**: {decision.get('decision', 'Unknown')}
- **Rationale**: {decision.get('rationale', 'N/A')}
- **Impact**: {decision.get('impact', 'N/A')}
"""
        else:
            report_content += "No major decisions made in this session.\n"
        
        report_content += "\n## 🔮 Next Steps\n"
        for i, step in enumerate(next_steps, 1):
            report_content += f"{i}. {step}\n"
        
        report_content += f"""
## 📎 References
- Commits: {', '.join(commits) if commits else 'No commits yet'}
- Files Modified: See git status
- Related Reports: N/A
- External Docs: N/A

## ✅ Compliance Check
- [x] Report follows template format
- [x] All sections completed
- [ ] Added to SYSTEM_CHANGELOG.md
- [x] Saved in correct date folder
- [x] Report number is sequential
"""
        
        # Create date directory if it doesn't exist
        date_dir = self.reports_dir / date_str
        date_dir.mkdir(parents=True, exist_ok=True)
        
        # Save report
        filename = f"report_{report_num}_{title.lower().replace(' ', '_')}.md"
        report_path = date_dir / filename
        
        with open(report_path, 'w') as f:
            f.write(report_content)
        
        print(f"✅ Report created: {report_path}")
        
        # Add to SYSTEM_CHANGELOG
        self.update_changelog(date_str, report_num, title, report_type, summary, version)
        
        return str(report_path)
    
    def update_changelog(self, date_str: str, report_num: str, title: str, 
                         report_type: str, summary: str, version: str):
        """Add entry to SYSTEM_CHANGELOG.md"""
        utc_time, cet_time = self.get_current_datetime()
        
        entry = f"""
## {utc_time} | {cet_time} - {title} [📔 REPORT]
**Report**: reports/{date_str}/report_{report_num}_{title.lower().replace(' ', '_')}.md
**Type**: {report_type}
**Summary**: {summary}
**Version**: {version}

---
"""
        
        # Read existing changelog
        if self.changelog_path.exists():
            with open(self.changelog_path, 'r') as f:
                content = f.read()
            
            # Find the insertion point (after the header section)
            lines = content.split('\n')
            insert_index = 0
            for i, line in enumerate(lines):
                if line.startswith('## ') and 'UTC' in line:
                    insert_index = i
                    break
            
            # Insert new entry
            lines.insert(insert_index, entry)
            
            # Write back
            with open(self.changelog_path, 'w') as f:
                f.write('\n'.join(lines))
            
            print(f"✅ Updated SYSTEM_CHANGELOG.md")
    
    def create_daily_summary(self):
        """Create daily summary report"""
        date_str = datetime.now().strftime("%Y-%m-%d")
        date_dir = self.reports_dir / date_str
        
        # Collect all reports from today
        reports = list(date_dir.glob("report_*.md")) if date_dir.exists() else []
        
        utc_time, cet_time = self.get_current_datetime()
        version = self.get_current_version()
        
        summary_content = f"""# Daily Summary - {date_str}

**Date**: {utc_time} | {cet_time}  
**Author**: Claude Code  
**Version**: {version}  

## 📊 Day Overview

Total Reports: {len(reports)}

## 📝 Reports Created Today
"""
        
        for report in sorted(reports):
            summary_content += f"- {report.name}\n"
        
        summary_content += """
## 🎯 Key Achievements
- [List major accomplishments]

## 🚧 Outstanding Issues
- [List unresolved issues]

## 📅 Tomorrow's Priorities
- [List top priorities for next day]

## 📈 Metrics Summary
- Total Commits: [X]
- Total Lines Changed: [X]
- Tests Passed: [X/Y]
- Deployment Status: [Status]

---
*End of Day Summary*
"""
        
        summary_path = date_dir / "DAILY_SUMMARY.md"
        with open(summary_path, 'w') as f:
            f.write(summary_content)
        
        print(f"✅ Daily summary created: {summary_path}")
        return str(summary_path)
    
    def validate_report(self, report_path: str) -> Dict[str, bool]:
        """Validate a report against the protocol"""
        validation = {
            "exists": False,
            "format_correct": False,
            "all_sections": False,
            "in_changelog": False,
            "sequential_number": False
        }
        
        report_path = Path(report_path)
        
        # Check existence
        validation["exists"] = report_path.exists()
        if not validation["exists"]:
            return validation
        
        # Check format
        with open(report_path, 'r') as f:
            content = f.read()
        
        required_sections = [
            "## 📊 Summary",
            "## 🔄 Work Performed",
            "## 📈 Progress Metrics",
            "## 🐛 Issues Encountered",
            "## 💡 Decisions Made",
            "## 🔮 Next Steps",
            "## 📎 References",
            "## ✅ Compliance Check"
        ]
        
        validation["all_sections"] = all(section in content for section in required_sections)
        
        # Check format (basic)
        validation["format_correct"] = content.startswith("# Report")
        
        # Check if in changelog
        if self.changelog_path.exists():
            with open(self.changelog_path, 'r') as f:
                changelog = f.read()
            validation["in_changelog"] = report_path.name in changelog
        
        # Check sequential number
        report_num = report_path.stem.split('_')[1]
        validation["sequential_number"] = report_num.isdigit() and len(report_num) == 3
        
        return validation
    
    def check_compliance(self) -> Dict[str, any]:
        """Check overall diary compliance"""
        today = datetime.now().strftime("%Y-%m-%d")
        today_dir = self.reports_dir / today
        
        compliance = {
            "has_reports_today": today_dir.exists() and len(list(today_dir.glob("report_*.md"))) > 0,
            "has_daily_summary": (today_dir / "DAILY_SUMMARY.md").exists() if today_dir.exists() else False,
            "reports_count": len(list(today_dir.glob("report_*.md"))) if today_dir.exists() else 0,
            "last_report_time": None,
            "compliance_score": 0
        }
        
        # Get last report time
        if today_dir.exists():
            reports = list(today_dir.glob("report_*.md"))
            if reports:
                latest = max(reports, key=lambda p: p.stat().st_mtime)
                compliance["last_report_time"] = datetime.fromtimestamp(latest.stat().st_mtime).strftime("%H:%M:%S")
        
        # Calculate compliance score
        score = 0
        if compliance["has_reports_today"]:
            score += 40
        if compliance["has_daily_summary"]:
            score += 20
        if compliance["reports_count"] >= 1:
            score += 20
        if compliance["reports_count"] >= 3:
            score += 20
        
        compliance["compliance_score"] = score
        
        return compliance


def main():
    """CLI interface for diary report generator"""
    parser = argparse.ArgumentParser(description="AVA OLO Diary Report Generator")
    parser.add_argument('action', choices=['create', 'validate', 'check', 'daily'],
                       help='Action to perform')
    parser.add_argument('--type', default='Daily',
                       choices=['Daily', 'Deployment', 'Investigation', 'Feature', 'BugFix', 'Configuration', 'Emergency'],
                       help='Type of report')
    parser.add_argument('--title', help='Report title')
    parser.add_argument('--summary', help='Report summary')
    parser.add_argument('--priority', default='Medium',
                       choices=['Low', 'Medium', 'High', 'Critical'],
                       help='Report priority')
    parser.add_argument('--report', help='Path to report for validation')
    
    args = parser.parse_args()
    generator = DiaryReportGenerator()
    
    if args.action == 'create':
        if not args.title or not args.summary:
            print("❌ Error: --title and --summary are required for create action")
            sys.exit(1)
        
        # Interactive mode for details
        print("📝 Creating new diary report...")
        print("Enter work performed (one per line, empty line to finish):")
        work_performed = []
        while True:
            task = input("> ")
            if not task:
                break
            work_performed.append(task)
        
        print("\nEnter issues encountered (empty line to skip):")
        issues = []
        while True:
            issue_desc = input("Issue description (empty to finish): ")
            if not issue_desc:
                break
            severity = input("Severity (Low/Medium/High/Critical): ")
            resolution = input("Resolution (Fixed/Workaround/Pending): ")
            time_spent = input("Time spent (e.g., '2 hours'): ")
            issues.append({
                "description": issue_desc,
                "severity": severity,
                "resolution": resolution,
                "time_spent": time_spent
            })
        
        print("\nEnter decisions made (empty line to skip):")
        decisions = []
        while True:
            decision = input("Decision (empty to finish): ")
            if not decision:
                break
            rationale = input("Rationale: ")
            impact = input("Impact: ")
            decisions.append({
                "decision": decision,
                "rationale": rationale,
                "impact": impact
            })
        
        print("\nEnter next steps (one per line, empty line to finish):")
        next_steps = []
        while True:
            step = input("> ")
            if not step:
                break
            next_steps.append(step)
        
        report_path = generator.create_report(
            report_type=args.type,
            title=args.title,
            summary=args.summary,
            work_performed=work_performed,
            issues=issues,
            decisions=decisions,
            next_steps=next_steps,
            priority=args.priority
        )
        
        print(f"\n✅ Report created successfully: {report_path}")
    
    elif args.action == 'validate':
        if not args.report:
            print("❌ Error: --report path is required for validate action")
            sys.exit(1)
        
        validation = generator.validate_report(args.report)
        print(f"\n📋 Validation Results for {args.report}:")
        for check, passed in validation.items():
            status = "✅" if passed else "❌"
            print(f"  {status} {check.replace('_', ' ').title()}")
        
        if all(validation.values()):
            print("\n✅ Report is fully compliant!")
        else:
            print("\n❌ Report has compliance issues!")
    
    elif args.action == 'check':
        compliance = generator.check_compliance()
        print("\n📊 Diary Compliance Status:")
        print(f"  Reports Today: {compliance['reports_count']}")
        print(f"  Has Daily Summary: {'✅' if compliance['has_daily_summary'] else '❌'}")
        print(f"  Last Report Time: {compliance['last_report_time'] or 'N/A'}")
        print(f"  Compliance Score: {compliance['compliance_score']}%")
        
        if compliance['compliance_score'] >= 90:
            print("\n🟢 Excellent compliance!")
        elif compliance['compliance_score'] >= 70:
            print("\n🟡 Good compliance")
        elif compliance['compliance_score'] >= 50:
            print("\n🟠 Needs improvement")
        else:
            print("\n🔴 Non-compliant - immediate action required!")
    
    elif args.action == 'daily':
        summary_path = generator.create_daily_summary()
        print(f"\n✅ Daily summary created: {summary_path}")


if __name__ == "__main__":
    main()