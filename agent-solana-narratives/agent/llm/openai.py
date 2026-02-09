"""
OpenAI-compatible LLM client.

Supports both OpenAI API and any OpenAI-compatible endpoints.
"""

import os
from typing import Optional
import requests

from .base import LLMClient, LLMError


class OpenAIClient(LLMClient):
    """
    OpenAI-compatible LLM client.
    
    Works with OpenAI API and any service that implements the same interface
    (e.g., vLLM, LM Studio, etc.)
    """
    
    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None, 
                 model: Optional[str] = None):
        """
        Initialize OpenAI client.
        
        Args:
            api_key: OpenAI API key (reads from env if not provided)
            base_url: Base URL for API (reads from env if not provided)
            model: Model name (reads from env if not provided)
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.base_url = base_url or os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        
        if not self.api_key:
            raise LLMError("OPENAI_API_KEY environment variable not set")
        
        # Ensure base_url ends without trailing slash
        self.base_url = self.base_url.rstrip("/")
        
    def generate(self, prompt: str, temperature: Optional[float] = None, 
                 max_tokens: Optional[int] = None) -> str:
        """
        Generate completion using OpenAI API.
        
        Args:
            prompt: Input prompt
            temperature: Sampling temperature (default: 0.7)
            max_tokens: Max tokens to generate (default: 1500)
            
        Returns:
            Generated text
            
        Raises:
            LLMError: If API call fails
        """
        url = f"{self.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": temperature if temperature is not None else 0.7,
            "max_tokens": max_tokens if max_tokens is not None else 1500
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=60)
            response.raise_for_status()
            
            data = response.json()
            return data["choices"][0]["message"]["content"]
            
        except requests.exceptions.RequestException as e:
            raise LLMError(f"OpenAI API request failed: {str(e)}")
        except (KeyError, IndexError) as e:
            raise LLMError(f"Unexpected API response format: {str(e)}")
