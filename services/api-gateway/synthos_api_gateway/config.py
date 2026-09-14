"""Configuration management for API Gateway"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal


class Settings(BaseSettings):
    """Application settings"""

    # Application
    app_name: str = "Synthos-OS API Gateway"
    app_version: str = "0.1.0"
    environment: Literal["development", "staging", "production"] = "development"
    debug: bool = False

    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    workers: int = 1

    # CORS
    cors_origins: list[str] = ["http://localhost:3000", "http://localhost:5173"]
    cors_allow_credentials: bool = True
    cors_allow_methods: list[str] = ["*"]
    cors_allow_headers: list[str] = ["*"]

    # Database
    database_url: str = "sqlite:///./synthos.db"
    database_pool_size: int = 5
    database_max_overflow: int = 10

    # Redis
    redis_url: str = "redis://localhost:6379/0"
    redis_pool_size: int = 10

    # Security
    secret_key: str = "development-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7

    # Logging
    log_level: str = "INFO"
    log_format: str = "json"
    log_file: str | None = None

    # Health Checks
    health_check_interval: int = 30
    health_check_timeout: int = 5

    # Rate Limiting
    rate_limit_enabled: bool = True
    rate_limit_requests: int = 100
    rate_limit_period: int = 60

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    def validate_configuration(self) -> list[str]:
        """Validate configuration and return list of warnings"""
        warnings = []

        if self.environment == "production":
            if self.secret_key == "development-secret-key-change-in-production":
                warnings.append("WARNING: Using default secret key in production")
            if self.debug:
                warnings.append("WARNING: Debug mode enabled in production")
            if "localhost" in self.cors_origins:
                warnings.append("WARNING: localhost in CORS origins in production")

        return warnings


# Global settings instance
settings = Settings()
