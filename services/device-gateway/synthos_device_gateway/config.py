"""Configuration management for Device Gateway"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Dict, List, Optional


class Settings(BaseSettings):
    """Device Gateway Settings"""

    # Application
    app_name: str = "Synthos Device Gateway"
    app_version: str = "0.1.0"
    environment: str = "development"
    device_debug: bool = True

    # Server
    host: str = "0.0.0.0"
    port: int = 8010
    workers: int = 1

    # Device Configuration
    max_connected_devices: int = 100
    device_timeout: int = 300  # 5 minutes
    connection_timeout: int = 30
    message_queue_size: int = 1000

    # Protocol Support
    enable_websocket: bool = True
    enable_mqtt: bool = True
    mqtt_broker_url: str = "mqtt://localhost:1883"
    websocket_port: int = 8011

    # Integration
    model_gateway_url: str = "http://localhost:8002"
    memory_engine_url: str = "http://localhost:8003"
    cognitive_engine_url: str = "http://localhost:8005"

    # Monitoring
    enable_metrics: bool = True
    enable_audit_logging: bool = True
    audit_log_path: str = "./logs/device_audit.log"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )