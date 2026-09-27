"""Configuration for Cognitive Engine"""

from pydantic_settings import BaseSettings
from typing import List, Optional


class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    app_name: str = "Synthos Cognitive Engine"
    app_version: str = "0.1.0"
    environment: str = "development"
    debug: bool = True
    
    # Server
    host: str = "0.0.0.0"
    port: int = 8005
    workers: int = 1
    
    # Model Gateway Integration
    model_gateway_url: str = "http://localhost:8002"
    memory_engine_url: str = "http://localhost:8003"
    
    # Reasoning Configuration
    max_reasoning_steps: int = 10
    reasoning_timeout: int = 60
    enable_chain_of_thought: bool = True
    enable_tree_of_thoughts: bool = False
    
    # Planning Configuration
    max_planning_depth: int = 5
    planning_horizon: int = 10
    enable_backtracking: bool = True
    
    # Context Management
    max_context_length: int = 4096
    context_window: int = 8192
    
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
        
        if not self.model_gateway_url:
            warnings.append("Model Gateway URL not configured")
        
        if not self.memory_engine_url:
            warnings.append("Memory Engine URL not configured")
        
        return warnings


settings = Settings()