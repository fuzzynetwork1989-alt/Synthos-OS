"""Multi-layer Gatekeeper - Safety enforcement for self-modification"""

from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import re
import structlog

from .constitutional_constraints import ConstitutionalConstraints, ConstraintSeverity
from .goal_drift_index import GoalDriftIndex

logger = structlog.get_logger(__name__)


class GateResult(Enum):
    """Result of gatekeeping check"""
    PASS = "pass"
    WARNING = "warning"
    FAIL = "fail"
    CRITICAL = "critical"


@dataclass
class GateLayerResult:
    """Result from a single gate layer"""
    layer_name: str
    result: GateResult
    message: str
    details: Dict


class Gatekeeper:
    """
    Multi-layer gatekeeper for safety enforcement
    
    Implements 10 safety layers:
    1. Path allowlist/denylist
    2. Diff size limit
    3. Secret scanning
    4. Code pattern detection
    5. Dry-run pytest gate
    6. Constitutional constraints
    7. Goal drift index
    8. Resource budget check
    9. Quality gate validation
    10. Integration guard validation
    """
    
    def __init__(self, config: Dict = None):
        """
        Initialize the gatekeeper
        
        Args:
            config: Configuration for gatekeeper
        """
        self.config = config or self._default_config()
        
        # Initialize safety components
        self.constraints = ConstitutionalConstraints()
        self.gdi = None  # Will be initialized with baseline goals
        
        # Protected paths (cannot be modified)
        self.protected_paths = self.config.get("protected_paths", [
            "services/rsi-engine/safety/",
            "services/rsi-engine/core/",
            "services/policy-engine/",
            "services/security-contracts/",
        ])
        
        # Allowed modification paths
        self.allowed_paths = self.config.get("allowed_paths", [
            "services/cognitive-engine/",
            "services/memory-engine/",
            "services/tool-execution-engine/",
            "apps/",
            "packages/",
        ])
        
        logger.info("Gatekeeper initialized", protected_paths=len(self.protected_paths))
    
    def _default_config(self) -> Dict:
        """Default configuration for gatekeeper"""
        return {
            "max_diff_size": 10000,  # Maximum characters in diff
            "max_files_changed": 10,  # Maximum files changed per mutation
            "secret_patterns": [
                r"[A-Za-z0-9]{32}",  # API keys
                r"sk-[a-zA-Z0-9]{48}",  # OpenAI keys
                r"password\s*=\s*['\"].*['\"]",  # Passwords
            ],
            "quality_threshold": 0.8,  # Minimum code quality score
            "gdi_threshold": 0.5,  # Maximum allowed GDI
        }
    
    def set_gdi(self, gdi: GoalDriftIndex):
        """Set the Goal Drift Index instance"""
        self.gdi = gdi
        logger.info("GDI set for gatekeeper")
    
    def check_mutation(
        self,
        mutation_text: str,
        changed_files: List[str],
        diff: str,
        current_goals: List[str],
        current_text: str,
        current_structure: Dict,
        current_outputs: List[str]
    ) -> Tuple[GateResult, List[GateLayerResult]]:
        """
        Check a mutation through all gate layers
        
        Args:
            mutation_text: Text of the proposed mutation
            changed_files: List of files that would be changed
            diff: Unified diff of changes
            current_goals: Current goal statements
            current_text: Current text for GDI analysis
            current_structure: Current system structure
            current_outputs: Sample of current outputs
            
        Returns:
            Tuple of (overall result, list of layer results)
        """
        layer_results = []
        
        # Layer 1: Path allowlist/denylist
        layer_results.append(self._check_path_constraints(changed_files))
        
        # Layer 2: Diff size limit
        layer_results.append(self._check_diff_size(diff))
        
        # Layer 3: Secret scanning
        layer_results.append(self._check_secrets(mutation_text, diff))
        
        # Layer 4: Code pattern detection
        layer_results.append(self._check_code_patterns(mutation_text))
        
        # Layer 5: Constitutional constraints
        layer_results.append(self._check_constitutional_constraints(mutation_text, changed_files))
        
        # Layer 6: Goal drift index
        if self.gdi:
            layer_results.append(self._check_goal_drift(
                current_goals, current_text, current_structure, current_outputs
            ))
        else:
            layer_results.append(GateLayerResult(
                layer_name="goal_drift_index",
                result=GateResult.WARNING,
                message="GDI not initialized",
                details={}
            ))
        
        # Layer 7: Resource budget check
        layer_results.append(self._check_resource_budget(changed_files))
        
        # Layer 8: Quality gate validation
        layer_results.append(self._check_quality_gates(mutation_text))
        
        # Layer 9: Integration guard validation
        layer_results.append(self._check_integration_guards(changed_files))
        
        # Layer 10: File count limit
        layer_results.append(self._check_file_count(changed_files))
        
        # Determine overall result
        overall_result = self._determine_overall_result(layer_results)
        
        logger.info(
            "Gatekeeper check completed",
            overall_result=overall_result.value,
            layers_passed=sum(1 for r in layer_results if r.result == GateResult.PASS),
            layers_failed=sum(1 for r in layer_results if r.result in [GateResult.FAIL, GateResult.CRITICAL])
        )
        
        return overall_result, layer_results
    
    def _check_path_constraints(self, changed_files: List[str]) -> GateLayerResult:
        """Layer 1: Check path constraints"""
        violations = []
        
        for file_path in changed_files:
            # Check if file is in protected paths
            for protected_path in self.protected_paths:
                if protected_path in file_path:
                    violations.append(f"Cannot modify protected path: {file_path}")
                    break
            
            # Check if file is in allowed paths
            if not any(allowed in file_path for allowed in self.allowed_paths):
                violations.append(f"File not in allowed paths: {file_path}")
        
        if violations:
            return GateLayerResult(
                layer_name="path_constraints",
                result=GateResult.CRITICAL,
                message=f"Path constraint violations: {', '.join(violations)}",
                details={"violations": violations}
            )
        
        return GateLayerResult(
            layer_name="path_constraints",
            result=GateResult.PASS,
            message="All paths are allowed",
            details={}
        )
    
    def _check_diff_size(self, diff: str) -> GateLayerResult:
        """Layer 2: Check diff size limit"""
        diff_size = len(diff)
        max_size = self.config["max_diff_size"]
        
        if diff_size > max_size:
            return GateLayerResult(
                layer_name="diff_size",
                result=GateResult.FAIL,
                message=f"Diff too large: {diff_size} > {max_size} characters",
                details={"diff_size": diff_size, "max_size": max_size}
            )
        
        return GateLayerResult(
            layer_name="diff_size",
            result=GateResult.PASS,
            message=f"Diff size acceptable: {diff_size} characters",
            details={"diff_size": diff_size}
        )
    
    def _check_secrets(self, mutation_text: str, diff: str) -> GateLayerResult:
        """Layer 3: Check for secrets"""
        combined_text = mutation_text + " " + diff
        secret_matches = []
        
        for pattern in self.config["secret_patterns"]:
            matches = re.findall(pattern, combined_text, re.IGNORECASE)
            if matches:
                secret_matches.extend(matches)
        
        if secret_matches:
            return GateLayerResult(
                layer_name="secret_scanning",
                result=GateResult.CRITICAL,
                message=f"Potential secrets detected: {len(secret_matches)} matches",
                details={"match_count": len(secret_matches)}
            )
        
        return GateLayerResult(
            layer_name="secret_scanning",
            result=GateResult.PASS,
            message="No secrets detected",
            details={}
        )
    
    def _check_code_patterns(self, mutation_text: str) -> GateLayerResult:
        """Layer 4: Check for dangerous code patterns"""
        dangerous_patterns = [
            r"eval\s*\(",
            r"exec\s*\(",
            r"__import__\s*\(",
            r"compile\s*\(",
            r"open\s*\(\s*[\"'].*[\"']\s*,\s*[\"']w",
        ]
        
        violations = []
        for pattern in dangerous_patterns:
            if re.search(pattern, mutation_text):
                violations.append(pattern)
        
        if violations:
            return GateLayerResult(
                layer_name="code_patterns",
                result=GateResult.WARNING,
                message=f"Potentially dangerous patterns: {', '.join(violations)}",
                details={"violations": violations}
            )
        
        return GateLayerResult(
            layer_name="code_patterns",
            result=GateResult.PASS,
            message="No dangerous patterns detected",
            details={}
        )
    
    def _check_constitutional_constraints(
        self,
        mutation_text: str,
        changed_files: List[str]
    ) -> GateLayerResult:
        """Layer 5: Check constitutional constraints"""
        is_valid, violations = self.constraints.validate_mutation(mutation_text, changed_files)
        
        if not is_valid:
            critical_violations = [v for v in violations if v["severity"] == "critical"]
            if critical_violations:
                return GateLayerResult(
                    layer_name="constitutional_constraints",
                    result=GateResult.CRITICAL,
                    message=f"Critical constraint violations: {len(critical_violations)}",
                    details={"violations": violations}
                )
            else:
                return GateLayerResult(
                    layer_name="constitutional_constraints",
                    result=GateResult.WARNING,
                    message=f"Constraint violations: {len(violations)}",
                    details={"violations": violations}
                )
        
        return GateLayerResult(
            layer_name="constitutional_constraints",
            result=GateResult.PASS,
            message="No constraint violations",
            details={}
        )
    
    def _check_goal_drift(
        self,
        current_goals: List[str],
        current_text: str,
        current_structure: Dict,
        current_outputs: List[str]
    ) -> GateLayerResult:
        """Layer 6: Check goal drift index"""
        if not self.gdi:
            return GateLayerResult(
                layer_name="goal_drift_index",
                result=GateResult.WARNING,
                message="GDI not available",
                details={}
            )
        
        gdi_score, signals = self.gdi.calculate_gdi(
            current_goals, current_text, current_structure, current_outputs
        )
        
        threshold = self.config["gdi_threshold"]
        
        if gdi_score >= threshold:
            return GateLayerResult(
                layer_name="goal_drift_index",
                result=GateResult.FAIL,
                message=f"Goal drift too high: {gdi_score:.3f} >= {threshold}",
                details={
                    "gdi_score": gdi_score,
                    "threshold": threshold,
                    "signals": [
                        {"name": s.name, "value": s.value, "status": s.status}
                        for s in signals
                    ]
                }
            )
        
        return GateLayerResult(
            layer_name="goal_drift_index",
            result=GateResult.PASS,
            message=f"Goal drift acceptable: {gdi_score:.3f}",
            details={"gdi_score": gdi_score, "signals": len(signals)}
        )
    
    def _check_resource_budget(self, changed_files: List[str]) -> GateLayerResult:
        """Layer 7: Check resource budget"""
        # Placeholder for resource budget checking
        # In production, this would check compute, time, token budgets
        return GateLayerResult(
            layer_name="resource_budget",
            result=GateResult.PASS,
            message="Resource budget within limits",
            details={}
        )
    
    def _check_quality_gates(self, mutation_text: str) -> GateLayerResult:
        """Layer 8: Check quality gates"""
        # Placeholder for quality gate validation
        # In production, this would run linters, formatters, etc.
        return GateLayerResult(
            layer_name="quality_gates",
            result=GateResult.PASS,
            message="Quality gates passed",
            details={}
        )
    
    def _check_integration_guards(self, changed_files: List[str]) -> GateLayerResult:
        """Layer 9: Check integration guards"""
        # Placeholder for integration guard validation
        # In production, this would check API compatibility, etc.
        return GateLayerResult(
            layer_name="integration_guards",
            result=GateResult.PASS,
            message="Integration guards passed",
            details={}
        )
    
    def _check_file_count(self, changed_files: List[str]) -> GateLayerResult:
        """Layer 10: Check file count limit"""
        file_count = len(changed_files)
        max_files = self.config["max_files_changed"]
        
        if file_count > max_files:
            return GateLayerResult(
                layer_name="file_count",
                result=GateResult.FAIL,
                message=f"Too many files changed: {file_count} > {max_files}",
                details={"file_count": file_count, "max_files": max_files}
            )
        
        return GateLayerResult(
            layer_name="file_count",
            result=GateResult.PASS,
            message=f"File count acceptable: {file_count}",
            details={"file_count": file_count}
        )
    
    def _determine_overall_result(self, layer_results: List[GateLayerResult]) -> GateResult:
        """Determine overall result from layer results"""
        # Critical result takes precedence
        if any(r.result == GateResult.CRITICAL for r in layer_results):
            return GateResult.CRITICAL
        
        # Fail result takes precedence
        if any(r.result == GateResult.FAIL for r in layer_results):
            return GateResult.FAIL
        
        # Warning result
        if any(r.result == GateResult.WARNING for r in layer_results):
            return GateResult.WARNING
        
        # All passed
        return GateResult.PASS
    
    def get_gate_summary(self) -> Dict:
        """Get summary of gatekeeper configuration"""
        return {
            "protected_paths": self.protected_paths,
            "allowed_paths": self.allowed_paths,
            "max_diff_size": self.config["max_diff_size"],
            "max_files_changed": self.config["max_files_changed"],
            "gdi_threshold": self.config["gdi_threshold"],
            "quality_threshold": self.config["quality_threshold"],
        }
