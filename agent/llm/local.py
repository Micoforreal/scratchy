"""
Local/self-hosted LLM client.

Supports HTTP-based self-hosted LLMs (e.g., Ollama, LM Studio, vLLM).
"""

import os
from typing import Optional
import requests

from .base import LLMClient, LLMError


class LocalLLMClient(LLMClient):
    """
    Client for self-hosted LLMs via HTTP.
    
    Supports common local LLM servers like Ollama, LM Studio, etc.
    Assumes OpenAI-compatible API format.
    """
    
    def __init__(self, base_url: Optional[str] = None, model: Optional[str] = None):
        """
        Initialize local LLM client.
        
        Args:
            base_url: Base URL for local LLM server (reads from env if not provided)
            model: Model name (reads from env if not provided)
        """
        self.base_url = base_url or os.getenv("LOCAL_LLM_BASE_URL", "http://localhost:11434")
        self.model = model or os.getenv("LOCAL_LLM_MODEL", "llama3")
        
        if not self.base_url:
            raise LLMError("LOCAL_LLM_BASE_URL environment variable not set")
        
        # Ensure base_url ends without trailing slash
        self.base_url = self.base_url.rstrip("/")
        
    def generate(self, prompt: str, temperature: Optional[float] = None, 
                 max_tokens: Optional[int] = None) -> str:
        """
        Generate completion using local LLM.
        
        Args:
            prompt: Input prompt
            temperature: Sampling temperature (default: 0.7)
            max_tokens: Max tokens to generate (default: 1500)
            
        Returns:
            Generated text
            
        Raises:
            LLMError: If API call fails
        """
        # Try OpenAI-compatible format first (most common)
        url = f"{self.base_url}/v1/chat/completions"
        headers = {"Content-Type": "application/json"}
        
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": temperature if temperature is not None else 0.7,
            "max_tokens": max_tokens if max_tokens is not None else 1500,
            "stream": False
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=300)
            response.raise_for_status()
            
            data = response.json()
            
            # Try OpenAI format
            if "choices" in data:
                return data["choices"][0]["message"]["content"]
            
            # Try Ollama format
            elif "response" in data:
                return data["response"]
            
            # Try simple message format
            elif "message" in data:
                return data["message"]
            
            else:
                raise LLMError(f"Unknown response format from local LLM: {data.keys()}")
                
        except requests.exceptions.RequestException as e:
            raise LLMError(f"Local LLM request failed: {str(e)}")
        except (KeyError, IndexError) as e:
            raise LLMError(f"Unexpected local LLM response format: {str(e)}")
