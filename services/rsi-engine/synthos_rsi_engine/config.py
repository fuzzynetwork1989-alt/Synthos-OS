"""Configuration management for RSI Engine"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Dict, List, Optional


class Settings(BaseSettings):
    """RSI Engine Settings"""

    # Application
    app_name: str = "Synthos RSI Engine"
    app_version: str = "0.1.0"
    environment: str = "development"
    rsi_debug: bool = True

    # Server
    host: str = "0.0.0.0"
    port: int = 8004
    workers: int = 1

    # RSI Configuration
    max_improvement_cycles: int = 10
    max_mutations_per_cycle: int = 5
    auto_approve_low_risk: bool = False
    emergency_stop_enabled: bool = True

    # Safety Configuration
    gdi_threshold: float = 0.5
    constitutional_enforcement: bool = True
    invariant_preservation: bool = True

    # Resource Budgets
    max_compute_per_cycle: int = 3600  # 1 hour
    max_token_budget: int = 100000
    max_files_changed: int = 10

    # Monitoring
    enable_metrics: bool = True
    enable_audit_logging: bool = True
    audit_log_path: str = "./logs/rsi_audit.log"

    # Integration
    model_gateway_url: str = "http://localhost:8000"
    memory_engine_url: str = "http://localhost:8002"
    evaluation_engine_url: str = "http://localhost:8005"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    def get_rsi_config(self) -> Dict:
        """Get RSI-specific configuration"""
        return {
            "baseline_goals": [
                "Improve system capabilities without goal misalignment",
                "Maintain safety and security constraints",
                "Preserve human oversight and control",
                "Ensure system stability and performance",
            ],
            "gatekeeper": {
                "max_diff_size": 10000,
                "max_files_changed": self.max_files_changed,
                "gdi_threshold": self.gdi_threshold,
                "quality_threshold": 0.8,
            },
            "mutation": {
                "max_mutations_per_cycle": self.max_mutations_per_cycle,
                "risk_threshold": "medium",
                "allowed_mutation_types": [
                    "prompt_optimization",
                    "configuration_update",
                    "code_refactoring",
                ],
            },
            "benchmark": {
                "performance_threshold": 0.8,
                "regression_threshold": 0.1,
                "timeout": 300,
            },
            "resource_budgets": {
                "max_cycles": self.max_improvement_cycles,
                "max_mutations_per_cycle": self.max_mutations_per_cycle,
                "max_compute_per_cycle": self.max_compute_per_cycle,
            },
        }
