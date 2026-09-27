"""Configuration management for Workflow Engine"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Dict, List, Optional


class Settings(BaseSettings):
    """Workflow Engine Settings"""

    # Application
    app_name: str = "Synthos Workflow Engine"
    app_version: str = "0.1.0"
    environment: str = "development"
    workflow_debug: bool = True

    # Server
    host: str = "0.0.0.0"
    port: int = 8007
    workers: int = 1

    # Workflow Configuration
    max_concurrent_workflows: int = 50
    max_workflow_steps: int = 100
    workflow_timeout: int = 3600  # 1 hour
    step_timeout: int = 300  # 5 minutes

    # Task Queue
    celery_broker_url: str = "redis://localhost:6379/1"
    celery_result_backend: str = "redis://localhost:6379/2"

    # Integration
    model_gateway_url: str = "http://localhost:8002"
    memory_engine_url: str = "http://localhost:8003"
    cognitive_engine_url: str = "http://localhost:8005"
    tool_execution_url: str = "http://localhost:8006"
    policy_engine_url: str = "http://localhost:8008"

    # Monitoring
    enable_metrics: bool = True
    enable_audit_logging: bool = True
    audit_log_path: str = "./logs/workflow_audit.log"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )