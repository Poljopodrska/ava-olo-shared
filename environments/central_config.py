#!/usr/bin/env python3
"""
Central Environment Configuration for AVA OLO
THIS IS THE ONLY PLACE FOR ENVIRONMENT VARIABLES - NO EXCEPTIONS!

All services MUST import from this module for environment variables.
No hardcoding allowed anywhere else in the codebase.
"""
import os
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)

class CentralConfig:
    """Single source of truth for ALL environment variables"""
    
    # ========== DATABASE CONFIGURATION ==========
    # These are used by both services
    DB_HOST = os.getenv('DB_HOST', 'farmer-crm-production.cifgmm0mqg5q.us-east-1.rds.amazonaws.com')
    DB_NAME = os.getenv('DB_NAME', 'farmer_crm')
    DB_USER = os.getenv('DB_USER', 'postgres')
    DB_PASSWORD = os.getenv('DB_PASSWORD')  # From AWS Secrets Manager
    DB_PORT = os.getenv('DB_PORT', '5432')
    
    # ========== API KEYS ==========
    # IMPORTANT: These ARE set in AWS ECS task definitions!
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')  # We have this in AWS!
    OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY')  # Weather service
    GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')  # For field drawing
    PERPLEXITY_API_KEY = os.getenv('PERPLEXITY_API_KEY')  # External search
    TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')  # WhatsApp integration
    
    # ========== AWS CONFIGURATION ==========
    AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')
    AWS_ACCOUNT_ID = os.getenv('AWS_ACCOUNT_ID', '127679825789')
    ECS_CLUSTER = os.getenv('ECS_CLUSTER', 'ava-olo-production')
    
    # ========== APPLICATION SETTINGS ==========
    APP_VERSION = os.getenv('APP_VERSION', '3.5.0')
    ENVIRONMENT = os.getenv('ENVIRONMENT', 'production')
    SERVICE_NAME = os.getenv('SERVICE_NAME', 'unknown')
    PORT = int(os.getenv('PORT', '8080'))
    
    # ========== FEATURE FLAGS ==========
    ENABLE_WEATHER = os.getenv('ENABLE_WEATHER', 'true').lower() == 'true'
    ENABLE_PERPLEXITY = os.getenv('ENABLE_PERPLEXITY', 'true').lower() == 'true'
    ENABLE_WHATSAPP = os.getenv('ENABLE_WHATSAPP', 'true').lower() == 'true'
    ENABLE_DEBUG = os.getenv('ENABLE_DEBUG', 'false').lower() == 'true'
    
    # ========== URLS AND ENDPOINTS ==========
    # Service URLs
    AGRICULTURAL_SERVICE_URL = os.getenv(
        'AGRICULTURAL_SERVICE_URL',
        'http://ava-olo-farmers-alb-82735690.us-east-1.elb.amazonaws.com'
    )
    MONITORING_SERVICE_URL = os.getenv(
        'MONITORING_SERVICE_URL', 
        'http://ava-olo-alb-65365776.us-east-1.elb.amazonaws.com'
    )
    
    # ========== SECURITY ==========
    SECRET_KEY = os.getenv('SECRET_KEY', 'default-secret-key-change-in-production')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', SECRET_KEY)
    DEV_ACCESS_KEY = os.getenv('DEV_ACCESS_KEY', 'ava-dev-2025-secure-key')
    
    @classmethod
    def get_database_url(cls) -> Optional[str]:
        """Construct database URL from components"""
        if not cls.DB_PASSWORD:
            logger.warning("Database password not set!")
            return None
            
        # Handle password encoding for special characters
        from urllib.parse import quote_plus
        password_encoded = quote_plus(cls.DB_PASSWORD)
        
        return f"postgresql://{cls.DB_USER}:{password_encoded}@{cls.DB_HOST}:{cls.DB_PORT}/{cls.DB_NAME}"
    
    @classmethod
    def validate_required_keys(cls) -> tuple[bool, list[str]]:
        """Ensure all required environment variables are present"""
        missing = []
        
        # Critical keys that MUST be present
        required_keys = {
            'DB_PASSWORD': cls.DB_PASSWORD,
            'OPENAI_API_KEY': cls.OPENAI_API_KEY,
        }
        
        # Optional but important keys
        important_keys = {
            'GOOGLE_MAPS_API_KEY': cls.GOOGLE_MAPS_API_KEY,
            'OPENWEATHER_API_KEY': cls.OPENWEATHER_API_KEY,
            'PERPLEXITY_API_KEY': cls.PERPLEXITY_API_KEY,
        }
        
        # Check required keys
        for key_name, key_value in required_keys.items():
            if not key_value:
                missing.append(f"{key_name} (REQUIRED)")
        
        # Check important keys and warn if missing
        for key_name, key_value in important_keys.items():
            if not key_value:
                logger.warning(f"{key_name} not set - some features may not work")
        
        if missing:
            logger.error(f"⚠️ Missing required environment variables: {missing}")
            logger.info("BUT these ARE set in AWS ECS task definition!")
            logger.info("Check: 1) Import from CentralConfig, 2) ECS deployment")
            logger.info("AWS CLI check: aws ecs describe-task-definition --task-definition <your-task>")
        
        return len(missing) == 0, missing
    
    @classmethod
    def debug_environment(cls):
        """Help Claude Code debug environment issues"""
        print("=" * 60)
        print("🔍 ENVIRONMENT VARIABLES DEBUG")
        print("=" * 60)
        print("🚨 REMINDER: All variables ARE set in AWS ECS task definitions!")
        print("")
        
        # Check critical variables
        print("📊 Variable Status:")
        variables = {
            'DB_HOST': cls.DB_HOST,
            'DB_NAME': cls.DB_NAME, 
            'DB_USER': cls.DB_USER,
            'DB_PASSWORD': cls.DB_PASSWORD,
            'OPENAI_API_KEY': cls.OPENAI_API_KEY,
            'OPENWEATHER_API_KEY': cls.OPENWEATHER_API_KEY,
            'GOOGLE_MAPS_API_KEY': cls.GOOGLE_MAPS_API_KEY,
            'APP_VERSION': cls.APP_VERSION,
            'ENVIRONMENT': cls.ENVIRONMENT
        }
        
        for var_name, var_value in variables.items():
            if var_name in ['DB_PASSWORD', 'OPENAI_API_KEY', 'OPENWEATHER_API_KEY', 'GOOGLE_MAPS_API_KEY']:
                # Mask sensitive values
                status = "✅ SET (hidden)" if var_value else "❌ NOT SET"
            else:
                status = f"✅ {var_value}" if var_value else "❌ NOT SET"
            
            print(f"  {var_name:20} : {status}")
        
        print("")
        print("🔧 If any variables show ❌ NOT SET:")
        print("1. Check you're importing from CentralConfig:")
        print("   from ava_olo_shared.environments.central_config import CentralConfig")
        print("2. Variables ARE in AWS ECS - verify with:")
        print("   aws ecs describe-task-definition --task-definition ava-olo-agricultural-task")
        print("3. For local dev, create .env file in project root")
        print("4. Verify ECS service is running latest task definition")
        print("")
        print("💡 Most common issue: Wrong import path or not using CentralConfig")
        print("=" * 60)
    
    @classmethod
    def get_all_config(cls) -> Dict[str, Any]:
        """Get all configuration as dictionary"""
        return {
            # Database
            'database': {
                'host': cls.DB_HOST,
                'name': cls.DB_NAME,
                'user': cls.DB_USER,
                'password_set': bool(cls.DB_PASSWORD),
                'port': cls.DB_PORT,
                'url': cls.get_database_url() is not None
            },
            # API Keys (masked for security)
            'api_keys': {
                'openai': cls._mask_key(cls.OPENAI_API_KEY),
                'google_maps': cls._mask_key(cls.GOOGLE_MAPS_API_KEY),
                'openweather': cls._mask_key(cls.OPENWEATHER_API_KEY),
                'perplexity': cls._mask_key(cls.PERPLEXITY_API_KEY),
                'twilio': cls._mask_key(cls.TWILIO_AUTH_TOKEN),
            },
            # Application
            'application': {
                'version': cls.APP_VERSION,
                'environment': cls.ENVIRONMENT,
                'service': cls.SERVICE_NAME,
                'port': cls.PORT
            },
            # Feature Flags
            'features': {
                'weather': cls.ENABLE_WEATHER,
                'perplexity': cls.ENABLE_PERPLEXITY,
                'whatsapp': cls.ENABLE_WHATSAPP,
                'debug': cls.ENABLE_DEBUG
            },
            # URLs
            'urls': {
                'agricultural_service': cls.AGRICULTURAL_SERVICE_URL,
                'monitoring_service': cls.MONITORING_SERVICE_URL
            }
        }
    
    @staticmethod
    def _mask_key(key: Optional[str]) -> str:
        """Mask API key for display"""
        if not key:
            return "NOT_SET"
        if len(key) < 8:
            return "INVALID"
        return f"{key[:4]}...{key[-4:]}"
    
    @classmethod
    def print_config_status(cls):
        """Print configuration status for debugging"""
        print("=" * 60)
        print("AVA OLO CENTRAL CONFIGURATION STATUS")
        print("=" * 60)
        
        is_valid, missing = cls.validate_required_keys()
        
        if is_valid:
            print("✅ All required environment variables are set")
        else:
            print("❌ Missing required variables:")
            for var in missing:
                print(f"   - {var}")
        
        print("\nConfiguration Summary:")
        config = cls.get_all_config()
        
        import json
        print(json.dumps(config, indent=2))
        print("=" * 60)


# Convenience function for other modules
def get_config() -> CentralConfig:
    """Get central configuration instance"""
    return CentralConfig


# Validate on import
if __name__ == "__main__":
    CentralConfig.print_config_status()