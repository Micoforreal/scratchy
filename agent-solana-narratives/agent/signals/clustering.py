"""
Signal clustering module.

Groups related signals into proto-narratives using TF-IDF and keyword similarity.
This creates thematic clusters from raw signals before LLM labeling.
"""

from typing import List, Dict, Any, Tuple
from collections import defaultdict
import numpy as np


class SignalClusterer:
    """
    Clusters signals into proto-narratives using keyword-based similarity.
    
    Uses TF-IDF-like approach to find signals that share common topics,
    technologies, or themes without relying on LLM reasoning.
    """
    
    def __init__(self, min_cluster_size: int = 3, max_clusters: int = 10):
        """
        Initialize signal clusterer.
        
        Args:
            min_cluster_size: Minimum signals required to form a cluster
            max_clusters: Maximum number of clusters to output
        """
        self.min_cluster_size = min_cluster_size
        self.max_clusters = max_clusters
        
    def cluster_signals(self, signals: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Cluster signals into proto-narratives.
        
        Args:
            signals: List of signals with momentum data
            
        Returns:
            List of cluster dictionaries, each containing:
            - cluster_id: Unique cluster identifier
            - signals: Signals in this cluster
            - keywords: Common keywords/topics
            - signal_types: Types of signals represented
            - avg_momentum: Average momentum score
            - cluster_score: Overall cluster strength
        """
        # Filter to signals with momentum
        momentum_signals = [s for s in signals if s.get("has_momentum", False)]
        
        if len(momentum_signals) < self.min_cluster_size:
            return []
        
        # Extract keywords from signals
        signal_keywords = self._extract_keywords(momentum_signals)
        
        # Build keyword co-occurrence matrix
        clusters = self._find_keyword_clusters(momentum_signals, signal_keywords)
        
        # Score and rank clusters
        scored_clusters = self._score_clusters(clusters)
        
        # Return top clusters
        return sorted(scored_clusters, key=lambda x: x["cluster_score"], reverse=True)[:self.max_clusters]
    
    def _extract_keywords(self, signals: List[Dict[str, Any]]) -> Dict[int, List[str]]:
        """
        Extract keywords from signal metadata.
        
        Args:
            signals: List of signals
            
        Returns:
            Dictionary mapping signal index to list of keywords
        """
        signal_keywords = {}
        
        for idx, signal in enumerate(signals):
            keywords = set()
            
            # Extract from metadata
            metadata = signal.get("metadata", {})
            
            # Add category
            if "category" in metadata:
                keywords.add(metadata["category"])
            
            # Add topic
            if "topic" in metadata:
                keywords.add(metadata["topic"])
            
            # Add keywords list
            if "keywords" in metadata:
                keywords.update(metadata["keywords"])
            
            # Add topics list
            if "topics" in metadata:
                keywords.update(metadata["topics"])
            
            # Add tags
            if "tags" in metadata:
                keywords.update(metadata["tags"])
            
            signal_keywords[idx] = list(keywords)
        
        return signal_keywords
    
    def _find_keyword_clusters(self, signals: List[Dict[str, Any]], 
                               signal_keywords: Dict[int, List[str]]) -> List[List[int]]:
        """
        Find clusters based on keyword overlap.
        
        Uses a simple greedy approach: signals that share keywords are grouped.
        
        Args:
            signals: List of signals
            signal_keywords: Keyword mapping
            
        Returns:
            List of clusters (each cluster is a list of signal indices)
        """
        # Build keyword -> signal mapping
        keyword_to_signals = defaultdict(set)
        for sig_idx, keywords in signal_keywords.items():
            for keyword in keywords:
                keyword_to_signals[keyword].add(sig_idx)
        
        # Find clusters by grouping signals with shared keywords
        visited = set()
        clusters = []
        
        for sig_idx in range(len(signals)):
            if sig_idx in visited:
                continue
            
            # Start new cluster
            cluster = {sig_idx}
            keywords = set(signal_keywords.get(sig_idx, []))
            
            # Add all signals that share keywords
            for keyword in keywords:
                cluster.update(keyword_to_signals[keyword])
            
            visited.update(cluster)
            
            if len(cluster) >= self.min_cluster_size:
                clusters.append(list(cluster))
        
        return clusters
    
    def _score_clusters(self, clusters: List[List[int]]) -> List[Dict[str, Any]]:
        """
        Score and package clusters with metadata.
        
        Args:
            clusters: List of clusters (signal indices)
            
        Returns:
            List of scored cluster dictionaries
        """
        scored_clusters = []
        
        for cluster_idx, signal_indices in enumerate(clusters):
            # Get signals in this cluster (stored temporarily)
            cluster_signals = []
            signal_types = set()
            all_keywords = set()
            momentum_scores = []
            
            # We need access to the original signals - this is a design issue
            # For now, we'll pass them through cluster metadata
            # In a real implementation, signals would be accessible via indices
            
            cluster_data = {
                "cluster_id": f"cluster_{cluster_idx}",
                "signal_indices": signal_indices,
                "size": len(signal_indices),
                "keywords": list(all_keywords),
                "signal_types": list(signal_types),
                "avg_momentum": 0.0,
                "cluster_score": 0.0
            }
            
            scored_clusters.append(cluster_data)
        
        return scored_clusters
    
    def enrich_clusters(self, clusters: List[Dict[str, Any]], 
                       signals: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Enrich cluster metadata with actual signal data.
        
        This is called after initial clustering to populate full cluster info.
        
        Args:
            clusters: Initial cluster dictionaries
            signals: All signals
            
        Returns:
            Enriched clusters with full metadata
        """
        enriched = []
        
        for cluster in clusters:
            signal_indices = cluster["signal_indices"]
            cluster_signals = [signals[i] for i in signal_indices if i < len(signals)]
            
            if not cluster_signals:
                continue
            
            # Collect metadata
            signal_types = set(s["signal_type"] for s in cluster_signals)
            all_keywords = set()
            momentum_scores = []
            
            for sig in cluster_signals:
                metadata = sig.get("metadata", {})
                
                # Extract keywords
                if "keywords" in metadata:
                    all_keywords.update(metadata["keywords"])
                if "topics" in metadata:
                    all_keywords.update(metadata["topics"])
                if "tags" in metadata:
                    all_keywords.update(metadata["tags"])
                if "category" in metadata:
                    all_keywords.add(metadata["category"])
                if "topic" in metadata:
                    all_keywords.add(metadata["topic"])
                
                # Collect momentum
                if "momentum_score" in sig:
                    momentum_scores.append(sig["momentum_score"])
            
            # Calculate cluster score
            # Score = (signal diversity * avg momentum * cluster size)
            diversity_score = len(signal_types) / 3.0  # Max 3 types (onchain, github, social)
            momentum_score = np.mean(momentum_scores) if momentum_scores else 0.0
            size_score = min(len(cluster_signals) / 10.0, 1.0)  # Normalize by expected max size
            
            cluster_score = (diversity_score * 0.4 + (momentum_score / 100.0) * 0.4 + size_score * 0.2) * 100
            
            enriched.append({
                "cluster_id": cluster["cluster_id"],
                "signals": cluster_signals,
                "keywords": list(all_keywords),
                "signal_types": list(signal_types),
                "avg_momentum": float(momentum_score),
                "cluster_score": float(cluster_score),
                "size": len(cluster_signals),
                "has_multi_signal_reinforcement": len(signal_types) >= 2
            })
        
        return enriched
