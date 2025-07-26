# Dependency Analysis Report
Generated: 2025-07-26T19:42:38.985334

## Summary
- Total Dependencies: 577
- Files Analyzed: 536
- Dependency Types: 6

## Dependency Breakdown by Type

### Api Call (258)
- `agronomic_approval.py` → `approval`
- `agronomic_approval.py` → `approval`
- `agronomic_approval.py` → `approve`
- `agronomic_approval.py` → `approval`
- `agronomic_approval.py` → `bulk_approve`
- `agronomic_approval.py` → `approval`
- `agronomic_approval.py` → `manual_message`
- `agronomic_approval.py` → `approval`
- `business_dashboard.py` → `metrics`
- `business_dashboard.py` → `farmer-growth`
- ... and 248 more

### Critical Component (131)
- `current_dashboard.html` → `critical_component:yellow_debug_box`
- `current_dashboard.html` → `critical_component:yellow_debug_box`
- `current_dashboard.html` → `critical_component:dashboard_layout`
- `current_dashboard.html` → `critical_component:navigation_menu`
- `current_dashboard.html` → `critical_component:yellow_debug_box`
- `current_dashboard.html` → `critical_component:dashboard_layout`
- `business-dashboard.html` → `critical_component:farmer_count_display`
- `business-dashboard.html` → `critical_component:farmer_count_display`
- `business-dashboard.html` → `critical_component:farmer_count_display`
- `business-dashboard.html` → `critical_component:farmer_count_display`
- ... and 121 more

### Python Import (120)
- `admin_dashboard.py` → `admin_dashboard_api.py`
- `admin_dashboard.py` → `dashboard_config.py`
- `check_existing_tables.py` → `config.py`
- `create_cava_tables.py` → `config.py`
- `health_check_dashboard.py` → `llm_query_processor.py`
- `main.py` → `config.py`
- `main.py` → `database_manager.py`
- `main.py` → `deployment_routes.py`
- `main.py` → `database_routes.py`
- `main.py` → `health_routes.py`
- ... and 110 more

### Static Href (42)
- `business-dashboard.html` → `dashboard-common.css`
- `database-dashboard.html` → `dashboard-common.css`
- `health-dashboard.html` → `dashboard-common.css`
- `index.html` → `dashboard-common.css`
- `agronomic_dashboard.html` → `constitutional-design-system-v2.css`
- `base_constitutional.html` → `constitutional-design.css`
- `business_dashboard_constitutional.html` → `constitutional-design-system-v2.css`
- `cava_registration.html` → `constitutional-design-v3.css`
- `dashboard.html` → `constitutional-design-v3.css`
- `database_dashboard_landing.html` → `constitutional-design-system-v2.css`
- ... and 32 more

### Static Src (14)
- `database-dashboard.html` → `database-queries.js`
- `dashboard.html` → `constitutional-interactions.js`
- `farmer_registration_old.html` → `field_drawing.js`
- `field_drawing_test.html` → `field_drawing.js`
- `landing.html` → `constitutional-interactions.js`
- `pure_chat.html` → `code-indicator.js`
- `register_chat.html` → `code-indicator.js`
- `register_llm.html` → `code-indicator.js`
- `register.html` → `constitutional-interactions.js`
- `signin.html` → `constitutional-interactions.js`
- ... and 4 more

### Template Extends (12)
- `database_explorer_enhanced.html` → `base_constitutional.html`
- `farmer_registration.html` → `base_constitutional.html`
- `register_fields.html` → `base_constitutional.html`
- `register_machinery.html` → `base_constitutional.html`
- `register_task.html` → `base_constitutional.html`
- `ui_dashboard_enhanced.html` → `base_constitutional.html`
- `database_explorer_enhanced.html` → `base_constitutional.html`
- `farmer_registration.html` → `base_constitutional.html`
- `register_fields.html` → `base_constitutional.html`
- `register_machinery.html` → `base_constitutional.html`
- ... and 2 more

## 🚨 Critical Component Dependencies (131)

### Yellow Debug Box
Used in 7 files:
- `current_dashboard.html` (line 25)
- `current_dashboard.html` (line 34)
- `current_dashboard.html` (line 116)
- `current_dashboard.html` (line 25)
- `current_dashboard.html` (line 34)
- `current_dashboard.html` (line 116)
- `database_schema_viewer.html` (line 230)

### Dashboard Layout
Used in 47 files:
- `current_dashboard.html` (line 58)
- `current_dashboard.html` (line 147)
- `index.html` (line 9)
- `index.html` (line 215)
- `agronomic_approval.html` (line 42)
- `agronomic_approval.html` (line 333)
- `agronomic_approval.html` (line 363)
- `agronomic_dashboard.html` (line 17)
- `agronomic_dashboard.html` (line 270)
- `business_dashboard.html` (line 50)
- `business_dashboard.html` (line 357)
- `business_dashboard.html` (line 375)
- `business_dashboard_constitutional.html` (line 46)
- `business_dashboard_constitutional.html` (line 217)
- `business_dashboard_constitutional.html` (line 234)
- `business_dashboard_constitutional.html` (line 304)
- `dashboard.html` (line 23)
- `dashboard.html` (line 470)
- `dashboard.html` (line 511)
- `farmer_registration_old.html` (line 66)
- `farmer_registration_old.html` (line 307)
- `ui_dashboard_enhanced.html` (line 7)
- `ui_dashboard_enhanced.html` (line 111)
- `ui_dashboard_enhanced.html` (line 139)
- `ui_dashboard_enhanced.html` (line 167)
- `current_dashboard.html` (line 58)
- `current_dashboard.html` (line 147)
- `index.html` (line 9)
- `index.html` (line 215)
- `agronomic_approval.html` (line 42)
- `agronomic_approval.html` (line 333)
- `agronomic_approval.html` (line 363)
- `agronomic_dashboard.html` (line 17)
- `agronomic_dashboard.html` (line 270)
- `business_dashboard.html` (line 50)
- `business_dashboard.html` (line 357)
- `business_dashboard.html` (line 375)
- `business_dashboard_constitutional.html` (line 46)
- `business_dashboard_constitutional.html` (line 217)
- `business_dashboard_constitutional.html` (line 234)
- `business_dashboard_constitutional.html` (line 304)
- `farmer_registration_old.html` (line 66)
- `farmer_registration_old.html` (line 307)
- `ui_dashboard_enhanced.html` (line 7)
- `ui_dashboard_enhanced.html` (line 111)
- `ui_dashboard_enhanced.html` (line 139)
- `ui_dashboard_enhanced.html` (line 167)

### Navigation Menu
Used in 27 files:
- `current_dashboard.html` (line 85)
- `database-dashboard.html` (line 16)
- `database-dashboard.html` (line 237)
- `database-dashboard.html` (line 262)
- `database-dashboard.html` (line 263)
- `base_constitutional.html` (line 11)
- `base_constitutional.html` (line 74)
- `base_constitutional.html` (line 78)
- `base_constitutional.html` (line 79)
- `base_constitutional.html` (line 96)
- `base_constitutional.html` (line 97)
- `base_constitutional.html` (line 102)
- `base_constitutional.html` (line 112)
- `register.html` (line 404)
- `current_dashboard.html` (line 85)
- `database-dashboard.html` (line 16)
- `database-dashboard.html` (line 237)
- `database-dashboard.html` (line 263)
- `database-dashboard.html` (line 264)
- `base_constitutional.html` (line 11)
- `base_constitutional.html` (line 74)
- `base_constitutional.html` (line 78)
- `base_constitutional.html` (line 79)
- `base_constitutional.html` (line 96)
- `base_constitutional.html` (line 97)
- `base_constitutional.html` (line 102)
- `base_constitutional.html` (line 112)

### Farmer Count Display
Used in 50 files:
- `business-dashboard.html` (line 294)
- `business-dashboard.html` (line 428)
- `business-dashboard.html` (line 428)
- `business-dashboard.html` (line 454)
- `business-dashboard.html` (line 454)
- `business-dashboard.html` (line 576)
- `business-dashboard.html` (line 576)
- `database-dashboard.html` (line 267)
- `database-dashboard.html` (line 267)
- `database-dashboard.html` (line 319)
- `index.html` (line 196)
- `index.html` (line 297)
- `index.html` (line 297)
- `index.html` (line 297)
- `business_dashboard.html` (line 502)
- `database_retrieval.html` (line 237)
- `database_retrieval.html` (line 289)
- `ui_dashboard_enhanced.html` (line 92)
- `ui_dashboard_enhanced.html` (line 190)
- `ui_dashboard_enhanced.html` (line 194)
- `ui_dashboard_enhanced.html` (line 194)
- `ui_dashboard_enhanced.html` (line 194)
- `ui_dashboard_enhanced.html` (line 234)
- `whatsapp_mock.html` (line 268)
- `business-dashboard.html` (line 294)
- `business-dashboard.html` (line 457)
- `business-dashboard.html` (line 457)
- `business-dashboard.html` (line 483)
- `business-dashboard.html` (line 483)
- `business-dashboard.html` (line 605)
- `business-dashboard.html` (line 605)
- `data-entry.html` (line 322)
- `data-entry.html` (line 323)
- `database-dashboard.html` (line 268)
- `database-dashboard.html` (line 268)
- `database-dashboard.html` (line 327)
- `index.html` (line 196)
- `index.html` (line 297)
- `index.html` (line 297)
- `index.html` (line 297)
- `business_dashboard.html` (line 502)
- `database_retrieval.html` (line 382)
- `database_retrieval.html` (line 438)
- `ui_dashboard_enhanced.html` (line 92)
- `ui_dashboard_enhanced.html` (line 190)
- `ui_dashboard_enhanced.html` (line 194)
- `ui_dashboard_enhanced.html` (line 194)
- `ui_dashboard_enhanced.html` (line 194)
- `ui_dashboard_enhanced.html` (line 234)
- `whatsapp_mock.html` (line 268)
