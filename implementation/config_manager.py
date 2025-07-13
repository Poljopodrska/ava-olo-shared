"""
Constitutional Configuration Manager
Centralized environment variable management

Ensures all services use the same configuration source
Constitutional compliance: Configuration over hardcoding
"""

import os
from pathlib import Path
from typing import Optional, Dict, Any
import logging
from dotenv import load_dotenv

logger = logging.getLogger(__name__)


class ConstitutionalConfig:
    """
    Centralized configuration manager
    Single source of truth for all environment variables
    """
    
    def __init__(self):
        self._load_environment()
        self._validate_required_vars()
    
    def _load_environment(self):
        """Load environment from root .env file"""
        # Find root .env file
        current_dir = Path(__file__).resolve()
        
        # Look for .env in parent directories up to root
        for parent in current_dir.parents:
            env_file = parent / '.env'
            if env_file.exists():
                load_dotenv(env_file, override=True)
                logger.info(f"Loaded environment from: {env_file}")
                self._env_file_path = env_file
                return
        
        # Fallback: look in current directory
        env_file = Path('.env')
        if env_file.exists():
            load_dotenv(env_file, override=True)
            logger.info(f"Loaded environment from: {env_file}")
            self._env_file_path = env_file
        else:
            logger.warning("No .env file found - using system environment only")
            self._env_file_path = None
    
    def _validate_required_vars(self):
        """Validate required environment variables"""
        required_vars = [
            'DB_HOST', 'DB_NAME', 'DB_USER', 'DB_PASSWORD',
            'OPENAI_API_KEY'
        ]
        
        missing_vars = []
        for var in required_vars:
            if not os.getenv(var):
                missing_vars.append(var)
        
        if missing_vars:
            logger.warning(f"Missing required environment variables: {missing_vars}")
            # Don't raise error to allow partial functionality
    
    # Database Configuration
    @property
    def db_host(self) -> str:
        return os.getenv('DB_HOST', 'localhost')
    
    @property
    def db_name(self) -> str:
        return os.getenv('DB_NAME', 'farmer_crm')
    
    @property
    def db_user(self) -> str:
        return os.getenv('DB_USER', 'postgres')
    
    @property
    def db_password(self) -> str:
        return os.getenv('DB_PASSWORD', '')
    
    @property
    def db_port(self) -> int:
        return int(os.getenv('DB_PORT', '5432'))
    
    @property
    def database_url(self) -> str:
        # Check if full URL is provided
        if os.getenv('DATABASE_URL'):
            return os.getenv('DATABASE_URL')
        # Otherwise construct from parts
        return f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"
    
    # LLM Configuration
    @property
    def openai_api_key(self) -> str:
        return os.getenv('OPENAI_API_KEY', '')
    
    @property
    def openai_model(self) -> str:
        return os.getenv('OPENAI_MODEL', 'gpt-4')
    
    @property
    def openai_temperature(self) -> float:
        return float(os.getenv('OPENAI_TEMPERATURE', '0.7'))
    
    # External APIs
    @property
    def perplexity_api_key(self) -> str:
        return os.getenv('PERPLEXITY_API_KEY', '')
    
    @property
    def pinecone_api_key(self) -> str:
        return os.getenv('PINECONE_API_KEY', '')
    
    @property
    def pinecone_env(self) -> str:
        return os.getenv('PINECONE_ENV', 'eu-west-1')
    
    @property
    def pinecone_host(self) -> str:
        return os.getenv('PINECONE_HOST', '')
    
    @property
    def pinecone_index_name(self) -> str:
        return os.getenv('PINECONE_INDEX_NAME', 'pinecone-crm-index')
    
    # Application Configuration
    @property
    def app_env(self) -> str:
        return os.getenv('APP_ENV', 'development')
    
    @property
    def log_level(self) -> str:
        return os.getenv('LOG_LEVEL', 'INFO')
    
    @property
    def is_production(self) -> bool:
        return self.app_env.lower() == 'production'
    
    # Localization (Amendment #13)
    @property
    def default_language(self) -> str:
        return os.getenv('DEFAULT_LANGUAGE', 'en')
    
    @property
    def supported_languages(self) -> list:
        return os.getenv('SUPPORTED_LANGUAGES', 'en').split(',')
    
    # Feature Flags
    @property
    def enable_llm_first(self) -> bool:
        return os.getenv('ENABLE_LLM_FIRST', 'true').lower() == 'true'
    
    @property
    def enable_country_localization(self) -> bool:
        return os.getenv('ENABLE_COUNTRY_LOCALIZATION', 'true').lower() == 'true'
    
    @property
    def enable_privacy_mode(self) -> bool:
        return os.getenv('ENABLE_PRIVACY_MODE', 'true').lower() == 'true'
    
    @property
    def enable_constitutional_checks(self) -> bool:
        return os.getenv('ENABLE_CONSTITUTIONAL_CHECKS', 'true').lower() == 'true'
    
    # Service Configuration
    @property
    def api_gateway_url(self) -> str:
        return os.getenv('API_GATEWAY_URL', 'http://localhost:8000')
    
    @property
    def api_gateway_port(self) -> int:
        return int(os.getenv('API_GATEWAY_PORT', '8000'))
    
    def get_config_dict(self) -> Dict[str, Any]:
        """Get all configuration as dictionary for debugging"""
        return {
            'database': {
                'host': self.db_host,
                'name': self.db_name,
                'user': self.db_user,
                'port': self.db_port,
                'url': self.database_url[:20] + '...' if self.database_url else None  # Hide password
            },
            'llm': {
                'model': self.openai_model,
                'temperature': self.openai_temperature,
                'api_key_set': bool(self.openai_api_key)
            },
            'app': {
                'env': self.app_env,
                'log_level': self.log_level,
                'is_production': self.is_production
            },
            'localization': {
                'default_language': self.default_language,
                'supported_languages': self.supported_languages
            },
            'features': {
                'llm_first': self.enable_llm_first,
                'country_localization': self.enable_country_localization,
                'privacy_mode': self.enable_privacy_mode,
                'constitutional_checks': self.enable_constitutional_checks
            },
            'env_file': str(self._env_file_path) if self._env_file_path else None
        }
    
    def validate_constitutional_compliance(self) -> Dict[str, bool]:
        """Validate configuration meets constitutional requirements"""
        return {
            'postgresql_only': 'postgresql' in self.database_url.lower(),
            'llm_configured': bool(self.openai_api_key),
            'privacy_enabled': self.enable_privacy_mode,
            'localization_ready': len(self.supported_languages) > 1,
            'production_ready': bool(self.db_host and self.db_password),
            'transparency_enabled': self.log_level in ['INFO', 'DEBUG']
        }


# Global configuration instance
config = ConstitutionalConfig()


# Convenience functions for backward compatibility
def get_database_url() -> str:
    """Get database URL for backward compatibility"""
    return config.database_url

def get_openai_api_key() -> str:
    """Get OpenAI API key for backward compatibility"""
    return config.openai_api_key

def get_config() -> ConstitutionalConfig:
    """Get configuration instance"""
    return config

def validate_config() -> bool:
    """Validate configuration is properly loaded"""
    compliance = config.validate_constitutional_compliance()
    all_valid = all(compliance.values())
    
    if not all_valid:
        logger.warning(f"Constitutional compliance issues: {compliance}")
    
    return all_valid


# Auto-validate on import
if __name__ != "__main__":
    if config.enable_constitutional_checks:
        validate_config()