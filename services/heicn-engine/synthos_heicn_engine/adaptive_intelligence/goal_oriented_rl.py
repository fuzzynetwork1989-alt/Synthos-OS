"""
Goal-Oriented Reinforcement Learning for HEICN

This module implements goal-oriented reinforcement learning that dynamically
adjusts objectives based on user feedback and system performance.
"""

from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
import structlog
from datetime import datetime
import numpy as np
import random

logger = structlog.get_logger(__name__)


@dataclass
class Goal:
    """A goal for the reinforcement learning system"""
    goal_id: str
    name: str
    description: str
    target_value: float
    current_value: float = 0.0
    priority: float = 1.0  # 0.0 to 1.0
    progress: float = 0.0  # 0.0 to 1.0
    achieved: bool = False
    created_at: datetime = field(default_factory=datetime.now)
    achieved_at: Optional[datetime] = None


@dataclass
class State:
    """A state in the reinforcement learning environment"""
    state_id: str
    features: Dict[str, float] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class Action:
    """An action that can be taken"""
    action_id: str
    name: str
    description: str
    parameters: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Reward:
    """Reward for a state-action pair"""
    state_id: str
    action_id: str
    value: float
    timestamp: datetime = field(default_factory=datetime.now)
    components: Dict[str, float] = field(default_factory=dict)


@dataclass
class QValue:
    """Q-value for state-action pair"""
    state_id: str
    action_id: str
    value: float
    last_updated: datetime = field(default_factory=datetime.now)
    visit_count: int = 0


class GoalOrientedRL:
    """
    Goal-Oriented Reinforcement Learning System.
    
    This system:
    - Dynamically adjusts objectives based on feedback
    - Learns optimal actions for goal achievement
    - Balances multiple goals with different priorities
    - Adapts to changing environments
    """
    
    def __init__(self, config: Optional[Dict] = None):
        """
        Initialize the goal-oriented RL system.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config or self._default_config()
        
        # Goals
        self._goals: Dict[str, Goal] = {}
        
        # States
        self._states: Dict[str, State] = {}
        self._current_state_id: Optional[str] = None
        
        # Actions
        self._actions: Dict[str, Action] = {}
        
        # Q-values
        self._q_values: Dict[str, QValue] = {}  # (state_id, action_id) -> QValue
        
        # Rewards
        self._reward_history: List[Reward] = []
        
        # Learning parameters
        self._learning_rate = self.config.get("learning_rate", 0.1)
        self._discount_factor = self.config.get("discount_factor", 0.9)
        self._exploration_rate = self.config.get("exploration_rate", 0.2)
        self._min_exploration_rate = self.config.get("min_exploration_rate", 0.01)
        self._exploration_decay = self.config.get("exploration_decay", 0.995)
        
        # Goal weights
        self._goal_weights: Dict[str, float] = {}
        
        logger.info("GoalOrientedRL initialized")
    
    def _default_config(self) -> Dict:
        """Default configuration"""
        return {
            "learning_rate": 0.1,
            "discount_factor": 0.9,
            "exploration_rate": 0.2,
            "min_exploration_rate": 0.01,
            "exploration_decay": 0.995,
            "max_goals": 20,
            "max_states": 1000,
            "max_actions": 50
        }
    
    def add_goal(
        self,
        goal_id: str,
        name: str,
        description: str,
        target_value: float,
        priority: float = 1.0
    ) -> str:
        """
        Add a goal to the system.
        
        Args:
            goal_id: Unique goal identifier
            name: Goal name
            description: Goal description
            target_value: Target value for the goal
            priority: Goal priority (0.0 to 1.0)
            
        Returns:
            Goal ID
        """
        goal = Goal(
            goal_id=goal_id,
            name=name,
            description=description,
            target_value=target_value,
            priority=priority
        )
        self._goals[goal_id] = goal
        self._goal_weights[goal_id] = priority
        
        logger.info("Goal added", goal_id=goal_id, name=name)
        return goal_id
    
    def update_goal_progress(self, goal_id: str, current_value: float) -> bool:
        """
        Update the progress of a goal.
        
        Args:
            goal_id: Goal identifier
            current_value: Current value of the goal
            
        Returns:
            True if updated successfully
        """
        if goal_id not in self._goals:
            return False
        
        goal = self._goals[goal_id]
        goal.current_value = current_value
        
        # Calculate progress
        if goal.target_value > 0:
            goal.progress = min(1.0, max(0.0, current_value / goal.target_value))
        else:
            goal.progress = 1.0
        
        # Check if achieved
        if not goal.achieved and goal.progress >= 0.99:
            goal.achieved = True
            goal.achieved_at = datetime.now()
        
        logger.info(
            "Goal progress updated",
            goal_id=goal_id,
            progress=goal.progress,
            achieved=goal.achieved
        )
        
        return True
    
    def get_goal(self, goal_id: str) -> Optional[Goal]:
        """Get a goal by ID"""
        return self._goals.get(goal_id)
    
    def get_all_goals(self) -> Dict[str, Goal]:
        """Get all goals"""
        return self._goals.copy()
    
    def remove_goal(self, goal_id: str) -> bool:
        """Remove a goal"""
        if goal_id in self._goals:
            del self._goals[goal_id]
            if goal_id in self._goal_weights:
                del self._goal_weights[goal_id]
            return True
        return False
    
    def add_action(
        self,
        action_id: str,
        name: str,
        description: str,
        parameters: Dict[str, Any] = None
    ) -> str:
        """
        Add an action to the system.
        
        Args:
            action_id: Unique action identifier
            name: Action name
            description: Action description
            parameters: Action parameters
            
        Returns:
            Action ID
        """
        action = Action(
            action_id=action_id,
            name=name,
            description=description,
            parameters=parameters or {}
        )
        self._actions[action_id] = action
        
        logger.info("Action added", action_id=action_id, name=name)
        return action_id
    
    def get_action(self, action_id: str) -> Optional[Action]:
        """Get an action by ID"""
        return self._actions.get(action_id)
    
    def get_all_actions(self) -> Dict[str, Action]:
        """Get all actions"""
        return self._actions.copy()
    
    def add_state(self, state_id: str, features: Dict[str, float]) -> str:
        """
        Add a state to the system.
        
        Args:
            state_id: Unique state identifier
            features: State features
            
        Returns:
            State ID
        """
        state = State(
            state_id=state_id,
            features=features
        )
        self._states[state_id] = state
        self._current_state_id = state_id
        
        # Initialize Q-values for this state and all actions
        for action_id in self._actions:
            q_key = self._get_q_key(state_id, action_id)
            if q_key not in self._q_values:
                self._q_values[q_key] = QValue(
                    state_id=state_id,
                    action_id=action_id,
                    value=0.0,
                    visit_count=0
                )
        
        logger.info("State added", state_id=state_id, feature_count=len(features))
        return state_id
    
    def get_state(self, state_id: str) -> Optional[State]:
        """Get a state by ID"""
        return self._states.get(state_id)
    
    def get_current_state(self) -> Optional[State]:
        """Get the current state"""
        if self._current_state_id:
            return self._states.get(self._current_state_id)
        return None
    
    def _get_q_key(self, state_id: str, action_id: str) -> str:
        """Get the key for a Q-value"""
        return f"{state_id}:{action_id}"
    
    def get_q_value(self, state_id: str, action_id: str) -> Optional[QValue]:
        """Get Q-value for a state-action pair"""
        q_key = self._get_q_key(state_id, action_id)
        return self._q_values.get(q_key)
    
    def update_q_value(
        self,
        state_id: str,
        action_id: str,
        reward: float
    ) -> bool:
        """
        Update Q-value using Q-learning update rule.
        
        Args:
            state_id: State identifier
            action_id: Action identifier
            reward: Reward received
            
        Returns:
            True if updated successfully
        """
        q_key = self._get_q_key(state_id, action_id)
        
        if q_key not in self._q_values:
            self._q_values[q_key] = QValue(
                state_id=state_id,
                action_id=action_id,
                value=0.0,
                visit_count=0
            )
        
        q_value = self._q_values[q_key]
        
        # Q-learning update
        # Q(s,a) = Q(s,a) + alpha * (reward + gamma * max(Q(s',a')) - Q(s,a))
        
        # For now, we use a simplified version
        # In a full implementation, we would track the next state
        
        # Calculate the maximum Q-value for the current state
        max_q = 0.0
        for a_id in self._actions:
            a_q_key = self._get_q_key(state_id, a_id)
            if a_q_key in self._q_values:
                max_q = max(max_q, self._q_values[a_q_key].value)
        
        # Update Q-value
        old_value = q_value.value
        q_value.value = old_value + self._learning_rate * (reward + self._discount_factor * max_q - old_value)
        q_value.last_updated = datetime.now()
        q_value.visit_count += 1
        
        # Decay exploration rate
        self._exploration_rate = max(
            self._min_exploration_rate,
            self._exploration_rate * self._exploration_decay
        )
        
        logger.info(
            "Q-value updated",
            state_id=state_id,
            action_id=action_id,
            old_value=old_value,
            new_value=q_value.value,
            reward=reward
        )
        
        return True
    
    def select_action(self, state_id: str = None) -> Tuple[str, bool]:
        """
        Select an action using epsilon-greedy policy.
        
        Args:
            state_id: State identifier (uses current state if None)
            
        Returns:
            Tuple of (action_id, is_exploratory)
        """
        state_id = state_id or self._current_state_id
        
        if not state_id or state_id not in self._states:
            return ("", False)
        
        # Epsilon-greedy selection
        if random.random() < self._exploration_rate:
            # Explore: select random action
            action_id = random.choice(list(self._actions.keys()))
            return (action_id, True)
        
        # Exploit: select action with highest Q-value
        best_action = None
        best_q = -float('inf')
        
        for action_id in self._actions:
            q_key = self._get_q_key(state_id, action_id)
            if q_key in self._q_values:
                if self._q_values[q_key].value > best_q:
                    best_q = self._q_values[q_key].value
                    best_action = action_id
        
        if best_action:
            return (best_action, False)
        
        # If no Q-values, select random
        return (random.choice(list(self._actions.keys())), False)
    
    def record_reward(
        self,
        state_id: str,
        action_id: str,
        reward_value: float,
        components: Dict[str, float] = None
    ) -> Reward:
        """
        Record a reward for a state-action pair.
        
        Args:
            state_id: State identifier
            action_id: Action identifier
            reward_value: Reward value
            components: Reward components
            
        Returns:
            Reward object
        """
        reward = Reward(
            state_id=state_id,
            action_id=action_id,
            value=reward_value,
            components=components or {}
        )
        self._reward_history.append(reward)
        
        # Keep history limited
        if len(self._reward_history) > self.config.get("max_reward_history", 1000):
            self._reward_history = self._reward_history[-1000:]
        
        # Update Q-value
        self.update_q_value(state_id, action_id, reward_value)
        
        logger.info(
            "Reward recorded",
            state_id=state_id,
            action_id=action_id,
            value=reward_value
        )
        
        return reward
    
    def calculate_reward(self, state_id: str = None) -> float:
        """
        Calculate the reward for the current state.
        
        Args:
            state_id: State identifier (uses current state if None)
            
        Returns:
            Reward value
        """
        state_id = state_id or self._current_state_id
        
        if not state_id or state_id not in self._states:
            return 0.0
        
        state = self._states[state_id]
        
        # Calculate reward based on goal progress
        total_reward = 0.0
        total_weight = 0.0
        
        for goal_id, goal in self._goals.items():
            weight = self._goal_weights.get(goal_id, 1.0)
            
            # Calculate reward component for this goal
            # Reward is based on progress toward the goal
            if goal.target_value > 0:
                progress = min(1.0, goal.current_value / goal.target_value)
            else:
                progress = 1.0
            
            # Non-linear reward: more reward for higher progress
            reward_component = progress * weight
            
            total_reward += reward_component
            total_weight += weight
        
        if total_weight > 0:
            return total_reward / total_weight
        
        return 0.0
    
    def suggest_actions(self) -> List[Dict[str, Any]]:
        """
        Suggest actions to improve goal achievement.
        
        Returns:
            List of suggested actions with priorities
        """
        suggestions = []
        
        if not self._current_state_id:
            return suggestions
        
        current_state = self._states[self._current_state_id]
        
        # Calculate current reward
        current_reward = self.calculate_reward()
        
        # For each action, estimate potential improvement
        for action_id in self._actions:
            q_key = self._get_q_key(self._current_state_id, action_id)
            q_value = self._q_values.get(q_key, QValue(self._current_state_id, action_id, 0.0))
            
            # Estimate improvement (difference from current reward)
            potential_reward = q_value.value
            improvement = potential_reward - current_reward
            
            suggestions.append({
                "action_id": action_id,
                "name": self._actions[action_id].name,
                "q_value": q_value.value,
                "improvement": improvement,
                "priority": improvement,
                "visit_count": q_value.visit_count
            })
        
        # Sort by improvement
        suggestions.sort(key=lambda x: x["improvement"], reverse=True)
        
        return suggestions
    
    def apply_action(self, action: Dict[str, Any]) -> bool:
        """
        Apply an action to the system.
        
        Args:
            action: Action to apply
            
        Returns:
            True if applied successfully
        """
        action_id = action.get("action_id")
        
        if action_id not in self._actions:
            return False
        
        # In a real implementation, this would actually apply the action
        # For now, we simulate it by updating state
        
        # Create new state based on action
        current_state = self.get_current_state()
        if current_state:
            new_state_id = str(datetime.now().timestamp())
            new_features = current_state.features.copy()
            
            # Simulate state change (in a real implementation, this would be based on the action)
            for key in new_features:
                new_features[key] = new_features[key] * (1 + random.uniform(-0.1, 0.1))
            
            self.add_state(new_state_id, new_features)
            
            # Record reward
            reward = self.calculate_reward(new_state_id)
            self.record_reward(self._current_state_id, action_id, reward)
            
            logger.info(
                "Action applied",
                action_id=action_id,
                reward=reward
            )
            
            return True
        
        return False
    
    def get_goal_progress(self) -> Dict[str, Any]:
        """
        Get progress toward all goals.
        
        Returns:
            Dictionary with goal progress information
        """
        overall_progress = 0.0
        total_weight = 0.0
        
        goal_progress = {}
        for goal_id, goal in self._goals.items():
            weight = self._goal_weights.get(goal_id, 1.0)
            goal_progress[goal_id] = {
                "name": goal.name,
                "current": goal.current_value,
                "target": goal.target_value,
                "progress": goal.progress,
                "achieved": goal.achieved
            }
            
            overall_progress += goal.progress * weight
            total_weight += weight
        
        if total_weight > 0:
            overall_progress /= total_weight
        
        return {
            "overall_progress": overall_progress,
            "goals": goal_progress
        }
    
    def get_info(self) -> Dict[str, Any]:
        """Get information about the goal-oriented RL system"""
        return {
            "system_type": "GoalOrientedRL",
            "goal_count": len(self._goals),
            "action_count": len(self._actions),
            "state_count": len(self._states),
            "q_value_count": len(self._q_values),
            "exploration_rate": self._exploration_rate,
            "learning_rate": self._learning_rate,
            "discount_factor": self._discount_factor
        }
