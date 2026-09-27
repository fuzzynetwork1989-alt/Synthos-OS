"""Audit Logger - Complete audit trail for RSI operations"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum
import structlog
from datetime import datetime
import json
import aiofiles

logger = structlog.get_logger(__name__)


class AuditEventType(Enum):
    """Types of audit events"""
    CYCLE_STARTED = "cycle_started"
    CYCLE_COMPLETED = "cycle_completed"
    CYCLE_FAILED = "cycle_failed"
    MUTATION_GENERATED = "mutation_generated"
    MUTATION_TESTED = "mutation_tested"
    MUTATION_APPROVED = "mutation_approved"
    MUTATION_REJECTED = "mutation_rejected"
    MUTATION_APPLIED = "mutation_applied"
    GATE_CHECK = "gate_check"
    GDI_MEASUREMENT = "gdi_measurement"
    CONSTRAINT_VIOLATION = "constraint_violation"
    PROPOSAL_SUBMITTED = "proposal_submitted"
    PROPOSAL_APPROVED = "proposal_approved"
    PROPOSAL_REJECTED = "proposal_rejected"
    EMERGENCY_STOP = "emergency_stop"
    ROLLBACK = "rollback"
    SYSTEM_STATE_CHANGE = "system_state_change"


@dataclass
class AuditEvent:
    """Single audit event"""
    event_id: str
    event_type: AuditEventType
    timestamp: datetime
    cycle_id: Optional[str]
    proposal_id: Optional[str]
    user_id: Optional[str]
    details: Dict
    severity: str  # "info", "warning", "error", "critical"


class AuditLogger:
    """
    Complete audit trail for RSI operations
    
    Provides append-only logging of all RSI operations with
    automatic secret redaction and structured event storage
    """
    
    def __init__(self, config: Dict = None):
        """
        Initialize audit logger
        
        Args:
            config: Configuration for audit logging
        """
        self.config = config or self._default_config()
        self.events: List[AuditEvent] = []
        self.event_counter = 0
        
        logger.info("Audit Logger initialized", config=self.config)
    
    def _default_config(self) -> Dict:
        """Default configuration for audit logger"""
        return {
            "log_file": "./logs/rsi_audit.log",
            "enable_file_logging": True,
            "enable_secret_redaction": True,
            "max_events_in_memory": 10000,
        }
    
    def log_event(
        self,
        event_type: AuditEventType,
        details: Dict,
        cycle_id: Optional[str] = None,
        proposal_id: Optional[str] = None,
        user_id: Optional[str] = None,
        severity: str = "info"
    ) -> AuditEvent:
        """
        Log an audit event
        
        Args:
            event_type: Type of the event
            details: Event details
            cycle_id: Associated cycle ID
            proposal_id: Associated proposal ID
            user_id: User who triggered the event
            severity: Event severity level
            
        Returns:
            AuditEvent object
        """
        self.event_counter += 1
        event_id = f"event_{self.event_counter}"
        
        # Redact secrets if enabled
        if self.config["enable_secret_redaction"]:
            details = self._redact_secrets(details)
        
        event = AuditEvent(
            event_id=event_id,
            event_type=event_type,
            timestamp=datetime.utcnow(),
            cycle_id=cycle_id,
            proposal_id=proposal_id,
            user_id=user_id,
            details=details,
            severity=severity
        )
        
        self.events.append(event)
        
        # Trim events if needed
        if len(self.events) > self.config["max_events_in_memory"]:
            self.events = self.events[-self.config["max_events_in_memory"]:]
        
        # Log to file if enabled
        if self.config["enable_file_logging"]:
            self._write_to_file(event)
        
        # Log to structlog
        logger.info(
            "Audit event logged",
            event_id=event_id,
            event_type=event_type.value,
            severity=severity
        )
        
        return event
    
    def _redact_secrets(self, data: Dict) -> Dict:
        """
        Redact secrets from data
        
        Args:
            data: Data to redact
            
        Returns:
            Redacted data
        """
        import re
        
        secret_patterns = [
            (r'password["\s]*:\s*["\'][^"\']+["\']', 'password": "***REDACTED***'),
            (r'api_key["\s]*:\s*["\'][^"\']+["\']', 'api_key": "***REDACTED***'),
            (r'secret["\s]*:\s*["\'][^"\']+["\']', 'secret": "***REDACTED***'),
            (r'token["\s]*:\s*["\'][^"\']+["\']', 'token": "***REDACTED***'),
            (r'sk-[a-zA-Z0-9]{48}', 'sk-***REDACTED***'),
            (r'[A-Za-z0-9]{32}', '***REDACTED***'),  # Generic 32-char strings
        ]
        
        data_str = json.dumps(data)
        
        for pattern, replacement in secret_patterns:
            data_str = re.sub(pattern, replacement, data_str, flags=re.IGNORECASE)
        
        return json.loads(data_str)
    
    async def _write_to_file(self, event: AuditEvent):
        """
        Write event to audit log file
        
        Args:
            event: Event to write
        """
        try:
            log_entry = {
                "event_id": event.event_id,
                "event_type": event.event_type.value,
                "timestamp": event.timestamp.isoformat(),
                "cycle_id": event.cycle_id,
                "proposal_id": event.proposal_id,
                "user_id": event.user_id,
                "details": event.details,
                "severity": event.severity
            }
            
            async with aiofiles.open(self.config["log_file"], mode="a") as f:
                await f.write(json.dumps(log_entry) + "\n")
        except Exception as e:
            logger.error("Failed to write audit event to file", error=str(e))
    
    def get_events(
        self,
        event_type: Optional[AuditEventType] = None,
        cycle_id: Optional[str] = None,
        proposal_id: Optional[str] = None,
        limit: Optional[int] = None
    ) -> List[AuditEvent]:
        """
        Get filtered audit events
        
        Args:
            event_type: Filter by event type
            cycle_id: Filter by cycle ID
            proposal_id: Filter by proposal ID
            limit: Maximum number of events to return
            
        Returns:
            List of matching audit events
        """
        filtered_events = self.events
        
        if event_type:
            filtered_events = [e for e in filtered_events if e.event_type == event_type]
        
        if cycle_id:
            filtered_events = [e for e in filtered_events if e.cycle_id == cycle_id]
        
        if proposal_id:
            filtered_events = [e for e in filtered_events if e.proposal_id == proposal_id]
        
        if limit:
            filtered_events = filtered_events[-limit:]
        
        return filtered_events
    
    def get_events_by_severity(self, severity: str) -> List[AuditEvent]:
        """Get events by severity level"""
        return [e for e in self.events if e.severity == severity]
    
    def get_events_by_time_range(
        self,
        start_time: datetime,
        end_time: datetime
    ) -> List[AuditEvent]:
        """Get events within a time range"""
        return [
            e for e in self.events
            if start_time <= e.timestamp <= end_time
        ]
    
    def get_statistics(self) -> Dict:
        """Get audit statistics"""
        total_events = len(self.events)
        by_type = {}
        by_severity = {}
        
        for event in self.events:
            # Count by type
            event_type = event.event_type.value
            by_type[event_type] = by_type.get(event_type, 0) + 1
            
            # Count by severity
            severity = event.severity
            by_severity[severity] = by_severity.get(severity, 0) + 1
        
        return {
            "total_events": total_events,
            "by_type": by_type,
            "by_severity": by_severity,
            "time_range": self._get_time_range()
        }
    
    def _get_time_range(self) -> Dict:
        """Get time range of logged events"""
        if not self.events:
            return {"start": None, "end": None}
        
        timestamps = [e.timestamp for e in self.events]
        return {
            "start": min(timestamps).isoformat(),
            "end": max(timestamps).isoformat()
        }
    
    def export_events(self, format: str = "json") -> str:
        """
        Export audit events
        
        Args:
            format: Export format ("json" or "csv")
            
        Returns:
            Exported data as string
        """
        if format == "json":
            return json.dumps([
                {
                    "event_id": e.event_id,
                    "event_type": e.event_type.value,
                    "timestamp": e.timestamp.isoformat(),
                    "cycle_id": e.cycle_id,
                    "proposal_id": e.proposal_id,
                    "user_id": e.user_id,
                    "details": e.details,
                    "severity": e.severity
                }
                for e in self.events
            ], indent=2)
        elif format == "csv":
            import csv
            import io
            
            output = io.StringIO()
            writer = csv.writer(output)
            
            # Write header
            writer.writerow([
                "event_id", "event_type", "timestamp", "cycle_id",
                "proposal_id", "user_id", "severity"
            ])
            
            # Write rows
            for e in self.events:
                writer.writerow([
                    e.event_id,
                    e.event_type.value,
                    e.timestamp.isoformat(),
                    e.cycle_id,
                    e.proposal_id,
                    e.user_id,
                    e.severity
                ])
            
            return output.getvalue()
        else:
            raise ValueError(f"Unsupported format: {format}")
