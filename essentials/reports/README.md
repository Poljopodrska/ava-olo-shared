# AVA OLO Reports Directory

This directory contains all reports generated during the development process of the AVA OLO system.

## Structure

Reports are organized by date in YYYY-MM-DD format:
```
reports/
├── README.md (this file)
├── 2025-07-20/
│   ├── report_001_ecs_migration_status.md
│   ├── report_002_deployment_analysis.md
│   └── ...
├── 2025-07-21/
│   └── ...
└── ...
```

## Naming Convention

Reports should follow this naming pattern:
`report_XXX_descriptive_name.md`

Where:
- `XXX` is a three-digit sequential number for that day (001, 002, etc.)
- `descriptive_name` is a brief description using underscores

## Report Types

Common report types include:
- **Investigation Reports** - Root cause analysis, debugging findings
- **Migration Reports** - Status and progress of system migrations
- **Performance Reports** - Performance analysis and optimization findings
- **Incident Reports** - Post-mortem analysis of production issues
- **Audit Reports** - Security, compliance, or code quality audits
- **Cost Analysis Reports** - AWS resource usage and optimization

## Report Template

Each report should include:
1. **Title** - Clear, descriptive title
2. **Date & Time** - Both UTC and CET timestamps
3. **Author** - Who created the report (usually Claude Code)
4. **Summary** - Executive summary (2-3 sentences)
5. **Details** - Main content of the report
6. **Recommendations** - Actionable next steps
7. **References** - Links to relevant code, logs, or documentation

## Integration with SYSTEM_CHANGELOG.md

When a report is created:
1. Add an entry to SYSTEM_CHANGELOG.md
2. Include a reference to the report file path
3. Use the appropriate icon (usually 🔍 for investigations)

Example changelog entry:
```markdown
## 2025-07-20 10:30:00 UTC | 12:30:00 CET - ECS Migration Analysis [🔍 INVESTIGATION]
**Report**: reports/2025-07-20/report_001_ecs_migration_status.md
**Summary**: Analyzed ECS migration blockers and cost implications
```

## Retention Policy

Reports are permanent documentation and should not be deleted. They serve as:
- Historical record of decisions and investigations
- Learning resources for future similar situations
- Audit trail for compliance and debugging