#!/usr/bin/env python3
"""
Verify v3.3.31 deployment and check for old validation code
"""
import requests
import json
from datetime import datetime

ALB_URL = "http://ava-olo-farmers-alb-82735690.us-east-1.elb.amazonaws.com"

def verify_deployment():
    print("🔍 Verifying v3.3.31-CAVA-step-1-pure Deployment")
    print("=" * 60)
    
    # 1. Check version endpoint
    print("\n1. Version Check:")
    try:
        response = requests.get(f"{ALB_URL}/version")
        if response.ok:
            version_data = response.json()
            print(f"✅ Reported Version: {version_data.get('version', 'Unknown')}")
            print(f"   Build ID: {version_data.get('build_id', 'Unknown')}")
            print(f"   Service: {version_data.get('service', 'Unknown')}")
            
            expected = "v3.3.31-CAVA-step-1-pure"
            actual = version_data.get('version', '')
            if actual == expected:
                print(f"   ✅ Version matches expected: {expected}")
            else:
                print(f"   ❌ Version mismatch! Expected: {expected}, Got: {actual}")
        else:
            print(f"❌ Version check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error checking version: {e}")
    
    # 2. Check deployment health
    print("\n2. Deployment Health Check:")
    try:
        response = requests.get(f"{ALB_URL}/api/deployment/health")
        if response.ok:
            health = response.json()
            print(f"✅ Deployment Valid: {health.get('deployment_valid', False)}")
            print(f"   Status: {health.get('status', 'Unknown')}")
            if 'last_deployment' in health:
                print(f"   Last Deployment: {health['last_deployment']}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error checking health: {e}")
    
    # 3. Check if pure chat endpoint exists
    print("\n3. Pure Chat Endpoint Check:")
    try:
        # Try to access the pure chat page
        response = requests.get(f"{ALB_URL}/auth/register/pure")
        if response.ok:
            print("✅ /auth/register/pure endpoint exists")
            # Check if it contains our minimal chat interface
            if "pure-" in response.text and "addMessageToChat" in response.text:
                print("   ✅ Contains pure chat interface code")
            else:
                print("   ❌ Page exists but doesn't contain expected pure chat code")
        else:
            print(f"❌ Pure chat endpoint not found: {response.status_code}")
    except Exception as e:
        print(f"❌ Error checking pure chat: {e}")
    
    # 4. Test chat endpoint behavior
    print("\n4. Testing Chat Behavior (Crocodile Test):")
    try:
        test_message = "But there are crocodiles flying around?"
        response = requests.post(
            f"{ALB_URL}/api/v1/registration/chat",
            json={
                "message": test_message,
                "session_id": f"test-{datetime.now().timestamp()}"
            }
        )
        
        if response.ok:
            data = response.json()
            ai_response = data.get('response', '')
            print(f"   User: '{test_message}'")
            print(f"   AVA: '{ai_response[:100]}...'")
            
            # Check for validation errors
            if "Please use only letters" in ai_response:
                print("   ❌ OLD VALIDATION STILL ACTIVE!")
            elif "error" in data and data.get('error'):
                print("   ❌ Error response received")
            else:
                print("   ✅ Natural response - no validation errors")
        else:
            print(f"❌ Chat test failed: {response.status_code}")
            print(f"   Response: {response.text[:200]}")
    except Exception as e:
        print(f"❌ Error testing chat: {e}")
    
    # 5. Check deployment verification
    print("\n5. Deployment Verification:")
    try:
        response = requests.get(f"{ALB_URL}/api/deployment/verify")
        if response.ok:
            verify_data = response.json()
            print(f"✅ Deployment Check:")
            print(f"   Version Match: {verify_data.get('version_match', False)}")
            print(f"   Expected: {verify_data.get('expected_version', 'Unknown')}")
            print(f"   Running: {verify_data.get('running_version', 'Unknown')}")
            
            if 'checks' in verify_data:
                for check, result in verify_data['checks'].items():
                    status = "✅" if result else "❌"
                    print(f"   {status} {check}")
        else:
            print(f"⚠️  Deployment verify endpoint not available: {response.status_code}")
    except Exception as e:
        print(f"❌ Error verifying deployment: {e}")
    
    # Summary
    print("\n" + "=" * 60)
    print("DEPLOYMENT STATUS SUMMARY:")
    print("- Check ECS console for stuck deployments")
    print("- May need to force new deployment")
    print("- Clear CloudFront cache if using CDN")
    print("\nTo force deployment:")
    print("aws ecs update-service --cluster ava-olo-production \\")
    print("  --service ava-agricultural-task --force-new-deployment")

if __name__ == "__main__":
    verify_deployment()