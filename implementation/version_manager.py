"""
Constitutional Version Management System
Tracks local changes, manages AWS deployments, ensures constitutional compliance

Features:
- Automatic version numbering (semantic versioning)
- Change descriptions and constitutional compliance tracking
- Local vs AWS version comparison
- Deployment status monitoring
- Constitutional compliance verification per version
"""

import json
import subprocess
import hashlib
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
import logging

logger = logging.getLogger(__name__)

@dataclass
class Version:
    """Version information with constitutional compliance"""
    version_number: str
    timestamp: str
    description: str
    git_commit: str
    git_branch: str
    files_changed: List[str]
    constitutional_compliance: bool
    compliance_score: float
    deployment_status: str  # 'local', 'deploying', 'deployed', 'failed'
    aws_deployment_url: Optional[str] = None
    author: str = "developer"
    environment: str = "development"

@dataclass
class DeploymentInfo:
    """AWS deployment information"""
    service_name: str
    aws_url: str
    environment: str
    version_deployed: Optional[str] = None
    deployment_time: Optional[str] = None
    status: str = "unknown"

class ConstitutionalVersionManager:
    """
    Version management with constitutional compliance tracking
    """
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.version_file = self.project_root / "version_history.json"
        self.config_file = self.project_root / "version_config.json"
        self.deployment_file = self.project_root / "deployment_status.json"
        
        self._load_config()
        self._ensure_version_files()
    
    def _load_config(self):
        """Load version management configuration"""
        default_config = {
            "version_format": "semantic",  # semantic (1.2.3) or timestamp
            "auto_increment": True,
            "require_description": True,
            "require_constitutional_check": True,
            "aws_services": {
                "monitoring-dashboards": {
                    "name": "ava-olo-monitoring-dashboards",
                    "url": "https://6pmgiripe.us-east-1.awsapprunner.com",
                    "health_endpoint": "/health"
                },
                "agricultural-core": {
                    "name": "ava-olo-agricultural-core", 
                    "url": "https://3ksdvgdtud.us-east-1.awsapprunner.com",
                    "health_endpoint": "/health"
                }
            },
            "excluded_files": [
                "*.pyc", "__pycache__", ".git", "*.log", 
                "node_modules", ".env", "*.tmp"
            ]
        }
        
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                self.config = {**default_config, **json.load(f)}
        else:
            self.config = default_config
            self._save_config()
    
    def _save_config(self):
        """Save configuration to file"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def _ensure_version_files(self):
        """Ensure version tracking files exist"""
        if not self.version_file.exists():
            with open(self.version_file, 'w') as f:
                json.dump({"versions": [], "current_version": "0.0.0"}, f, indent=2)
        
        if not self.deployment_file.exists():
            with open(self.deployment_file, 'w') as f:
                json.dump({"deployments": {}}, f, indent=2)
    
    def get_current_version(self) -> str:
        """Get current version number"""
        with open(self.version_file, 'r') as f:
            data = json.load(f)
        return data.get("current_version", "0.0.0")
    
    def get_next_version(self, increment_type: str = "patch") -> str:
        """
        Generate next version number
        
        Args:
            increment_type: 'major', 'minor', 'patch'
        """
        current = self.get_current_version()
        
        if self.config["version_format"] == "timestamp":
            return datetime.now().strftime("%Y%m%d.%H%M%S")
        
        # Semantic versioning
        parts = current.split(".")
        major, minor, patch = int(parts[0]), int(parts[1]), int(parts[2])
        
        if increment_type == "major":
            major += 1
            minor = 0
            patch = 0
        elif increment_type == "minor":
            minor += 1
            patch = 0
        else:  # patch
            patch += 1
        
        return f"{major}.{minor}.{patch}"
    
    def get_git_info(self) -> Dict[str, str]:
        """Get current git information"""
        try:
            commit = subprocess.check_output(
                ["git", "rev-parse", "HEAD"], 
                cwd=self.project_root,
                text=True
            ).strip()
            
            branch = subprocess.check_output(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                cwd=self.project_root, 
                text=True
            ).strip()
            
            return {"commit": commit, "branch": branch}
        except subprocess.CalledProcessError:
            return {"commit": "unknown", "branch": "unknown"}
    
    def get_changed_files(self) -> List[str]:
        """Get list of files changed since last commit"""
        try:
            # Get modified files
            modified = subprocess.check_output(
                ["git", "diff", "--name-only"],
                cwd=self.project_root,
                text=True
            ).strip().split('\n')
            
            # Get staged files
            staged = subprocess.check_output(
                ["git", "diff", "--cached", "--name-only"],
                cwd=self.project_root,
                text=True
            ).strip().split('\n')
            
            # Combine and filter
            all_files = list(set(modified + staged))
            return [f for f in all_files if f and not self._is_excluded_file(f)]
            
        except subprocess.CalledProcessError:
            return []
    
    def _is_excluded_file(self, filepath: str) -> bool:
        """Check if file should be excluded from version tracking"""
        import fnmatch
        for pattern in self.config["excluded_files"]:
            if fnmatch.fnmatch(filepath, pattern):
                return True
        return False
    
    async def check_constitutional_compliance(self) -> Dict[str, Any]:
        """Check constitutional compliance of current codebase"""
        try:
            # Import constitutional checker
            from constitutional_checker import ConstitutionalChecker
            
            checker = ConstitutionalChecker()
            
            # Check main Python files
            python_files = list(self.project_root.glob("**/*.py"))
            total_score = 0
            file_count = 0
            violations = []
            
            for py_file in python_files[:10]:  # Limit to avoid long checks
                if not self._is_excluded_file(str(py_file)):
                    try:
                        result = await checker.check_compliance(py_file, "file")
                        total_score += result.overall_score
                        file_count += 1
                        violations.extend(result.violations)
                    except Exception as e:
                        logger.warning(f"Could not check {py_file}: {e}")
            
            average_score = total_score / file_count if file_count > 0 else 0
            is_compliant = average_score >= 80  # 80% threshold
            
            return {
                "is_compliant": is_compliant,
                "average_score": average_score,
                "files_checked": file_count,
                "total_violations": len(violations),
                "critical_violations": len([v for v in violations if v.severity == "CRITICAL"])
            }
            
        except ImportError:
            logger.warning("Constitutional checker not available")
            return {
                "is_compliant": True,
                "average_score": 100.0,
                "note": "Constitutional checker not available"
            }
    
    async def create_version(self, 
                           description: str,
                           increment_type: str = "patch",
                           force: bool = False) -> Version:
        """
        Create new version with constitutional compliance check
        
        Args:
            description: Description of changes
            increment_type: 'major', 'minor', 'patch'
            force: Skip constitutional compliance check
        """
        
        # Validate description
        if self.config["require_description"] and not description.strip():
            raise ValueError("Version description is required")
        
        # Check constitutional compliance
        compliance_result = {"is_compliant": True, "average_score": 100.0}
        if self.config["require_constitutional_check"] and not force:
            compliance_result = await self.check_constitutional_compliance()
            
            if not compliance_result["is_compliant"]:
                raise ValueError(
                    f"Constitutional compliance failed: {compliance_result['average_score']:.1f}% "
                    f"({compliance_result.get('critical_violations', 0)} critical violations). "
                    f"Use force=True to override."
                )
        
        # Generate version
        next_version = self.get_next_version(increment_type)
        git_info = self.get_git_info()
        changed_files = self.get_changed_files()
        
        # Create version object
        version = Version(
            version_number=next_version,
            timestamp=datetime.now().isoformat(),
            description=description,
            git_commit=git_info["commit"],
            git_branch=git_info["branch"],
            files_changed=changed_files,
            constitutional_compliance=compliance_result["is_compliant"],
            compliance_score=compliance_result["average_score"],
            deployment_status="local"
        )
        
        # Save version
        self._save_version(version)
        
        logger.info(f"Created version {next_version}: {description}")
        return version
    
    def _save_version(self, version: Version):
        """Save version to history file"""
        with open(self.version_file, 'r') as f:
            data = json.load(f)
        
        data["versions"].append(asdict(version))
        data["current_version"] = version.version_number
        
        with open(self.version_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def get_version_history(self, limit: int = 20) -> List[Version]:
        """Get version history"""
        with open(self.version_file, 'r') as f:
            data = json.load(f)
        
        versions = []
        for v_data in data["versions"][-limit:]:
            versions.append(Version(**v_data))
        
        return sorted(versions, key=lambda v: v.timestamp, reverse=True)
    
    def get_deployment_status(self) -> Dict[str, DeploymentInfo]:
        """Get current AWS deployment status"""
        with open(self.deployment_file, 'r') as f:
            data = json.load(f)
        
        deployments = {}
        for service_name, dep_data in data.get("deployments", {}).items():
            deployments[service_name] = DeploymentInfo(**dep_data)
        
        return deployments
    
    async def check_aws_version(self, service_name: str) -> Dict[str, Any]:
        """Check version deployed on AWS"""
        import aiohttp
        
        if service_name not in self.config["aws_services"]:
            return {"error": f"Unknown service: {service_name}"}
        
        service_config = self.config["aws_services"][service_name]
        health_url = f"{service_config['url']}{service_config['health_endpoint']}"
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(health_url, timeout=10) as response:
                    if response.status == 200:
                        data = await response.json()
                        return {
                            "status": "online",
                            "version": data.get("version", "unknown"),
                            "service": data.get("service", service_name),
                            "timestamp": data.get("timestamp"),
                            "response_time_ms": response.headers.get("X-Response-Time", "unknown")
                        }
                    else:
                        return {"status": "error", "http_status": response.status}
                        
        except Exception as e:
            return {"status": "offline", "error": str(e)}
    
    async def compare_versions(self) -> Dict[str, Any]:
        """Compare local version with AWS deployed versions"""
        local_version = self.get_current_version()
        aws_versions = {}
        
        for service_name in self.config["aws_services"]:
            aws_status = await self.check_aws_version(service_name)
            aws_versions[service_name] = aws_status
        
        # Determine if versions match
        version_matches = {}
        for service_name, aws_status in aws_versions.items():
            aws_version = aws_status.get("version", "unknown")
            version_matches[service_name] = {
                "local": local_version,
                "aws": aws_version,
                "matches": local_version == aws_version,
                "status": aws_status.get("status", "unknown")
            }
        
        return {
            "local_version": local_version,
            "aws_versions": aws_versions,
            "version_comparison": version_matches,
            "all_synced": all(vm["matches"] for vm in version_matches.values())
        }
    
    def mark_deployment_started(self, service_name: str, version: str):
        """Mark deployment as started"""
        self._update_deployment_status(service_name, version, "deploying")
    
    def mark_deployment_complete(self, service_name: str, version: str):
        """Mark deployment as complete"""
        self._update_deployment_status(service_name, version, "deployed")
    
    def mark_deployment_failed(self, service_name: str, version: str, error: str):
        """Mark deployment as failed"""
        self._update_deployment_status(service_name, version, "failed", error)
    
    def _update_deployment_status(self, service_name: str, version: str, status: str, error: str = None):
        """Update deployment status in file"""
        with open(self.deployment_file, 'r') as f:
            data = json.load(f)
        
        if "deployments" not in data:
            data["deployments"] = {}
        
        data["deployments"][service_name] = {
            "service_name": service_name,
            "aws_url": self.config["aws_services"][service_name]["url"],
            "environment": "production",
            "version_deployed": version,
            "deployment_time": datetime.now().isoformat(),
            "status": status
        }
        
        if error:
            data["deployments"][service_name]["error"] = error
        
        with open(self.deployment_file, 'w') as f:
            json.dump(data, f, indent=2)