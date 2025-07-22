# scripts/verify_v3_3_26_deployment.py
import time
import requests

def verify_deployment():
    """Verify v3.3.26 is actually deployed"""
    
    print("🔍 Verifying v3.3.26 Deployment")
    print("=" * 40)
    
    alb_url = "http://ava-olo-farmers-alb-82735690.us-east-1.elb.amazonaws.com"
    
    # Keep checking for 5 minutes
    start_time = time.time()
    success = False
    
    while time.time() - start_time < 300:  # 5 minutes
        try:
            # Check version
            response = requests.get(f"{alb_url}/version", timeout=5)
            if response.ok:
                version_data = response.json()
                current_version = version_data.get('version', 'unknown')
                
                print(f"\nCurrent version: {current_version}")
                
                if '3.3.26' in current_version:
                    print("✅ v3.3.26 is deployed!")
                    
                    # Test debug endpoint
                    debug_response = requests.get(f"{alb_url}/api/v1/debug/services")
                    if debug_response.ok:
                        print("✅ Debug endpoint working")
                    
                    success = True
                    break
                else:
                    print("⏳ Waiting for v3.3.26...")
            else:
                print(f"❌ Version endpoint returned: {response.status_code}")
                
        except Exception as e:
            print(f"⏳ Service not ready: {e}")
        
        time.sleep(10)
    
    if success:
        print("\n🎉 DEPLOYMENT SUCCESSFUL!")
        print(f"Visit: {alb_url}/dashboard")
    else:
        print("\n❌ Deployment failed or timed out")
        print("Check ECS console for issues")

if __name__ == "__main__":
    verify_deployment()