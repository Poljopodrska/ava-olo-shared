#!/usr/bin/env python3
"""
Test Hungarian Minority Farmer Scenario
Tests the complete smart country/language detection system with override capability

Scenario: Hungarian minority farmer living in Croatia
- Has Croatian phone number (+385...)
- Speaks Hungarian as primary language
- Should get country = HR (from phone), language = HU (override)
"""

import asyncio
import os
import sys
from datetime import datetime

# Add paths for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.join(os.path.dirname(__file__), 'ava-olo-agricultural-core'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'ava-olo-shared'))

async def test_smart_country_detection():
    """Test smart country detection system"""
    print("🧪 Testing Smart Country Detection...")
    print("=" * 60)
    
    try:
        from smart_country_detector import SmartCountryDetector
        detector = SmartCountryDetector()
        
        # Test scenarios
        scenarios = [
            {
                'name': 'Croatian farmer with Croatian number (auto-detection)',
                'phone': '+385123456789',
                'expected_country': 'HR',
                'expected_language': 'hr'
            },
            {
                'name': 'Hungarian minority farmer with Croatian number (override)',
                'phone': '+385987654321',
                'language_override': 'hu',
                'ethnicity': 'Hungarian',
                'expected_country': 'HR',
                'expected_language': 'hu'
            },
            {
                'name': 'Bulgarian mango farmer (auto-detection)',
                'phone': '+359123456789',
                'expected_country': 'BG',
                'expected_language': 'bg'
            },
            {
                'name': 'Italian minority in Slovenia (override)',
                'phone': '+386123456789',
                'language_override': 'it',
                'ethnicity': 'Italian',
                'expected_country': 'SI',
                'expected_language': 'it'
            }
        ]
        
        all_passed = True
        
        for scenario in scenarios:
            print(f"\n📱 {scenario['name']}:")
            
            result = detector.detect_with_override(
                phone_number=scenario['phone'],
                language_override=scenario.get('language_override'),
                ethnicity=scenario.get('ethnicity')
            )
            
            country_ok = result.country_code == scenario['expected_country']
            language_ok = result.primary_language == scenario['expected_language']
            
            print(f"   Phone: {scenario['phone']}")
            print(f"   Country: {result.country_code} ({'✅' if country_ok else '❌ Expected ' + scenario['expected_country']})")
            print(f"   Language: {result.primary_language} ({'✅' if language_ok else '❌ Expected ' + scenario['expected_language']})")
            print(f"   Confidence: {result.confidence_score:.2f}")
            
            if result.is_override:
                print(f"   ✅ Override: {result.override_reason}")
            
            if result.cultural_notes:
                print(f"   📝 Culture: {result.cultural_notes}")
            
            if not (country_ok and language_ok):
                all_passed = False
        
        return all_passed
        
    except ImportError as e:
        print(f"❌ Smart country detector not available: {e}")
        return False
    except Exception as e:
        print(f"❌ Smart detection test failed: {e}")
        return False

async def test_llm_engine_with_smart_detection():
    """Test LLM engine with smart detection"""
    print("\n\n🧠 Testing LLM Engine with Smart Detection...")
    print("=" * 60)
    
    try:
        from llm_first_database_engine import LLMDatabaseQueryEngine, DatabaseQuery
        engine = LLMDatabaseQueryEngine()
        
        # Test Hungarian minority farmer scenario
        test_queries = [
            {
                'name': 'Hungarian minority farmer query',
                'query': DatabaseQuery(
                    natural_language_query="Hány hektár földem van?",  # How many hectares do I have?
                    farmer_id=123,
                    phone_number="+385987654321",  # Croatian number
                    language="hu",  # Hungarian language
                    language_override=True,
                    ethnicity="Hungarian"
                ),
                'expected_language': 'hu',
                'expected_country': 'HR'
            },
            {
                'name': 'Croatian farmer auto-detection',
                'query': DatabaseQuery(
                    natural_language_query="Koliko polja imam?",  # How many fields do I have?
                    farmer_id=456,
                    phone_number="+385123456789"
                ),
                'expected_language': 'hr',
                'expected_country': 'HR'
            },
            {
                'name': 'Bulgarian mango farmer',
                'query': DatabaseQuery(
                    natural_language_query="Колко манго дървета имам?",  # How many mango trees?
                    farmer_id=789,
                    phone_number="+359123456789"
                ),
                'expected_language': 'bg',
                'expected_country': 'BG'
            }
        ]
        
        all_passed = True
        
        for test in test_queries:
            print(f"\n🔍 {test['name']}:")
            print(f"   Query: {test['query'].natural_language_query}")
            print(f"   Phone: {test['query'].phone_number}")
            
            try:
                start_time = datetime.now()
                result = await engine.process_farmer_query(test['query'])
                end_time = datetime.now()
                duration = (end_time - start_time).total_seconds()
                
                print(f"   ✅ Processed in {duration:.2f} seconds")
                print(f"   🗄️ SQL: {result.sql_query[:100]}...")
                print(f"   💬 Response: {result.natural_language_response[:150]}...")
                print(f"   📊 Results: {len(result.raw_results)} records")
                print(f"   🏛️ Constitutional: {result.constitutional_compliance}")
                
                # Check metadata for smart detection
                metadata = result.processing_metadata
                if 'constitutional_compliance' in metadata:
                    compliance = metadata['constitutional_compliance']
                    print(f"   📋 Compliance: LLM-first={compliance.get('llm_first')}, Privacy={compliance.get('privacy_first')}")
                
            except Exception as e:
                print(f"   ❌ Query failed: {e}")
                all_passed = False
        
        return all_passed
        
    except ImportError as e:
        print(f"❌ LLM engine not available: {e}")
        return False
    except Exception as e:
        print(f"❌ LLM engine test failed: {e}")
        return False

async def test_database_schema_compliance():
    """Test database schema for constitutional compliance"""
    print("\n\n🗄️ Testing Database Schema Compliance...")
    print("=" * 60)
    
    try:
        # Test that schema update script exists
        schema_file = os.path.join(os.path.dirname(__file__), 'aurora_schema_update_smart_localization.sql')
        
        if os.path.exists(schema_file):
            print("✅ Smart localization schema update script exists")
            
            # Check key components in schema
            with open(schema_file, 'r') as f:
                content = f.read()
                
                checks = [
                    ('Remove hardcoded defaults', 'ALTER COLUMN country DROP DEFAULT'),
                    ('Amendment #13 columns', 'country_code VARCHAR(3)'),
                    ('Smart detection function', 'smart_detect_country_language'),
                    ('Country mapping table', 'country_language_mapping'),
                    ('Hungarian minority support', 'Hungarian'),
                    ('Trigger for auto-detection', 'trigger_smart_country_language'),
                    ('Constitutional compliance view', 'constitutional_compliance_check')
                ]
                
                all_checks_passed = True
                
                for check_name, pattern in checks:
                    if pattern in content:
                        print(f"   ✅ {check_name}")
                    else:
                        print(f"   ❌ Missing: {check_name}")
                        all_checks_passed = False
                
                return all_checks_passed
        else:
            print("❌ Schema update script not found")
            return False
            
    except Exception as e:
        print(f"❌ Schema compliance test failed: {e}")
        return False

def test_configuration_completeness():
    """Test that configuration is complete"""
    print("\n\n⚙️ Testing Configuration Completeness...")
    print("=" * 60)
    
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        # Check critical configuration
        checks = [
            ('Aurora RDS Host', os.getenv('DB_HOST'), lambda x: 'amazonaws.com' in str(x)),
            ('Constitutional Database', os.getenv('DB_NAME'), lambda x: x == 'farmer_crm'),
            ('OpenAI API Key', os.getenv('OPENAI_API_KEY'), lambda x: str(x).startswith('sk-')),
            ('LLM First Enabled', os.getenv('ENABLE_LLM_FIRST'), lambda x: str(x).lower() == 'true'),
            ('Country Localization', os.getenv('ENABLE_COUNTRY_LOCALIZATION'), lambda x: str(x).lower() == 'true'),
        ]
        
        all_passed = True
        
        for check_name, value, validator in checks:
            if value and validator(value):
                print(f"   ✅ {check_name}")
            else:
                print(f"   ❌ {check_name}: {value}")
                all_passed = False
        
        return all_passed
        
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

async def main():
    """Run complete Hungarian minority farmer test suite"""
    print("🇭🇺 HUNGARIAN MINORITY FARMER TEST SUITE")
    print("=" * 70)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    
    # Test components
    tests = [
        ("Configuration Completeness", test_configuration_completeness, False),
        ("Smart Country Detection", test_smart_country_detection, True),
        ("Database Schema Compliance", test_database_schema_compliance, False),
        ("LLM Engine Integration", test_llm_engine_with_smart_detection, True)
    ]
    
    results = []
    
    for test_name, test_func, is_async in tests:
        print(f"\n{'='*70}")
        print(f"Running: {test_name}")
        print('='*70)
        
        try:
            if is_async:
                result = await test_func()
            else:
                result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Test failed with error: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "="*70)
    print("📊 TEST SUMMARY")
    print("="*70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"  {test_name}: {status}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    percentage = (passed / total * 100) if total > 0 else 0
    
    print("\n" + "="*70)
    if percentage == 100:
        print("🎉 ALL TESTS PASSED!")
        print("✅ Hungarian minority farmer scenario fully supported")
        print("✅ Smart country/language detection working")
        print("✅ Constitutional compliance achieved")
    elif percentage >= 75:
        print("⚠️ MOSTLY WORKING - Minor issues detected")
        print(f"   {percentage:.0f}% of tests passed")
    else:
        print("❌ SIGNIFICANT ISSUES DETECTED")
        print(f"   Only {percentage:.0f}% of tests passed")
        print("   Please address the failures above")
    
    print("\n📝 Example Usage:")
    print("Hungarian minority farmer with Croatian number:")
    print("  Phone: +385987654321 (Croatian)")
    print("  Language: Hungarian (override)")
    print("  Result: Country=HR, Language=HU")
    print("="*70)

if __name__ == "__main__":
    asyncio.run(main())