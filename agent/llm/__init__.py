"""
LLM client package.

Provides abstraction and implementations for LLM interactions.
"""

import os
from typing import Optional

from .base import LLMClient, LLMError
from .openai import OpenAIClient
from .local import LocalLLMClient


def get_llm_client(provider: Optional[str] = None) -> LLMClient:
    """
    Factory function to get the appropriate LLM client.
    
    Args:
        provider: LLM provider ("openai" or "local"). Reads from env if not provided.
        
    Returns:
        Configured LLM client instance
        
    Raises:
        LLMError: If provider is invalid or configuration is missing
    """
    provider = provider or os.getenv("LLM_PROVIDER", "openai")
    
    if provider == "openai":
        return OpenAIClient()
    elif provider == "local":
        return LocalLLMClient()
    else:
        raise LLMError(f"Unknown LLM provider: {provider}. Must be 'openai' or 'local'")


__all__ = ["LLMClient", "LLMError", "OpenAIClient", "LocalLLMClient", "get_llm_client"]
