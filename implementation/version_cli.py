"""
Command Line Interface for Version Management
Simple commands for developers to manage versions

Usage:
    python version_cli.py status
    python version_cli.py create "Added Bulgarian mango support"
    python version_cli.py compare
    python version_cli.py deploy monitoring-dashboards
"""

import asyncio
import argparse
import sys
from pathlib import Path
import json
from version_manager import ConstitutionalVersionManager

class VersionCLI:
    """Command line interface for version management"""
    
    def __init__(self):
        self.manager = ConstitutionalVersionManager()
    
    async def cmd_status(self):
        """Show current version status"""
        current = self.manager.get_current_version()
        git_info = self.manager.get_git_info()
        changed_files = self.manager.get_changed_files()
        
        print(f"🎯 Current Version: {current}")
        print(f"📂 Git Branch: {git_info['branch']}")
        print(f"📝 Git Commit: {git_info['commit'][:8]}")
        print(f"📄 Changed Files: {len(changed_files)}")
        
        if changed_files:
            print("   📋 Files:")
            for file in changed_files[:10]:
                print(f"      - {file}")
            if len(changed_files) > 10:
                print(f"      ... and {len(changed_files) - 10} more")
        
        # Constitutional compliance
        try:
            compliance = await self.manager.check_constitutional_compliance()
            status_icon = "✅" if compliance["is_compliant"] else "❌"
            print(f"🏛️ Constitutional Compliance: {status_icon} {compliance['average_score']:.1f}%")
            
            if not compliance["is_compliant"]:
                print(f"   ⚠️ Critical Violations: {compliance.get('critical_violations', 0)}")
        except Exception as e:
            print(f"🏛️ Constitutional Check: ⚠️ Error ({e})")
    
    async def cmd_history(self, limit: int = 10):
        """Show version history"""
        versions = self.manager.get_version_history(limit)
        
        print(f"📚 Version History (last {len(versions)}):")
        print("=" * 60)
        
        for version in versions:
            compliance_icon = "✅" if version.constitutional_compliance else "❌"
            deployment_icon = "🚀" if version.deployment_status == "deployed" else "📦"
            
            print(f"{deployment_icon} {version.version_number} ({version.timestamp[:19]})")
            print(f"   📝 {version.description}")
            print(f"   🏛️ Constitutional: {compliance_icon} {version.compliance_score:.1f}%")
            print(f"   📂 Files: {len(version.files_changed)} changed")
            print(f"   🌿 Branch: {version.git_branch}")
            print()
    
    async def cmd_create(self, description: str, increment_type: str = "patch"):
        """Create new version"""
        try:
            print(f"🔄 Creating new {increment_type} version...")
            print(f"📝 Description: {description}")
            
            # Check if there are changes
            changed_files = self.manager.get_changed_files()
            if not changed_files:
                print("⚠️ No changed files detected. Continue anyway? (y/n)")
                if input().lower() != 'y':
                    print("❌ Version creation cancelled")
                    return
            
            # Create version
            version = await self.manager.create_version(description, increment_type)
            
            print(f"✅ Created version {version.version_number}")
            print(f"🏛️ Constitutional Score: {version.compliance_score:.1f}%")
            print(f"📄 Files Changed: {len(version.files_changed)}")
            
            # Show next steps
            print("\n🚀 Next Steps:")
            print("   1. Review changes: git diff")
            print("   2. Commit changes: git add . && git commit -m 'version {}'".format(version.version_number))
            print("   3. Deploy: python version_cli.py deploy <service-name>")
            
        except ValueError as e:
            print(f"❌ Error: {e}")
            sys.exit(1)
    
    async def cmd_compare(self):
        """Compare local and AWS versions"""
        print("🔍 Comparing local and AWS versions...")
        
        comparison = await self.manager.compare_versions()
        
        print(f"📦 Local Version: {comparison['local_version']}")
        print("☁️ AWS Versions:")
        
        for service_name, info in comparison['version_comparison'].items():
            status_icon = "✅" if info['matches'] else "❌"
            aws_status = info['status']
            status_icon_aws = "🟢" if aws_status == "online" else "🔴"
            
            print(f"   {service_name}:")
            print(f"      {status_icon} Version Match: {info['matches']}")
            print(f"      📦 Local: {info['local']}")
            print(f"      ☁️ AWS: {info['aws']}")
            print(f"      {status_icon_aws} Status: {aws_status}")
        
        if comparison['all_synced']:
            print("\n🎉 All services are synchronized!")
        else:
            print("\n⚠️ Version mismatches detected. Consider deploying.")
    
    async def cmd_deploy(self, service_name: str):
        """Deploy to AWS (simulation)"""
        current_version = self.manager.get_current_version()
        
        print(f"🚀 Deploying {service_name} version {current_version}...")
        
        # Mark deployment started
        self.manager.mark_deployment_started(service_name, current_version)
        
        # Simulate deployment steps
        print("   📦 Building deployment package...")
        await asyncio.sleep(1)  # Simulate build time
        
        print("   ☁️ Uploading to AWS App Runner...")
        await asyncio.sleep(2)  # Simulate upload time
        
        print("   🔄 AWS App Runner deploying...")
        await asyncio.sleep(3)  # Simulate deployment time
        
        # Check if deployment succeeded (by checking AWS)
        aws_status = await self.manager.check_aws_version(service_name)
        
        if aws_status.get("status") == "online":
            self.manager.mark_deployment_complete(service_name, current_version)
            print(f"   ✅ Deployment successful!")
            print(f"   🌐 URL: {self.manager.config['aws_services'][service_name]['url']}")
        else:
            error_msg = aws_status.get("error", "Unknown deployment error")
            self.manager.mark_deployment_failed(service_name, current_version, error_msg)
            print(f"   ❌ Deployment failed: {error_msg}")
    
    async def cmd_init(self):
        """Initialize version management in current directory"""
        print("🔧 Initializing Constitutional Version Management...")
        
        # Create version files
        self.manager._ensure_version_files()
        
        # Create initial version
        try:
            initial_version = await self.manager.create_version(
                "Initial version - Constitutional system initialized",
                force=True
            )
            print(f"✅ Initialized with version {initial_version.version_number}")
        except Exception as e:
            print(f"⚠️ Could not create initial version: {e}")
        
        print("📁 Created files:")
        print("   - version_history.json")
        print("   - version_config.json") 
        print("   - deployment_status.json")
        print("\n🎯 Next steps:")
        print("   python version_cli.py status")

def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(description="Constitutional Version Management")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Status command
    subparsers.add_parser('status', help='Show current version status')
    
    # History command
    history_parser = subparsers.add_parser('history', help='Show version history')
    history_parser.add_argument('--limit', type=int, default=10, help='Number of versions to show')
    
    # Create command
    create_parser = subparsers.add_parser('create', help='Create new version')
    create_parser.add_argument('description', help='Version description')
    create_parser.add_argument('--type', choices=['major', 'minor', 'patch'], 
                             default='patch', help='Version increment type')
    
    # Compare command
    subparsers.add_parser('compare', help='Compare local and AWS versions')
    
    # Deploy command
    deploy_parser = subparsers.add_parser('deploy', help='Deploy to AWS')
    deploy_parser.add_argument('service', choices=['monitoring-dashboards', 'agricultural-core'],
                             help='Service to deploy')
    
    # Init command
    subparsers.add_parser('init', help='Initialize version management')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Create CLI instance and run command
    cli = VersionCLI()
    
    if args.command == 'status':
        asyncio.run(cli.cmd_status())
    elif args.command == 'history':
        asyncio.run(cli.cmd_history(args.limit))
    elif args.command == 'create':
        asyncio.run(cli.cmd_create(args.description, args.type))
    elif args.command == 'compare':
        asyncio.run(cli.cmd_compare())
    elif args.command == 'deploy':
        asyncio.run(cli.cmd_deploy(args.service))
    elif args.command == 'init':
        asyncio.run(cli.cmd_init())

if __name__ == "__main__":
    main()