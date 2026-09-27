"""RSI Coordinator - Main orchestration for recursive self-improvement"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum
import structlog

from ..safety.gatekeeper import Gatekeeper, GateResult
from ..safety.goal_drift_index import GoalDriftIndex
from ..safety.constitutional_constraints import ConstitutionalConstraints
from ..mutation.generator import MutationGenerator
from ..evaluation.benchmark_runner import BenchmarkRunner
from ..autonomous.meta_rsi import MetaRSI, ImprovementStrategy
from ..autonomous.continuous_rsi import ContinuousRSI

logger = structlog.get_logger(__name__)


class RSICycleStatus(Enum):
    """Status of an RSI improvement cycle"""
    PENDING = "pending"
    REFLECTING = "reflecting"
    GENERATING = "generating"
    TESTING = "testing"
    VALIDATING = "validating"
    APPROVED = "approved"
    REJECTED = "rejected"
    APPLIED = "applied"
    FAILED = "failed"


@dataclass
class RSICycle:
    """Single RSI improvement cycle"""
    cycle_id: str
    status: RSICycleStatus
    timestamp: str
    mutations_generated: int
    mutations_tested: int
    mutations_approved: int
    gdi_before: float
    gdi_after: float
    performance_delta: float
    gate_results: List[Dict]
    error_message: Optional[str] = None


class RSICoordinator:
    """
    Main coordinator for Recursive Self-Improvement
    
    Orchestrates the complete RSI cycle:
    1. Reflection & Analysis
    2. Mutation Generation
    3. Dry-Run Testing
    4. Safety Validation
    5. Governance & Approval
    6. Application & Monitoring
    """
    
    def __init__(self, config: Dict = None):
        """
        Initialize RSI Coordinator
        
        Args:
            config: Configuration for RSI coordinator
        """
        self.config = config or self._default_config()
        
        # Initialize safety components
        self.gatekeeper = Gatekeeper(self.config.get("gatekeeper", {}))
        self.constraints = ConstitutionalConstraints()
        
        # Initialize RSI components
        self.mutation_generator = MutationGenerator(self.config.get("mutation", {}))
        self.benchmark_runner = BenchmarkRunner(self.config.get("benchmark", {}))
        
        # Initialize autonomous components
        self.meta_rsi = MetaRSI(self.config.get("meta_rsi", {}))
        self.continuous_rsi: Optional[Any] = None  # Will be initialized later
        
        # GDI will be initialized with baseline goals
        self.gdi: Optional[GoalDriftIndex] = None
        
        # Cycle history
        self.cycle_history: List[RSICycle] = []
        self.current_cycle: Optional[RSICycle] = None
        
        # Resource budgets
        self.resource_budgets = self.config.get("resource_budgets", {
            "max_cycles": 10,
            "max_mutations_per_cycle": 5,
            "max_compute_per_cycle": 3600,  # 1 hour in seconds
        })
        
        # Current cycle count
        self.cycle_count = 0
        
        logger.info("RSI Coordinator initialized", config=self.config)
    
    def _default_config(self) -> Dict:
        """Default configuration for RSI coordinator"""
        return {
            "baseline_goals": [
                "Improve system capabilities without goal misalignment",
                "Maintain safety and security constraints",
                "Preserve human oversight and control",
                "Ensure system stability and performance",
            ],
            "gatekeeper": {},
            "mutation": {},
            "benchmark": {},
            "resource_budgets": {},
        }
    
    def initialize_gdi(self, baseline_goals: List[str]):
        """
        Initialize Goal Drift Index with baseline goals
        
        Args:
            baseline_goals: List of baseline goal statements
        """
        self.gdi = GoalDriftIndex(baseline_goals)
        self.gatekeeper.set_gdi(self.gdi)
        logger.info("GDI initialized", num_goals=len(baseline_goals))
    
    def start_improvement_cycle(
        self,
        trigger_reason: str,
        auto_approve: bool = False
    ) -> RSICycle:
        """
        Start a new RSI improvement cycle
        
        Args:
            trigger_reason: Reason for starting the cycle
            auto_approve: Whether to auto-approve low-risk changes
            
        Returns:
            RSICycle object representing the new cycle
        """
        # Check cycle budget
        if self.cycle_count >= self.resource_budgets["max_cycles"]:
            logger.warning("Maximum cycle limit reached", cycle_count=self.cycle_count)
            raise RuntimeError("Maximum cycle limit reached")
        
        # Create new cycle
        cycle_id = f"cycle_{self.cycle_count + 1}"
        self.current_cycle = RSICycle(
            cycle_id=cycle_id,
            status=RSICycleStatus.PENDING,
            timestamp=self._get_timestamp(),
            mutations_generated=0,
            mutations_tested=0,
            mutations_approved=0,
            gdi_before=0.0,
            gdi_after=0.0,
            performance_delta=0.0,
            gate_results=[],
        )
        
        logger.info(
            "Starting RSI improvement cycle",
            cycle_id=cycle_id,
            trigger_reason=trigger_reason,
            auto_approve=auto_approve
        )
        
        # Execute the cycle
        try:
            self._execute_cycle(trigger_reason, auto_approve)
        except Exception as e:
            logger.error("RSI cycle failed", cycle_id=cycle_id, error=str(e))
            self.current_cycle.status = RSICycleStatus.FAILED
            self.current_cycle.error_message = str(e)
        
        # Store cycle in history
        self.cycle_history.append(self.current_cycle)
        self.cycle_count += 1
        
        return self.current_cycle
    
    def _execute_cycle(self, trigger_reason: str, auto_approve: bool):
        """Execute the complete RSI cycle"""
        cycle = self.current_cycle
        
        # Phase 1: Reflection & Analysis
        cycle.status = RSICycleStatus.REFLECTING
        logger.info("Phase 1: Reflection & Analysis", cycle_id=cycle.cycle_id)
        
        analysis_results = self._perform_system_analysis()
        
        # Measure baseline GDI
        if self.gdi:
            baseline_gdi, _ = self.gdi.calculate_gdi(
                self.config["baseline_goals"],
                "",  # Current text placeholder
                {},  # Current structure placeholder
                []   # Current outputs placeholder
            )
            cycle.gdi_before = baseline_gdi
        
        # Phase 2: Mutation Generation
        cycle.status = RSICycleStatus.GENERATING
        logger.info("Phase 2: Mutation Generation", cycle_id=cycle.cycle_id)
        
        mutations = self.mutation_generator.generate_mutations(
            analysis_results,
            max_mutations=self.resource_budgets["max_mutations_per_cycle"]
        )
        cycle.mutations_generated = len(mutations)
        
        # Phase 3: Dry-Run Testing
        cycle.status = RSICycleStatus.TESTING
        logger.info("Phase 3: Dry-Run Testing", cycle_id=cycle.cycle_id)
        
        tested_mutations = []
        for mutation in mutations:
            test_result = self._test_mutation(mutation)
            if test_result["passed"]:
                tested_mutations.append(mutation)
        
        cycle.mutations_tested = len(tested_mutations)
        
        # Phase 4: Safety Validation
        cycle.status = RSICycleStatus.VALIDATING
        logger.info("Phase 4: Safety Validation", cycle_id=cycle.cycle_id)
        
        validated_mutations = []
        for mutation in tested_mutations:
            gate_result, layer_results = self.gatekeeper.check_mutation(
                mutation["text"],
                mutation["changed_files"],
                mutation["diff"],
                self.config["baseline_goals"],
                "",
                {},
                []
            )
            
            cycle.gate_results.append({
                "mutation_id": mutation["id"],
                "result": gate_result.value,
                "layer_results": [
                    {
                        "layer": r.layer_name,
                        "result": r.result.value,
                        "message": r.message
                    }
                    for r in layer_results
                ]
            })
            
            if gate_result in [GateResult.PASS, GateResult.WARNING]:
                if auto_approve or gate_result == GateResult.PASS:
                    validated_mutations.append(mutation)
        
        # Phase 5: Governance & Approval
        if validated_mutations:
            cycle.status = RSICycleStatus.APPROVED
            cycle.mutations_approved = len(validated_mutations)
            logger.info(
                "Mutations approved",
                cycle_id=cycle.cycle_id,
                approved_count=len(validated_mutations)
            )
            
            # Phase 6: Application & Monitoring
            cycle.status = RSICycleStatus.APPLIED
            logger.info("Phase 6: Application & Monitoring", cycle_id=cycle.cycle_id)
            
            for mutation in validated_mutations:
                self._apply_mutation(mutation)
            
            # Measure post-application GDI
            if self.gdi:
                post_gdi, _ = self.gdi.calculate_gdi(
                    self.config["baseline_goals"],
                    "",
                    {},
                    []
                )
                cycle.gdi_after = post_gdi
            
            # Measure performance delta
            cycle.performance_delta = self._measure_performance_delta()
            
        else:
            cycle.status = RSICycleStatus.REJECTED
            logger.info("No mutations approved", cycle_id=cycle.cycle_id)
    
    def _perform_system_analysis(self) -> Dict:
        """Perform system self-analysis"""
        # Placeholder for system analysis
        # In production, this would:
        # - Analyze code architecture
        # - Profile performance
        # - Map dependencies
        # - Assess code quality
        
        return {
            "performance_bottlenecks": [],
            "code_quality_issues": [],
            "missing_capabilities": [],
            "optimization_opportunities": [],
        }
    
    def _test_mutation(self, mutation: Dict) -> Dict:
        """Test a mutation in sandbox"""
        # Placeholder for mutation testing
        # In production, this would:
        # - Execute mutation in sandbox
        # - Run test suite
        # - Measure performance
        # - Check for regressions
        
        return {
            "passed": True,
            "test_results": {},
            "performance_metrics": {},
        }
    
    def _apply_mutation(self, mutation: Dict):
        """Apply a mutation to the system"""
        # Placeholder for mutation application
        # In production, this would:
        # - Apply changes on new git branch
        # - Run full test suite
        # - Rollback on failure
        # - Update system state
        
        logger.info("Applying mutation", mutation_id=mutation["id"])
    
    def _measure_performance_delta(self) -> float:
        """Measure performance delta after mutation application"""
        # Placeholder for performance measurement
        # In production, this would run benchmarks and compare
        
        return 0.0
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.utcnow().isoformat()
    
    def get_cycle_status(self, cycle_id: str) -> Optional[RSICycle]:
        """Get status of a specific cycle"""
        for cycle in self.cycle_history:
            if cycle.cycle_id == cycle_id:
                return cycle
        return None
    
    def get_system_status(self) -> Dict:
        """Get overall RSI system status"""
        return {
            "current_cycle": self.current_cycle.cycle_id if self.current_cycle else None,
            "cycle_count": self.cycle_count,
            "total_mutations_generated": sum(c.mutations_generated for c in self.cycle_history),
            "total_mutations_approved": sum(c.mutations_approved for c in self.cycle_history),
            "resource_budgets": self.resource_budgets,
            "gdi_status": "active" if self.gdi else "inactive",
        }
    
    def emergency_stop(self):
        """Emergency stop - halt all RSI activity"""
        logger.warning("Emergency stop triggered")
        
        # Stop continuous RSI if active
        if self.continuous_rsi:
            self.continuous_rsi.trigger_emergency_stop()
        
        if self.current_cycle:
            self.current_cycle.status = RSICycleStatus.FAILED
            self.current_cycle.error_message = "Emergency stop triggered"
    
    def enable_autonomous_mode(self, safety_override_key: Optional[str] = None) -> bool:
        """
        Enable autonomous improvement mode
        
        Args:
            safety_override_key: Optional safety override key for enhanced autonomy
            
        Returns:
            True if autonomous mode enabled successfully
        """
        if not self.continuous_rsi:
            self.continuous_rsi = ContinuousRSI(self, self.meta_rsi, self.config.get("continuous_rsi", {}))
        
        return self.continuous_rsi.enable_autonomous_mode(safety_override_key)
    
    def disable_autonomous_mode(self):
        """Disable autonomous improvement mode"""
        if self.continuous_rsi:
            self.continuous_rsi.disable_autonomous_mode()
    
    def get_meta_rsi_metrics(self) -> Dict:
        """Get Meta-RSI performance metrics"""
        return self.meta_rsi.get_meta_metrics()
    
    def get_autonomous_status(self) -> Dict:
        """Get autonomous mode status"""
        if self.continuous_rsi:
            return self.continuous_rsi.get_autonomous_status()
        return {
            "autonomous_enabled": False,
            "continuous_rsi_initialized": False,
        }
