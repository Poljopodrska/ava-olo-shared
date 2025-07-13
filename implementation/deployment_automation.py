"""
Automated Deployment with Version Management
Handles Git commits, version creation, and AWS deployment

Usage:
    python deployment_automation.py --commit "Added mango support" --deploy all
"""

import asyncio
import subprocess
import argparse
from pathlib import Path
from version_manager import ConstitutionalVersionManager

class ConstitutionalDeployment:
    """Automated deployment with constitutional compliance"""
    
    def __init__(self):
        self.manager = ConstitutionalVersionManager()
    
    async def auto_commit_and_version(self, 
                                    commit_message: str,
                                    version_description: str = None,
                                    increment_type: str = "patch") -> str:
        """
        Automatically commit changes and create version
        
        Returns: New version number
        """
        
        # Use commit message as version description if not provided
        if not version_description:
            version_description = commit_message
        
        print(f"🔄 Auto-commit and version process starting...")
        
        # 1. Check if there are changes to commit
        changed_files = self.manager.get_changed_files()
        if not changed_files:
            print("⚠️ No changes detected to commit")
            return self.manager.get_current_version()
        
        print(f"📄 Found {len(changed_files)} changed files")
        
        # 2. Add all changes to git
        try:
            subprocess.run(["git", "add", "."], check=True, cwd=self.manager.project_root)
            print("✅ Added files to git staging")
        except subprocess.CalledProcessError as e:
            raise Exception(f"Failed to add files to git: {e}")
        
        # 3. Create version (this includes constitutional check)
        try:
            version = await self.manager.create_version(version_description, increment_type)
            print(f"✅ Created version {version.version_number}")
        except ValueError as e:
            print(f"❌ Version creation failed: {e}")
            raise
        
        # 4. Update commit message with version
        full_commit_message = f"{commit_message} (v{version.version_number})"
        
        # 5. Commit to git
        try:
            subprocess.run(
                ["git", "commit", "-m", full_commit_message], 
                check=True, 
                cwd=self.manager.project_root
            )
            print(f"✅ Committed to git: {full_commit_message}")
        except subprocess.CalledProcessError as e:
            raise Exception(f"Failed to commit to git: {e}")
        
        # 6. Push to origin (optional, for AWS deployment trigger)
        try:
            git_info = self.manager.get_git_info()
            subprocess.run(
                ["git", "push", "origin", git_info["branch"]], 
                check=True, 
                cwd=self.manager.project_root
            )
            print(f"✅ Pushed to origin/{git_info['branch']}")
        except subprocess.CalledProcessError as e:
            print(f"⚠️ Failed to push to git (continuing anyway): {e}")
        
        return version.version_number
    
    async def deploy_all_services(self, version: str):
        """Deploy all configured services"""
        services = list(self.manager.config["aws_services"].keys())
        
        print(f"🚀 Deploying version {version} to all services...")
        
        for service_name in services:
            print(f"\n📦 Deploying {service_name}...")
            
            # Mark deployment started
            self.manager.mark_deployment_started(service_name, version)
            
            # For AWS App Runner, deployment happens automatically on git push
            # We just monitor the deployment
            await self._monitor_deployment(service_name, version)
    
    async def _monitor_deployment(self, service_name: str, version: str):
        """Monitor AWS deployment progress"""
        print(f"👀 Monitoring {service_name} deployment...")
        
        max_checks = 20  # 10 minutes max
        check_interval = 30  # 30 seconds
        
        for i in range(max_checks):
            await asyncio.sleep(check_interval)
            
            aws_status = await self.manager.check_aws_version(service_name)
            
            if aws_status.get("status") == "online":
                aws_version = aws_status.get("version", "unknown")
                
                if aws_version == version:
                    self.manager.mark_deployment_complete(service_name, version)
                    print(f"✅ {service_name} deployment successful!")
                    return
                else:
                    print(f"⏳ {service_name} online but version mismatch (AWS: {aws_version}, Expected: {version})")
            else:
                print(f"⏳ {service_name} deployment in progress... (check {i+1}/{max_checks})")
        
        # Deployment took too long
        error_msg = f"Deployment timeout after {max_checks * check_interval} seconds"
        self.manager.mark_deployment_failed(service_name, version, error_msg)
        print(f"❌ {service_name} deployment failed: {error_msg}")
    
    async def full_deployment_workflow(self, 
                                     commit_message: str,
                                     deploy_services: list = None,
                                     increment_type: str = "patch"):
        """
        Complete deployment workflow:
        1. Constitutional compliance check
        2. Git commit with version
        3. AWS deployment
        4. Verification
        """
        
        print("🏛️ Starting Constitutional Deployment Workflow")
        print("=" * 50)
        
        try:
            # Step 1: Commit and create version
            version = await self.auto_commit_and_version(commit_message, increment_type=increment_type)
            
            # Step 2: Deploy services
            if deploy_services:
                if "all" in deploy_services:
                    await self.deploy_all_services(version)
                else:
                    for service in deploy_services:
                        if service in self.manager.config["aws_services"]:
                            await self._monitor_deployment(service, version)
                        else:
                            print(f"⚠️ Unknown service: {service}")
            
            # Step 3: Final verification
            print(f"\n🎯 Deployment Workflow Complete!")
            print(f"📦 Version: {version}")
            print(f"💬 Message: {commit_message}")
            
            # Show final status
            comparison = await self.manager.compare_versions()
            if comparison['all_synced']:
                print("✅ All services synchronized!")
            else:
                print("⚠️ Some services may still be deploying...")
            
        except Exception as e:
            print(f"❌ Deployment workflow failed: {e}")
            raise

async def main():
    """Main deployment automation entry point"""
    parser = argparse.ArgumentParser(description="Constitutional Deployment Automation")
    
    parser.add_argument("--commit", "-c", required=True, 
                       help="Commit message")
    parser.add_argument("--deploy", "-d", nargs="+", 
                       choices=["monitoring-dashboards", "agricultural-core", "all"],
                       help="Services to deploy")
    parser.add_argument("--type", "-t", choices=["major", "minor", "patch"],
                       default="patch", help="Version increment type")
    
    args = parser.parse_args()
    
    deployment = ConstitutionalDeployment()
    
    await deployment.full_deployment_workflow(
        commit_message=args.commit,
        deploy_services=args.deploy,
        increment_type=args.type
    )

if __name__ == "__main__":
    asyncio.run(main())