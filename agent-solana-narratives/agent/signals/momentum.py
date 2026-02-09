"""
Momentum detection module.

Detects acceleration and trend changes in signals over time.
Computes growth rates and identifies signals with strong momentum.
"""

from typing import List, Dict, Any
from datetime import datetime, timedelta
import numpy as np


class MomentumDetector:
    """
    Detects momentum (acceleration) in time-series signals.
    
    Compares recent performance against baseline to identify
    emerging or accelerating trends.
    """
    
    def __init__(self, threshold_pct: float = 15.0, window_days: int = 14):
        """
        Initialize momentum detector.
        
        Args:
            threshold_pct: Minimum growth percentage to qualify as momentum
            window_days: Time window for analysis
        """
        self.threshold_pct = threshold_pct
        self.window_days = window_days
        
    def detect_momentum(self, signals: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Detect momentum in signals.
        
        Adds momentum-related fields to each signal:
        - momentum_score: Growth rate as percentage
        - has_momentum: Boolean flag if above threshold
        - trend: "accelerating", "growing", "flat", or "declining"
        
        Args:
            signals: List of normalized signals
            
        Returns:
            Signals with momentum fields added
        """
        # Group by (signal_type, metric) for time-series analysis
        grouped = {}
        for signal in signals:
            key = (signal["signal_type"], signal["metric"], signal.get("metadata", {}).get("category"))
            if key not in grouped:
                grouped[key] = []
            grouped[key].append(signal)
        
        # Analyze momentum for each group
        processed_signals = []
        for group_signals in grouped.values():
            momentum_signals = self._analyze_group_momentum(group_signals)
            processed_signals.extend(momentum_signals)
        
        return processed_signals
    
    def _analyze_group_momentum(self, signals: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Analyze momentum for a group of related signals.
        
        Args:
            signals: Signals with same type/metric
            
        Returns:
            Signals with momentum analysis added
        """
        if len(signals) < 2:
            # Not enough data points for momentum
            for signal in signals:
                signal["momentum_score"] = 0.0
                signal["has_momentum"] = False
                signal["trend"] = "insufficient_data"
            return signals
        
        # Sort by timestamp
        sorted_signals = sorted(signals, key=lambda x: x["timestamp"])
        
        # Split into first half (baseline) and second half (recent)
        midpoint = len(sorted_signals) // 2
        baseline = sorted_signals[:midpoint]
        recent = sorted_signals[midpoint:]
        
        baseline_avg = np.mean([s["value"] for s in baseline])
        recent_avg = np.mean([s["value"] for s in recent])
        
        # Calculate growth rate
        if baseline_avg == 0:
            growth_pct = 0.0
        else:
            growth_pct = ((recent_avg - baseline_avg) / baseline_avg) * 100
        
        # Determine trend
        trend = self._classify_trend(growth_pct)
        has_momentum = abs(growth_pct) >= self.threshold_pct and growth_pct > 0
        
        # Add momentum data to all signals in group
        for signal in sorted_signals:
            signal["momentum_score"] = float(growth_pct)
            signal["has_momentum"] = has_momentum
            signal["trend"] = trend
            
            # Add velocity (rate of change) for recent signals
            if signal in recent:
                signal["is_recent"] = True
            else:
                signal["is_recent"] = False
        
        return sorted_signals
    
    def _classify_trend(self, growth_pct: float) -> str:
        """
        Classify trend based on growth percentage.
        
        Args:
            growth_pct: Growth percentage
            
        Returns:
            Trend classification string
        """
        if growth_pct >= self.threshold_pct * 1.5:
            return "accelerating"
        elif growth_pct >= self.threshold_pct:
            return "strong_growth"
        elif growth_pct > 5:
            return "growing"
        elif growth_pct > -5:
            return "flat"
        elif growth_pct > -self.threshold_pct:
            return "declining"
        else:
            return "sharp_decline"
    
    def aggregate_momentum(self, signals: List[Dict[str, Any]], 
                          signal_type: str = None) -> Dict[str, Any]:
        """
        Aggregate momentum statistics across signals.
        
        Args:
            signals: List of signals with momentum data
            signal_type: Optional filter by signal type
            
        Returns:
            Dictionary with aggregate momentum metrics
        """
        if signal_type:
            signals = [s for s in signals if s["signal_type"] == signal_type]
        
        if not signals:
            return {"count": 0, "avg_momentum": 0.0, "signals_with_momentum": 0}
        
        momentum_scores = [s["momentum_score"] for s in signals if "momentum_score" in s]
        has_momentum_count = sum(1 for s in signals if s.get("has_momentum", False))
        
        return {
            "count": len(signals),
            "avg_momentum": float(np.mean(momentum_scores)) if momentum_scores else 0.0,
            "max_momentum": float(np.max(momentum_scores)) if momentum_scores else 0.0,
            "signals_with_momentum": has_momentum_count,
            "momentum_rate": has_momentum_count / len(signals) if signals else 0.0
        }
