"""Database configuration"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal


class DatabaseSettings(BaseSettings):
    """Database settings"""

    # Database type
    database_type: Literal["sqlite", "postgresql"] = "sqlite"

    # SQLite settings
    sqlite_path: str = "./synthos.db"

    # PostgreSQL settings
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_user: str = "synthos"
    postgres_password: str = "synthos"
    postgres_database: str = "synthos"

    # Connection pool settings
    pool_size: int = 5
    max_overflow: int = 10
    pool_timeout: int = 30
    pool_recycle: int = 3600

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def database_url(self) -> str:
        """Get the database URL based on database type"""
        if self.database_type == "sqlite":
            return f"sqlite+aiosqlite:///{self.sqlite_path}"
        elif self.database_type == "postgresql":
            return (
                f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}"
                f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_database}"
            )
        else:
            raise ValueError(f"Unsupported database type: {self.database_type}")

    @property
    def sync_database_url(self) -> str:
        """Get the synchronous database URL for Alembic migrations"""
        if self.database_type == "sqlite":
            return f"sqlite:///{self.sqlite_path}"
        elif self.database_type == "postgresql":
            return (
                f"postgresql://{self.postgres_user}:{self.postgres_password}"
                f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_database}"
            )
        else:
            raise ValueError(f"Unsupported database type: {self.database_type}")


# Global settings instance
settings = DatabaseSettings()
