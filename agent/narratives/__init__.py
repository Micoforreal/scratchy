"""
Narratives package.

Provides narrative detection, explanation, and idea generation.
"""

from .detect import NarrativeDetector
from .explain import NarrativeExplainer
from .ideas import IdeaGenerator

__all__ = ["NarrativeDetector", "NarrativeExplainer", "IdeaGenerator"]
