"""
Signal collectors package.

Provides collectors for onchain, GitHub, and social signals.
"""

from .onchain import OnchainCollector
from .github import GitHubCollector
from .social import SocialCollector

__all__ = ["OnchainCollector", "GitHubCollector", "SocialCollector"]
