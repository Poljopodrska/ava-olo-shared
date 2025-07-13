-- Database Schema Updates for Constitutional Amendment #13
-- Country-Based Localization Implementation
-- 
-- This schema maintains constitutional compliance:
-- - PostgreSQL only (Principle #2)
-- - No hardcoded country-specific data (Principle #1)
-- - Privacy-first design (Principle #5)

-- =====================================================
-- FARMER TABLE ENHANCEMENTS
-- =====================================================

-- Add country and localization columns to farmers table
ALTER TABLE farmers 
ADD COLUMN IF NOT EXISTS country_code VARCHAR(3),
ADD COLUMN IF NOT EXISTS preferred_language VARCHAR(10),
ADD COLUMN IF NOT EXISTS whatsapp_number VARCHAR(20) UNIQUE,
ADD COLUMN IF NOT EXISTS timezone VARCHAR(50),
ADD COLUMN IF NOT EXISTS localization_preferences JSONB DEFAULT '{}';

-- Add indexes for efficient querying
CREATE INDEX IF NOT EXISTS idx_farmers_country_code ON farmers(country_code);
CREATE INDEX IF NOT EXISTS idx_farmers_whatsapp_number ON farmers(whatsapp_number);
CREATE INDEX IF NOT EXISTS idx_farmers_language ON farmers(preferred_language);

-- Add comments for documentation
COMMENT ON COLUMN farmers.country_code IS 'ISO 3166-1 alpha-2 country code detected from WhatsApp number';
COMMENT ON COLUMN farmers.preferred_language IS 'ISO 639-1 language code for farmer communication';
COMMENT ON COLUMN farmers.whatsapp_number IS 'Full WhatsApp number including country code';
COMMENT ON COLUMN farmers.timezone IS 'IANA timezone identifier (e.g., Europe/Sofia)';
COMMENT ON COLUMN farmers.localization_preferences IS 'JSON object with farmer-specific preferences (units, date format, etc.)';

-- =====================================================
-- KNOWLEDGE SOURCES TABLE
-- =====================================================

-- Create table for tracking information relevance
CREATE TABLE IF NOT EXISTS knowledge_sources (
    id SERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    relevance_type VARCHAR(20) NOT NULL CHECK (relevance_type IN ('FARMER', 'COUNTRY', 'GLOBAL')),
    farmer_id INTEGER REFERENCES farmers(farmer_id),
    country_code VARCHAR(3),
    language VARCHAR(10),
    source_type VARCHAR(50) NOT NULL,
    source_metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT true,
    
    -- Constraints to ensure data integrity
    CONSTRAINT chk_farmer_relevance CHECK (
        (relevance_type = 'FARMER' AND farmer_id IS NOT NULL) OR
        (relevance_type = 'COUNTRY' AND country_code IS NOT NULL) OR
        (relevance_type = 'GLOBAL')
    )
);

-- Add indexes for efficient querying
CREATE INDEX IF NOT EXISTS idx_knowledge_relevance ON knowledge_sources(relevance_type);
CREATE INDEX IF NOT EXISTS idx_knowledge_farmer ON knowledge_sources(farmer_id) WHERE farmer_id IS NOT NULL;
CREATE INDEX IF NOT EXISTS idx_knowledge_country ON knowledge_sources(country_code) WHERE country_code IS NOT NULL;
CREATE INDEX IF NOT EXISTS idx_knowledge_language ON knowledge_sources(language);
CREATE INDEX IF NOT EXISTS idx_knowledge_active ON knowledge_sources(is_active);

-- Add comments
COMMENT ON TABLE knowledge_sources IS 'Stores agricultural knowledge with relevance hierarchy (Amendment #13)';
COMMENT ON COLUMN knowledge_sources.relevance_type IS 'FARMER=farmer-specific, COUNTRY=country-specific, GLOBAL=universal';
COMMENT ON COLUMN knowledge_sources.source_type IS 'Origin of information: database, rag, external, user_input, etc.';

-- =====================================================
-- COUNTRY AGRICULTURAL PROFILES
-- =====================================================

-- Store country-specific agricultural information
CREATE TABLE IF NOT EXISTS country_agricultural_profiles (
    country_code VARCHAR(3) PRIMARY KEY,
    country_name VARCHAR(100) NOT NULL,
    agricultural_zones JSONB DEFAULT '[]',
    primary_crops JSONB DEFAULT '[]',
    growing_seasons JSONB DEFAULT '{}',
    measurement_system VARCHAR(20) DEFAULT 'metric',
    regulatory_framework TEXT,
    climate_classification VARCHAR(50),
    last_updated TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB DEFAULT '{}'
);

-- Add comments
COMMENT ON TABLE country_agricultural_profiles IS 'Country-specific agricultural context (no hardcoded logic)';
COMMENT ON COLUMN country_agricultural_profiles.agricultural_zones IS 'Array of agricultural zone definitions';
COMMENT ON COLUMN country_agricultural_profiles.primary_crops IS 'Array of commonly grown crops with metadata';
COMMENT ON COLUMN country_agricultural_profiles.growing_seasons IS 'JSON object mapping crops to typical seasons';

-- =====================================================
-- LOCALIZED CONTENT CACHE
-- =====================================================

-- Cache for localized responses to improve performance
CREATE TABLE IF NOT EXISTS localized_content_cache (
    id SERIAL PRIMARY KEY,
    content_hash VARCHAR(64) NOT NULL,
    country_code VARCHAR(3),
    language VARCHAR(10) NOT NULL,
    original_content TEXT NOT NULL,
    localized_content TEXT NOT NULL,
    content_type VARCHAR(50),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP WITH TIME ZONE,
    hit_count INTEGER DEFAULT 0
);

-- Add indexes
CREATE INDEX IF NOT EXISTS idx_cache_hash ON localized_content_cache(content_hash);
CREATE INDEX IF NOT EXISTS idx_cache_country_lang ON localized_content_cache(country_code, language);
CREATE INDEX IF NOT EXISTS idx_cache_expires ON localized_content_cache(expires_at) WHERE expires_at IS NOT NULL;

-- =====================================================
-- AUDIT TRAIL FOR LOCALIZATION
-- =====================================================

-- Track localization decisions for transparency (Principle #8)
CREATE TABLE IF NOT EXISTS localization_audit_log (
    id SERIAL PRIMARY KEY,
    farmer_id INTEGER REFERENCES farmers(farmer_id),
    whatsapp_number VARCHAR(20),
    detected_country VARCHAR(3),
    detected_language VARCHAR(10),
    query_text TEXT,
    information_sources JSONB DEFAULT '[]',
    synthesis_metadata JSONB DEFAULT '{}',
    response_language VARCHAR(10),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Add index for farmer lookup
CREATE INDEX IF NOT EXISTS idx_audit_farmer ON localization_audit_log(farmer_id);
CREATE INDEX IF NOT EXISTS idx_audit_timestamp ON localization_audit_log(created_at);

-- =====================================================
-- VIEWS FOR EASY QUERYING
-- =====================================================

-- View for farmer localization context
CREATE OR REPLACE VIEW v_farmer_localization_context AS
SELECT 
    f.farmer_id,
    f.first_name,
    f.last_name,
    f.whatsapp_number,
    f.country_code,
    f.preferred_language,
    f.timezone,
    cap.country_name,
    cap.measurement_system,
    cap.agricultural_zones,
    f.localization_preferences
FROM farmers f
LEFT JOIN country_agricultural_profiles cap ON f.country_code = cap.country_code
WHERE f.is_active = true;

-- View for knowledge by relevance
CREATE OR REPLACE VIEW v_knowledge_hierarchy AS
SELECT 
    ks.id,
    ks.relevance_type,
    ks.content,
    ks.language,
    CASE 
        WHEN ks.relevance_type = 'FARMER' THEN 
            f.first_name || ' ' || f.last_name || ' (' || f.farmer_id || ')'
        WHEN ks.relevance_type = 'COUNTRY' THEN 
            cap.country_name || ' (' || ks.country_code || ')'
        ELSE 'Global Knowledge'
    END as relevance_context,
    ks.source_type,
    ks.created_at
FROM knowledge_sources ks
LEFT JOIN farmers f ON ks.farmer_id = f.farmer_id
LEFT JOIN country_agricultural_profiles cap ON ks.country_code = cap.country_code
WHERE ks.is_active = true
ORDER BY 
    CASE ks.relevance_type 
        WHEN 'FARMER' THEN 1 
        WHEN 'COUNTRY' THEN 2 
        WHEN 'GLOBAL' THEN 3 
    END,
    ks.created_at DESC;

-- =====================================================
-- FUNCTIONS FOR LOCALIZATION
-- =====================================================

-- Function to get farmer's full localization context
CREATE OR REPLACE FUNCTION get_farmer_localization_context(p_whatsapp_number VARCHAR)
RETURNS JSON AS $$
DECLARE
    v_result JSON;
BEGIN
    SELECT json_build_object(
        'farmer_id', f.farmer_id,
        'country_code', f.country_code,
        'country_name', cap.country_name,
        'preferred_language', f.preferred_language,
        'timezone', f.timezone,
        'measurement_system', COALESCE(cap.measurement_system, 'metric'),
        'agricultural_zones', cap.agricultural_zones,
        'localization_preferences', f.localization_preferences
    ) INTO v_result
    FROM farmers f
    LEFT JOIN country_agricultural_profiles cap ON f.country_code = cap.country_code
    WHERE f.whatsapp_number = p_whatsapp_number
    AND f.is_active = true;
    
    RETURN v_result;
END;
$$ LANGUAGE plpgsql;

-- Function to get hierarchical knowledge for a query
CREATE OR REPLACE FUNCTION get_hierarchical_knowledge(
    p_farmer_id INTEGER,
    p_country_code VARCHAR,
    p_limit INTEGER DEFAULT 10
)
RETURNS TABLE (
    content TEXT,
    relevance_type VARCHAR,
    relevance_priority INTEGER,
    source_type VARCHAR,
    metadata JSONB
) AS $$
BEGIN
    RETURN QUERY
    -- Farmer-specific knowledge (priority 1)
    SELECT 
        ks.content,
        ks.relevance_type,
        1 as relevance_priority,
        ks.source_type,
        ks.source_metadata
    FROM knowledge_sources ks
    WHERE ks.farmer_id = p_farmer_id
    AND ks.is_active = true
    
    UNION ALL
    
    -- Country-specific knowledge (priority 2)
    SELECT 
        ks.content,
        ks.relevance_type,
        2 as relevance_priority,
        ks.source_type,
        ks.source_metadata
    FROM knowledge_sources ks
    WHERE ks.country_code = p_country_code
    AND ks.relevance_type = 'COUNTRY'
    AND ks.is_active = true
    
    UNION ALL
    
    -- Global knowledge (priority 3)
    SELECT 
        ks.content,
        ks.relevance_type,
        3 as relevance_priority,
        ks.source_type,
        ks.source_metadata
    FROM knowledge_sources ks
    WHERE ks.relevance_type = 'GLOBAL'
    AND ks.is_active = true
    
    ORDER BY relevance_priority, content
    LIMIT p_limit;
END;
$$ LANGUAGE plpgsql;

-- =====================================================
-- MIGRATION HELPERS
-- =====================================================

-- Update existing farmers with country codes based on existing data
-- (This would need to be customized based on actual data)
CREATE OR REPLACE FUNCTION migrate_existing_farmers_country()
RETURNS void AS $$
BEGIN
    -- This is a placeholder - actual migration would detect from phone numbers
    -- or other existing data. No hardcoded country assignments!
    UPDATE farmers 
    SET country_code = NULL,
        preferred_language = NULL
    WHERE country_code IS NULL;
    
    -- Log migration
    INSERT INTO localization_audit_log (
        query_text,
        synthesis_metadata,
        created_at
    ) VALUES (
        'Migration: Initialized country_code fields',
        '{"migration": "amendment_13", "affected_farmers": "all"}',
        CURRENT_TIMESTAMP
    );
END;
$$ LANGUAGE plpgsql;

-- =====================================================
-- SECURITY AND PERMISSIONS
-- =====================================================

-- Ensure proper permissions (adjust based on your user setup)
-- GRANT SELECT ON knowledge_sources TO ava_olo_read;
-- GRANT INSERT, UPDATE ON knowledge_sources TO ava_olo_write;
-- GRANT SELECT ON v_farmer_localization_context TO ava_olo_read;
-- GRANT SELECT ON v_knowledge_hierarchy TO ava_olo_read;
-- GRANT EXECUTE ON FUNCTION get_farmer_localization_context TO ava_olo_read;
-- GRANT EXECUTE ON FUNCTION get_hierarchical_knowledge TO ava_olo_read;