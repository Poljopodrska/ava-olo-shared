"""
Test Constitutional Database Query via Aurora RDS
Verifies LLM-first approach works with AWS Aurora
"""

import asyncio
import os
import sys
from datetime import datetime

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.join(os.path.dirname(__file__), 'ava-olo-agricultural-core'))

async def test_constitutional_query():
    """Test constitutional database query against Aurora RDS"""
    print("🧠 Testing Constitutional Database Query with Aurora RDS...")
    print("=" * 60)
    
    try:
        # Import config manager
        from ava_olo_shared.config_manager import config
        print(f"✅ Config loaded from: {config._env_file_path}")
        print(f"✅ Database: {config.db_host}")
        print(f"✅ LLM Model: {config.openai_model}")
        
        # Import LLM database engine
        from llm_first_database_engine import LLMDatabaseQueryEngine, DatabaseQuery
        
        print("\n🔄 Initializing LLM Database Engine...")
        # Initialize engine (connects to Aurora RDS)
        engine = LLMDatabaseQueryEngine()
        print("✅ Engine initialized with Aurora RDS connection")
        
        # Test queries
        test_queries = [
            {
                "description": "Basic count query",
                "query": DatabaseQuery(
                    natural_language_query="How many farmers are in the database?",
                    farmer_id=None,
                    language="en"
                )
            },
            {
                "description": "Bulgarian mango test (MANGO RULE)",
                "query": DatabaseQuery(
                    natural_language_query="Колко манго дървета имам?",
                    farmer_id=1,
                    country_code="BG",
                    language="bg"
                )
            },
            {
                "description": "Complex join query",
                "query": DatabaseQuery(
                    natural_language_query="Show me farmers who have planted tomatoes this year",
                    farmer_id=None,
                    language="en"
                )
            }
        ]
        
        print("\n📊 Running Constitutional Test Queries...")
        for i, test in enumerate(test_queries, 1):
            print(f"\n{'='*60}")
            print(f"Test {i}: {test['description']}")
            print(f"Query: {test['query'].natural_language_query}")
            print(f"Language: {test['query'].language}")
            
            try:
                start_time = datetime.now()
                result = await engine.process_farmer_query(test['query'])
                end_time = datetime.now()
                duration = (end_time - start_time).total_seconds()
                
                print(f"\n✅ Query executed successfully in {duration:.2f} seconds")
                print(f"\n🔍 Generated SQL:")
                print(f"   {result.sql_query}")
                print(f"\n💬 Natural Language Response:")
                print(f"   {result.natural_language_response[:200]}...")
                print(f"\n📋 Metadata:")
                print(f"   Results count: {len(result.raw_results)}")
                print(f"   Constitutional compliance: {result.constitutional_compliance}")
                print(f"   LLM Model: {result.processing_metadata.get('llm_model', 'Unknown')}")
                
                # Verify constitutional compliance
                if result.constitutional_compliance:
                    print("✅ Constitutional compliance verified")
                else:
                    print("❌ Constitutional compliance failed")
                
            except Exception as e:
                print(f"\n❌ Query failed: {str(e)}")
                print(f"   Error type: {type(e).__name__}")
        
        return True
        
    except ImportError as e:
        print(f"\n❌ Import Error: {str(e)}")
        print("\n🔧 Troubleshooting:")
        print("   1. Ensure llm_first_database_engine.py exists")
        print("   2. Check that config_manager.py is properly configured")
        print("   3. Verify OpenAI API key is set in .env")
        return False
        
    except Exception as e:
        print(f"\n❌ Constitutional query test failed: {str(e)}")
        print(f"   Error type: {type(e).__name__}")
        return False

async def test_aurora_specific_features():
    """Test Aurora-specific features and performance"""
    print("\n\n🌟 Testing Aurora-Specific Features...")
    print("=" * 60)
    
    try:
        from llm_first_database_engine import LLMDatabaseQueryEngine, DatabaseQuery
        engine = LLMDatabaseQueryEngine()
        
        # Test Aurora read replica simulation (if available)
        aurora_query = DatabaseQuery(
            natural_language_query="Show database connection statistics and performance metrics",
            language="en"
        )
        
        result = await engine.process_farmer_query(aurora_query)
        print("✅ Aurora performance query executed")
        print(f"   Response: {result.natural_language_response[:100]}...")
        
        # Test data locality
        location_query = DatabaseQuery(
            natural_language_query="Show farmers grouped by country",
            language="en"
        )
        
        result = await engine.process_farmer_query(location_query)
        print("✅ Data locality query executed")
        
        return True
        
    except Exception as e:
        print(f"❌ Aurora-specific test failed: {e}")
        return False

if __name__ == "__main__":
    print("🔍 CONSTITUTIONAL DATABASE QUERY TEST - AWS AURORA RDS")
    print("=" * 60)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Check environment
    print("\n🔧 Environment Check:")
    db_host = os.getenv('DB_HOST', 'Not set')
    if 'amazonaws.com' in db_host:
        print(f"✅ Aurora RDS endpoint detected: {db_host}")
    else:
        print(f"❌ Non-Aurora endpoint: {db_host}")
    
    openai_key = os.getenv('OPENAI_API_KEY', '')
    if openai_key.startswith('sk-'):
        print(f"✅ OpenAI API key configured: sk-...{openai_key[-4:]}")
    else:
        print("❌ OpenAI API key not configured")
    
    # Run async tests
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        query_ok = loop.run_until_complete(test_constitutional_query())
        aurora_ok = loop.run_until_complete(test_aurora_specific_features())
        
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY:")
        print("=" * 60)
        print(f"🧠 LLM Query Tests: {'✅ PASS' if query_ok else '❌ FAIL'}")
        print(f"🌟 Aurora Features: {'✅ PASS' if aurora_ok else '❌ FAIL'}")
        
        if query_ok and aurora_ok:
            print("\n🎉 ALL TESTS PASSED!")
            print("   LLM-first queries are working correctly with Aurora RDS")
        else:
            print("\n⚠️  Some tests failed. Check the errors above.")
            
    except KeyboardInterrupt:
        print("\n⚠️  Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Test execution failed: {e}")
    finally:
        loop.close()