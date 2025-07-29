#!/usr/bin/env python3
"""
Central Version Management for AVA OLO
Single source of truth for version across all services
"""
import os
from typing import Optional

class VersionManager:
    """Central version management for all services"""
    
    # Version should be set as environment variable or in deployment
    # NEVER hardcode versions in individual services
    CURRENT_VERSION = "3.5.29"  # This will be the deployed version
    
    @staticmethod
    def get_current_version() -> str:
        """Get current version from environment or fallback"""
        # Priority order:
        # 1. Environment variable
        # 2. Class constant (for deployment)
        # 3. Development fallback
        return os.getenv('APP_VERSION', VersionManager.CURRENT_VERSION)
    
    @staticmethod
    def get_badge_html(position: str = "top-right") -> str:
        """Returns HTML for version badge"""
        version = VersionManager.get_current_version()
        
        # Position styles
        positions = {
            "top-right": "top: 10px; right: 10px;",
            "top-left": "top: 10px; left: 10px;",
            "bottom-right": "bottom: 10px; right: 10px;",
            "bottom-left": "bottom: 10px; left: 10px;"
        }
        
        position_style = positions.get(position, positions["top-right"])
        
        return f'''
        <div id="version-badge" class="ava-version-badge" style="
            position: fixed;
            {position_style}
            background: #8B4513;
            color: white;
            padding: 5px 10px;
            border-radius: 5px;
            font-size: 12px;
            font-weight: bold;
            z-index: 9999;
            box-shadow: 0 2px 4px rgba(0,0,0,0.2);
            cursor: pointer;
            transition: all 0.3s ease;
        " onclick="this.style.opacity = this.style.opacity == '0.3' ? '1' : '0.3';" 
          title="Click to toggle opacity">
            v{version}
        </div>
        '''
    
    @staticmethod
    def get_badge_css() -> str:
        """Returns CSS for version badge"""
        return '''
        <style>
            .ava-version-badge {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            }
            .ava-version-badge:hover {
                transform: scale(1.05);
                background: #A0522D !important;
            }
        </style>
        '''
    
    @staticmethod
    def inject_into_html(html_content: str) -> str:
        """Inject version badge into any HTML content"""
        version_html = VersionManager.get_badge_html()
        version_css = VersionManager.get_badge_css()
        
        # Try to inject before </body>
        if '</body>' in html_content:
            return html_content.replace('</body>', f'{version_css}{version_html}</body>')
        # Otherwise inject at the end
        return html_content + version_css + version_html
    
    @staticmethod
    def get_version_info() -> dict:
        """Get detailed version information"""
        return {
            "version": VersionManager.get_current_version(),
            "environment": os.getenv('ENVIRONMENT', 'development'),
            "service": os.getenv('SERVICE_NAME', 'unknown'),
            "deployment_time": os.getenv('DEPLOYMENT_TIMESTAMP', 'unknown')
        }