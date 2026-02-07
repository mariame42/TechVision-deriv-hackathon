"""
Application settings and configuration.

Manages environment variables, feature flags, and BigQuery credentials.
"""

import os
from typing import Optional
from dataclasses import dataclass


@dataclass
class Settings:
    """
    Application settings loaded from environment variables.
    """
    # Feature flags
    use_mock_internal: bool = True
    use_mock_external: bool = True
    
    # BigQuery settings
    bigquery_project: Optional[str] = None
    bigquery_dataset: Optional[str] = None
    bigquery_credentials_path: Optional[str] = None
    
    # External API settings
    coingecko_api_key: Optional[str] = None
    bloomberg_api_key: Optional[str] = None
    
    # PostgreSQL settings
    postgres_host: str = "localhost"
    postgres_database: str = "trading_db"
    postgres_user: str = "postgres"
    postgres_password: Optional[str] = None
    postgres_port: str = "5432"
    
    # LLM settings
    llm_model: str = "openai/gpt-3.5-turbo"  # Default for OpenRouter (use format: provider/model)
    llm_provider: str = "openrouter"  # or "vertex-ai", "openai", etc.
    llm_api_key: Optional[str] = None
    openrouter_api_key: Optional[str] = None
    openrouter_base_url: str = "https://openrouter.ai/api/v1"
    
    @classmethod
    def from_env(cls) -> "Settings":
        """
        Load settings from environment variables.
        
        Returns:
            Settings instance
        """
        return cls(
            use_mock_internal=os.getenv("USE_MOCK_INTERNAL", "true").lower() == "true",
            use_mock_external=os.getenv("USE_MOCK_EXTERNAL", "true").lower() == "true",
            bigquery_project=os.getenv("BIGQUERY_PROJECT"),
            bigquery_dataset=os.getenv("BIGQUERY_DATASET"),
            bigquery_credentials_path=os.getenv("BIGQUERY_CREDENTIALS_PATH"),
            coingecko_api_key=os.getenv("COINGECKO_API_KEY"),
            bloomberg_api_key=os.getenv("BLOOMBERG_API_KEY"),
            postgres_host=os.getenv("POSTGRES_HOST", "localhost"),
            postgres_database=os.getenv("POSTGRES_DATABASE", "trading_db"),
            postgres_user=os.getenv("POSTGRES_USER", "postgres"),
            postgres_password=os.getenv("POSTGRES_PASSWORD"),
            postgres_port=os.getenv("POSTGRES_PORT", "5432"),
            llm_model=os.getenv("LLM_MODEL", "openai/gpt-3.5-turbo"),
            llm_provider=os.getenv("LLM_PROVIDER", "openrouter"),
            llm_api_key=os.getenv("LLM_API_KEY"),
            openrouter_api_key=os.getenv("OPENROUTER_API_KEY"),
            openrouter_base_url=os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1"),
        )


# Global settings instance
_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """
    Get the global settings instance.
    
    Returns:
        Settings instance
    """
    global _settings
    if _settings is None:
        _settings = Settings.from_env()
    return _settings

