"""
Signal normalization module.

Converts raw signal values into comparable normalized scores (0-1 scale).
Uses min-max normalization with configurable methods.
"""

from typing import List, Dict, Any
import numpy as np


class SignalNormalizer:
    """
    Normalizes raw signals into comparable scores.
    
    Different metrics have different scales (e.g., transaction counts vs TVL),
    so normalization is essential for fair comparison and aggregation.
    """
    
    def __init__(self, method: str = "minmax"):
        """
        Initialize normalizer.
        
        Args:
            method: Normalization method ("minmax" or "zscore")
        """
        self.method = method
        
    def normalize_signals(self, signals: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Normalize a list of signals.
        
        Adds a 'normalized_score' field to each signal based on its metric group.
        
        Args:
            signals: List of signal dictionaries
            
        Returns:
            List of signals with added 'normalized_score' field
        """
        # Group signals by (signal_type, metric) to normalize within categories
        grouped = {}
        for signal in signals:
            key = (signal["signal_type"], signal["metric"])
            if key not in grouped:
                grouped[key] = []
            grouped[key].append(signal)
        
        # Normalize each group
        normalized_signals = []
        for group_signals in grouped.values():
            normalized_group = self._normalize_group(group_signals)
            normalized_signals.extend(normalized_group)
        
        return normalized_signals
    
    def _normalize_group(self, signals: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Normalize a group of signals of the same type.
        
        Args:
            signals: List of signals with the same (signal_type, metric)
            
        Returns:
            Signals with normalized_score added
        """
        if not signals:
            return signals
        
        values = np.array([s["value"] for s in signals])
        
        if self.method == "minmax":
            normalized = self._minmax_normalize(values)
        elif self.method == "zscore":
            normalized = self._zscore_normalize(values)
        else:
            raise ValueError(f"Unknown normalization method: {self.method}")
        
        # Add normalized scores to signals
        for signal, norm_score in zip(signals, normalized):
            signal["normalized_score"] = float(norm_score)
        
        return signals
    
    def _minmax_normalize(self, values: np.ndarray) -> np.ndarray:
        """
        Min-max normalization: scales values to [0, 1].
        
        Formula: (x - min) / (max - min)
        """
        min_val = np.min(values)
        max_val = np.max(values)
        
        if max_val == min_val:
            # All values are the same - return 0.5 as neutral
            return np.full_like(values, 0.5, dtype=float)
        
        return (values - min_val) / (max_val - min_val)
    
    def _zscore_normalize(self, values: np.ndarray) -> np.ndarray:
        """
        Z-score normalization: centers around mean with unit variance.
        
        Formula: (x - mean) / std
        Then maps to [0, 1] via sigmoid approximation.
        """
        mean = np.mean(values)
        std = np.std(values)
        
        if std == 0:
            return np.full_like(values, 0.5, dtype=float)
        
        zscores = (values - mean) / std
        
        # Map to [0, 1] using sigmoid-like function
        # Clip to reasonable z-score range [-3, 3] then scale
        clipped = np.clip(zscores, -3, 3)
        normalized = (clipped + 3) / 6  # Maps [-3, 3] to [0, 1]
        
        return normalized
