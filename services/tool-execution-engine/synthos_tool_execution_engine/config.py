"""Configuration for Tool Execution Engine"""

from pydantic_settings import BaseSettings
from typing import List, Optional


class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    app_name: str = "Synthos Tool Execution Engine"
    app_version: str = "0.1.0"
    environment: str = "development"
    debug: bool = True
    
    # Server
    host: str = "0.0.0.0"
    port: int = 8006
    workers: int = 1
    
    # Sandbox Configuration
    enable_sandbox: bool = True
    sandbox_timeout: int = 300  # 5 minutes
    max_memory_mb: int = 512
    max_cpu_time: int = 60  # seconds
    
    # Tool Registry
    tool_registry_path: str = "./tools/registry.json"
    allow_custom_tools: bool = False
    
    # Security
    enable_security_checks: bool = True
    allowed_domains: List[str] = ["localhost", "127.0.0.1"]
    blocked_commands: List[str] = ["rm -rf", "format", "del /q"]
    
    # Monitoring
    enable_metrics: bool = True
    enable_tracing: bool = True
    
    # CORS
    cors_origins: List[str] = ["http://localhost:3000", "http://localhost:5173"]
    cors_allow_credentials: bool = True
    cors_allow_methods: List[str] = ["*"]
    cors_allow_headers: List[str] = ["*"]
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
    
    def validate_configuration(self) -> List[str]:
        """Validate configuration and return warnings"""
        warnings = []
        
        if not self.enable_sandbox:
            warnings.append("Sandbox is disabled - tools will run without isolation")
        
        return warnings


settings = Settings()