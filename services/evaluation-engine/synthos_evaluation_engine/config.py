"""Configuration management for Evaluation Engine"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Dict, List, Optional


class Settings(BaseSettings):
    """Evaluation Engine Settings"""

    # Application
    app_name: str = "Synthos Evaluation Engine"
    app_version: str = "0.1.0"
    environment: str = "development"
    evaluation_debug: bool = True

    # Server
    host: str = "0.0.0.0"
    port: int = 8009
    workers: int = 1

    # Evaluation Configuration
    max_concurrent_evaluations: int = 10
    evaluation_timeout: int = 1800  # 30 minutes
    benchmark_timeout: int = 3600  # 1 hour

    # Test Configuration
    test_parallel_workers: int = 4
    test_retry_attempts: int = 3
    test_coverage_threshold: float = 0.8

    # Integration
    model_gateway_url: str = "http://localhost:8002"
    memory_engine_url: str = "http://localhost:8003"
    rsi_engine_url: str = "http://localhost:8001"

    # Monitoring
    enable_metrics: bool = True
    enable_audit_logging: bool = True
    audit_log_path: str = "./logs/evaluation_audit.log"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )