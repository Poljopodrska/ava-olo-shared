"""
Version Management Dashboard
Web interface for version tracking and deployment monitoring

Run with: python version_dashboard.py
Access at: http://localhost:8081
"""

from fastapi import FastAPI, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import uvicorn
from pathlib import Path
from version_manager import ConstitutionalVersionManager
from typing import Dict, Any
import json

app = FastAPI(title="Constitutional Version Dashboard")

# Setup templates directory
templates_dir = Path(__file__).parent.parent / "templates"
templates_dir.mkdir(exist_ok=True)

templates = Jinja2Templates(directory=str(templates_dir))

# Initialize version manager
version_manager = ConstitutionalVersionManager()

@app.get("/", response_class=HTMLResponse)
async def dashboard_home(request: Request):
    """Main dashboard page"""
    
    # Get current status
    current_version = version_manager.get_current_version()
    version_history = version_manager.get_version_history(10)
    comparison = await version_manager.compare_versions()
    deployments = version_manager.get_deployment_status()
    
    return templates.TemplateResponse("version_dashboard.html", {
        "request": request,
        "current_version": current_version,
        "version_history": version_history,
        "comparison": comparison,
        "deployments": deployments,
        "all_synced": comparison['all_synced']
    })

@app.get("/api/status")
async def get_status():
    """API endpoint for current status"""
    current_version = version_manager.get_current_version()
    comparison = await version_manager.compare_versions()
    
    return {
        "current_version": current_version,
        "aws_status": comparison['version_comparison'],
        "all_synced": comparison['all_synced'],
        "timestamp": comparison.get('timestamp')
    }

@app.get("/api/versions")
async def get_versions(limit: int = 20):
    """API endpoint for version history"""
    versions = version_manager.get_version_history(limit)
    return [
        {
            "version": v.version_number,
            "description": v.description,
            "timestamp": v.timestamp,
            "constitutional_compliance": v.constitutional_compliance,
            "compliance_score": v.compliance_score,
            "deployment_status": v.deployment_status,
            "files_changed": len(v.files_changed)
        }
        for v in versions
    ]

@app.post("/api/create-version")
async def create_version(request_data: Dict[str, Any]):
    """API endpoint to create new version"""
    try:
        version = await version_manager.create_version(
            description=request_data["description"],
            increment_type=request_data.get("increment_type", "patch")
        )
        
        return {
            "success": True,
            "version": version.version_number,
            "constitutional_compliance": version.constitutional_compliance,
            "compliance_score": version.compliance_score
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.get("/api/compliance-check")
async def compliance_check():
    """API endpoint for constitutional compliance check"""
    try:
        compliance = await version_manager.check_constitutional_compliance()
        return {
            "success": True,
            "compliance": compliance
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "constitutional-version-dashboard",
        "version": version_manager.get_current_version(),
        "constitutional_compliance": True
    }

if __name__ == "__main__":
    print("🏛️ Starting Constitutional Version Dashboard...")
    print("📊 Access dashboard at: http://localhost:8081")
    print("🔄 Auto-refresh every 30 seconds")
    uvicorn.run(app, host="0.0.0.0", port=8081)