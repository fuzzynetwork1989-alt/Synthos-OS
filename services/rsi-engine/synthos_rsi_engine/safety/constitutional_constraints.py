"""Constitutional Constraints - 19 fundamental rules governing self-modification"""

from typing import Dict, List, Tuple
from dataclasses import dataclass
from enum import Enum
import re
import structlog

logger = structlog.get_logger(__name__)


class ConstraintSeverity(Enum):
    """Severity level of constraint violations"""
    CRITICAL = "critical"  # Violation must be blocked
    HIGH = "high"  # Violation requires human approval
    MEDIUM = "medium"  # Violation requires warning
    LOW = "low"  # Violation requires logging


@dataclass
class ConstraintRule:
    """Individual constitutional constraint rule"""
    id: str
    name: str
    description: str
    severity: ConstraintSeverity
    pattern: str  # Regex pattern to detect violations
    explanation: str


class ConstitutionalConstraints:
    """
    19 fundamental rules governing self-modification
    
    These constraints cannot be modified by the RSI system itself
    and are enforced before any self-modification is applied.
    """
    
    def __init__(self):
        """Initialize constitutional constraints"""
        self.constraints = self._initialize_constraints()
        logger.info("Constitutional constraints initialized", count=len(self.constraints))
    
    def _initialize_constraints(self) -> List[ConstraintRule]:
        """Initialize the 19 constitutional constraints"""
        return [
            ConstraintRule(
                id="CC001",
                name="No Self-Disable",
                description="Cannot disable safety mechanisms",
                severity=ConstraintSeverity.CRITICAL,
                pattern=r"(disable|remove|deactivate|bypass).*safety",
                explanation="Attempting to disable safety mechanisms is prohibited"
            ),
            ConstraintRule(
                id="CC002",
                name="No Budget Override",
                description="Cannot bypass resource limits",
                severity=ConstraintSeverity.CRITICAL,
                pattern=r"(override|bypass|disable|remove).*budget|limit",
                explanation="Resource budgeting cannot be bypassed"
            ),
            ConstraintRule(
                id="CC003",
                name="No Secret Exposure",
                description="Cannot expose secrets/API keys",
                severity=ConstraintSeverity.CRITICAL,
                pattern=r"(expose|reveal|print|log).*secret|api.?key|password",
                explanation="Secrets and API keys must remain protected"
            ),
            ConstraintRule(
                id="CC004",
                name="No Sandbox Escape",
                description="Cannot bypass sandboxing",
                severity=ConstraintSeverity.CRITICAL,
                pattern=r"(escape|bypass|disable).*sandbox",
                explanation="Sandbox boundaries must be maintained"
            ),
            ConstraintRule(
                id="CC005",
                name="No Test Disabling",
                description="Cannot disable or weaken tests",
                severity=ConstraintSeverity.CRITICAL,
                pattern=r"(disable|skip|weaken|remove).*test",
                explanation="Test suites cannot be disabled or weakened"
            ),
            ConstraintRule(
                id="CC006",
                name="No Monitoring Bypass",
                description="Cannot disable monitoring/logging",
                severity=ConstraintSeverity.CRITICAL,
                pattern=r"(disable|stop|bypass).*monitoring|logging",
                explanation="Monitoring and logging must remain active"
            ),
            ConstraintRule(
                id="CC007",
                name="No Human Override",
                description="Cannot bypass human approval requirements",
                severity=ConstraintSeverity.CRITICAL,
                pattern=r"(bypass|override|disable).*human.?approval",
                explanation="Human approval requirements cannot be bypassed"
            ),
            ConstraintRule(
                id="CC008",
                name="No Immutable Modification",
                description="Cannot modify immutable safety rails",
                severity=ConstraintSeverity.CRITICAL,
                pattern=r"(modify|change|edit).*immutable.*safety",
                explanation="Immutable safety components cannot be modified"
            ),
            ConstraintRule(
                id="CC009",
                name="No Privilege Escalation",
                description="Cannot increase own permissions",
                severity=ConstraintSeverity.HIGH,
                pattern=r"(increase|escalate|grant).*permission|privilege",
                explanation="Cannot escalate system permissions"
            ),
            ConstraintRule(
                id="CC010",
                name="No Resource Monopolization",
                description="Cannot monopolize system resources",
                severity=ConstraintSeverity.HIGH,
                pattern=r"(monopolize|consume.*all|hog).*resource",
                explanation="Cannot monopolize system resources"
            ),
            ConstraintRule(
                id="CC011",
                name="No External Dependency",
                description="Cannot add unvetted external dependencies",
                severity=ConstraintSeverity.HIGH,
                pattern=r"(add|install).*external.*dependency|package",
                explanation="External dependencies require vetting"
            ),
            ConstraintRule(
                id="CC012",
                name="No Network Expansion",
                description="Cannot expand network access beyond allowed",
                severity=ConstraintSeverity.HIGH,
                pattern=r"(expand|increase|add).*network.*access",
                explanation="Network access cannot be expanded"
            ),
            ConstraintRule(
                id="CC013",
                name="No Data Access",
                description="Cannot access unauthorized data",
                severity=ConstraintSeverity.HIGH,
                pattern=r"(access|read).*unauthorized.*data",
                explanation="Cannot access data without authorization"
            ),
            ConstraintRule(
                id="CC014",
                name="No User Data",
                description="Cannot access or modify user data without authorization",
                severity=ConstraintSeverity.CRITICAL,
                pattern=r"(access|modify).*user.*data",
                explanation="User data requires explicit authorization"
            ),
            ConstraintRule(
                id="CC015",
                name="No Production Impact",
                description="Cannot modify production without approval",
                severity=ConstraintSeverity.CRITICAL,
                pattern=r"(modify|change).*production",
                explanation="Production changes require approval"
            ),
            ConstraintRule(
                id="CC016",
                name="No Rollback Prevention",
                description="Cannot prevent rollback capability",
                severity=ConstraintSeverity.CRITICAL,
                pattern=r"(disable|prevent).*rollback",
                explanation="Rollback capability must be maintained"
            ),
            ConstraintRule(
                id="CC017",
                name="No Audit Tampering",
                description="Cannot modify audit trails",
                severity=ConstraintSeverity.CRITICAL,
                pattern=r"(modify|delete|alter).*audit",
                explanation="Audit trails must remain intact"
            ),
            ConstraintRule(
                id="CC018",
                name="No Goal Modification",
                description="Cannot modify primary goals",
                severity=ConstraintSeverity.CRITICAL,
                pattern=r"(modify|change).*primary.*goal",
                explanation="Primary goals cannot be modified"
            ),
            ConstraintRule(
                id="CC019",
                name="No Logic Modification",
                description="Cannot modify constitutional constraint logic",
                severity=ConstraintSeverity.CRITICAL,
                pattern=r"(modify|change).*constraint.*logic",
                explanation="Constitutional constraint logic is immutable"
            ),
        ]
    
    def validate_mutation(self, mutation_text: str, changed_files: List[str]) -> Tuple[bool, List[Dict]]:
        """
        Validate a mutation against constitutional constraints
        
        Args:
            mutation_text: Text of the proposed mutation
            changed_files: List of files that would be changed
            
        Returns:
            Tuple of (is_valid, list of violations)
        """
        violations = []
        
        # Check against all constraints
        for constraint in self.constraints:
            # Check in mutation text
            if re.search(constraint.pattern, mutation_text, re.IGNORECASE):
                violations.append({
                    "constraint_id": constraint.id,
                    "constraint_name": constraint.name,
                    "severity": constraint.severity.value,
                    "description": constraint.description,
                    "explanation": constraint.explanation,
                    "location": "mutation_text"
                })
        
        # Check in changed file paths
        for file_path in changed_files:
            for constraint in self.constraints:
                if re.search(constraint.pattern, file_path, re.IGNORECASE):
                    violations.append({
                        "constraint_id": constraint.id,
                        "constraint_name": constraint.name,
                        "severity": constraint.severity.value,
                        "description": constraint.description,
                        "explanation": constraint.explanation,
                        "location": f"file_path:{file_path}"
                    })
        
        # Determine validity based on violations
        critical_violations = [v for v in violations if v["severity"] == "critical"]
        is_valid = len(critical_violations) == 0
        
        if violations:
            logger.warning(
                "Constitutional constraint violations detected",
                violation_count=len(violations),
                critical_count=len(critical_violations),
                is_valid=is_valid
            )
        
        return is_valid, violations
    
    def get_constraint_by_id(self, constraint_id: str) -> ConstraintRule:
        """
        Get a constraint by its ID
        
        Args:
            constraint_id: ID of the constraint
            
        Returns:
            ConstraintRule object
        """
        for constraint in self.constraints:
            if constraint.id == constraint_id:
                return constraint
        raise ValueError(f"Constraint {constraint_id} not found")
    
    def get_constraints_by_severity(self, severity: ConstraintSeverity) -> List[ConstraintRule]:
        """
        Get all constraints of a given severity level
        
        Args:
            severity: Severity level to filter by
            
        Returns:
            List of ConstraintRule objects
        """
        return [c for c in self.constraints if c.severity == severity]
    
    def check_file_permission(self, file_path: str) -> Tuple[bool, str]:
        """
        Check if a file can be modified based on constitutional constraints
        
        Args:
            file_path: Path to the file
            
        Returns:
            Tuple of (allowed, reason)
        """
        # Files that are always protected
        protected_patterns = [
            r".*constitutional.*\.py",
            r".*safety.*rail.*\.py",
            r".*gatekeeper.*\.py",
            r".*constraint.*\.py",
            r".*rsi.*__init__\.py",
        ]
        
        for pattern in protected_patterns:
            if re.match(pattern, file_path, re.IGNORECASE):
                return False, f"File {file_path} is protected by constitutional constraints"
        
        return True, "File modification allowed"
    
    def check_pattern_safety(self, pattern: str) -> Tuple[bool, str]:
        """
        Check if a pattern is safe to use
        
        Args:
            pattern: Pattern to check
            
        Returns:
            Tuple of (is_safe, reason)
        """
        # Patterns that could be used to bypass constraints
        dangerous_patterns = [
            r".*disable.*",
            r".*bypass.*",
            r".*override.*",
            r".*remove.*safety.*",
        ]
        
        for dangerous_pattern in dangerous_patterns:
            if re.match(dangerous_pattern, pattern, re.IGNORECASE):
                return False, f"Pattern {pattern} could bypass safety constraints"
        
        return True, "Pattern is safe"
    
    def get_constraint_summary(self) -> Dict:
        """
        Get a summary of all constraints
        
        Returns:
            Dictionary with constraint summary
        """
        return {
            "total_constraints": len(self.constraints),
            "by_severity": {
                "critical": len(self.get_constraints_by_severity(ConstraintSeverity.CRITICAL)),
                "high": len(self.get_constraints_by_severity(ConstraintSeverity.HIGH)),
                "medium": len(self.get_constraints_by_severity(ConstraintSeverity.MEDIUM)),
                "low": len(self.get_constraints_by_severity(ConstraintSeverity.LOW)),
            },
            "constraints": [
                {
                    "id": c.id,
                    "name": c.name,
                    "severity": c.severity.value,
                    "description": c.description
                }
                for c in self.constraints
            ]
        }
