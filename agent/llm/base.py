"""
Abstract LLM client interface.

This module provides the base abstraction for LLM interactions,
allowing the system to swap between different LLM providers.
"""

from abc import ABC, abstractmethod
from typing import Optional


class LLMClient(ABC):
    """
    Abstract base class for LLM clients.
    
    All LLM providers must implement this interface to ensure
    consistency and swappability across the system.
    """
    
    @abstractmethod
    def generate(self, prompt: str, temperature: Optional[float] = None, 
                 max_tokens: Optional[int] = None) -> str:
        """
        Generate text completion from a prompt.
        
        Args:
            prompt: The input prompt for generation
            temperature: Sampling temperature (0.0 to 1.0). Lower = more deterministic
            max_tokens: Maximum tokens to generate
            
        Returns:
            Generated text completion as a string
            
        Raises:
            LLMError: If generation fails
        """
        pass


class LLMError(Exception):
    """Custom exception for LLM-related errors."""
    pass
