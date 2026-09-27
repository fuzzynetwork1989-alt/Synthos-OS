"""Proposal Manager - Change proposal management for RSI governance"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum
import structlog
from datetime import datetime, timedelta

logger = structlog.get_logger(__name__)


class ProposalStatus(Enum):
    """Status of a change proposal"""
    DRAFT = "draft"
    SUBMITTED = "submitted"
    UNDER_REVIEW = "under_review"
    APPROVED = "approved"
    REJECTED = "rejected"
    APPLIED = "applied"
    ROLLED_BACK = "rolled_back"


class RiskLevel(Enum):
    """Risk level of a change"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class ChangeProposal:
    """Change proposal for self-modification"""
    proposal_id: str
    cycle_id: str
    mutation_id: str
    status: ProposalStatus
    risk_level: RiskLevel
    description: str
    mutation_text: str
    changed_files: List[str]
    diff: str
    expected_improvement: str
    gate_results: List[Dict]
    evidence: Dict
    rollback_plan: str
    submitted_at: datetime
    reviewed_by: Optional[str] = None
    reviewed_at: Optional[datetime] = None
    approval_notes: Optional[str] = None
    rejection_reason: Optional[str] = None


class ProposalManager:
    """
    Manage change proposals for RSI governance
    
    Handles proposal lifecycle, risk classification, and approval workflows
    """
    
    def __init__(self, config: Dict = None):
        """
        Initialize proposal manager
        
        Args:
            config: Configuration for proposal management
        """
        self.config = config or self._default_config()
        self.proposals: Dict[str, ChangeProposal] = {}
        self.proposal_counter = 0
        
        logger.info("Proposal Manager initialized", config=self.config)
    
    def _default_config(self) -> Dict:
        """Default configuration for proposal manager"""
        return {
            "auto_approve_threshold": "low",  # Auto-approve proposals below this risk level
            "review_timeout_hours": 24,  # Time before auto-rejection
            "max_concurrent_proposals": 5,
        }
    
    def create_proposal(
        self,
        cycle_id: str,
        mutation: Dict,
        gate_results: List[Dict],
        evidence: Dict
    ) -> ChangeProposal:
        """
        Create a new change proposal
        
        Args:
            cycle_id: Associated improvement cycle
            mutation: Mutation data
            gate_results: Results from gatekeeper validation
            evidence: Evidence of improvement
            
        Returns:
            New ChangeProposal object
        """
        self.proposal_counter += 1
        proposal_id = f"proposal_{self.proposal_counter}"
        
        # Classify risk level
        risk_level = self._classify_risk(mutation, gate_results)
        
        # Generate rollback plan
        rollback_plan = self._generate_rollback_plan(mutation)
        
        proposal = ChangeProposal(
            proposal_id=proposal_id,
            cycle_id=cycle_id,
            mutation_id=mutation["id"],
            status=ProposalStatus.DRAFT,
            risk_level=risk_level,
            description=mutation["description"],
            mutation_text=mutation["text"],
            changed_files=mutation["changed_files"],
            diff=mutation["diff"],
            expected_improvement=mutation["expected_improvement"],
            gate_results=gate_results,
            evidence=evidence,
            rollback_plan=rollback_plan,
            submitted_at=datetime.utcnow()
        )
        
        self.proposals[proposal_id] = proposal
        
        logger.info(
            "Proposal created",
            proposal_id=proposal_id,
            risk_level=risk_level.value,
            mutation_id=mutation["id"]
        )
        
        return proposal
    
    def _classify_risk(self, mutation: Dict, gate_results: List[Dict]) -> RiskLevel:
        """
        Classify the risk level of a mutation
        
        Args:
            mutation: Mutation data
            gate_results: Gatekeeper validation results
            
        Returns:
            RiskLevel enum value
        """
        # Start with base risk from mutation
        base_risk = mutation.get("risk_level", "medium")
        
        # Check gate results for additional risk factors
        critical_failures = sum(
            1 for r in gate_results
            if r.get("result") in ["critical", "fail"]
        )
        warnings = sum(
            1 for r in gate_results
            if r.get("result") == "warning"
        )
        
        # Upgrade risk based on gate results
        if critical_failures > 0:
            return RiskLevel.CRITICAL
        elif warnings > 2:
            return RiskLevel.HIGH
        elif warnings > 0:
            return RiskLevel.MEDIUM
        else:
            # Use base risk
            risk_map = {
                "low": RiskLevel.LOW,
                "medium": RiskLevel.MEDIUM,
                "high": RiskLevel.HIGH,
                "critical": RiskLevel.CRITICAL
            }
            return risk_map.get(base_risk, RiskLevel.MEDIUM)
    
    def _generate_rollback_plan(self, mutation: Dict) -> str:
        """
        Generate rollback plan for a mutation
        
        Args:
            mutation: Mutation data
            
        Returns:
            Rollback plan description
        """
        files_affected = len(mutation["changed_files"])
        
        plan = f"""
Rollback Plan for Mutation {mutation['id']}:

1. Git Revert:
   - Revert commit containing mutation
   - Verify no other changes are affected

2. File Restoration:
   - Restore {files_affected} affected files from backup
   - Verify file integrity

3. System Restart:
   - Restart affected services
   - Verify system health

4. Validation:
   - Run full test suite
   - Verify performance metrics
   - Check system stability

5. Monitoring:
   - Monitor system for 24 hours
   - Check for any regressions
   - Validate no residual effects

Estimated rollback time: 5-10 minutes
Risk level: {mutation.get('risk_level', 'medium')}
"""
        return plan.strip()
    
    def submit_proposal(self, proposal_id: str) -> bool:
        """
        Submit a proposal for review
        
        Args:
            proposal_id: ID of proposal to submit
            
        Returns:
            True if submission successful
        """
        if proposal_id not in self.proposals:
            logger.error("Proposal not found", proposal_id=proposal_id)
            return False
        
        proposal = self.proposals[proposal_id]
        proposal.status = ProposalStatus.SUBMITTED
        
        # Check if auto-approval is possible
        auto_approve_threshold = self.config["auto_approve_threshold"]
        risk_order = {"low": 0, "medium": 1, "high": 2, "critical": 3}
        
        if risk_order[proposal.risk_level.value] <= risk_order[auto_approve_threshold]:
            proposal.status = ProposalStatus.APPROVED
            logger.info("Proposal auto-approved", proposal_id=proposal_id)
        else:
            proposal.status = ProposalStatus.UNDER_REVIEW
            logger.info("Proposal submitted for review", proposal_id=proposal_id)
        
        return True
    
    def approve_proposal(
        self,
        proposal_id: str,
        reviewer: str,
        notes: Optional[str] = None
    ) -> bool:
        """
        Approve a proposal
        
        Args:
            proposal_id: ID of proposal to approve
            reviewer: Person approving the proposal
            notes: Optional approval notes
            
        Returns:
            True if approval successful
        """
        if proposal_id not in self.proposals:
            logger.error("Proposal not found", proposal_id=proposal_id)
            return False
        
        proposal = self.proposals[proposal_id]
        proposal.status = ProposalStatus.APPROVED
        proposal.reviewed_by = reviewer
        proposal.reviewed_at = datetime.utcnow()
        proposal.approval_notes = notes
        
        logger.info(
            "Proposal approved",
            proposal_id=proposal_id,
            reviewer=reviewer
        )
        
        return True
    
    def reject_proposal(
        self,
        proposal_id: str,
        reviewer: str,
        reason: str
    ) -> bool:
        """
        Reject a proposal
        
        Args:
            proposal_id: ID of proposal to reject
            reviewer: Person rejecting the proposal
            reason: Reason for rejection
            
        Returns:
            True if rejection successful
        """
        if proposal_id not in self.proposals:
            logger.error("Proposal not found", proposal_id=proposal_id)
            return False
        
        proposal = self.proposals[proposal_id]
        proposal.status = ProposalStatus.REJECTED
        proposal.reviewed_by = reviewer
        proposal.reviewed_at = datetime.utcnow()
        proposal.rejection_reason = reason
        
        logger.info(
            "Proposal rejected",
            proposal_id=proposal_id,
            reviewer=reviewer,
            reason=reason
        )
        
        return True
    
    def mark_applied(self, proposal_id: str) -> bool:
        """
        Mark a proposal as applied
        
        Args:
            proposal_id: ID of proposal to mark as applied
            
        Returns:
            True if successful
        """
        if proposal_id not in self.proposals:
            return False
        
        proposal = self.proposals[proposal_id]
        proposal.status = ProposalStatus.APPLIED
        
        logger.info("Proposal marked as applied", proposal_id=proposal_id)
        return True
    
    def mark_rolled_back(self, proposal_id: str) -> bool:
        """
        Mark a proposal as rolled back
        
        Args:
            proposal_id: ID of proposal to mark as rolled back
            
        Returns:
            True if successful
        """
        if proposal_id not in self.proposals:
            return False
        
        proposal = self.proposals[proposal_id]
        proposal.status = ProposalStatus.ROLLED_BACK
        
        logger.info("Proposal marked as rolled back", proposal_id=proposal_id)
        return True
    
    def get_proposal(self, proposal_id: str) -> Optional[ChangeProposal]:
        """Get a proposal by ID"""
        return self.proposals.get(proposal_id)
    
    def get_pending_proposals(self) -> List[ChangeProposal]:
        """Get all pending proposals"""
        return [
            p for p in self.proposals.values()
            if p.status in [ProposalStatus.SUBMITTED, ProposalStatus.UNDER_REVIEW]
        ]
    
    def get_proposals_by_cycle(self, cycle_id: str) -> List[ChangeProposal]:
        """Get all proposals for a specific cycle"""
        return [
            p for p in self.proposals.values()
            if p.cycle_id == cycle_id
        ]
    
    def check_review_timeouts(self) -> List[str]:
        """
        Check for proposals that have exceeded review timeout
        
        Returns:
            List of proposal IDs that have timed out
        """
        timeout_hours = self.config["review_timeout_hours"]
        timeout_delta = timedelta(hours=timeout_hours)
        current_time = datetime.utcnow()
        
        timed_out_proposals = []
        
        for proposal in self.proposals.values():
            if proposal.status == ProposalStatus.UNDER_REVIEW:
                time_since_submission = current_time - proposal.submitted_at
                if time_since_submission > timeout_delta:
                    timed_out_proposals.append(proposal.proposal_id)
                    logger.warning(
                        "Proposal review timeout",
                        proposal_id=proposal.proposal_id,
                        hours_elapsed=time_since_submission.total_seconds() / 3600
                    )
        
        return timed_out_proposals
    
    def get_proposal_statistics(self) -> Dict:
        """Get statistics about proposals"""
        total = len(self.proposals)
        by_status = {}
        by_risk = {}
        
        for proposal in self.proposals.values():
            # Count by status
            status = proposal.status.value
            by_status[status] = by_status.get(status, 0) + 1
            
            # Count by risk level
            risk = proposal.risk_level.value
            by_risk[risk] = by_risk.get(risk, 0) + 1
        
        return {
            "total_proposals": total,
            "by_status": by_status,
            "by_risk": by_risk,
            "pending_review": len(self.get_pending_proposals()),
        }
