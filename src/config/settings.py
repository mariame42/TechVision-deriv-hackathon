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
    
    # LLM settings
    llm_model: str = "gemini-pro"
    llm_provider: str = "vertex-ai"  # or "openai", etc.
    llm_api_key: Optional[str] = None
    
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
            llm_model=os.getenv("LLM_MODEL", "gemini-pro"),
            llm_provider=os.getenv("LLM_PROVIDER", "vertex-ai"),
            llm_api_key=os.getenv("LLM_API_KEY"),
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

