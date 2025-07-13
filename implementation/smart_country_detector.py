"""
Smart Country/Language Detector with Override Capability
Constitutional Amendment #13 - Enhanced Version

Handles cases like Hungarian minority farmer with Croatian phone number:
- Detects country from phone number (Croatia)
- But allows language override (Hungarian)
- Supports cultural context and ethnicity
"""

import re
import logging
from typing import Dict, Optional, List, Tuple
from dataclasses import dataclass
from datetime import datetime

logger = logging.getLogger(__name__)


@dataclass
class SmartDetectionResult:
    """Result of smart country/language detection"""
    country_code: str
    country_name: str
    primary_language: str
    secondary_languages: List[str]
    phone_prefix: str
    confidence_score: float
    detection_method: str
    cultural_notes: Optional[str] = None
    is_override: bool = False
    override_reason: Optional[str] = None


class SmartCountryDetector:
    """
    Enhanced country detector with smart language inference and override capability
    Constitutional compliance: Works for any farmer in any country with any language preference
    """
    
    def __init__(self):
        self.country_mapping = self._load_country_mapping()
        self.phone_mapping = self._build_phone_mapping()
        
    def _load_country_mapping(self) -> Dict[str, Dict]:
        """Load comprehensive country-language mapping"""
        return {
            # Balkan Region (High priority for AVA OLO)
            'HR': {
                'country_name': 'Croatia',
                'primary_language': 'hr',
                'secondary_languages': ['en'],
                'phone_prefixes': ['+385'],
                'cultural_notes': 'Croatian primary language, English secondary. Italian minority in Istria.',
                'minorities': ['italian', 'serbian', 'hungarian'],
                'currency': 'EUR',
                'timezone': 'Europe/Zagreb'
            },
            'SI': {
                'country_name': 'Slovenia',
                'primary_language': 'sl',
                'secondary_languages': ['hr', 'en', 'it'],
                'phone_prefixes': ['+386'],
                'cultural_notes': 'Slovenian primary, Croatian/Italian minorities, English business',
                'minorities': ['croatian', 'italian', 'hungarian'],
                'currency': 'EUR',
                'timezone': 'Europe/Ljubljana'
            },
            'BG': {
                'country_name': 'Bulgaria',
                'primary_language': 'bg',
                'secondary_languages': ['en', 'tr'],
                'phone_prefixes': ['+359'],
                'cultural_notes': 'Bulgarian primary language, Turkish minority, English business',
                'minorities': ['turkish', 'roma'],
                'currency': 'BGN',
                'timezone': 'Europe/Sofia'
            },
            'HU': {
                'country_name': 'Hungary',
                'primary_language': 'hu',
                'secondary_languages': ['hr', 'en', 'de'],
                'phone_prefixes': ['+36'],
                'cultural_notes': 'Hungarian primary, Croatian minority in south, German business',
                'minorities': ['croatian', 'serbian', 'romanian'],
                'currency': 'HUF',
                'timezone': 'Europe/Budapest'
            },
            'RS': {
                'country_name': 'Serbia',
                'primary_language': 'sr',
                'secondary_languages': ['hr', 'hu', 'en'],
                'phone_prefixes': ['+381'],
                'cultural_notes': 'Serbian primary, Croatian and Hungarian minorities',
                'minorities': ['croatian', 'hungarian', 'bosniaq'],
                'currency': 'RSD',
                'timezone': 'Europe/Belgrade'
            },
            'BA': {
                'country_name': 'Bosnia and Herzegovina',
                'primary_language': 'bs',
                'secondary_languages': ['hr', 'sr', 'en'],
                'phone_prefixes': ['+387'],
                'cultural_notes': 'Bosnian/Croatian/Serbian trilingual environment',
                'minorities': ['croatian', 'serbian'],
                'currency': 'BAM',
                'timezone': 'Europe/Sarajevo'
            },
            'AT': {
                'country_name': 'Austria',
                'primary_language': 'de',
                'secondary_languages': ['hr', 'en', 'hu'],
                'phone_prefixes': ['+43'],
                'cultural_notes': 'German primary, Croatian minority (Burgenland), Hungarian minority',
                'minorities': ['croatian', 'hungarian', 'slovenian'],
                'currency': 'EUR',
                'timezone': 'Europe/Vienna'
            },
            'IT': {
                'country_name': 'Italy',
                'primary_language': 'it',
                'secondary_languages': ['hr', 'sl', 'en'],
                'phone_prefixes': ['+39'],
                'cultural_notes': 'Italian primary, Croatian/Slovenian minorities in northeast',
                'minorities': ['croatian', 'slovenian', 'german'],
                'currency': 'EUR',
                'timezone': 'Europe/Rome'
            },
            
            # Western Europe
            'DE': {
                'country_name': 'Germany',
                'primary_language': 'de',
                'secondary_languages': ['en', 'tr'],
                'phone_prefixes': ['+49'],
                'cultural_notes': 'German primary, Turkish minority, English business',
                'minorities': ['turkish', 'polish', 'russian'],
                'currency': 'EUR',
                'timezone': 'Europe/Berlin'
            },
            'FR': {
                'country_name': 'France',
                'primary_language': 'fr',
                'secondary_languages': ['en', 'ar'],
                'phone_prefixes': ['+33'],
                'cultural_notes': 'French primary, Arabic-speaking minorities',
                'minorities': ['arabic', 'portuguese', 'spanish'],
                'currency': 'EUR',
                'timezone': 'Europe/Paris'
            },
            'ES': {
                'country_name': 'Spain',
                'primary_language': 'es',
                'secondary_languages': ['ca', 'eu', 'en'],
                'phone_prefixes': ['+34'],
                'cultural_notes': 'Spanish primary, Catalan and Basque regional languages',
                'minorities': ['catalan', 'basque', 'galician'],
                'currency': 'EUR',
                'timezone': 'Europe/Madrid'
            },
            'GB': {
                'country_name': 'United Kingdom',
                'primary_language': 'en',
                'secondary_languages': ['cy', 'gd'],
                'phone_prefixes': ['+44'],
                'cultural_notes': 'English primary, Welsh and Scottish Gaelic regional',
                'minorities': ['polish', 'urdu', 'punjabi'],
                'currency': 'GBP',
                'timezone': 'Europe/London'
            },
            
            # Global Agricultural Powers
            'US': {
                'country_name': 'United States',
                'primary_language': 'en',
                'secondary_languages': ['es'],
                'phone_prefixes': ['+1'],
                'cultural_notes': 'English primary, Spanish significant minority',
                'minorities': ['spanish', 'chinese', 'vietnamese'],
                'currency': 'USD',
                'timezone': 'America/New_York'
            },
            'BR': {
                'country_name': 'Brazil',
                'primary_language': 'pt',
                'secondary_languages': ['en', 'es'],
                'phone_prefixes': ['+55'],
                'cultural_notes': 'Portuguese primary, agricultural powerhouse',
                'minorities': ['japanese', 'german', 'italian'],
                'currency': 'BRL',
                'timezone': 'America/Sao_Paulo'
            },
            'IN': {
                'country_name': 'India',
                'primary_language': 'hi',
                'secondary_languages': ['en', 'ta', 'te', 'bn'],
                'phone_prefixes': ['+91'],
                'cultural_notes': 'Hindi/English primary, highly multilingual',
                'minorities': ['tamil', 'telugu', 'bengali', 'marathi'],
                'currency': 'INR',
                'timezone': 'Asia/Kolkata'
            },
            'CN': {
                'country_name': 'China',
                'primary_language': 'zh',
                'secondary_languages': ['en'],
                'phone_prefixes': ['+86'],
                'cultural_notes': 'Chinese primary, English business language',
                'minorities': ['uighur', 'tibetan', 'mongolian'],
                'currency': 'CNY',
                'timezone': 'Asia/Shanghai'
            },
            'TH': {
                'country_name': 'Thailand',
                'primary_language': 'th',
                'secondary_languages': ['en'],
                'phone_prefixes': ['+66'],
                'cultural_notes': 'Thai primary, agricultural economy, mango production',
                'minorities': ['malay', 'chinese', 'khmer'],
                'currency': 'THB',
                'timezone': 'Asia/Bangkok'
            }
        }
    
    def _build_phone_mapping(self) -> Dict[str, str]:
        """Build reverse mapping from phone prefix to country code"""
        phone_mapping = {}
        for country_code, info in self.country_mapping.items():
            for prefix in info['phone_prefixes']:
                phone_mapping[prefix] = country_code
        return phone_mapping
    
    def detect_from_phone(self, phone_number: str) -> SmartDetectionResult:
        """Detect country from phone number with smart confidence scoring"""
        if not phone_number:
            return self._create_fallback_result("No phone number provided")
        
        # Clean phone number
        clean_phone = re.sub(r'[^\d+]', '', phone_number)
        
        # Try different prefix lengths (longest first for accuracy)
        for prefix_length in range(4, 0, -1):
            if len(clean_phone) >= prefix_length + 1:  # +1 for the + sign
                if clean_phone.startswith('+'):
                    prefix = clean_phone[:prefix_length + 1]
                    
                    if prefix in self.phone_mapping:
                        country_code = self.phone_mapping[prefix]
                        country_info = self.country_mapping[country_code]
                        
                        # Confidence based on prefix length and specificity
                        confidence = 0.8 + (prefix_length * 0.05)
                        confidence = min(confidence, 0.99)
                        
                        return SmartDetectionResult(
                            country_code=country_code,
                            country_name=country_info['country_name'],
                            primary_language=country_info['primary_language'],
                            secondary_languages=country_info['secondary_languages'],
                            phone_prefix=prefix,
                            confidence_score=confidence,
                            detection_method="phone_prefix",
                            cultural_notes=country_info['cultural_notes']
                        )
        
        return self._create_fallback_result(f"Unknown phone prefix: {clean_phone[:5]}...")
    
    def detect_with_override(self, 
                           phone_number: str,
                           language_override: Optional[str] = None,
                           country_override: Optional[str] = None,
                           ethnicity: Optional[str] = None,
                           cultural_context: Optional[str] = None) -> SmartDetectionResult:
        """
        Smart detection with override capability for minority farmers
        
        Example: Hungarian minority farmer with Croatian phone number
        - phone_number: "+385123456789" (Croatian)
        - language_override: "hu" (Hungarian preference)
        - ethnicity: "Hungarian"
        """
        
        # Start with phone-based detection
        base_result = self.detect_from_phone(phone_number)
        
        # Apply overrides
        if country_override:
            if country_override in self.country_mapping:
                country_info = self.country_mapping[country_override]
                base_result.country_code = country_override
                base_result.country_name = country_info['country_name']
                base_result.is_override = True
                base_result.override_reason = "Manual country override"
                base_result.confidence_score = 1.0
            else:
                logger.warning(f"Unknown country override: {country_override}")
        
        if language_override:
            # Validate language override makes sense
            if self._is_valid_language_for_country(language_override, base_result.country_code, ethnicity):
                base_result.primary_language = language_override
                base_result.is_override = True
                base_result.override_reason = f"Language override for {ethnicity or 'minority'} speaker"
                
                # Add cultural context
                if ethnicity:
                    base_result.cultural_notes = f"{ethnicity} minority in {base_result.country_name}. Language: {language_override}"
            else:
                logger.warning(f"Unusual language override: {language_override} for {base_result.country_code}")
        
        # Add ethnicity context
        if ethnicity:
            base_result.cultural_notes = f"{base_result.cultural_notes or ''} | Ethnicity: {ethnicity}"
        
        if cultural_context:
            base_result.cultural_notes = f"{base_result.cultural_notes or ''} | Context: {cultural_context}"
        
        return base_result
    
    def _is_valid_language_for_country(self, language: str, country_code: str, ethnicity: Optional[str] = None) -> bool:
        """Check if language override is reasonable for the country"""
        if country_code not in self.country_mapping:
            return True  # Allow if country unknown
        
        country_info = self.country_mapping[country_code]
        
        # Check if it's primary or secondary language
        if language in [country_info['primary_language']] + country_info['secondary_languages']:
            return True
        
        # Check if it's a known minority language
        if ethnicity and any(ethnicity.lower() in minority for minority in country_info.get('minorities', [])):
            return True
        
        # Special cases for common minority languages
        minority_patterns = {
            'hu': ['hungarian', 'magyar'],
            'hr': ['croatian', 'croatian'],
            'sr': ['serbian', 'srpski'],
            'it': ['italian', 'italiana'],
            'de': ['german', 'deutsch'],
            'tr': ['turkish', 'türk']
        }
        
        if language in minority_patterns and ethnicity:
            for pattern in minority_patterns[language]:
                if pattern in ethnicity.lower():
                    return True
        
        return False
    
    def _create_fallback_result(self, reason: str) -> SmartDetectionResult:
        """Create fallback result for unknown cases"""
        return SmartDetectionResult(
            country_code='XX',
            country_name='Unknown',
            primary_language='en',
            secondary_languages=[],
            phone_prefix='',
            confidence_score=0.1,
            detection_method="fallback",
            cultural_notes=f"Fallback to English. Reason: {reason}"
        )
    
    def get_country_info(self, phone_number: str, **overrides) -> Dict[str, any]:
        """Backward compatibility method"""
        result = self.detect_with_override(phone_number, **overrides)
        
        return {
            'country_code': result.country_code,
            'country_name': result.country_name,
            'primary_language': result.primary_language,
            'languages': [result.primary_language] + result.secondary_languages,
            'detection_method': result.detection_method,
            'confidence': result.confidence_score,
            'cultural_notes': result.cultural_notes,
            'is_override': result.is_override
        }
    
    def test_scenarios(self):
        """Test common scenarios including minority farmers"""
        test_cases = [
            {
                'name': 'Croatian farmer with Croatian number',
                'phone': '+385123456789',
                'expected_country': 'HR',
                'expected_language': 'hr'
            },
            {
                'name': 'Hungarian minority farmer with Croatian number',
                'phone': '+385987654321',
                'language_override': 'hu',
                'ethnicity': 'Hungarian',
                'expected_country': 'HR',
                'expected_language': 'hu'
            },
            {
                'name': 'Bulgarian mango farmer',
                'phone': '+359123456789',
                'expected_country': 'BG',
                'expected_language': 'bg'
            },
            {
                'name': 'Italian minority in Slovenia',
                'phone': '+386123456789',
                'language_override': 'it',
                'ethnicity': 'Italian',
                'expected_country': 'SI',
                'expected_language': 'it'
            },
            {
                'name': 'Thai mango farmer',
                'phone': '+66123456789',
                'expected_country': 'TH',
                'expected_language': 'th'
            }
        ]
        
        print("🧪 Testing Smart Country Detection Scenarios:")
        print("=" * 60)
        
        for test in test_cases:
            result = self.detect_with_override(
                phone_number=test['phone'],
                language_override=test.get('language_override'),
                ethnicity=test.get('ethnicity')
            )
            
            country_ok = result.country_code == test['expected_country']
            language_ok = result.primary_language == test['expected_language']
            
            print(f"\n📱 {test['name']}:")
            print(f"   Phone: {test['phone']}")
            print(f"   Country: {result.country_code} ({'✅' if country_ok else '❌'})")
            print(f"   Language: {result.primary_language} ({'✅' if language_ok else '❌'})")
            print(f"   Confidence: {result.confidence_score:.2f}")
            if result.is_override:
                print(f"   Override: {result.override_reason}")
            if result.cultural_notes:
                print(f"   Culture: {result.cultural_notes}")


if __name__ == "__main__":
    detector = SmartCountryDetector()
    detector.test_scenarios()