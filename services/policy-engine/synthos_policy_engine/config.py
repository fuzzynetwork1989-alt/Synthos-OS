"""Configuration management for Policy Engine"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Dict, List, Optional


class Settings(BaseSettings):
    """Policy Engine Settings"""

    # Application
    app_name: str = "Synthos Policy Engine"
    app_version: str = "0.1.0"
    environment: str = "development"
    policy_debug: bool = True

    # Server
    host: str = "0.0.0.0"
    port: int = 8008
    workers: int = 1

    # Policy Configuration
    policy_enforcement_mode: str = "strict"  # strict, permissive, audit_only
    policy_cache_ttl: int = 300  # 5 minutes
    max_policy_depth: int = 10

    # Integration
    model_gateway_url: str = "http://localhost:8002"
    memory_engine_url: str = "http://localhost:8003"
    rsi_engine_url: str = "http://localhost:8001"

    # Monitoring
    enable_metrics: bool = True
    enable_audit_logging: bool = True
    audit_log_path: str = "./logs/policy_audit.log"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )