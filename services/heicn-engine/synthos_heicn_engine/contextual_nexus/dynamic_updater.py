"""
Dynamic Context Updater - Real-time context updates based on new interactions

This module provides real-time updates to the contextual nexus based on
new user interactions, system events, and environmental changes.
"""

from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
import structlog
from datetime import datetime
import asyncio
import uuid

logger = structlog.get_logger(__name__)


@dataclass
class ContextUpdate:
    """An update to the context"""
    update_id: str
    context_type: str  # "user", "system", "environment"
    entity_id: str
    changes: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    priority: int = 1  # 1-5, 5 being highest
    source: str = ""


@dataclass
class ContextChange:
    """A detected change in context"""
    change_id: str
    context_type: str
    entity_id: str
    old_value: Any
    new_value: Any
    significance: float = 0.5  # 0.0 to 1.0
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class UpdateRule:
    """A rule for updating context"""
    rule_id: str
    name: str
    condition: Dict[str, Any]
    action: Dict[str, Any]
    priority: int = 1
    enabled: bool = True


@dataclass
class UpdateStrategy:
    """A strategy for updating context"""
    strategy_id: str
    name: str
    description: str
    frequency: float  # updates per second
    scope: str  # "full", "partial", "targeted"
    resource_usage: float = 0.5  # 0.0 to 1.0


class DynamicContextUpdater:
    """
    Dynamic Context Updater - Provides real-time context updates.
    
    This system:
    - Monitors for context changes
    - Applies updates based on rules and strategies
    - Propagates changes through the knowledge graph
    - Optimizes update frequency and scope
    """
    
    def __init__(self, config: Optional[Dict] = None):
        """
        Initialize the dynamic context updater.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config or self._default_config()
        
        # Update history
        self._updates: Dict[str, ContextUpdate] = {}
        self._update_history: List[ContextUpdate] = []
        
        # Change detection
        self._changes: Dict[str, ContextChange] = {}
        self._change_history: List[ContextChange] = []
        
        # Update rules
        self._rules: Dict[str, UpdateRule] = {}
        
        # Update strategies
        self._strategies: Dict[str, UpdateStrategy] = {}
        
        # Monitoring state
        self._monitoring = False
        self._monitoring_task: Optional[asyncio.Task] = None
        
        # Event callbacks
        self._event_callbacks: Dict[str, List[Any]] = {
            "context_updated": [],
            "change_detected": []
        }
        
        # Current context state
        self._current_state: Dict[str, Dict[str, Any]] = {
            "user": {},
            "system": {},
            "environment": {}
        }
        
        logger.info("DynamicContextUpdater initialized")
    
    def _default_config(self) -> Dict:
        """Default configuration"""
        return {
            "max_history": 1000,
            "update_frequency": 1.0,  # updates per second
            "change_detection_interval": 0.1,  # seconds
            "propagation_depth": 3,
            "enabled": True
        }
    
    def add_update_rule(
        self,
        rule_id: str,
        name: str,
        condition: Dict[str, Any],
        action: Dict[str, Any],
        priority: int = 1,
        enabled: bool = True
    ) -> str:
        """
        Add an update rule.
        
        Args:
            rule_id: Unique rule identifier
            name: Rule name
            condition: Condition for applying the rule
            action: Action to take when condition is met
            priority: Rule priority
            enabled: Whether the rule is enabled
            
        Returns:
            Rule ID
        """
        rule = UpdateRule(
            rule_id=rule_id,
            name=name,
            condition=condition,
            action=action,
            priority=priority,
            enabled=enabled
        )
        
        self._rules[rule_id] = rule
        
        logger.info("Update rule added", rule_id=rule_id, name=name)
        return rule_id
    
    def get_update_rule(self, rule_id: str) -> Optional[UpdateRule]:
        """Get an update rule by ID"""
        return self._rules.get(rule_id)
    
    def get_all_update_rules(self) -> Dict[str, UpdateRule]:
        """Get all update rules"""
        return self._rules.copy()
    
    def remove_update_rule(self, rule_id: str) -> bool:
        """Remove an update rule"""
        if rule_id in self._rules:
            del self._rules[rule_id]
            return True
        return False
    
    def add_update_strategy(
        self,
        strategy_id: str,
        name: str,
        description: str,
        frequency: float,
        scope: str,
        resource_usage: float = 0.5
    ) -> str:
        """
        Add an update strategy.
        
        Args:
            strategy_id: Unique strategy identifier
            name: Strategy name
            description: Strategy description
            frequency: Update frequency (updates per second)
            scope: Update scope ("full", "partial", "targeted")
            resource_usage: Resource usage (0.0 to 1.0)
            
        Returns:
            Strategy ID
        """
        strategy = UpdateStrategy(
            strategy_id=strategy_id,
            name=name,
            description=description,
            frequency=frequency,
            scope=scope,
            resource_usage=resource_usage
        )
        
        self._strategies[strategy_id] = strategy
        
        logger.info("Update strategy added", strategy_id=strategy_id, name=name)
        return strategy_id
    
    def get_update_strategy(self, strategy_id: str) -> Optional[UpdateStrategy]:
        """Get an update strategy by ID"""
        return self._strategies.get(strategy_id)
    
    def get_all_update_strategies(self) -> Dict[str, UpdateStrategy]:
        """Get all update strategies"""
        return self._strategies.copy()
    
    def record_update(
        self,
        context_type: str,
        entity_id: str,
        changes: Dict[str, Any],
        priority: int = 1,
        source: str = ""
    ) -> str:
        """
        Record a context update.
        
        Args:
            context_type: Type of context ("user", "system", "environment")
            entity_id: Entity identifier
            changes: Dictionary of changes
            priority: Update priority
            source: Update source
            
        Returns:
            Update ID
        """
        update_id = str(uuid.uuid4())
        
        update = ContextUpdate(
            update_id=update_id,
            context_type=context_type,
            entity_id=entity_id,
            changes=changes,
            timestamp=datetime.now(),
            priority=priority,
            source=source
        )
        
        self._updates[update_id] = update
        self._update_history.append(update)
        
        # Keep history limited
        if len(self._update_history) > self.config.get("max_history", 1000):
            self._update_history = self._update_history[-1000:]
        
        # Update current state
        if context_type not in self._current_state:
            self._current_state[context_type] = {}
        if entity_id not in self._current_state[context_type]:
            self._current_state[context_type][entity_id] = {}
        
        self._current_state[context_type][entity_id].update(changes)
        
        # Detect changes
        self._detect_changes(update)
        
        # Trigger callbacks
        for callback in self._event_callbacks.get("context_updated", []):
            try:
                callback(update)
            except Exception as e:
                logger.error("Error in context_updated callback", error=str(e))
        
        logger.info(
            "Update recorded",
            update_id=update_id,
            context_type=context_type,
            entity_id=entity_id
        )
        
        return update_id
    
    def _detect_changes(self, update: ContextUpdate):
        """Detect changes based on an update"""
        context_type = update.context_type
        entity_id = update.entity_id
        
        if context_type not in self._current_state:
            return
        if entity_id not in self._current_state[context_type]:
            return
        
        # For each change, detect if it's significant
        for key, new_value in update.changes.items():
            old_value = self._current_state[context_type][entity_id].get(key)
            
            if old_value is not None and old_value != new_value:
                # Calculate significance
                significance = self._calculate_significance(context_type, entity_id, key, old_value, new_value)
                
                change = ContextChange(
                    change_id=str(uuid.uuid4()),
                    context_type=context_type,
                    entity_id=entity_id,
                    old_value=old_value,
                    new_value=new_value,
                    significance=significance,
                    timestamp=datetime.now()
                )
                
                self._changes[change.change_id] = change
                self._change_history.append(change)
                
                # Keep history limited
                if len(self._change_history) > self.config.get("max_history", 1000):
                    self._change_history = self._change_history[-1000:]
                
                # Trigger callbacks
                for callback in self._event_callbacks.get("change_detected", []):
                    try:
                        callback(change)
                    except Exception as e:
                        logger.error("Error in change_detected callback", error=str(e))
                
                logger.info(
                    "Change detected",
                    change_id=change.change_id,
                    context_type=context_type,
                    entity_id=entity_id,
                    key=key,
                    significance=significance
                )
    
    def _calculate_significance(
        self,
        context_type: str,
        entity_id: str,
        key: str,
        old_value: Any,
        new_value: Any
    ) -> float:
        """
        Calculate the significance of a change.
        
        Args:
            context_type: Context type
            entity_id: Entity ID
            key: Changed key
            old_value: Old value
            new_value: New value
            
        Returns:
            Significance score (0.0 to 1.0)
        """
        # Base significance
        significance = 0.5
        
        # Increase significance for certain context types
        if context_type == "user":
            significance += 0.2
        elif context_type == "system":
            significance += 0.1
        
        # Increase significance for numeric changes based on magnitude
        if isinstance(old_value, (int, float)) and isinstance(new_value, (int, float)):
            if old_value != 0:
                magnitude = abs(new_value - old_value) / abs(old_value)
                significance += min(0.3, magnitude * 0.5)
        
        # Increase significance for certain keys
        important_keys = ["status", "priority", "enabled", "active", "critical"]
        if key.lower() in important_keys:
            significance += 0.2
        
        # Clamp to 0-1 range
        return min(1.0, max(0.0, significance))
    
    def get_current_state(self, context_type: str = None) -> Dict[str, Any]:
        """
        Get the current context state.
        
        Args:
            context_type: Optional context type filter
            
        Returns:
            Current state dictionary
        """
        if context_type:
            return self._current_state.get(context_type, {}).copy()
        return {k: v.copy() for k, v in self._current_state.items()}
    
    def get_entity_state(self, context_type: str, entity_id: str) -> Dict[str, Any]:
        """
        Get the state of a specific entity.
        
        Args:
            context_type: Context type
            entity_id: Entity ID
            
        Returns:
            Entity state dictionary
        """
        if context_type in self._current_state and entity_id in self._current_state[context_type]:
            return self._current_state[context_type][entity_id].copy()
        return {}
    
    def get_changes(self, context_type: str = None, entity_id: str = None) -> List[ContextChange]:
        """
        Get detected changes.
        
        Args:
            context_type: Optional context type filter
            entity_id: Optional entity ID filter
            
        Returns:
            List of context changes
        """
        changes = list(self._change_history)
        
        if context_type:
            changes = [c for c in changes if c.context_type == context_type]
        if entity_id:
            changes = [c for c in changes if c.entity_id == entity_id]
        
        return changes
    
    def get_updates(self, context_type: str = None, entity_id: str = None) -> List[ContextUpdate]:
        """
        Get recorded updates.
        
        Args:
            context_type: Optional context type filter
            entity_id: Optional entity ID filter
            
        Returns:
            List of context updates
        """
        updates = list(self._update_history)
        
        if context_type:
            updates = [u for u in updates if u.context_type == context_type]
        if entity_id:
            updates = [u for u in updates if u.entity_id == entity_id]
        
        return updates
    
    def apply_update_rules(self) -> List[ContextUpdate]:
        """
        Apply all enabled update rules to the current state.
        
        Returns:
            List of updates generated by rules
        """
        updates = []
        
        for rule in self._rules.values():
            if not rule.enabled:
                continue
            
            # Check if condition is met
            condition_met = True
            
            for key, expected_value in rule.condition.items():
                # Parse the condition key (format: "context_type.entity_id.key")
                parts = key.split(".")
                if len(parts) >= 3:
                    ctx_type = parts[0]
                    ent_id = parts[1]
                    field = ".".join(parts[2:])
                    
                    if ctx_type in self._current_state and ent_id in self._current_state[ctx_type]:
                        actual_value = self._current_state[ctx_type][ent_id].get(field)
                        if actual_value != expected_value:
                            condition_met = False
                            break
                else:
                    # Check in any context
                    found = False
                    for ctx_type, entities in self._current_state.items():
                        for ent_id, entity in entities.items():
                            if field in entity and entity[field] == expected_value:
                                found = True
                                break
                        if found:
                            break
                    if not found:
                        condition_met = False
                        break
            
            if condition_met:
                # Apply the action
                update = self._apply_rule_action(rule)
                if update:
                    updates.append(update)
        
        return updates
    
    def _apply_rule_action(self, rule: UpdateRule) -> Optional[ContextUpdate]:
        """
        Apply the action of an update rule.
        
        Args:
            rule: Update rule
            
        Returns:
            Context update or None
        """
        # Parse the action
        context_type = rule.action.get("context_type")
        entity_id = rule.action.get("entity_id")
        changes = rule.action.get("changes", {})
        
        if not context_type or not entity_id:
            return None
        
        # Create update
        update = self.record_update(
            context_type=context_type,
            entity_id=entity_id,
            changes=changes,
            priority=rule.priority,
            source=f"rule:{rule.rule_id}"
        )
        
        return self._updates.get(update.update_id)
    
    def update_from_interaction(self, user_id: str, interaction_data: Dict[str, Any]) -> List[ContextUpdate]:
        """
        Update context based on a user interaction.
        
        Args:
            user_id: User identifier
            interaction_data: Interaction data
            
        Returns:
            List of updates generated
        """
        updates = []
        
        # Update user context
        user_changes = {}
        
        # Extract user-related information from interaction
        if "preferences" in interaction_data:
            user_changes["preferences"] = interaction_data["preferences"]
        if "interests" in interaction_data:
            user_changes["interests"] = interaction_data["interests"]
        if "expertise" in interaction_data:
            user_changes["expertise"] = interaction_data["expertise"]
        if "emotional_state" in interaction_data:
            user_changes["emotional_state"] = interaction_data["emotional_state"]
        if "engagement_level" in interaction_data:
            user_changes["engagement_level"] = interaction_data["engagement_level"]
        if "current_goal" in interaction_data:
            user_changes["current_goal"] = interaction_data["current_goal"]
        
        if user_changes:
            update = self.record_update(
                context_type="user",
                entity_id=user_id,
                changes=user_changes,
                priority=3,
                source="interaction"
            )
            updates.append(self._updates[update.update_id])
        
        # Update system context based on interaction
        system_changes = {}
        
        if "system_impact" in interaction_data:
            system_changes["impact"] = interaction_data["system_impact"]
        if "resource_usage" in interaction_data:
            system_changes["resource_usage"] = interaction_data["resource_usage"]
        
        if system_changes:
            update = self.record_update(
                context_type="system",
                entity_id="global",
                changes=system_changes,
                priority=2,
                source="interaction"
            )
            updates.append(self._updates[update.update_id])
        
        # Apply update rules
        rule_updates = self.apply_update_rules()
        updates.extend(rule_updates)
        
        return updates
    
    async def start_monitoring(self):
        """Start continuous monitoring for context changes"""
        if self._monitoring:
            return
        
        self._monitoring = True
        self._monitoring_task = asyncio.create_task(self._monitoring_loop())
        
        logger.info("Context monitoring started")
    
    async def stop_monitoring(self):
        """Stop continuous monitoring"""
        if not self._monitoring:
            return
        
        self._monitoring = False
        if self._monitoring_task:
            self._monitoring_task.cancel()
            try:
                await self._monitoring_task
            except asyncio.CancelledError:
                pass
        
        logger.info("Context monitoring stopped")
    
    async def _monitoring_loop(self):
        """Continuous monitoring loop"""
        interval = self.config.get("change_detection_interval", 0.1)
        
        while self._monitoring:
            try:
                # Check for changes
                self.apply_update_rules()
                
                # Small delay
                await asyncio.sleep(interval)
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error("Error in monitoring loop", error=str(e))
                await asyncio.sleep(1.0)  # Wait before retrying
    
    def on(self, event: str, callback: Any):
        """
        Register a callback for an event.
        
        Args:
            event: Event name
            callback: Callback function
        """
        if event not in self._event_callbacks:
            self._event_callbacks[event] = []
        self._event_callbacks[event].append(callback)
        return callback
    
    def off(self, event: str, callback: Any) -> bool:
        """
        Unregister a callback for an event.
        
        Args:
            event: Event name
            callback: Callback function to remove
            
        Returns:
            True if removed successfully
        """
        if event in self._event_callbacks:
            try:
                self._event_callbacks[event].remove(callback)
                return True
            except ValueError:
                pass
        return False
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about the dynamic context updater.
        
        Returns:
            Statistics dictionary
        """
        return {
            "update_count": len(self._updates),
            "change_count": len(self._changes),
            "rule_count": len(self._rules),
            "strategy_count": len(self._strategies),
            "monitoring": self._monitoring,
            "entity_counts": {
                ctx: len(entities)
                for ctx, entities in self._current_state.items()
            }
        }
    
    def get_info(self) -> Dict[str, Any]:
        """Get information about the dynamic context updater"""
        return {
            "system_type": "DynamicContextUpdater",
            "update_count": len(self._updates),
            "change_count": len(self._changes),
            "rule_count": len(self._rules),
            "strategy_count": len(self._strategies),
            "monitoring": self._monitoring
        }
