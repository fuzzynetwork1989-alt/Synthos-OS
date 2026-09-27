"""Meta-RSI - Self-Improving the Improvement Process"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import structlog
from datetime import datetime, timedelta
import json

logger = structlog.get_logger(__name__)


class ImprovementStrategy(Enum):
    """Strategies for self-improvement"""
    CONSERVATIVE = "conservative"  # Low-risk, incremental changes
    BALANCED = "balanced"  # Mix of risk levels
    AGGRESSIVE = "aggressive"  # Higher-risk, potentially higher reward
    ADAPTIVE = "adaptive"  # Dynamically adjusts based on success


@dataclass
class ImprovementGene:
    """A gene representing a successful improvement pattern"""
    gene_id: str
    pattern_type: str  # "prompt", "config", "code", "workflow"
    mutation_template: Dict
    success_rate: float
    avg_improvement: float
    risk_level: str
    last_used: datetime
    usage_count: int
    generation: int  # Evolutionary generation


@dataclass
class CognitiveDNA:
    """Cognitive DNA encoding successful improvement patterns"""
    genes: List[ImprovementGene] = field(default_factory=list)
    generation: int = 0
    last_evolution: Optional[datetime] = None
    fitness_score: float = 0.0


class MetaRSI:
    """
    Meta-Recursive Self-Improvement
    
    Enhances the RSI system by:
    1. Learning from past improvement cycles
    2. Encoding successful patterns as genes
    3. Evolving improvement strategies
    4. Self-optimizing the improvement process
    """
    
    def __init__(self, config: Dict = None):
        """
        Initialize Meta-RSI system
        
        Args:
            config: Configuration for Meta-RSI
        """
        self.config = config or self._default_config()
        
        # Cognitive DNA
        self.dna = CognitiveDNA()
        
        # Performance history
        self.performance_history: List[Dict] = []
        
        # Strategy performance tracking
        self.strategy_performance: Dict[str, Dict] = {
            "conservative": {"success_rate": 0.0, "avg_improvement": 0.0, "attempts": 0},
            "balanced": {"success_rate": 0.0, "avg_improvement": 0.0, "attempts": 0},
            "aggressive": {"success_rate": 0.0, "avg_improvement": 0.0, "attempts": 0},
        }
        
        # Current strategy
        self.current_strategy = ImprovementStrategy.ADAPTIVE
        
        # Learning parameters
        self.learning_rate = self.config.get("learning_rate", 0.1)
        self.exploration_rate = self.config.get("exploration_rate", 0.2)
        
        logger.info("Meta-RSI initialized", strategy=self.current_strategy.value)
    
    def _default_config(self) -> Dict:
        """Default configuration for Meta-RSI"""
        return {
            "learning_rate": 0.1,
            "exploration_rate": 0.2,
            "min_gene_success_rate": 0.6,
            "max_genes": 100,
            "evolution_interval_hours": 24,
            "strategy_switch_threshold": 0.15,
        }
    
    def analyze_cycle_performance(self, cycle_data: Dict) -> Dict:
        """
        Analyze performance of an improvement cycle
        
        Args:
            cycle_data: Data from completed improvement cycle
            
        Returns:
            Analysis results with insights
        """
        analysis = {
            "cycle_id": cycle_data.get("cycle_id"),
            "success": cycle_data.get("status") == "approved",
            "mutations_tested": cycle_data.get("mutations_tested", 0),
            "mutations_approved": cycle_data.get("mutations_approved", 0),
            "gdi_delta": cycle_data.get("gdi_after", 0) - cycle_data.get("gdi_before", 0),
            "performance_delta": cycle_data.get("performance_delta", 0),
            "timestamp": datetime.now().isoformat(),
        }
        
        # Calculate success rate
        if analysis["mutations_tested"] > 0:
            analysis["success_rate"] = analysis["mutations_approved"] / analysis["mutations_tested"]
        else:
            analysis["success_rate"] = 0.0
        
        # Store in performance history
        self.performance_history.append(analysis)
        
        # Update strategy performance
        strategy = cycle_data.get("strategy", "adaptive")
        if strategy in self.strategy_performance:
            perf = self.strategy_performance[strategy]
            perf["attempts"] += 1
            # Update moving averages
            perf["success_rate"] = self._update_moving_average(
                perf["success_rate"], analysis["success_rate"], perf["attempts"]
            )
            perf["avg_improvement"] = self._update_moving_average(
                perf["avg_improvement"], analysis["performance_delta"], perf["attempts"]
            )
        
        logger.info(
            "Cycle performance analyzed",
            cycle_id=analysis["cycle_id"],
            success_rate=analysis["success_rate"],
            performance_delta=analysis["performance_delta"]
        )
        
        return analysis
    
    def extract_genes(self, cycle_data: Dict) -> List[ImprovementGene]:
        """
        Extract improvement genes from successful cycles
        
        Args:
            cycle_data: Data from completed improvement cycle
            
        Returns:
            List of extracted genes
        """
        genes = []
        
        if cycle_data.get("status") != "approved":
            return genes
        
        # Extract genes from approved mutations
        for mutation in cycle_data.get("approved_mutations", []):
            gene = ImprovementGene(
                gene_id=f"gene_{len(self.dna.genes)}_{datetime.now().timestamp()}",
                pattern_type=mutation.get("type", "unknown"),
                mutation_template=mutation,
                success_rate=1.0,  # Initially high since it was approved
                avg_improvement=mutation.get("measured_improvement", 0.0),
                risk_level=mutation.get("risk_level", "medium"),
                last_used=datetime.now(),
                usage_count=1,
                generation=self.dna.generation,
            )
            genes.append(gene)
        
        # Add to DNA
        self.dna.genes.extend(genes)
        
        # Limit DNA size
        max_genes = self.config.get("max_genes", 100)
        if len(self.dna.genes) > max_genes:
            # Prune least successful genes
            self.dna.genes.sort(key=lambda g: g.success_rate, reverse=True)
            self.dna.genes = self.dna.genes[:max_genes]
        
        logger.info("Genes extracted", count=len(genes), total_genes=len(self.dna.genes))
        
        return genes
    
    def evolve_dna(self) -> CognitiveDNA:
        """
        Evolve the cognitive DNA through genetic operations
        
        Returns:
            Evolved DNA
        """
        if len(self.dna.genes) < 2:
            logger.info("Insufficient genes for evolution")
            return self.dna
        
        # Selection: Select best performing genes
        sorted_genes = sorted(self.dna.genes, key=lambda g: g.success_rate, reverse=True)
        top_genes = sorted_genes[:len(sorted_genes) // 2]
        
        # Crossover: Combine traits from successful genes
        new_genes = []
        for i in range(0, len(top_genes) - 1, 2):
            if i + 1 < len(top_genes):
                child = self._crossover_genes(top_genes[i], top_genes[i + 1])
                new_genes.append(child)
        
        # Mutation: Randomly modify some genes
        for gene in new_genes:
            if hash(gene.gene_id) % 10 < 3:  # 30% mutation rate
                self._mutate_gene(gene)
        
        # Update DNA
        self.dna.genes.extend(new_genes)
        self.dna.generation += 1
        self.dna.last_evolution = datetime.now()
        
        # Calculate fitness score
        self.dna.fitness_score = self._calculate_fitness()
        
        # Prune to maintain size
        max_genes = self.config.get("max_genes", 100)
        if len(self.dna.genes) > max_genes:
            self.dna.genes.sort(key=lambda g: g.success_rate, reverse=True)
            self.dna.genes = self.dna.genes[:max_genes]
        
        logger.info(
            "DNA evolved",
            generation=self.dna.generation,
            new_genes=len(new_genes),
            fitness_score=self.dna.fitness_score
        )
        
        return self.dna
    
    def recommend_strategy(self) -> ImprovementStrategy:
        """
        Recommend improvement strategy based on performance
        
        Returns:
            Recommended strategy
        """
        if self.current_strategy == ImprovementStrategy.ADAPTIVE:
            # Choose best performing strategy
            best_strategy = max(
                self.strategy_performance.items(),
                key=lambda x: x[1]["success_rate"] * x[1]["avg_improvement"]
            )
            
            # Consider exploration
            import random
            if random.random() < self.exploration_rate:
                strategies = list(ImprovementStrategy)
                strategies.remove(ImprovementStrategy.ADAPTIVE)
                return random.choice(strategies)
            
            return ImprovementStrategy(best_strategy[0])
        
        return self.current_strategy
    
    def get_mutation_suggestions(self, context: Dict) -> List[Dict]:
        """
        Get mutation suggestions based on cognitive DNA
        
        Args:
            context: Current system context
            
        Returns:
            List of suggested mutations
        """
        suggestions = []
        
        # Get relevant genes based on context
        relevant_genes = self._get_relevant_genes(context)
        
        # Generate suggestions from genes
        for gene in relevant_genes[:5]:  # Top 5 relevant genes
            suggestion = {
                "type": gene.pattern_type,
                "template": gene.mutation_template,
                "expected_success_rate": gene.success_rate,
                "expected_improvement": gene.avg_improvement,
                "risk_level": gene.risk_level,
                "gene_id": gene.gene_id,
                "generation": gene.generation,
            }
            suggestions.append(suggestion)
        
        logger.info("Mutation suggestions generated", count=len(suggestions))
        
        return suggestions
    
    def _update_moving_average(self, current_avg: float, new_value: float, count: int) -> float:
        """Update moving average with new value"""
        if count == 1:
            return new_value
        return current_avg + (new_value - current_avg) / count
    
    def _crossover_genes(self, parent1: ImprovementGene, parent2: ImprovementGene) -> ImprovementGene:
        """Create child gene through crossover"""
        child = ImprovementGene(
            gene_id=f"gene_{len(self.dna.genes)}_{datetime.now().timestamp()}",
            pattern_type=parent1.pattern_type if hash(parent1.gene_id) % 2 == 0 else parent2.pattern_type,
            mutation_template=self._merge_templates(parent1.mutation_template, parent2.mutation_template),
            success_rate=(parent1.success_rate + parent2.success_rate) / 2,
            avg_improvement=(parent1.avg_improvement + parent2.avg_improvement) / 2,
            risk_level=parent1.risk_level if parent1.success_rate > parent2.success_rate else parent2.risk_level,
            last_used=datetime.now(),
            usage_count=0,
            generation=self.dna.generation + 1,
        )
        return child
    
    def _mutate_gene(self, gene: ImprovementGene):
        """Apply random mutation to gene"""
        # Mutate success rate slightly
        import random
        gene.success_rate = max(0.0, min(1.0, gene.success_rate + random.uniform(-0.1, 0.1)))
        gene.generation = self.dna.generation + 1
    
    def _merge_templates(self, template1: Dict, template2: Dict) -> Dict:
        """Merge two mutation templates"""
        merged = template1.copy()
        for key, value in template2.items():
            if key not in merged or hash(key) % 2 == 0:
                merged[key] = value
        return merged
    
    def _calculate_fitness(self) -> float:
        """Calculate overall fitness score of DNA"""
        if not self.dna.genes:
            return 0.0
        
        total_success = sum(g.success_rate for g in self.dna.genes)
        total_improvement = sum(g.avg_improvement for g in self.dna.genes)
        
        fitness = (total_success / len(self.dna.genes)) * 0.7 + (total_improvement / len(self.dna.genes)) * 0.3
        return fitness
    
    def _get_relevant_genes(self, context: Dict) -> List[ImprovementGene]:
        """Get genes relevant to current context"""
        # Simple relevance scoring based on pattern type matching
        context_type = context.get("type", "general")
        
        scored_genes = []
        for gene in self.dna.genes:
            relevance = 1.0
            if gene.pattern_type == context_type:
                relevance = 2.0
            elif gene.pattern_type == "general":
                relevance = 1.5
            
            # Boost recently used successful genes
            days_since_use = (datetime.now() - gene.last_used).days
            if days_since_use < 7:
                relevance *= 1.2
            
            scored_genes.append((gene, relevance))
        
        # Sort by relevance and success rate
        scored_genes.sort(key=lambda x: (x[1] * x[0].success_rate), reverse=True)
        
        return [gene for gene, _ in scored_genes]
    
    def get_meta_metrics(self) -> Dict:
        """Get Meta-RSI performance metrics"""
        return {
            "dna_generation": self.dna.generation,
            "gene_count": len(self.dna.genes),
            "fitness_score": self.dna.fitness_score,
            "current_strategy": self.current_strategy.value,
            "strategy_performance": self.strategy_performance,
            "performance_history_size": len(self.performance_history),
            "last_evolution": self.dna.last_evolution.isoformat() if self.dna.last_evolution else None,
        }