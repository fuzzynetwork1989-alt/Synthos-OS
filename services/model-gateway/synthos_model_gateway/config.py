"""Configuration for Model Gateway"""

from pydantic_settings import BaseSettings
from typing import List, Optional


class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    app_name: str = "Synthos Model Gateway"
    app_version: str = "0.1.0"
    environment: str = "development"
    debug: bool = True
    
    # Server
    host: str = "0.0.0.0"
    port: int = 8002
    workers: int = 1
    
    # Model Providers
    ollama_base_url: str = "http://localhost:11434"
    lm_studio_base_url: str = "http://localhost:1234"
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    
    # Default Model Configuration
    default_provider: str = "ollama"
    default_model: str = "llama2"
    fallback_models: List[str] = ["llama2", "mistral", "neural-chat"]
    
    # Performance
    max_concurrent_requests: int = 10
    request_timeout: int = 120
    max_tokens: int = 4096
    temperature: float = 0.7
    
    # Caching
    enable_cache: bool = True
    cache_ttl: int = 3600  # 1 hour
    
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
        
        if not self.ollama_base_url:
            warnings.append("Ollama base URL not configured")
        
        if self.default_provider not in ["ollama", "lm_studio", "openai", "anthropic"]:
            warnings.append(f"Unknown default provider: {self.default_provider}")
        
        return warnings


settings = Settings()