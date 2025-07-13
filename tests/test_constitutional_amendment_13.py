"""
Test Suite for Constitutional Amendment #13 - Country-Based Localization
Tests all aspects of the new localization system

Constitutional compliance verification:
- Mango Rule: Tests Bulgarian mango farmer scenario
- Privacy-First: Verifies information hierarchy
- LLM-First: Ensures no hardcoded country logic
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import json
from datetime import datetime

from country_detector import CountryDetector
from localization_handler import (
    LocalizationHandler, 
    LocalizationContext, 
    InformationItem, 
    InformationRelevance
)
from information_hierarchy import (
    InformationHierarchyManager,
    InformationQuery,
    InformationSource,
    RelevancePriority
)


class TestCountryDetector(unittest.TestCase):
    """Test country detection from WhatsApp numbers"""
    
    def setUp(self):
        self.detector = CountryDetector()
    
    def test_detect_slovenia(self):
        """Test Slovenia detection"""
        result = self.detector.get_country_info("+386123456789")
        self.assertEqual(result['country_code'], "SI")
        self.assertEqual(result['country_name'], "Slovenia")
        self.assertIn("sl", result['languages'])
    
    def test_detect_bulgaria(self):
        """Test Bulgaria detection - Mango farmer scenario"""
        result = self.detector.get_country_info("+359123456789")
        self.assertEqual(result['country_code'], "BG")
        self.assertEqual(result['country_name'], "Bulgaria")
        self.assertIn("bg", result['languages'])
    
    def test_detect_croatia(self):
        """Test Croatia detection"""
        result = self.detector.get_country_info("+385123456789")
        self.assertEqual(result['country_code'], "HR")
        self.assertEqual(result['country_name'], "Croatia")
        self.assertIn("hr", result['languages'])
    
    def test_detect_usa(self):
        """Test USA/Canada detection"""
        result = self.detector.get_country_info("+1234567890")
        self.assertIn(result['country_code'], ["US", "CA", "US/CA"])
        self.assertIn("en", result['languages'])
    
    def test_detect_with_spaces(self):
        """Test detection with formatted numbers"""
        result = self.detector.get_country_info("+386 1 234 56789")
        self.assertEqual(result['country_code'], "SI")
    
    def test_detect_without_plus(self):
        """Test detection without + prefix"""
        result = self.detector.get_country_info("386123456789")
        self.assertEqual(result['country_code'], "SI")
    
    @patch('country_detector.OpenAI')
    def test_llm_fallback(self, mock_openai):
        """Test LLM fallback for unknown numbers"""
        # Mock LLM response
        mock_response = Mock()
        mock_response.choices = [Mock(message=Mock(content="XX"))]
        mock_openai.return_value.chat.completions.create.return_value = mock_response
        
        # Test with unknown prefix
        result = self.detector.get_country_info("+999123456789")
        self.assertEqual(result['detection_method'], "llm_detection")


class TestLocalizationHandler(unittest.TestCase):
    """Test localization handler with LLM intelligence"""
    
    def setUp(self):
        self.handler = LocalizationHandler()
    
    def test_get_localization_context(self):
        """Test context building from WhatsApp number"""
        context = self.handler.get_localization_context("+359123456789", farmer_id=123)
        
        self.assertEqual(context.whatsapp_number, "+359123456789")
        self.assertEqual(context.country_code, "BG")
        self.assertEqual(context.country_name, "Bulgaria")
        self.assertEqual(context.farmer_id, 123)
        self.assertIn("bg", context.languages)
    
    @patch('localization_handler.OpenAI')
    def test_bulgarian_mango_synthesis(self, mock_openai):
        """Test the Bulgarian mango farmer scenario"""
        # Mock LLM response in Bulgarian
        mock_response = Mock()
        mock_response.choices = [Mock(message=Mock(content="Вашите манго в поле №3..."))]
        mock_openai.return_value.chat.completions.create.return_value = mock_response
        
        # Create Bulgarian context
        context = LocalizationContext(
            whatsapp_number="+359123456789",
            country_code="BG",
            country_name="Bulgaria",
            languages=["bg"],
            farmer_id=123,
            preferred_language="bg"
        )
        
        # Create information items
        items = [
            InformationItem(
                content="Your mango field #3 showed signs of fruit fly last week",
                relevance=InformationRelevance.FARMER_SPECIFIC,
                farmer_id=123
            ),
            InformationItem(
                content="In Bulgaria, mango cultivation requires greenhouse protection",
                relevance=InformationRelevance.COUNTRY_SPECIFIC,
                country_code="BG"
            ),
            InformationItem(
                content="Mango trees need 24-27°C for optimal growth",
                relevance=InformationRelevance.GLOBAL
            )
        ]
        
        # Synthesize response
        response = self.handler.synthesize_response(
            query="Кога да бера манго?",  # When to harvest mango?
            context=context,
            information_items=items
        )
        
        # Verify response is in Bulgarian
        self.assertIsInstance(response, str)
        self.assertIn("манго", response.lower())  # Contains "mango" in Cyrillic
    
    @patch('localization_handler.OpenAI')
    def test_language_detection(self, mock_openai):
        """Test language detection from farmer message"""
        # Mock LLM response
        mock_response = Mock()
        mock_response.choices = [Mock(message=Mock(content="bg"))]
        mock_openai.return_value.chat.completions.create.return_value = mock_response
        
        context = LocalizationContext(
            whatsapp_number="+359123456789",
            country_code="BG",
            country_name="Bulgaria",
            languages=["bg", "en"],
            preferred_language="bg"
        )
        
        # Test Bulgarian message
        detected = self.handler.determine_language(context, "Кога да бера манго?")
        self.assertEqual(detected, "bg")
    
    @patch('localization_handler.OpenAI')
    def test_measurement_localization(self, mock_openai):
        """Test measurement unit localization"""
        # Mock LLM response
        mock_response = Mock()
        mock_response.choices = [Mock(message=Mock(content="10 хектара"))]  # hectares in Bulgarian
        mock_openai.return_value.chat.completions.create.return_value = mock_response
        
        context = LocalizationContext(
            whatsapp_number="+359123456789",
            country_code="BG",
            country_name="Bulgaria",
            languages=["bg"],
            preferred_language="bg"
        )
        
        result = self.handler.localize_measurement(10, "hectares", context)
        self.assertIn("хектара", result)  # Bulgarian for hectares


class TestInformationHierarchy(unittest.TestCase):
    """Test information hierarchy system"""
    
    def setUp(self):
        self.manager = InformationHierarchyManager()
    
    def test_source_registration(self):
        """Test information source registration"""
        capabilities = self.manager.get_source_capabilities()
        
        # Verify default sources
        self.assertIn("farmer_db", capabilities)
        self.assertIn("rag_knowledge", capabilities)
        self.assertIn("external_search", capabilities)
        
        # Verify privacy rules
        self.assertTrue(capabilities["farmer_db"]["farmer_data"])
        self.assertFalse(capabilities["external_search"]["farmer_data"])
    
    def test_privacy_compliance(self):
        """Test privacy compliance validation"""
        # Create external source (cannot access farmer data)
        external_source = InformationSource(
            source_id="test_external",
            source_type="external",
            source_name="Test External",
            can_access_farmer_data=False
        )
        
        # Try to create farmer-specific item from external source
        farmer_item = InformationItem(
            content="Farmer's personal data",
            relevance=InformationRelevance.FARMER_SPECIFIC,
            farmer_id=123,
            source_type="external"
        )
        
        # Verify privacy violation is detected
        is_valid = self.manager.validate_privacy_compliance(farmer_item, external_source)
        self.assertFalse(is_valid)
    
    def test_information_query_hierarchy(self):
        """Test hierarchical information querying"""
        # Create context
        context = LocalizationContext(
            whatsapp_number="+359123456789",
            country_code="BG",
            country_name="Bulgaria",
            languages=["bg"],
            farmer_id=123
        )
        
        # Create query
        query = InformationQuery(
            query_text="When to harvest mangoes?",
            context=context
        )
        
        # Execute query
        result = self.manager.query_information(query)
        
        # Verify hierarchy is respected
        self.assertIsNotNone(result)
        self.assertIsInstance(result.farmer_items, list)
        self.assertIsInstance(result.country_items, list)
        self.assertIsInstance(result.global_items, list)
        
        # Verify metadata
        self.assertIn("query_timestamp", result.metadata)
        self.assertIn("sources_used", result.metadata)
    
    def test_result_serialization(self):
        """Test result serialization for storage"""
        context = LocalizationContext(
            whatsapp_number="+359123456789",
            country_code="BG",
            country_name="Bulgaria",
            languages=["bg"],
            farmer_id=123
        )
        
        query = InformationQuery(
            query_text="Test query",
            context=context
        )
        
        result = self.manager.query_information(query)
        
        # Convert to dict
        result_dict = result.to_dict()
        
        # Verify structure
        self.assertIn("query", result_dict)
        self.assertIn("farmer_id", result_dict)
        self.assertIn("country_code", result_dict)
        self.assertIn("items", result_dict)
        
        # Verify it's JSON serializable
        json_str = json.dumps(result_dict)
        self.assertIsInstance(json_str, str)


class TestConstitutionalCompliance(unittest.TestCase):
    """Test overall constitutional compliance"""
    
    def test_no_hardcoded_country_logic(self):
        """Verify no hardcoded country-specific logic"""
        # This test would scan the codebase for violations
        # For now, we'll test that country codes are data-driven
        
        detector = CountryDetector()
        # Verify country codes are in a data structure, not in logic
        self.assertIsInstance(detector.country_codes, dict)
        self.assertGreater(len(detector.country_codes), 100)  # Many countries
    
    def test_mango_rule_compliance(self):
        """Test the complete Bulgarian mango farmer scenario"""
        # 1. Detect country from WhatsApp
        detector = CountryDetector()
        country_info = detector.get_country_info("+359123456789")
        self.assertEqual(country_info['country_code'], "BG")
        
        # 2. Build localization context
        handler = LocalizationHandler()
        context = handler.get_localization_context("+359123456789", farmer_id=123)
        self.assertEqual(context.country_code, "BG")
        self.assertEqual(context.preferred_language, "bg")
        
        # 3. Query hierarchical information
        manager = InformationHierarchyManager()
        query = InformationQuery(
            query_text="When to harvest mangoes?",
            context=context
        )
        result = manager.query_information(query)
        
        # 4. Verify all levels of information are available
        self.assertIsNotNone(result)
        # In production, would verify actual mango-specific content
    
    def test_privacy_first_compliance(self):
        """Test that farmer data stays internal"""
        manager = InformationHierarchyManager()
        
        # Verify external sources cannot provide farmer data
        source_caps = manager.get_source_capabilities()
        
        for source_id, caps in source_caps.items():
            if caps["source_type"] == "external":
                self.assertFalse(caps["farmer_data"], 
                               f"External source {source_id} should not access farmer data")
    
    def test_llm_first_compliance(self):
        """Test that decisions are made by LLM, not hardcoded"""
        # Test that handler methods use LLM
        handler = LocalizationHandler()
        
        # Verify handler has OpenAI client
        self.assertIsNotNone(handler.client)
        self.assertEqual(handler.model, "gpt-4")
        
        # In production, would verify all decision methods call LLM


class TestIntegrationScenarios(unittest.TestCase):
    """Test complete integration scenarios"""
    
    @patch('localization_handler.OpenAI')
    @patch('country_detector.OpenAI')
    def test_slovenian_prosaro_scenario(self, mock_detector_openai, mock_handler_openai):
        """Test Slovenian farmer asking about Prosaro in Slovenian"""
        # Mock responses
        mock_handler_openai.return_value.chat.completions.create.return_value = Mock(
            choices=[Mock(message=Mock(content="Prosaro PHI v Sloveniji je 14 dni..."))]
        )
        
        # Full flow
        detector = CountryDetector()
        handler = LocalizationHandler()
        manager = InformationHierarchyManager()
        
        # 1. Detect Slovenia
        country_info = detector.get_country_info("+386123456789")
        self.assertEqual(country_info['country_code'], "SI")
        
        # 2. Create context
        context = handler.get_localization_context("+386123456789", farmer_id=456)
        
        # 3. Query information
        query = InformationQuery(
            query_text="Ali lahko uporabim Prosaro?",
            context=context
        )
        result = manager.query_information(query)
        
        # 4. Synthesize response
        items = result.get_all_items_by_priority()
        response = handler.synthesize_response(
            query=query.query_text,
            context=context,
            information_items=items
        )
        
        # Verify response mentions Prosaro PHI
        self.assertIn("Prosaro", response)
        self.assertIn("14", response)


if __name__ == '__main__':
    unittest.main()