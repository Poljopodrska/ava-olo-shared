# 📁 AVA OLO Folder Structure Guide

## Overview
This guide documents the organized folder structure for the AVA OLO agricultural system, designed for efficient development and easy navigation.

## Root Structure

```
ava-olo-constitutional/
├── 📁 ava-olo-shared/              # Shared infrastructure and docs
├── 🌾 ava-olo-agricultural-core/   # Farmer-facing service
├── 📊 ava-olo-monitoring-dashboards/ # Business intelligence service
├── 🗑️ cleanup_scripts/             # File organization scripts
└── 📄 README.md                    # Project overview
```

## Detailed Structure

### 📁 ava-olo-shared/
Central location for shared resources across all services

```
ava-olo-shared/
├── essentials/                    # Core documentation
│   ├── web_claude_upload/        # ONLY files for Web Claude (8 files)
│   │   ├── AVA_OLO_CONSTITUTION.md
│   │   ├── IMPLEMENTATION_GUIDELINES.md
│   │   ├── SPECIFICATION_GUIDELINES.md
│   │   ├── CAVA_TECHNICAL_SPECIFICATION.md
│   │   ├── DATABASE_SCHEMA.md
│   │   ├── MANGO_RULE_CLARIFICATION.md
│   │   ├── QUICK_START.md
│   │   ├── SYSTEM_CHANGELOG.md
│   │   ├── README.md             # Upload instructions
│   │   └── UPLOAD_CHECKLIST.md   # Pre-upload checklist
│   │
│   ├── guidelines/               # All development guidelines
│   ├── reports/                  # Investigation and audit reports
│   └── archives/                 # Old but important docs
│
├── environments/                 # Central configuration
│   └── central_config.py        # ALL environment variables
│
├── protection_system/           # Deployment protection
│   ├── feature_protection.py
│   └── constitutional_guard.py
│
├── deployment_tools/            # Scripts and tools
│   ├── deploy_*.sh
│   └── verify_*.py
│
├── design-system/              # Constitutional design
│   ├── constitutional-design-v3.css
│   └── assets/
│
└── version_config.py           # Central version management
```

### 🌾 ava-olo-agricultural-core/
Farmer-facing application with CAVA integration

```
ava-olo-agricultural-core/
├── modules/                    # Core business logic
│   ├── api/                   # API endpoints
│   ├── core/                  # Core services
│   ├── farmer/                # Farmer-specific logic
│   └── cava/                  # CAVA conversation engine
│
├── templates/                 # HTML templates
├── static/                    # Static assets
├── tests/                     # All test files
├── migrations/                # Database migrations
├── main.py                    # Main application
├── requirements.txt           # Python dependencies
└── Dockerfile                 # Container definition
```

### 📊 ava-olo-monitoring-dashboards/
Business intelligence and monitoring dashboards

```
ava-olo-monitoring-dashboards/
├── modules/                    # Dashboard logic
│   ├── api/                   # API endpoints
│   ├── core/                  # Core services
│   │   ├── feature_protection.py
│   │   ├── constitutional_guard.py
│   │   ├── version_middleware.py
│   │   └── maps_config.py
│   └── dashboards/            # Dashboard modules
│
├── static/                    # Static assets
│   └── dashboards/           # Dashboard HTML/JS
│       ├── field-drawing.html
│       └── js/
│
├── templates/                 # HTML templates
├── tests/                     # All test files
├── main.py                    # Main application
└── requirements.txt           # Python dependencies
```

## 🚨 Important Locations

### For Web Claude Upload
**ALWAYS use**: `/ava-olo-shared/essentials/web_claude_upload/`
- Contains exactly 8 essential files
- No need to search for files elsewhere
- Updated automatically from main essentials

### For Environment Variables
**ONLY location**: `/ava-olo-shared/environments/central_config.py`
- All API keys
- Database configuration
- Service URLs
- Feature flags

### For Documentation
**Primary location**: `/ava-olo-shared/essentials/`
- Constitutional documents
- Guidelines
- System changelog
- Reports in subdirectories

### For Git Hooks
**Location**: `/.githooks/`
- Commit message validation
- Version format enforcement

## 🗑️ Cleanup Status

### Duplicate Files
- **Found**: 150+ duplicate files between services
- **Action**: Keep in service-specific locations for now
- **Future**: Gradually consolidate to shared folder

### Obsolete Files
- `*_backup.py` files
- `*_old.md` files
- Test files outside test directories
- Temporary deployment triggers

### AWS CLI Duplicates
- Both services have full AWS CLI copies
- Consider removing or using system-wide installation

## 📋 File Organization Rules

1. **Documentation**: All in `/essentials/`
2. **Shared Code**: In `/ava-olo-shared/`
3. **Service Code**: In respective service folders
4. **Tests**: Always in `/tests/` subdirectory
5. **Static Files**: In `/static/` subdirectory
6. **Templates**: In `/templates/` subdirectory

## 🔄 Maintenance Tasks

### Weekly
- Clean up duplicate files
- Update Web Claude upload folder
- Check for obsolete files

### Monthly
- Review folder structure
- Consolidate shared code
- Archive old reports

## 🎯 Benefits of This Structure

1. **Web Claude Ready**: Upload folder has exactly what's needed
2. **No Searching**: Clear locations for everything
3. **No Duplication**: Shared resources in one place
4. **Easy Navigation**: Logical organization
5. **Constitutional Compliance**: Follows all principles

---

**Last Updated**: 2025-07-27
**Version**: v3.5.1 - File organization structure