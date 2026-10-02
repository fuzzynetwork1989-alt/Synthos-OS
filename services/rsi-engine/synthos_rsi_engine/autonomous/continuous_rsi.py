"""Continuous Autonomous RSI - Self-Triggering Improvement Cycles"""

from typing import Dict, List, Optional, Callable, Any
from dataclasses import dataclass
from enum import Enum
import structlog
from datetime import datetime, timedelta
import asyncio
import threading
import time

from .meta_rsi import MetaRSI, ImprovementStrategy

logger = structlog.get_logger(__name__)


class TriggerCondition(Enum):
    """Conditions that can trigger autonomous improvement"""
    PERFORMANCE_DEGRADATION = "performance_degradation"
    TIME_BASED = "time_based"
    ERROR_RATE_THRESHOLD = "error_rate_threshold"
    RESOURCE_PRESSURE = "resource_pressure"
    OPPORTUNITY_DETECTED = "opportunity_detected"
    MANUAL_REQUEST = "manual_request"


@dataclass
class TriggerEvent:
    """Event that triggers an improvement cycle"""
    condition: TriggerCondition
    severity: str  # "low", "medium", "high"
    context: Dict
    timestamp: datetime
    auto_approve: bool


class ContinuousRSI:
    """
    Continuous Autonomous RSI System
    
    Features:
    1. Self-triggering improvement cycles based on conditions
    2. Adaptive resource budgeting
    3. Continuous monitoring and anomaly detection
    4. Smart triggering to avoid unnecessary cycles
    5. Emergency safety overrides
    """
    
    def __init__(self, coordinator: Any, meta_rsi: MetaRSI, config: Dict = None):
        """
        Initialize Continuous RSI
        
        Args:
            coordinator: RSI Coordinator instance
            meta_rsi: Meta-RSI instance
            config: Configuration for continuous RSI
        """
        self.coordinator = coordinator
        self.meta_rsi = meta_rsi
        self.config = config or self._default_config()
        
        # Autonomous mode control
        self.autonomous_enabled = False
        self.emergency_stop_triggered = False
        
        # Monitoring state
        self.performance_baseline: Dict[str, Any] = {}
        self.current_metrics: Dict[str, Any] = {}
        self.trigger_history: List[TriggerEvent] = []
        
        # Adaptive resource budgeting
        self.resource_multipliers = {
            "conservative": 0.5,
            "balanced": 1.0,
            "aggressive": 1.5,
        }
        
        # Thread for continuous monitoring
        self.monitoring_thread: Optional[threading.Thread] = None
        self.stop_monitoring = False
        
        # Callbacks for triggers
        self.trigger_callbacks: List[Callable] = []
        
        logger.info("Continuous RSI initialized", autonomous=self.autonomous_enabled)
    
    def _default_config(self) -> Dict:
        """Default configuration for continuous RSI"""
        return {
            "monitoring_interval_seconds": 60,
            "performance_degradation_threshold": 0.15,  # 15% degradation
            "error_rate_threshold": 0.05,  # 5% error rate
            "min_time_between_cycles": 3600,  # 1 hour minimum
            "max_cycles_per_day": 10,
            "auto_approve_threshold": "low",  # Auto-approve low-risk changes
            "resource_pressure_threshold": 0.8,  # 80% resource usage
        }
    
    def enable_autonomous_mode(self, safety_override_key: Optional[str] = None):
        """
        Enable autonomous improvement mode
        
        Args:
            safety_override_key: Optional safety override key
        """
        if self.emergency_stop_triggered:
            logger.error("Cannot enable autonomous mode - emergency stop triggered")
            return False
        
        if safety_override_key and not self._verify_safety_override(safety_override_key):
            logger.error("Invalid safety override key")
            return False
        
        self.autonomous_enabled = True
        self._establish_performance_baseline()
        
        # Start monitoring thread
        self.monitoring_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
        self.monitoring_thread.start()
        
        logger.info("Autonomous mode enabled", safety_override=bool(safety_override_key))
        return True
    
    def disable_autonomous_mode(self):
        """Disable autonomous improvement mode"""
        self.autonomous_enabled = False
        self.stop_monitoring = True
        
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=5)
        
        logger.info("Autonomous mode disabled")
    
    def trigger_emergency_stop(self):
        """Trigger emergency stop - halts all autonomous activity"""
        self.emergency_stop_triggered = True
        self.autonomous_enabled = False
        self.stop_monitoring = True
        
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=5)
        
        logger.critical("Emergency stop triggered")
    
    def clear_emergency_stop(self, safety_override_key: str):
        """
        Clear emergency stop with safety override
        
        Args:
            safety_override_key: Safety override key
        """
        if not self._verify_safety_override(safety_override_key):
            logger.error("Invalid safety override key")
            return False
        
        self.emergency_stop_triggered = False
        logger.info("Emergency stop cleared")
        return True
    
    def manual_trigger(self, reason: str, context: Dict = None) -> bool:
        """
        Manually trigger an improvement cycle
        
        Args:
            reason: Reason for manual trigger
            context: Additional context
            
        Returns:
            True if trigger successful
        """
        if self.emergency_stop_triggered:
            logger.error("Cannot trigger - emergency stop active")
            return False
        
        if not self._can_trigger_cycle():
            logger.warning("Cannot trigger - cooling down or limit reached")
            return False
        
        event = TriggerEvent(
            condition=TriggerCondition.MANUAL_REQUEST,
            severity="medium",
            context=context or {},
            timestamp=datetime.now(),
            auto_approve=False
        )
        
        return self._execute_triggered_cycle(event)
    
    def _monitoring_loop(self):
        """Main monitoring loop for autonomous triggering"""
        while not self.stop_monitoring:
            try:
                if self.autonomous_enabled and not self.emergency_stop_triggered:
                    self._check_trigger_conditions()
                
                time.sleep(self.config["monitoring_interval_seconds"])
            except Exception as e:
                logger.error("Error in monitoring loop", error=str(e))
    
    def _check_trigger_conditions(self):
        """Check if any trigger conditions are met"""
        if not self._can_trigger_cycle():
            return
        
        current_metrics = self._collect_current_metrics()
        self.current_metrics = current_metrics
        
        # Check performance degradation
        if self._check_performance_degradation(current_metrics):
            self._trigger_cycle(
                TriggerCondition.PERFORMANCE_DEGRADATION,
                current_metrics
            )
            return
        
        # Check error rate
        if self._check_error_rate(current_metrics):
            self._trigger_cycle(
                TriggerCondition.ERROR_RATE_THRESHOLD,
                current_metrics
            )
            return
        
        # Check resource pressure
        if self._check_resource_pressure(current_metrics):
            self._trigger_cycle(
                TriggerCondition.RESOURCE_PRESSURE,
                current_metrics
            )
            return
        
        # Check for improvement opportunities
        if self._check_improvement_opportunities(current_metrics):
            self._trigger_cycle(
                TriggerCondition.OPPORTUNITY_DETECTED,
                current_metrics
            )
            return
    
    def _check_performance_degradation(self, metrics: Dict) -> bool:
        """Check if performance has degraded"""
        if not self.performance_baseline:
            return False
        
        threshold = self.config["performance_degradation_threshold"]
        
        for metric, baseline_value in self.performance_baseline.items():
            current_value = metrics.get(metric, baseline_value)
            if baseline_value > 0:
                degradation = (baseline_value - current_value) / baseline_value
                if degradation > threshold:
                    logger.warning(
                        "Performance degradation detected",
                        metric=metric,
                        degradation=degradation
                    )
                    return True
        
        return False
    
    def _check_error_rate(self, metrics: Dict) -> bool:
        """Check if error rate exceeds threshold"""
        error_rate = metrics.get("error_rate", 0.0)
        threshold = self.config["error_rate_threshold"]
        
        if error_rate > threshold:
            logger.warning("Error rate threshold exceeded", error_rate=error_rate)
            return True
        
        return False
    
    def _check_resource_pressure(self, metrics: Dict) -> bool:
        """Check if resource pressure is high"""
        cpu_usage = metrics.get("cpu_usage", 0.0)
        memory_usage = metrics.get("memory_usage", 0.0)
        threshold = self.config["resource_pressure_threshold"]
        
        if cpu_usage > threshold or memory_usage > threshold:
            logger.warning("Resource pressure detected", cpu=cpu_usage, memory=memory_usage)
            return True
        
        return False
    
    def _check_improvement_opportunities(self, metrics: Dict) -> bool:
        """Check for improvement opportunities using Meta-RSI"""
        # Get strategy recommendation
        strategy = self.meta_rsi.recommend_strategy()
        
        # If strategy suggests aggressive improvement and conditions are favorable
        if strategy == ImprovementStrategy.AGGRESSIVE:
            # Check if we have recent successful patterns
            if len(self.meta_rsi.dna.genes) > 5:
                avg_success = sum(g.success_rate for g in self.meta_rsi.dna.genes) / len(self.meta_rsi.dna.genes)
                if avg_success > 0.8:
                    logger.info("Improvement opportunity detected", strategy=strategy.value)
                    return True
        
        return False
    
    def _trigger_cycle(self, condition: TriggerCondition, context: Dict):
        """Trigger an improvement cycle"""
        severity = self._assess_trigger_severity(condition, context)
        auto_approve = severity == "low" and self.config["auto_approve_threshold"] == "low"
        
        event = TriggerEvent(
            condition=condition,
            severity=severity,
            context=context,
            timestamp=datetime.now(),
            auto_approve=auto_approve
        )
        
        self.trigger_history.append(event)
        self._execute_triggered_cycle(event)
    
    def _execute_triggered_cycle(self, event: TriggerEvent) -> bool:
        """Execute a triggered improvement cycle"""
        try:
            # Get recommended strategy
            strategy = self.meta_rsi.recommend_strategy()
            
            # Adjust resource budgets based on strategy
            self._adjust_resource_budgets(strategy)
            
            # Get mutation suggestions from Meta-RSI
            suggestions = self.meta_rsi.get_mutation_suggestions(event.context)
            
            # Start improvement cycle
            cycle = self.coordinator.start_improvement_cycle(
                trigger_reason=f"Autonomous trigger: {event.condition.value}",
                auto_approve=event.auto_approve
            )
            
            # Analyze cycle performance
            cycle_data = {
                "cycle_id": cycle.cycle_id,
                "status": cycle.status.value,
                "mutations_tested": cycle.mutations_tested,
                "mutations_approved": cycle.mutations_approved,
                "gdi_before": cycle.gdi_before,
                "gdi_after": cycle.gdi_after,
                "performance_delta": cycle.performance_delta,
                "strategy": strategy.value,
                "approved_mutations": suggestions,  # Placeholder
            }
            
            # Update Meta-RSI with cycle results
            self.meta_rsi.analyze_cycle_performance(cycle_data)
            self.meta_rsi.extract_genes(cycle_data)
            
            # Evolve DNA periodically
            if len(self.meta_rsi.performance_history) % 5 == 0:
                self.meta_rsi.evolve_dna()
            
            logger.info(
                "Autonomous cycle completed",
                cycle_id=cycle.cycle_id,
                status=cycle.status.value
            )
            
            # Notify callbacks
            for callback in self.trigger_callbacks:
                try:
                    callback(event, cycle)
                except Exception as e:
                    logger.error("Trigger callback error", error=str(e))
            
            return True
            
        except Exception as e:
            logger.error("Failed to execute triggered cycle", error=str(e))
            return False
    
    def _can_trigger_cycle(self) -> bool:
        """Check if a cycle can be triggered"""
        if not self.autonomous_enabled:
            return False
        
        if self.emergency_stop_triggered:
            return False
        
        # Check minimum time between cycles
        if self.trigger_history:
            last_trigger = self.trigger_history[-1]
            min_interval = timedelta(seconds=self.config["min_time_between_cycles"])
            if datetime.now() - last_trigger.timestamp < min_interval:
                return False
        
        # Check max cycles per day
        day_ago = datetime.now() - timedelta(days=1)
        recent_triggers = [
            t for t in self.trigger_history
            if t.timestamp > day_ago
        ]
        if len(recent_triggers) >= self.config["max_cycles_per_day"]:
            return False
        
        return True
    
    def _assess_trigger_severity(self, condition: TriggerCondition, context: Dict) -> str:
        """Assess severity of trigger condition"""
        if condition == TriggerCondition.ERROR_RATE_THRESHOLD:
            return "high"
        elif condition == TriggerCondition.PERFORMANCE_DEGRADATION:
            degradation = context.get("degradation", 0)
            if degradation > 0.3:
                return "high"
            elif degradation > 0.15:
                return "medium"
            return "low"
        elif condition == TriggerCondition.RESOURCE_PRESSURE:
            return "medium"
        else:
            return "low"
    
    def _adjust_resource_budgets(self, strategy: ImprovementStrategy):
        """Adjust resource budgets based on strategy"""
        multiplier = self.resource_multipliers.get(strategy.value, 1.0)
        
        self.coordinator.resource_budgets = {
            "max_cycles": int(10 * multiplier),
            "max_mutations_per_cycle": int(5 * multiplier),
            "max_compute_per_cycle": int(3600 * multiplier),
        }
        
        logger.info("Resource budgets adjusted", strategy=strategy.value, multiplier=multiplier)
    
    def _establish_performance_baseline(self):
        """Establish performance baseline for monitoring"""
        self.performance_baseline = self._collect_current_metrics()
        logger.info("Performance baseline established", baseline=self.performance_baseline)
    
    def _collect_current_metrics(self) -> Dict:
        """Collect current system metrics"""
        # Placeholder - in production, this would collect real metrics
        return {
            "response_time": 100.0,  # ms
            "error_rate": 0.01,  # 1%
            "cpu_usage": 0.3,  # 30%
            "memory_usage": 0.4,  # 40%
            "throughput": 1000.0,  # requests/sec
        }
    
    def _verify_safety_override(self, key: str) -> bool:
        """Verify safety override key"""
        # In production, this would use proper cryptographic verification
        expected_key = self.config.get("safety_override_key", "default-override-key")
        return key == expected_key
    
    def add_trigger_callback(self, callback: Callable):
        """Add callback for trigger events"""
        self.trigger_callbacks.append(callback)
    
    def get_autonomous_status(self) -> Dict:
        """Get current autonomous status"""
        return {
            "autonomous_enabled": self.autonomous_enabled,
            "emergency_stop_triggered": self.emergency_stop_triggered,
            "monitoring_active": self.monitoring_thread and self.monitoring_thread.is_alive(),
            "trigger_history_count": len(self.trigger_history),
            "performance_baseline": self.performance_baseline,
            "current_metrics": self.current_metrics,
            "resource_budgets": self.coordinator.resource_budgets,
        }