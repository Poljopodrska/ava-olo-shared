# AVA OLO Database Schema
*Auto-generated every 15 minutes - DO NOT EDIT MANUALLY*  
*Last Updated: [Pending first auto-update]*

## Overview
This document contains the current database schema for the AVA OLO agricultural CRM system.
All tables, columns, types, and relationships are automatically extracted from the production database.

## Tables

### farmers
*Core farmer information table*

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| id | integer | NO | auto-increment | PK |
| first_name | varchar(100) | NO | | |
| last_name | varchar(100) | NO | | |
| whatsapp_number | varchar(50) | NO | | UNIQUE |
| farm_location | text | YES | | |
| primary_crops | text | YES | | |
| created_at | timestamp | NO | CURRENT_TIMESTAMP | |
| updated_at | timestamp | YES | | |

### fields
*Farmer field boundaries and information*

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| id | integer | NO | auto-increment | PK |
| farmer_id | integer | NO | | FK→farmers.id |
| field_name | varchar(255) | NO | | |
| coordinates | jsonb | YES | | |
| area_hectares | decimal(10,2) | YES | | |
| crop_type | varchar(100) | YES | | |
| created_at | timestamp | NO | CURRENT_TIMESTAMP | |

### conversations
*Chat history between farmers and AVA OLO*

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| id | integer | NO | auto-increment | PK |
| farmer_id | integer | NO | | FK→farmers.id |
| message | text | NO | | |
| sender | varchar(20) | NO | | |
| timestamp | timestamp | NO | CURRENT_TIMESTAMP | |

### llm_debug_log
*All LLM queries for transparency*

| Column | Type | Nullable | Default | Key |
|--------|------|----------|---------|-----|
| id | integer | NO | auto-increment | PK |
| query_type | varchar(100) | NO | | |
| input_data | jsonb | NO | | |
| output_data | jsonb | YES | | |
| timestamp | timestamp | NO | CURRENT_TIMESTAMP | |

## Notes
- All farmer personal data must be encrypted (PRIVACY-FIRST principle)
- WhatsApp numbers are the primary farmer identifier
- All queries should be logged to llm_debug_log for transparency
- Schema follows PostgreSQL-only principle (no other databases)

## Usage
- Web Claude: Reference this for specification writing
- Claude Code: Use for implementation queries
- Auto-updates: Every 15 minutes from production database

## Setup Instructions
1. Set DATABASE_URL environment variable
2. Run: `crontab -e`
3. Add: `*/15 * * * * cd /path/to/ava-olo-shared/scripts && python3 update_database_schema.py`
4. Schema will auto-update every 15 minutes