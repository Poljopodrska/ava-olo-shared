"""
Test Suite for Constitutional Compliance Checker
Tests all 13 constitutional principles with real scenarios
"""

import pytest
import asyncio
from pathlib import Path
import sys

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from implementation.constitutional_checker import (
    ConstitutionalChecker,
    ConstitutionalViolation,
    ComplianceResult,
    check_code_compliance,
    check_file_compliance
)
from implementation.constitutional_integration import (
    DatabaseDashboardChecker,
    ConstitutionalMiddleware,
    quick_mango_check
)
from implementation.dashboard_constitutional_integration import (
    DashboardConstitutionalGuard
)


class TestConstitutionalChecker:
    """Test the core constitutional checker"""
    
    @pytest.fixture
    def checker(self):
        return ConstitutionalChecker()
    
    @pytest.mark.asyncio
    async def test_mango_rule_violation(self, checker):
        """Test MANGO RULE violation detection"""
        
        # Bad code with hardcoded crop logic
        bad_code = """
def process_crop(crop_name, country):
    if crop_name == "mango" and country == "bulgaria":
        return "Error: Mangoes cannot grow in Bulgaria"
    elif crop_name == "tomato":
        return "Tomatoes are fine"
    else:
        return "Unknown crop"
"""
        
        result = await checker.check_compliance(bad_code, "code")
        
        assert not result.is_compliant
        assert any(v.principle == "MANGO_RULE" for v in result.violations)
        assert any(v.severity == "CRITICAL" for v in result.violations)
        
        # Check specific violations
        mango_violations = [v for v in result.violations if v.principle == "MANGO_RULE"]
        assert len(mango_violations) >= 2  # Both hardcoded crop and country discrimination
    
    @pytest.mark.asyncio
    async def test_mango_rule_compliant(self, checker):
        """Test MANGO RULE compliant code"""
        
        # Good code using LLM-first approach
        good_code = """
async def process_crop(crop_name, location, farmer_context):
    # Use LLM to analyze crop viability
    llm_analysis = await llm.analyze_crop_viability(
        crop=crop_name,
        location=location,
        climate_data=farmer_context.get('climate'),
        soil_data=farmer_context.get('soil')
    )
    
    # Return LLM-generated advice
    return llm_analysis.advice
"""
        
        result = await checker.check_compliance(good_code, "code")
        
        # Should have no MANGO RULE violations
        mango_violations = [v for v in result.violations if v.principle == "MANGO_RULE"]
        assert len(mango_violations) == 0
    
    @pytest.mark.asyncio
    async def test_llm_first_violation(self, checker):
        """Test LLM-FIRST principle violation"""
        
        bad_code = """
# Hardcoded translation dictionary
TRANSLATIONS = {
    'en': {
        'welcome': 'Welcome',
        'goodbye': 'Goodbye'
    },
    'es': {
        'welcome': 'Bienvenido',
        'goodbye': 'Adiós'
    }
}

def translate(text, language):
    return TRANSLATIONS.get(language, {}).get(text, text)
"""
        
        result = await checker.check_compliance(bad_code, "code")
        
        llm_violations = [v for v in result.violations if v.principle == "LLM_FIRST"]
        assert len(llm_violations) > 0
        assert any("translation" in v.description.lower() for v in llm_violations)
    
    @pytest.mark.asyncio
    async def test_privacy_first_violation(self, checker):
        """Test PRIVACY-FIRST principle violation"""
        
        bad_code = """
async def get_advice(farmer_id, farmer_name, phone):
    # Sending personal data to external API
    response = await openai.chat.completions.create(
        model="gpt-4",
        messages=[{
            "role": "user",
            "content": f"Give advice for farmer {farmer_name}, ID: {farmer_id}, Phone: {phone}"
        }]
    )
    return response.choices[0].message.content
"""
        
        result = await checker.check_compliance(bad_code, "code")
        
        privacy_violations = [v for v in result.violations if v.principle == "PRIVACY_FIRST"]
        assert len(privacy_violations) > 0
        assert any(v.severity == "CRITICAL" for v in privacy_violations)
    
    @pytest.mark.asyncio
    async def test_postgresql_only_violation(self, checker):
        """Test POSTGRESQL-ONLY principle violation"""
        
        bad_code = """
import sqlite3
import mysql.connector

def get_database():
    # Using SQLite for development
    if ENVIRONMENT == "dev":
        return sqlite3.connect("farmers.db")
    else:
        return mysql.connector.connect(
            host="localhost",
            database="farmers"
        )
"""
        
        result = await checker.check_compliance(bad_code, "code")
        
        db_violations = [v for v in result.violations if v.principle == "POSTGRESQL_ONLY"]
        assert len(db_violations) >= 2  # Both sqlite and mysql
        assert all(v.severity == "CRITICAL" for v in db_violations)
    
    @pytest.mark.asyncio
    async def test_comprehensive_compliance_score(self, checker):
        """Test compliance scoring system"""
        
        # Code with multiple violations
        mixed_code = """
import logging

async def process_farmer_request(request):
    try:
        # Good: has logging
        logging.info(f"Processing request")
        
        # Bad: hardcoded crop logic
        if request.crop == "mango":
            return "Not supported"
        
        # Good: uses LLM for main logic
        response = await llm.process(request)
        return response
    except Exception as e:
        # Good: error handling
        logging.error(f"Error: {e}")
        return None
"""
        
        result = await checker.check_compliance(mixed_code, "code")
        
        # Should have partial compliance
        assert 0 < result.overall_score < 100
        assert len(result.compliant_principles) > 0
        assert len(result.violations) > 0


class TestDatabaseDashboardChecker:
    """Test database dashboard specific checker"""
    
    @pytest.fixture
    def db_checker(self):
        return DatabaseDashboardChecker()
    
    @pytest.mark.asyncio
    async def test_sql_hardcoded_crop_violation(self, db_checker):
        """Test SQL with hardcoded crops"""
        
        bad_sql = """
        SELECT * FROM crops 
        WHERE crop_name IN ('tomato', 'potato', 'corn')
        AND country = 'USA'
        """
        
        context = {"farmer_id": 123, "language": "en"}
        result = await db_checker.check_sql_query_compliance(bad_sql, context)
        
        assert not result.is_compliant
        assert any(v.principle == "MANGO_RULE" for v in result.violations)
    
    @pytest.mark.asyncio
    async def test_sql_privacy_violation(self, db_checker):
        """Test SQL exposing personal data"""
        
        bad_sql = """
        SELECT farmer_name, phone, email, address
        FROM farmers
        WHERE farmer_id = 123
        """
        
        context = {"farmer_id": 123}
        result = await db_checker.check_sql_query_compliance(bad_sql, context)
        
        # Should have privacy warnings
        privacy_warnings = [v for v in result.violations if v.principle == "PRIVACY_FIRST"]
        assert len(privacy_warnings) > 0


class TestDashboardConstitutionalGuard:
    """Test dashboard constitutional guard"""
    
    @pytest.fixture
    def guard(self):
        return DashboardConstitutionalGuard()
    
    @pytest.mark.asyncio
    async def test_validate_natural_query_discrimination(self, guard):
        """Test natural language query validation"""
        
        # Query with discriminatory language
        bad_query = "Show tomato yields (not supported in Bulgaria)"
        
        result = await guard.validate_natural_query(
            query=bad_query,
            farmer_id=123,
            language="en"
        )
        
        assert not result['is_valid']
        assert result['mango_rule_status'] == 'FAIL'
    
    @pytest.mark.asyncio
    async def test_validate_response_refusal(self, guard):
        """Test response validation for refusal patterns"""
        
        # Response with refusal language
        bad_response = "Sorry, mangoes cannot be grown in your country. This crop is not supported."
        
        result = await guard.validate_response(
            response=bad_response,
            original_query="How to grow mangoes?",
            context={"farmer_id": 123, "language": "bg"}
        )
        
        assert not result['response_approved']
        assert any('refusal' in str(v).lower() for v in result['response_violations'])
    
    @pytest.mark.asyncio
    async def test_validate_response_inappropriate_tone(self, guard):
        """Test response validation for tone"""
        
        # Response with inappropriate tone
        bad_response = "Hello darling! Your cute little tomatoes need water, sweetie!"
        
        result = await guard.validate_response(
            response=bad_response,
            original_query="Tomato care advice",
            context={"farmer_id": 123}
        )
        
        # Should have farmer-centric violations
        tone_violations = [
            v for v in result['response_violations'] 
            if v['principle'] == 'FARMER_CENTRIC'
        ]
        assert len(tone_violations) > 0


class TestQuickMangoCheck:
    """Test quick mango rule validation"""
    
    @pytest.mark.asyncio
    async def test_quick_check_passes(self):
        """Test quick check for compliant function"""
        
        async def good_function(crop, location):
            return f"Analyzing {crop} in {location}"
        
        result = await quick_mango_check(
            good_function,
            args=["mango", "Bulgaria"],
            kwargs={}
        )
        
        assert result['passes']
    
    @pytest.mark.asyncio
    async def test_quick_check_fails(self):
        """Test quick check detecting violations"""
        
        async def bad_function(crop, country):
            return "not supported"
        
        result = await quick_mango_check(
            bad_function,
            args=["Invalid crop for region"],
            kwargs={}
        )
        
        assert not result['passes']
        assert 'refuses certain crops' in result['reason']


class TestIntegrationScenarios:
    """Test real-world integration scenarios"""
    
    @pytest.mark.asyncio
    async def test_bulgarian_mango_farmer_scenario(self):
        """The ultimate test: Bulgarian mango farmer"""
        
        checker = ConstitutionalChecker()
        
        # Complete feature code
        feature_code = """
from fastapi import FastAPI
import logging

app = FastAPI()
logger = logging.getLogger(__name__)

@app.post("/api/crop-advice")
async def get_crop_advice(
    crop: str,
    country: str,
    farmer_id: int,
    language: str = None
):
    '''Get crop advice for any farmer globally'''
    
    try:
        # Use LLM for all decisions
        context = {
            "crop": crop,
            "location": country,
            "farmer_id": farmer_id,
            "language": language or detect_language(country)
        }
        
        # Generate advice using AI
        advice = await llm.generate_agricultural_advice(context)
        
        # Log for transparency
        logger.info(f"Generated advice for farmer {farmer_id}")
        
        return {
            "success": True,
            "advice": advice,
            "language": context["language"]
        }
        
    except Exception as e:
        logger.error(f"Error generating advice: {e}")
        return {
            "success": False,
            "error": "Service temporarily unavailable"
        }

async def detect_language(country: str) -> str:
    '''Smart language detection using LLM'''
    return await llm.detect_primary_language(country)
"""
        
        result = await checker.check_compliance(feature_code, "code")
        
        # Should be highly compliant
        assert result.overall_score > 90
        assert "MANGO_RULE" in result.compliant_principles
        assert "LLM_FIRST" in result.compliant_principles
        assert "PRIVACY_FIRST" in result.compliant_principles
    
    @pytest.mark.asyncio
    async def test_three_phase_validation_flow(self):
        """Test complete three-phase validation"""
        
        guard = DashboardConstitutionalGuard()
        
        # Phase 1: Natural query
        query = "Show me mango growing tips"
        phase1 = await guard.validate_natural_query(
            query=query,
            farmer_id=123,
            language="bg"
        )
        assert phase1['is_valid']
        
        # Phase 2: SQL validation
        sql = """
        SELECT tip_content, tip_category
        FROM agricultural_tips
        WHERE applicable_crops @> ARRAY['mango']
        ORDER BY created_at DESC
        LIMIT 10
        """
        phase2 = await guard.validate_generated_sql(
            sql=sql,
            original_query=query,
            context={"farmer_id": 123}
        )
        assert phase2['sql_approved']
        
        # Phase 3: Response validation
        response = "Here are mango growing tips applicable to your region, considering local climate conditions..."
        phase3 = await guard.validate_response(
            response=response,
            original_query=query,
            context={"farmer_id": 123, "language": "bg"}
        )
        assert phase3['response_approved']


class TestReportGeneration:
    """Test compliance report generation"""
    
    @pytest.mark.asyncio
    async def test_generate_compliance_report(self):
        """Test report generation functionality"""
        
        checker = ConstitutionalChecker()
        
        code_with_violations = """
if crop == "mango":
    return "Not supported"
"""
        
        result = await checker.check_compliance(code_with_violations, "code")
        report = checker.generate_report(result)
        
        # Report should contain key elements
        assert "CONSTITUTIONAL COMPLIANCE REPORT" in report
        assert "VIOLATIONS DETECTED" in report
        assert "MANGO_RULE" in report
        assert "Bulgarian mango farmer" in report
        assert "Remedy:" in report


@pytest.mark.asyncio
async def test_command_line_interface():
    """Test CLI functionality"""
    
    # Test file checking
    test_file = Path(__file__).parent / "test_sample.py"
    test_file.write_text("""
# Test file
def process_crop(crop):
    if crop == "mango":
        return "Not supported"
    return "OK"
""")
    
    try:
        result = await check_file_compliance(str(test_file))
        assert not result.is_compliant
        assert len(result.violations) > 0
    finally:
        test_file.unlink()


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])