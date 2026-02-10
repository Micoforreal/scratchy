"""
Narrative detection module.

Selects and ranks final narratives from signal clusters.
This is the algorithmic (non-LLM) stage that determines which narratives qualify.
"""

from typing import List, Dict, Any
import numpy as np


class NarrativeDetector:
    """
    Detects and ranks narratives from signal clusters.
    
    This is a purely algorithmic process - no LLM reasoning here.
    LLMs are only used later for labeling and explanation.
    """
    
    def __init__(self, min_signal_types: int = 2, min_momentum_score: float = 20.0, 
                 max_narratives: int = 7):
        """
        Initialize narrative detector.
        
        Args:
            min_signal_types: Minimum number of different signal types required
            min_momentum_score: Minimum momentum score to qualify
            max_narratives: Maximum narratives to output
        """
        self.min_signal_types = min_signal_types
        self.min_momentum_score = min_momentum_score
        self.max_narratives = max_narratives
        
    def detect_narratives(self, clusters: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Detect narratives from signal clusters.
        
        Filters clusters based on:
        1. Multiple signal type reinforcement (onchain + github + social)
        2. Sufficient momentum score
        3. Overall cluster quality
        
        Args:
            clusters: List of enriched clusters
            
        Returns:
            List of narrative dictionaries, ranked by strength
        """
        # Filter clusters that meet narrative criteria
        candidate_narratives = []
        
        for cluster in clusters:
            # Check if cluster meets minimum requirements
            if not self._qualifies_as_narrative(cluster):
                continue
            
            # Convert cluster to narrative format
            narrative = self._cluster_to_narrative(cluster)
            candidate_narratives.append(narrative)
        
        # Rank narratives by composite score
        ranked_narratives = self._rank_narratives(candidate_narratives)
        
        # Return top N narratives
        return ranked_narratives[:self.max_narratives]
    
    def _qualifies_as_narrative(self, cluster: Dict[str, Any]) -> bool:
        """
        Check if a cluster qualifies as a narrative.
        
        Requirements:
        1. Multiple signal types (onchain + github or social, etc.)
        2. Sufficient momentum
        3. Minimum cluster size
        
        Args:
            cluster: Cluster dictionary
            
        Returns:
            True if cluster qualifies as narrative
        """
        # Check signal type diversity
        signal_types = cluster.get("signal_types", [])
        if len(signal_types) < self.min_signal_types:
            return False
        
        # Check momentum
        avg_momentum = cluster.get("avg_momentum", 0.0)
        if avg_momentum < self.min_momentum_score:
            return False
        
        # Check cluster quality score
        cluster_score = cluster.get("cluster_score", 0.0)
        if cluster_score < 30.0:  # Arbitrary threshold for cluster quality
            return False
        
        return True
    
    def _cluster_to_narrative(self, cluster: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert a cluster into a narrative structure.
        
        Args:
            cluster: Cluster dictionary
            
        Returns:
            Narrative dictionary
        """
        # Extract key information
        keywords = cluster.get("keywords", [])
        signals = cluster.get("signals", [])
        signal_types = cluster.get("signal_types", [])
        
        # Generate initial narrative name from keywords
        # This is a simple heuristic - LLM will refine later
        narrative_name = self._generate_narrative_name(keywords)
        
        # Calculate narrative strength score
        strength_score = self._calculate_narrative_strength(cluster)
        
        return {
            "narrative_id": cluster["cluster_id"],
            "narrative_name": narrative_name,
            "keywords": keywords,
            "signal_types": signal_types,
            "signals": signals,
            "momentum_score": cluster.get("avg_momentum", 0.0),
            "cluster_score": cluster.get("cluster_score", 0.0),
            "strength_score": strength_score,
            "signal_count": len(signals),
            "evidence": self._extract_evidence(signals)
        }
    
    def _generate_narrative_name(self, keywords: List[str]) -> str:
        """
        Generate a simple narrative name from keywords.
        
        This is a placeholder - LLM will generate better names.
        
        Args:
            keywords: List of keywords
            
        Returns:
            Simple narrative name
        """
        if not keywords:
            return "unnamed_narrative"
        
        # Use top 2-3 keywords
        top_keywords = keywords[:3]
        return "_".join(top_keywords).replace(" ", "_").lower()
    
    def _calculate_narrative_strength(self, cluster: Dict[str, Any]) -> float:
        """
        Calculate overall narrative strength score (0-100).
        
        Combines:
        - Momentum score
        - Signal diversity
        - Cluster quality
        
        Args:
            cluster: Cluster dictionary
            
        Returns:
            Strength score (0-100)
        """
        momentum = cluster.get("avg_momentum", 0.0)
        cluster_score = cluster.get("cluster_score", 0.0)
        
        # Normalize momentum to 0-100 scale (assuming typical range 0-50%)
        momentum_normalized = min(momentum / 50.0 * 100, 100)
        
        # Composite score: 60% momentum, 40% cluster quality
        strength = (momentum_normalized * 0.6) + (cluster_score * 0.4)
        
        return float(min(strength, 100.0))
    
    def _extract_evidence(self, signals: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Extract key evidence from signals for narrative explanation.
        
        Args:
            signals: List of signals
            
        Returns:
            Evidence dictionary with key facts
        """
        evidence = {
            "onchain": [],
            "github": [],
            "social": []
        }
        
        for signal in signals:
            signal_type = signal["signal_type"]
            
            if signal_type not in evidence:
                continue
            
            evidence_item = {
                "metric": signal["metric"],
                "value": signal["value"],
                "momentum": signal.get("momentum_score", 0.0),
                "metadata": signal.get("metadata", {})
            }
            
            evidence[signal_type].append(evidence_item)
        
        return evidence
    
    def _rank_narratives(self, narratives: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Rank narratives by strength score.
        
        Args:
            narratives: List of narratives
            
        Returns:
            Sorted list of narratives (strongest first)
        """
        return sorted(narratives, key=lambda x: x["strength_score"], reverse=True)
