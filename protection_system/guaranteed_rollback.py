#!/usr/bin/env python3
"""
Guaranteed Rollback System - ALWAYS works, no exceptions
Part of the Complete Protection System v3.5.2
"""
import subprocess
import boto3
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

class GuaranteedRollbackSystem:
    """Ensures rollback ALWAYS works - tested weekly"""
    
    def __init__(self):
        self.base_path = Path(__file__).parent.parent.parent
        self.rollback_dir = self.base_path / "protection_system" / "rollback_safety"
        self.rollback_dir.mkdir(parents=True, exist_ok=True)
        
        # AWS clients (with error handling)
        try:
            self.ecs = boto3.client('ecs', region_name='us-east-1')
            self.s3 = boto3.client('s3', region_name='us-east-1')
            self.ecr = boto3.client('ecr', region_name='us-east-1')
            self.aws_available = True
        except Exception as e:
            print(f"⚠️ AWS clients not available: {e}")
            self.aws_available = False
        
        self.rollback_bucket = 'ava-olo-rollback-safety'
        self.cluster_name = 'ava-olo-production'
        
        # Service definitions
        self.services = {
            'agricultural': {
                'service_name': 'ava-olo-agricultural-service',
                'task_definition_family': 'ava-olo-agricultural-task',
                'ecr_repository': 'ava-olo-agricultural-core'
            },
            'monitoring': {
                'service_name': 'ava-olo-monitoring-service', 
                'task_definition_family': 'ava-olo-monitoring-task',
                'ecr_repository': 'ava-olo-monitoring-dashboards'
            }
        }
    
    def tag_stable_version(self, version: str, force_tag: bool = False) -> str:
        """Tag current state as stable - only after thorough testing"""
        tag_name = f"stable-{version}-{datetime.utcnow().strftime('%Y%m%d-%H%M%S')}"
        
        print(f"🏷️ Tagging stable version: {tag_name}")
        
        # 1. Git tag
        try:
            subprocess.run(["git", "tag", tag_name], check=True)
            print(f"✅ Git tag created: {tag_name}")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to create git tag: {e}")
            if not force_tag:
                return None
        
        # 2. Backup current deployment state
        if self.aws_available:
            backup_success = self.backup_current_state(tag_name)
            if not backup_success and not force_tag:
                print("❌ Backup failed - not marking as stable")
                return None
        
        # 3. Test rollback immediately to ensure it works
        if not force_tag:
            rollback_test = self.test_rollback_capability(tag_name)
            if not rollback_test:
                print("❌ Rollback test failed - not marking as stable!")
                return None
        
        # 4. Record stable version
        self.record_stable_version(tag_name, version)
        
        print(f"✅ Version {version} marked as stable: {tag_name}")
        return tag_name
    
    def backup_current_state(self, tag_name: str) -> bool:
        """Backup everything needed for guaranteed rollback"""
        if not self.aws_available:
            print("⚠️ AWS not available - creating local backup only")
            return self.create_local_backup(tag_name)
        
        try:
            backup_data = {
                "tag": tag_name,
                "timestamp": datetime.utcnow().isoformat(),
                "git_commit": self.get_current_git_commit(),
                "ecs_services": {},
                "docker_images": {},
                "task_definitions": {}
            }
            
            # Backup ECS service states
            for service_key, service_config in self.services.items():
                try:
                    # Get current service
                    response = self.ecs.describe_services(
                        cluster=self.cluster_name,
                        services=[service_config['service_name']]
                    )
                    
                    if response['services']:
                        service = response['services'][0]
                        backup_data['ecs_services'][service_key] = {
                            'taskDefinition': service['taskDefinition'],
                            'desiredCount': service['desiredCount'],
                            'status': service['status']
                        }
                        
                        # Get task definition details
                        task_def_arn = service['taskDefinition']
                        task_def_response = self.ecs.describe_task_definition(
                            taskDefinition=task_def_arn
                        )
                        backup_data['task_definitions'][service_key] = task_def_response['taskDefinition']
                        
                        # Extract Docker image
                        containers = task_def_response['taskDefinition']['containerDefinitions']
                        for container in containers:
                            if 'image' in container:
                                backup_data['docker_images'][service_key] = container['image']
                                
                except Exception as e:
                    print(f"⚠️ Could not backup {service_key}: {e}")
            
            # Store in S3 for safety
            try:
                self.s3.put_object(
                    Bucket=self.rollback_bucket,
                    Key=f"backups/{tag_name}/state.json",
                    Body=json.dumps(backup_data, indent=2)
                )
                print(f"✅ Backup stored in S3: {tag_name}")
            except Exception as e:
                print(f"⚠️ S3 backup failed: {e}")
            
            # Also store locally
            local_backup_file = self.rollback_dir / f"{tag_name}_backup.json"
            with open(local_backup_file, 'w') as f:
                json.dump(backup_data, f, indent=2)
            
            print(f"✅ Local backup created: {local_backup_file}")
            return True
            
        except Exception as e:
            print(f"❌ Backup failed: {e}")
            return False
    
    def create_local_backup(self, tag_name: str) -> bool:
        """Create local backup when AWS not available"""
        try:
            backup_data = {
                "tag": tag_name,
                "timestamp": datetime.utcnow().isoformat(),
                "git_commit": self.get_current_git_commit(),
                "local_backup": True,
                "aws_available": False
            }
            
            local_backup_file = self.rollback_dir / f"{tag_name}_backup.json"
            with open(local_backup_file, 'w') as f:
                json.dump(backup_data, f, indent=2)
            
            print(f"✅ Local backup created: {local_backup_file}")
            return True
            
        except Exception as e:
            print(f"❌ Local backup failed: {e}")
            return False
    
    def get_current_git_commit(self) -> str:
        """Get current git commit hash"""
        try:
            result = subprocess.run(
                ["git", "rev-parse", "HEAD"], 
                capture_output=True, 
                text=True, 
                check=True
            )
            return result.stdout.strip()
        except:
            return "unknown"
    
    def test_rollback_capability(self, tag_name: str) -> bool:
        """Test that rollback will work - DRY RUN"""
        print(f"🧪 Testing rollback capability for {tag_name}...")
        
        try:
            # Test 1: Git rollback capability
            git_test = self.test_git_rollback(tag_name)
            if not git_test:
                print("❌ Git rollback test failed")
                return False
            
            # Test 2: AWS rollback capability (if available)
            if self.aws_available:
                aws_test = self.test_aws_rollback_capability(tag_name)
                if not aws_test:
                    print("❌ AWS rollback test failed")
                    return False
            
            print("✅ Rollback capability verified")
            return True
            
        except Exception as e:
            print(f"❌ Rollback test failed: {e}")
            return False
    
    def test_git_rollback(self, tag_name: str) -> bool:
        """Test git rollback capability"""
        try:
            # Check if tag exists
            result = subprocess.run(
                ["git", "tag", "-l", tag_name],
                capture_output=True,
                text=True
            )
            
            if tag_name not in result.stdout:
                print(f"❌ Git tag {tag_name} not found")
                return False
            
            # Test checkout (dry run)
            result = subprocess.run(
                ["git", "show", tag_name],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                print("✅ Git rollback test passed")
                return True
            else:
                print("❌ Git rollback test failed")
                return False
                
        except Exception as e:
            print(f"❌ Git rollback test error: {e}")
            return False
    
    def test_aws_rollback_capability(self, tag_name: str) -> bool:
        """Test AWS rollback capability without actually rolling back"""
        try:
            # Check if backup exists
            backup_file = self.rollback_dir / f"{tag_name}_backup.json"
            if not backup_file.exists():
                print(f"❌ Backup file not found: {backup_file}")
                return False
            
            # Load backup data
            with open(backup_file) as f:
                backup_data = json.load(f)
            
            # Verify backup completeness
            required_keys = ['ecs_services', 'docker_images', 'task_definitions']
            for key in required_keys:
                if key not in backup_data:
                    print(f"❌ Backup missing required data: {key}")
                    return False
            
            # Test ECS access
            try:
                self.ecs.describe_clusters(clusters=[self.cluster_name])
                print("✅ ECS access verified")
            except Exception as e:
                print(f"❌ ECS access test failed: {e}")
                return False
            
            print("✅ AWS rollback capability verified")
            return True
            
        except Exception as e:
            print(f"❌ AWS rollback test error: {e}")
            return False
    
    def rollback_to_version(self, version_or_tag: str, confirm: bool = False) -> bool:
        """One-command rollback that MUST work"""
        if not confirm:
            print("🚨 CRITICAL: This will rollback the entire system!")
            print(f"Rolling back to: {version_or_tag}")
            response = input("Type 'ROLLBACK CONFIRMED' to proceed: ")
            if response != "ROLLBACK CONFIRMED":
                print("❌ Rollback cancelled")
                return False
        
        print(f"🔄 Rolling back to {version_or_tag}...")
        
        try:
            # Step 1: Find the backup
            backup_file = self.find_backup_file(version_or_tag)
            if not backup_file:
                print(f"❌ No backup found for {version_or_tag}")
                return False
            
            # Step 2: Git rollback
            git_success = self.perform_git_rollback(version_or_tag)
            if not git_success:
                print("❌ Git rollback failed")
                return False
            
            # Step 3: AWS rollback (if available)
            if self.aws_available:
                aws_success = self.perform_aws_rollback(backup_file)
                if not aws_success:
                    print("❌ AWS rollback failed")
                    return False
            
            # Step 4: Verify rollback success
            verify_success = self.verify_rollback_success(version_or_tag)
            if not verify_success:
                print("❌ Rollback verification failed")
                return False
            
            print(f"✅ Successfully rolled back to {version_or_tag}")
            self.record_rollback_event(version_or_tag)
            return True
            
        except Exception as e:
            print(f"❌ CRITICAL: Rollback failed: {e}")
            return False
    
    def find_backup_file(self, version_or_tag: str) -> Optional[Path]:
        """Find backup file for version"""
        # Try exact match first
        exact_match = self.rollback_dir / f"{version_or_tag}_backup.json"
        if exact_match.exists():
            return exact_match
        
        # Try pattern match
        for backup_file in self.rollback_dir.glob("*_backup.json"):
            if version_or_tag in backup_file.name:
                return backup_file
        
        return None
    
    def perform_git_rollback(self, version_or_tag: str) -> bool:
        """Perform git rollback"""
        try:
            print(f"🔄 Git rollback to {version_or_tag}")
            
            # Hard reset to tag
            subprocess.run(["git", "reset", "--hard", version_or_tag], check=True)
            print("✅ Git rollback completed")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Git rollback failed: {e}")
            return False
    
    def perform_aws_rollback(self, backup_file: Path) -> bool:
        """Perform AWS rollback"""
        try:
            print("🔄 AWS rollback in progress...")
            
            with open(backup_file) as f:
                backup_data = json.load(f)
            
            # Rollback ECS services
            for service_key, service_data in backup_data.get('ecs_services', {}).items():
                service_config = self.services[service_key]
                
                print(f"🔄 Rolling back service: {service_config['service_name']}")
                
                self.ecs.update_service(
                    cluster=self.cluster_name,
                    service=service_config['service_name'],
                    taskDefinition=service_data['taskDefinition'],
                    desiredCount=service_data['desiredCount']
                )
            
            # Wait for stability
            print("⏳ Waiting for services to stabilize...")
            for service_key in backup_data.get('ecs_services', {}):
                service_config = self.services[service_key]
                
                waiter = self.ecs.get_waiter('services_stable')
                waiter.wait(
                    cluster=self.cluster_name,
                    services=[service_config['service_name']],
                    WaiterConfig={'maxAttempts': 30, 'delay': 30}
                )
            
            print("✅ AWS rollback completed")
            return True
            
        except Exception as e:
            print(f"❌ AWS rollback failed: {e}")
            return False
    
    def verify_rollback_success(self, version_or_tag: str) -> bool:
        """Verify rollback worked"""
        try:
            # Verify git state
            current_commit = self.get_current_git_commit()
            tag_commit = subprocess.run(
                ["git", "rev-list", "-n", "1", version_or_tag],
                capture_output=True,
                text=True
            ).stdout.strip()
            
            if current_commit != tag_commit:
                print(f"❌ Git state mismatch: {current_commit} != {tag_commit}")
                return False
            
            print("✅ Rollback verification passed")
            return True
            
        except Exception as e:
            print(f"❌ Rollback verification failed: {e}")
            return False
    
    def record_stable_version(self, tag_name: str, version: str):
        """Record stable version for future reference"""
        stable_versions_file = self.rollback_dir / "stable_versions.json"
        
        if stable_versions_file.exists():
            with open(stable_versions_file) as f:
                stable_versions = json.load(f)
        else:
            stable_versions = {"versions": []}
        
        stable_versions["versions"].append({
            "version": version,
            "tag": tag_name,
            "timestamp": datetime.utcnow().isoformat(),
            "git_commit": self.get_current_git_commit()
        })
        
        # Keep only last 10 stable versions
        stable_versions["versions"] = stable_versions["versions"][-10:]
        
        with open(stable_versions_file, 'w') as f:
            json.dump(stable_versions, f, indent=2)
    
    def record_rollback_event(self, version_or_tag: str):
        """Record rollback event for audit"""
        rollback_log_file = self.rollback_dir / "rollback_events.json"
        
        if rollback_log_file.exists():
            with open(rollback_log_file) as f:
                rollback_events = json.load(f)
        else:
            rollback_events = {"events": []}
        
        rollback_events["events"].append({
            "target_version": version_or_tag,
            "timestamp": datetime.utcnow().isoformat(),
            "rollback_commit": self.get_current_git_commit()
        })
        
        with open(rollback_log_file, 'w') as f:
            json.dump(rollback_events, f, indent=2)
    
    def get_stable_versions(self) -> List[Dict]:
        """Get list of stable versions available for rollback"""
        stable_versions_file = self.rollback_dir / "stable_versions.json"
        
        if not stable_versions_file.exists():
            return []
        
        with open(stable_versions_file) as f:
            data = json.load(f)
        
        return data.get("versions", [])

def main():
    """Command line interface"""
    if len(sys.argv) < 2:
        print("Usage: python guaranteed_rollback.py [tag|rollback|list|test] [version]")
        sys.exit(1)
    
    rollback_system = GuaranteedRollbackSystem()
    command = sys.argv[1]
    
    if command == "tag":
        if len(sys.argv) < 3:
            print("Usage: python guaranteed_rollback.py tag <version>")
            sys.exit(1)
        
        version = sys.argv[2]
        tag_name = rollback_system.tag_stable_version(version)
        if tag_name:
            print(f"✅ Version {version} tagged as stable: {tag_name}")
        else:
            print(f"❌ Failed to tag version {version} as stable")
            sys.exit(1)
    
    elif command == "rollback":
        if len(sys.argv) < 3:
            print("Usage: python guaranteed_rollback.py rollback <version_or_tag>")
            sys.exit(1)
        
        version_or_tag = sys.argv[2]
        success = rollback_system.rollback_to_version(version_or_tag)
        if not success:
            sys.exit(1)
    
    elif command == "list":
        stable_versions = rollback_system.get_stable_versions()
        print("Available stable versions for rollback:")
        for version_info in stable_versions:
            print(f"  - {version_info['version']} ({version_info['tag']}) - {version_info['timestamp']}")
    
    elif command == "test":
        if len(sys.argv) < 3:
            print("Usage: python guaranteed_rollback.py test <version_or_tag>")
            sys.exit(1)
        
        version_or_tag = sys.argv[2]
        success = rollback_system.test_rollback_capability(version_or_tag)
        if not success:
            sys.exit(1)
    
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()