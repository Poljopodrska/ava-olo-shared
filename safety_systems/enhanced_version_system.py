#!/usr/bin/env python3
"""
Enhanced Version Management System
Tracks deployments, rollbacks, and version history with Git integration
"""

import json
import subprocess
import os
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import sqlite3

class DeploymentStatus(Enum):
    DEPLOYED = "deployed"
    ROLLBACK = "rollback"
    FAILED = "failed"
    IN_PROGRESS = "in_progress"

@dataclass
class Version:
    version: str
    service: str
    deployed_at: str
    status: DeploymentStatus
    message: str
    git_commit: Optional[str] = None
    author: Optional[str] = None
    compliance_score: Optional[int] = None
    health_status: Optional[str] = None
    rollback_from: Optional[str] = None
    duration_seconds: Optional[int] = None

class EnhancedVersionSystem:
    def __init__(self, db_path: str = "version_history.db"):
        self.db_path = db_path
        self._init_database()
        
    def _init_database(self):
        """Initialize SQLite database for version tracking"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS version_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                version TEXT NOT NULL,
                service TEXT NOT NULL,
                deployed_at TEXT NOT NULL,
                status TEXT NOT NULL,
                message TEXT,
                git_commit TEXT,
                author TEXT,
                compliance_score INTEGER,
                health_status TEXT,
                rollback_from TEXT,
                duration_seconds INTEGER,
                UNIQUE(version, service)
            )
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_service_deployed 
            ON version_history(service, deployed_at DESC)
        """)
        
        conn.commit()
        conn.close()
    
    def get_git_info(self) -> Tuple[str, str]:
        """Get current git commit hash and author"""
        try:
            commit = subprocess.run(
                ['git', 'rev-parse', 'HEAD'],
                capture_output=True, text=True
            ).stdout.strip()[:7]
            
            author = subprocess.run(
                ['git', 'log', '-1', '--pretty=format:%an'],
                capture_output=True, text=True
            ).stdout.strip()
            
            return commit, author
        except:
            return "unknown", "unknown"
    
    def record_deployment(self, 
                         version: str,
                         service: str,
                         message: str,
                         compliance_score: int = None,
                         duration_seconds: int = None) -> Version:
        """Record a new deployment"""
        commit, author = self.get_git_info()
        
        deployment = Version(
            version=version,
            service=service,
            deployed_at=datetime.utcnow().isoformat() + 'Z',
            status=DeploymentStatus.DEPLOYED,
            message=message,
            git_commit=commit,
            author=author,
            compliance_score=compliance_score,
            health_status="healthy",
            duration_seconds=duration_seconds
        )
        
        self._save_version(deployment)
        return deployment
    
    def record_rollback(self,
                       service: str,
                       rollback_to: str,
                       rollback_from: str,
                       reason: str,
                       duration_seconds: int = None) -> Version:
        """Record a rollback event"""
        rollback = Version(
            version=rollback_to,
            service=service,
            deployed_at=datetime.utcnow().isoformat() + 'Z',
            status=DeploymentStatus.ROLLBACK,
            message=f"Rollback: {reason}",
            rollback_from=rollback_from,
            health_status="recovering",
            duration_seconds=duration_seconds
        )
        
        self._save_version(rollback)
        return rollback
    
    def record_failure(self,
                      version: str,
                      service: str,
                      reason: str) -> Version:
        """Record a deployment failure"""
        failure = Version(
            version=version,
            service=service,
            deployed_at=datetime.utcnow().isoformat() + 'Z',
            status=DeploymentStatus.FAILED,
            message=f"Failed: {reason}",
            health_status="failed"
        )
        
        self._save_version(failure)
        return failure
    
    def _save_version(self, version: Version):
        """Save version to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT OR REPLACE INTO version_history 
                (version, service, deployed_at, status, message, git_commit, 
                 author, compliance_score, health_status, rollback_from, duration_seconds)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                version.version,
                version.service,
                version.deployed_at,
                version.status.value,
                version.message,
                version.git_commit,
                version.author,
                version.compliance_score,
                version.health_status,
                version.rollback_from,
                version.duration_seconds
            ))
            
            conn.commit()
        finally:
            conn.close()
    
    def get_current_version(self, service: str) -> Optional[Version]:
        """Get the current deployed version for a service"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                SELECT * FROM version_history
                WHERE service = ? AND status IN ('deployed', 'rollback')
                ORDER BY deployed_at DESC
                LIMIT 1
            """, (service,))
            
            row = cursor.fetchone()
            if row:
                return self._row_to_version(row)
            return None
        finally:
            conn.close()
    
    def get_previous_stable_version(self, service: str) -> Optional[Version]:
        """Get the previous stable version for rollback"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Get all deployed versions, skip the current one
            cursor.execute("""
                SELECT * FROM version_history
                WHERE service = ? AND status = 'deployed'
                ORDER BY deployed_at DESC
                LIMIT 2
            """, (service,))
            
            rows = cursor.fetchall()
            if len(rows) >= 2:
                return self._row_to_version(rows[1])
            elif len(rows) == 1:
                return self._row_to_version(rows[0])
            return None
        finally:
            conn.close()
    
    def get_version_history(self, service: str, limit: int = 10) -> List[Version]:
        """Get version history for a service"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                SELECT * FROM version_history
                WHERE service = ?
                ORDER BY deployed_at DESC
                LIMIT ?
            """, (service, limit))
            
            rows = cursor.fetchall()
            return [self._row_to_version(row) for row in rows]
        finally:
            conn.close()
    
    def get_deployment_stats(self, service: str, days: int = 30) -> Dict:
        """Get deployment statistics for a service"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Calculate date threshold
            threshold = datetime.utcnow().replace(microsecond=0)
            threshold = threshold.replace(day=threshold.day - days)
            threshold_str = threshold.isoformat() + 'Z'
            
            # Total deployments
            cursor.execute("""
                SELECT COUNT(*) FROM version_history
                WHERE service = ? AND deployed_at >= ?
            """, (service, threshold_str))
            total = cursor.fetchone()[0]
            
            # Successful deployments
            cursor.execute("""
                SELECT COUNT(*) FROM version_history
                WHERE service = ? AND deployed_at >= ? AND status = 'deployed'
            """, (service, threshold_str))
            successful = cursor.fetchone()[0]
            
            # Rollbacks
            cursor.execute("""
                SELECT COUNT(*) FROM version_history
                WHERE service = ? AND deployed_at >= ? AND status = 'rollback'
            """, (service, threshold_str))
            rollbacks = cursor.fetchone()[0]
            
            # Failures
            cursor.execute("""
                SELECT COUNT(*) FROM version_history
                WHERE service = ? AND deployed_at >= ? AND status = 'failed'
            """, (service, threshold_str))
            failures = cursor.fetchone()[0]
            
            # Average compliance score
            cursor.execute("""
                SELECT AVG(compliance_score) FROM version_history
                WHERE service = ? AND deployed_at >= ? AND compliance_score IS NOT NULL
            """, (service, threshold_str))
            avg_compliance = cursor.fetchone()[0] or 0
            
            return {
                "service": service,
                "period_days": days,
                "total_deployments": total,
                "successful": successful,
                "rollbacks": rollbacks,
                "failures": failures,
                "success_rate": round(successful / total * 100, 2) if total > 0 else 0,
                "average_compliance_score": round(avg_compliance, 2)
            }
        finally:
            conn.close()
    
    def _row_to_version(self, row) -> Version:
        """Convert database row to Version object"""
        return Version(
            version=row[1],
            service=row[2],
            deployed_at=row[3],
            status=DeploymentStatus(row[4]),
            message=row[5],
            git_commit=row[6],
            author=row[7],
            compliance_score=row[8],
            health_status=row[9],
            rollback_from=row[10],
            duration_seconds=row[11]
        )
    
    def export_to_json(self, service: str = None) -> str:
        """Export version history to JSON"""
        if service:
            versions = self.get_version_history(service, limit=100)
        else:
            # Get all versions
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM version_history ORDER BY deployed_at DESC")
            rows = cursor.fetchall()
            conn.close()
            versions = [self._row_to_version(row) for row in rows]
        
        return json.dumps({
            "exported_at": datetime.utcnow().isoformat() + 'Z',
            "versions": [asdict(v) for v in versions]
        }, indent=2, default=str)
    
    def detect_rollback_pattern(self, service: str) -> Optional[str]:
        """Detect if service is in a rollback pattern"""
        history = self.get_version_history(service, limit=5)
        
        if len(history) < 2:
            return None
        
        # Check if last deployment was a rollback
        if history[0].status == DeploymentStatus.ROLLBACK:
            return f"Service rolled back from {history[0].rollback_from} to {history[0].version}"
        
        # Check for repeated rollbacks
        rollback_count = sum(1 for v in history[:5] if v.status == DeploymentStatus.ROLLBACK)
        if rollback_count >= 2:
            return f"Multiple rollbacks detected ({rollback_count} in last 5 deployments)"
        
        return None

# CLI Interface
def main():
    """Command line interface for version system"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Enhanced Version Management System")
    parser.add_argument("action", choices=["record", "current", "history", "stats", "export"],
                       help="Action to perform")
    parser.add_argument("--service", required=True, help="Service name")
    parser.add_argument("--version", help="Version number")
    parser.add_argument("--message", help="Deployment message")
    parser.add_argument("--status", choices=["deployed", "rollback", "failed"],
                       default="deployed", help="Deployment status")
    parser.add_argument("--compliance-score", type=int, help="Constitutional compliance score")
    parser.add_argument("--limit", type=int, default=10, help="Number of history entries")
    parser.add_argument("--days", type=int, default=30, help="Days for statistics")
    
    args = parser.parse_args()
    
    vs = EnhancedVersionSystem()
    
    if args.action == "record":
        if args.status == "deployed":
            version = vs.record_deployment(
                version=args.version,
                service=args.service,
                message=args.message or "Manual deployment",
                compliance_score=args.compliance_score
            )
            print(f"✅ Recorded deployment: {version.version}")
        elif args.status == "rollback":
            # For rollback, version is what we're rolling back TO
            current = vs.get_current_version(args.service)
            version = vs.record_rollback(
                service=args.service,
                rollback_to=args.version,
                rollback_from=current.version if current else "unknown",
                reason=args.message or "Manual rollback"
            )
            print(f"🔄 Recorded rollback to: {version.version}")
        elif args.status == "failed":
            version = vs.record_failure(
                version=args.version,
                service=args.service,
                reason=args.message or "Deployment failed"
            )
            print(f"❌ Recorded failure: {version.version}")
    
    elif args.action == "current":
        current = vs.get_current_version(args.service)
        if current:
            print(f"Current version for {args.service}:")
            print(f"  Version: {current.version}")
            print(f"  Status: {current.status.value}")
            print(f"  Deployed: {current.deployed_at}")
            print(f"  Message: {current.message}")
            if current.compliance_score:
                print(f"  Compliance: {current.compliance_score}%")
        else:
            print(f"No version found for {args.service}")
    
    elif args.action == "history":
        history = vs.get_version_history(args.service, limit=args.limit)
        print(f"Version history for {args.service}:")
        print("-" * 80)
        
        for v in history:
            status_emoji = {
                DeploymentStatus.DEPLOYED: "✅",
                DeploymentStatus.ROLLBACK: "🔄",
                DeploymentStatus.FAILED: "❌",
                DeploymentStatus.IN_PROGRESS: "⏳"
            }
            
            print(f"{status_emoji.get(v.status, '❓')} {v.version} - {v.deployed_at}")
            print(f"   {v.message}")
            if v.compliance_score:
                print(f"   Compliance: {v.compliance_score}%")
            print()
    
    elif args.action == "stats":
        stats = vs.get_deployment_stats(args.service, days=args.days)
        print(f"Deployment statistics for {args.service} (last {args.days} days):")
        print("-" * 60)
        print(f"Total deployments: {stats['total_deployments']}")
        print(f"Successful: {stats['successful']}")
        print(f"Rollbacks: {stats['rollbacks']}")
        print(f"Failures: {stats['failures']}")
        print(f"Success rate: {stats['success_rate']}%")
        print(f"Average compliance score: {stats['average_compliance_score']}%")
        
        # Check for rollback patterns
        pattern = vs.detect_rollback_pattern(args.service)
        if pattern:
            print(f"\n⚠️  Warning: {pattern}")
    
    elif args.action == "export":
        json_data = vs.export_to_json(args.service)
        print(json_data)

if __name__ == "__main__":
    main()