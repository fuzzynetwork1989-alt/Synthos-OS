"""Configuration for Memory Engine"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    app_name: str = "Synthos Memory Engine"
    app_version: str = "0.1.0"
    environment: str = "development"
    memory_debug: bool = True
    
    # Server
    host: str = "0.0.0.0"
    port: int = 8003
    workers: int = 1
    
    # Database
    database_url: str = "sqlite+aiosqlite:///./synthos_memory.db"
    redis_url: str = "redis://localhost:6379"
    
    # Memory Configuration
    max_memory_size: int = 1000000  # Maximum memory entries
    memory_ttl: int = 86400  # 24 hours default TTL
    enable_persistence: bool = True
    enable_vector_search: bool = True
    
    # Vector Search
    vector_dimension: int = 1536
    similarity_threshold: float = 0.7
    max_results: int = 10
    
    # Caching
    enable_cache: bool = True
    cache_ttl: int = 3600  # 1 hour
    
    # Monitoring
    enable_metrics: bool = True
    enable_tracing: bool = True
    
    # CORS
    cors_origins: list = ["http://localhost:3000", "http://localhost:5173"]
    cors_allow_credentials: bool = True
    cors_allow_methods: list = ["*"]
    cors_allow_headers: list = ["*"]
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
    
    def validate_configuration(self) -> list:
        """Validate configuration and return warnings"""
        warnings = []
        
        if not self.database_url:
            warnings.append("Database URL not configured")
        
        if not self.redis_url:
            warnings.append("Redis URL not configured")
        
        return warnings


settings = Settings()