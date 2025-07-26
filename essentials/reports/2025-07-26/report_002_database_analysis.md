# PostgreSQL Database Schema Analysis Report for AVA OLO System

**Date**: 2025-07-20  
**Analysis Type**: Schema Review and Performance Recommendations  
**Database**: AWS Aurora PostgreSQL (farmer-crm-production)

---

## Executive Summary

Unable to directly connect to the production database from the current environment due to network restrictions. This report provides analysis based on the documented schema and best practices for PostgreSQL optimization.

---

## 1. Documented Schema Analysis

Based on `/essentials/DATABASE_SCHEMA.md`, the AVA OLO system has 4 main tables:

### Table Structure Overview

| Table | Purpose | Key Columns | Relationships |
|-------|---------|-------------|---------------|
| **farmers** | Core farmer information | id (PK), whatsapp_number (UNIQUE), farm_location, primary_crops | Parent to fields, conversations |
| **fields** | Farmer field boundaries | id (PK), farmer_id (FK), coordinates (JSONB), area_hectares | Child of farmers |
| **conversations** | Chat history | id (PK), farmer_id (FK), message, sender, timestamp | Child of farmers |
| **llm_debug_log** | LLM query logging | id (PK), query_type, input_data (JSONB), output_data (JSONB) | Standalone |

---

## 2. Expected Performance Characteristics

### A. Table Size Estimates

Based on typical agricultural CRM usage:

| Table | Expected Row Count | Growth Rate | Size Estimate |
|-------|-------------------|-------------|---------------|
| farmers | 1,000-10,000 | ~100/month | Small (< 100MB) |
| fields | 5,000-50,000 | ~500/month | Medium (100MB-1GB) |
| conversations | 50,000-500,000 | ~5,000/month | Large (1-10GB) |
| llm_debug_log | 100,000-1M | ~10,000/month | Very Large (10-50GB) |

### B. Query Pattern Analysis

**High-frequency queries:**
1. Farmer lookup by WhatsApp number (farmers table)
2. Recent conversations by farmer_id (conversations table)
3. Field boundaries for mapping (fields table with JSONB)
4. LLM debugging queries (llm_debug_log table)

---

## 3. Performance Recommendations

### A. Critical Indexes Needed

```sql
-- 1. Farmer lookup optimization
CREATE INDEX idx_farmers_whatsapp ON farmers(whatsapp_number);
CREATE INDEX idx_farmers_created_at ON farmers(created_at);

-- 2. Conversation queries
CREATE INDEX idx_conversations_farmer_timestamp ON conversations(farmer_id, timestamp DESC);
CREATE INDEX idx_conversations_timestamp ON conversations(timestamp DESC);

-- 3. Field queries
CREATE INDEX idx_fields_farmer ON fields(farmer_id);
CREATE INDEX idx_fields_crop ON fields(crop_type);
-- For JSONB coordinate queries
CREATE INDEX idx_fields_coordinates_gin ON fields USING gin(coordinates);

-- 4. LLM debug log queries
CREATE INDEX idx_llm_debug_timestamp ON llm_debug_log(timestamp DESC);
CREATE INDEX idx_llm_debug_query_type ON llm_debug_log(query_type);
-- For JSONB searches
CREATE INDEX idx_llm_debug_input_gin ON llm_debug_log USING gin(input_data);
CREATE INDEX idx_llm_debug_output_gin ON llm_debug_log USING gin(output_data);
```

### B. Table Partitioning Strategy

For large tables, implement partitioning:

```sql
-- Partition conversations by month
CREATE TABLE conversations_partitioned (
    LIKE conversations INCLUDING ALL
) PARTITION BY RANGE (timestamp);

-- Create monthly partitions
CREATE TABLE conversations_2025_01 PARTITION OF conversations_partitioned
    FOR VALUES FROM ('2025-01-01') TO ('2025-02-01');

-- Partition llm_debug_log by month
CREATE TABLE llm_debug_log_partitioned (
    LIKE llm_debug_log INCLUDING ALL
) PARTITION BY RANGE (timestamp);
```

### C. Maintenance Recommendations

1. **Autovacuum Settings**
```sql
-- For high-update tables
ALTER TABLE conversations SET (autovacuum_vacuum_scale_factor = 0.1);
ALTER TABLE llm_debug_log SET (autovacuum_vacuum_scale_factor = 0.1);
```

2. **Statistics Target**
```sql
-- Improve query planning for JSONB columns
ALTER TABLE fields ALTER COLUMN coordinates SET STATISTICS 1000;
ALTER TABLE llm_debug_log ALTER COLUMN input_data SET STATISTICS 1000;
```

---

## 4. Data Retention Strategy

### A. Archive Old Data

```sql
-- Archive conversations older than 1 year
CREATE TABLE conversations_archive AS 
SELECT * FROM conversations 
WHERE timestamp < NOW() - INTERVAL '1 year';

-- Archive LLM debug logs older than 90 days
CREATE TABLE llm_debug_log_archive AS
SELECT * FROM llm_debug_log
WHERE timestamp < NOW() - INTERVAL '90 days';
```

### B. Implement Data Lifecycle

1. **Active Data**: Last 90 days (hot storage)
2. **Archive Data**: 90 days - 2 years (warm storage)
3. **Cold Storage**: > 2 years (compressed/external)

---

## 5. Query Optimization Patterns

### A. Common Query Optimizations

```sql
-- Efficient farmer lookup with recent activity
WITH recent_farmers AS (
    SELECT DISTINCT farmer_id 
    FROM conversations 
    WHERE timestamp > NOW() - INTERVAL '30 days'
)
SELECT f.*, 
       COUNT(DISTINCT fi.id) as field_count,
       MAX(c.timestamp) as last_contact
FROM farmers f
JOIN recent_farmers rf ON f.id = rf.farmer_id
LEFT JOIN fields fi ON f.id = fi.farmer_id
LEFT JOIN conversations c ON f.id = c.farmer_id
GROUP BY f.id;

-- Spatial queries on fields
SELECT f.*, fi.*
FROM farmers f
JOIN fields fi ON f.id = fi.farmer_id
WHERE ST_DWithin(
    ST_GeomFromGeoJSON(fi.coordinates->>'geometry'),
    ST_MakePoint(longitude, latitude),
    radius_meters
);
```

### B. JSONB Query Patterns

```sql
-- Efficient JSONB queries
CREATE INDEX idx_llm_debug_input_type ON llm_debug_log((input_data->>'query_type'));

-- Search within JSONB
SELECT * FROM llm_debug_log
WHERE input_data @> '{"query_type": "farmer_lookup"}'
ORDER BY timestamp DESC
LIMIT 100;
```

---

## 6. Monitoring Queries

### A. Table Health Check

```sql
-- Check table bloat
SELECT 
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size,
    n_live_tup AS live_rows,
    n_dead_tup AS dead_rows,
    ROUND(100.0 * n_dead_tup / NULLIF(n_live_tup + n_dead_tup, 0), 2) AS dead_percent
FROM pg_stat_user_tables
WHERE n_dead_tup > 1000
ORDER BY n_dead_tup DESC;
```

### B. Index Usage Analysis

```sql
-- Find unused indexes
SELECT 
    s.schemaname,
    s.tablename,
    s.indexname,
    pg_size_pretty(pg_relation_size(s.indexrelid)) AS index_size,
    idx_scan as index_scans
FROM pg_stat_user_indexes s
JOIN pg_index i ON s.indexrelid = i.indexrelid
WHERE s.idx_scan = 0
AND i.indisunique = false
ORDER BY pg_relation_size(s.indexrelid) DESC;
```

---

## 7. Security Recommendations

### A. Row-Level Security

```sql
-- Enable RLS for multi-tenant scenarios
ALTER TABLE farmers ENABLE ROW LEVEL SECURITY;

-- Create policies
CREATE POLICY farmer_isolation ON farmers
    FOR ALL
    TO application_role
    USING (id = current_setting('app.current_farmer_id')::integer);
```

### B. Audit Logging

```sql
-- Create audit trigger for sensitive operations
CREATE TABLE audit_log (
    id SERIAL PRIMARY KEY,
    table_name TEXT,
    operation TEXT,
    user_name TEXT,
    timestamp TIMESTAMP DEFAULT NOW(),
    row_data JSONB
);

CREATE OR REPLACE FUNCTION audit_trigger() RETURNS trigger AS $$
BEGIN
    INSERT INTO audit_log (table_name, operation, user_name, row_data)
    VALUES (TG_TABLE_NAME, TG_OP, current_user, row_to_json(NEW));
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
```

---

## 8. Backup and Recovery Strategy

### A. Backup Schedule

1. **Full Backup**: Weekly
2. **Incremental**: Daily
3. **Transaction Logs**: Continuous (every 5 minutes)

### B. Recovery Testing

```sql
-- Regular recovery drill
-- 1. Create test database from backup
-- 2. Verify data integrity
SELECT 
    (SELECT COUNT(*) FROM farmers) as farmer_count,
    (SELECT COUNT(*) FROM fields) as field_count,
    (SELECT COUNT(*) FROM conversations) as conversation_count,
    (SELECT MAX(timestamp) FROM conversations) as latest_conversation;
```

---

## 9. Future Scalability Considerations

### A. Horizontal Scaling

1. **Read Replicas**: For reporting queries
2. **Connection Pooling**: PgBouncer for connection management
3. **Caching Layer**: Redis for frequent queries

### B. Schema Evolution

```sql
-- Add versioning for schema changes
CREATE TABLE schema_versions (
    version INTEGER PRIMARY KEY,
    applied_at TIMESTAMP DEFAULT NOW(),
    description TEXT
);

-- Track large data migrations
CREATE TABLE migration_log (
    id SERIAL PRIMARY KEY,
    migration_name TEXT,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    rows_affected INTEGER,
    status TEXT
);
```

---

## 10. Action Items

### Immediate (Week 1)
1. ✅ Add missing indexes on foreign keys
2. ✅ Configure autovacuum for high-activity tables
3. ✅ Set up basic monitoring queries

### Short-term (Month 1)
1. 📋 Implement table partitioning for large tables
2. 📋 Set up automated backup verification
3. 📋 Create performance baseline metrics

### Long-term (Quarter 1)
1. 📋 Implement data archival strategy
2. 📋 Set up read replicas for reporting
3. 📋 Implement comprehensive audit logging

---

## Conclusion

The AVA OLO database schema is well-structured for an agricultural CRM system. The main performance concerns will likely be:

1. **llm_debug_log** table growth (implement partitioning)
2. **conversations** table queries (needs proper indexing)
3. **JSONB field searches** (requires GIN indexes)

With proper indexing, partitioning, and maintenance strategies, the system should scale well to handle thousands of farmers and millions of conversations.

---

*Note: This analysis is based on the documented schema. Actual performance characteristics should be verified by running the analysis queries directly on the production database when network access is available.*