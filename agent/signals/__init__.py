"""
Signal processing package.

Provides normalization, momentum detection, and clustering functionality.
"""

from .normalize import SignalNormalizer
from .momentum import MomentumDetector
from .clustering import SignalClusterer

__all__ = ["SignalNormalizer", "MomentumDetector", "SignalClusterer"]
