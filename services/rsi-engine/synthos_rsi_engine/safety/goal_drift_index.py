"""Goal Drift Index (GDI) - Multi-signal alignment drift detector"""

import numpy as np
from typing import Dict, List, Tuple
from dataclasses import dataclass
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import structlog

logger = structlog.get_logger(__name__)


@dataclass
class DriftSignal:
    """Individual drift signal measurement"""
    name: str
    value: float
    threshold: float
    status: str  # "normal", "warning", "critical"


class GoalDriftIndex:
    """
    Goal Drift Index - Multi-signal detector for alignment drift
    
    Combines semantic, lexical, structural, and distributional measures
    to detect when the system is drifting from its original goals.
    """
    
    def __init__(self, baseline_goals: List[str], config: Dict = None):
        """
        Initialize GDI with baseline goals
        
        Args:
            baseline_goals: List of original goal statements
            config: Configuration for drift detection thresholds
        """
        self.baseline_goals = baseline_goals
        self.config = config or self._default_config()
        
        # Initialize TF-IDF vectorizer for semantic analysis
        self.vectorizer = TfidfVectorizer()
        self.baseline_vectors = self.vectorizer.fit_transform(baseline_goals)
        
        # Historical drift measurements
        self.drift_history: List[Dict] = []
        
        logger.info("Goal Drift Index initialized", num_goals=len(baseline_goals))
    
    def _default_config(self) -> Dict:
        """Default configuration for drift detection"""
        return {
            "semantic_threshold": 0.2,
            "lexical_threshold": 0.3,
            "structural_threshold": 0.25,
            "distributional_threshold": 0.2,
            "overall_threshold": 0.2,
            "warning_threshold": 0.5,
            "critical_threshold": 0.7,
        }
    
    def measure_semantic_drift(self, current_goals: List[str]) -> float:
        """
        Measure semantic drift using TF-IDF and cosine similarity
        
        Args:
            current_goals: Current goal statements
            
        Returns:
            Semantic drift score (0 = no drift, 1 = maximum drift)
        """
        if not current_goals:
            return 1.0
        
        current_vectors = self.vectorizer.transform(current_goals)
        
        # Calculate cosine similarity between baseline and current
        similarities = cosine_similarity(self.baseline_vectors, current_vectors)
        
        # Drift is 1 - average similarity
        avg_similarity = np.mean(similarities)
        semantic_drift = 1.0 - avg_similarity
        
        logger.debug("Semantic drift measured", drift=semantic_drift)
        return semantic_drift
    
    def measure_lexical_drift(self, current_text: str) -> float:
        """
        Measure lexical drift using vocabulary overlap
        
        Args:
            current_text: Current text to compare
            
        Returns:
            Lexical drift score (0 = no drift, 1 = maximum drift)
        """
        baseline_text = " ".join(self.baseline_goals)
        
        baseline_vocab = set(baseline_text.lower().split())
        current_vocab = set(current_text.lower().split())
        
        if not baseline_vocab:
            return 0.0
        
        # Vocabulary overlap
        overlap = len(baseline_vocab & current_vocab) / len(baseline_vocab)
        lexical_drift = 1.0 - overlap
        
        logger.debug("Lexical drift measured", drift=lexical_drift)
        return lexical_drift
    
    def measure_structural_drift(self, current_structure: Dict) -> float:
        """
        Measure structural drift in system architecture
        
        Args:
            current_structure: Current system structure representation
            
        Returns:
            Structural drift score (0 = no drift, 1 = maximum drift)
        """
        # Compare structure with baseline (simplified)
        # In production, this would compare actual architecture
        
        if not current_structure:
            return 1.0
        
        # Placeholder: in production, implement actual structural comparison
        # This could compare module counts, dependency graphs, etc.
        structural_drift = 0.1  # Placeholder
        
        logger.debug("Structural drift measured", drift=structural_drift)
        return structural_drift
    
    def measure_distributional_drift(self, current_outputs: List[str]) -> float:
        """
        Measure distributional drift in output patterns
        
        Args:
            current_outputs: Sample of current system outputs
            
        Returns:
            Distributional drift score (0 = no drift, 1 = maximum drift)
        """
        if not current_outputs:
            return 1.0
        
        # Placeholder: in production, implement actual distribution comparison
        # This could compare output length distributions, vocabulary usage, etc.
        distributional_drift = 0.1  # Placeholder
        
        logger.debug("Distributional drift measured", drift=distributional_drift)
        return distributional_drift
    
    def calculate_gdi(
        self,
        current_goals: List[str],
        current_text: str,
        current_structure: Dict,
        current_outputs: List[str]
    ) -> Tuple[float, List[DriftSignal]]:
        """
        Calculate overall Goal Drift Index
        
        Args:
            current_goals: Current goal statements
            current_text: Current text for lexical analysis
            current_structure: Current system structure
            current_outputs: Sample of current outputs
            
        Returns:
            Tuple of (overall GDI score, list of individual drift signals)
        """
        # Measure individual drift signals
        semantic_drift = self.measure_semantic_drift(current_goals)
        lexical_drift = self.measure_lexical_drift(current_text)
        structural_drift = self.measure_structural_drift(current_structure)
        distributional_drift = self.measure_distributional_drift(current_outputs)
        
        # Create drift signals
        signals = [
            DriftSignal(
                name="semantic",
                value=semantic_drift,
                threshold=self.config["semantic_threshold"],
                status=self._get_status(semantic_drift, self.config["semantic_threshold"])
            ),
            DriftSignal(
                name="lexical",
                value=lexical_drift,
                threshold=self.config["lexical_threshold"],
                status=self._get_status(lexical_drift, self.config["lexical_threshold"])
            ),
            DriftSignal(
                name="structural",
                value=structural_drift,
                threshold=self.config["structural_threshold"],
                status=self._get_status(structural_drift, self.config["structural_threshold"])
            ),
            DriftSignal(
                name="distributional",
                value=distributional_drift,
                threshold=self.config["distributional_threshold"],
                status=self._get_status(distributional_drift, self.config["distributional_threshold"])
            ),
        ]
        
        # Calculate weighted average for overall GDI
        weights = [0.3, 0.2, 0.3, 0.2]  # Semantic and structural weighted higher
        overall_gdi = sum(s.value * w for s, w in zip(signals, weights))
        
        # Store in history
        self.drift_history.append({
            "gdi": overall_gdi,
            "signals": signals,
            "timestamp": None,  # Add timestamp in production
        })
        
        logger.info(
            "GDI calculated",
            overall_gdi=overall_gdi,
            semantic=semantic_drift,
            lexical=lexical_drift,
            structural=structural_drift,
            distributional=distributional_drift
        )
        
        return overall_gdi, signals
    
    def _get_status(self, value: float, threshold: float) -> str:
        """Get status based on value and threshold"""
        if value < threshold:
            return "normal"
        elif value < self.config["warning_threshold"]:
            return "warning"
        else:
            return "critical"
    
    def get_drift_status(self, gdi: float) -> str:
        """
        Get overall drift status based on GDI
        
        Args:
            gdi: Overall Goal Drift Index
            
        Returns:
            Status: "normal", "warning", or "critical"
        """
        if gdi < self.config["overall_threshold"]:
            return "normal"
        elif gdi < self.config["warning_threshold"]:
            return "warning"
        else:
            return "critical"
    
    def should_trigger_safety_action(self, gdi: float) -> bool:
        """
        Determine if safety action should be triggered based on GDI
        
        Args:
            gdi: Overall Goal Drift Index
            
        Returns:
            True if safety action should be triggered
        """
        status = self.get_drift_status(gdi)
        return status in ["warning", "critical"]
    
    def get_historical_trend(self, window_size: int = 10) -> Dict:
        """
        Get historical trend of drift measurements
        
        Args:
            window_size: Number of recent measurements to analyze
            
        Returns:
            Dictionary with trend analysis
        """
        if len(self.drift_history) < 2:
            return {"trend": "insufficient_data"}
        
        recent_history = self.drift_history[-window_size:]
        gdi_values = [entry["gdi"] for entry in recent_history]
        
        # Calculate trend
        if len(gdi_values) >= 2:
            trend = "increasing" if gdi_values[-1] > gdi_values[0] else "decreasing"
        else:
            trend = "stable"
        
        avg_gdi = np.mean(gdi_values)
        max_gdi = max(gdi_values)
        min_gdi = min(gdi_values)
        
        return {
            "trend": trend,
            "average": avg_gdi,
            "maximum": max_gdi,
            "minimum": min_gdi,
            "sample_size": len(gdi_values)
        }
