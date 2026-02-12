"""
Abstract interface for onchain data providers.

This allows easy swapping between different data sources:
- Helius API (recommended - fast, free tier available)
- Solana RPC (free, but rate limited)
- Other analytics APIs (Flipside, DuneSQL, etc.)
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta


class OnchainProvider(ABC):
    """Abstract base class for onchain data providers."""
    
    @abstractmethod
    def get_transaction_volume(self, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        """
        Get transaction volume data for the time period.
        
        Returns list of dicts with:
        - timestamp: datetime
        - value: int (transaction count or volume)
        - metadata: dict with additional context
        """
        pass
    
    @abstractmethod
    def get_active_wallets(self, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        """Get active wallet count data."""
        pass
    
    @abstractmethod
    def get_program_deployments(self, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        """Get new program deployment data."""
        pass
    
    @abstractmethod
    def get_tvl(self, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        """Get Total Value Locked data."""
        pass


class HeliusProvider(OnchainProvider):
    """
    Helius API provider for onchain data.
    
    Recommended choice:
    - Free tier: 100 requests/second
    - No credit card required for free tier
    - Rich data including NFT, token, and account info
    
    Sign up: https://www.helius.dev/
    """
    
    def __init__(self, api_key: str):
        """Initialize with Helius API key."""
        import os
        self.api_key = api_key or os.getenv("HELIUS_API_KEY")
        if not self.api_key:
            raise ValueError("HELIUS_API_KEY environment variable not set")
        self.base_url = "https://api.helius.xyz/v0"
    
    def get_transaction_volume(self, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        """Get transaction volume from Helius API."""
        import requests
        
        results = []
        current_date = start_date
        
        while current_date <= end_date:
            try:
                # Helius endpoint for transaction stats
                url = f"{self.base_url}/transactions"
                params = {
                    "api-key": self.api_key,
                    "start": int(current_date.timestamp()),
                    "end": int((current_date + timedelta(days=1)).timestamp()),
                    "limit": 1000
                }
                
                response = requests.get(url, params=params, timeout=30)
                response.raise_for_status()
                
                data = response.json()
                
                # Aggregate transaction count
                tx_count = len(data.get("transactions", []))
                
                results.append({
                    "timestamp": current_date,
                    "value": tx_count,
                    "metadata": {
                        "source": "helius",
                        "category": "transaction_volume"
                    }
                })
                
            except Exception as e:
                print(f"⚠️  Error fetching transaction data from Helius: {e}")
                # Fall back to mock data for this day
                results.append({
                    "timestamp": current_date,
                    "value": 0,
                    "metadata": {
                        "source": "helius",
                        "category": "transaction_volume",
                        "error": str(e)
                    }
                })
            
            current_date += timedelta(days=1)
        
        return results
    
    def get_active_wallets(self, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        """Get active wallet count - approximate using account analysis."""
        import requests
        
        results = []
        current_date = start_date
        
        while current_date <= end_date:
            try:
                # Use accounts endpoint to estimate active accounts
                url = f"{self.base_url}/accounts"
                params = {
                    "api-key": self.api_key,
                    "before": int((current_date + timedelta(days=1)).timestamp()),
                    "limit": 1000
                }
                
                response = requests.get(url, params=params, timeout=30)
                response.raise_for_status()
                
                data = response.json()
                wallet_count = len(data.get("accounts", []))
                
                results.append({
                    "timestamp": current_date,
                    "value": wallet_count,
                    "metadata": {
                        "source": "helius",
                        "category": "active_wallets"
                    }
                })
                
            except Exception as e:
                print(f"⚠️  Error fetching wallet data from Helius: {e}")
                results.append({
                    "timestamp": current_date,
                    "value": 0,
                    "metadata": {
                        "source": "helius",
                        "category": "active_wallets",
                        "error": str(e)
                    }
                })
            
            current_date += timedelta(days=1)
        
        return results
    
    def get_program_deployments(self, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        """Get new program deployments from Helius API."""
        import requests
        
        results = []
        current_date = start_date
        
        while current_date <= end_date:
            try:
                # Get programs deployed on this date
                url = f"{self.base_url}/programs"
                params = {
                    "api-key": self.api_key,
                    "created_after": int(current_date.timestamp()),
                    "created_before": int((current_date + timedelta(days=1)).timestamp()),
                    "limit": 1000
                }
                
                response = requests.get(url, params=params, timeout=30)
                response.raise_for_status()
                
                data = response.json()
                program_count = len(data.get("programs", []))
                
                # Check for AI-related programs in metadata
                ai_programs = sum(
                    1 for prog in data.get("programs", [])
                    if any(tag in str(prog).lower() for tag in ["ai", "agent", "bot"])
                )
                
                results.append({
                    "timestamp": current_date,
                    "value": program_count,
                    "metadata": {
                        "source": "helius",
                        "category": "program_deployments",
                        "ai_related": ai_programs,
                        "tags": ["ai", "agents"] if ai_programs > 0 else []
                    }
                })
                
            except Exception as e:
                print(f"⚠️  Error fetching program data from Helius: {e}")
                results.append({
                    "timestamp": current_date,
                    "value": 0,
                    "metadata": {
                        "source": "helius",
                        "category": "program_deployments",
                        "error": str(e)
                    }
                })
            
            current_date += timedelta(days=1)
        
        return results
    
    def get_tvl(self, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        """Get TVL data - requires additional API calls or external data."""
        # Note: Helius doesn't directly provide TVL data
        # You would need to aggregate from DeFi program accounts
        results = []
        current_date = start_date
        
        while current_date <= end_date:
            try:
                # Get all accounts and filter for DeFi programs
                import requests
                
                url = f"{self.base_url}/accounts"
                params = {
                    "api-key": self.api_key,
                    "before": int((current_date + timedelta(days=1)).timestamp()),
                    "limit": 5000
                }
                
                response = requests.get(url, params=params, timeout=30)
                response.raise_for_status()
                
                data = response.json()
                
                # Approximate TVL by summing account balances
                # This is a rough estimate - real TVL calculation is more complex
                tvl = sum(
                    float(acc.get("lamports", 0)) / 1e9  # Convert lamports to SOL
                    for acc in data.get("accounts", [])
                )
                
                results.append({
                    "timestamp": current_date,
                    "value": int(tvl * 150),  # Approximate SOL to USD (adjust as needed)
                    "metadata": {
                        "source": "helius",
                        "category": "tvl",
                        "note": "Approximate - based on account balances"
                    }
                })
                
            except Exception as e:
                print(f"⚠️  Error fetching TVL data from Helius: {e}")
                results.append({
                    "timestamp": current_date,
                    "value": 0,
                    "metadata": {
                        "source": "helius",
                        "category": "tvl",
                        "error": str(e)
                    }
                })
            
            current_date += timedelta(days=1)
        
        return results


class SolanaRPCProvider(OnchainProvider):
    """
    Solana RPC provider for onchain data.
    
    Free option but:
    - Rate limited (~40 requests/10 seconds)
    - Less rich data than Helius
    - Slower responses
    
    Can use: https://api.mainnet-beta.solana.com (rate limited)
    Or: https://api.rpcpool.com (better, but less free tier)
    """
    
    def __init__(self, rpc_url: str = None):
        """Initialize with RPC endpoint."""
        import os
        self.rpc_url = rpc_url or os.getenv("SOLANA_RPC_URL", "https://api.mainnet-beta.solana.com")
    
    def get_transaction_volume(self, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        """Get transaction volume via RPC (slow, not recommended for production)."""
        import requests
        import time
        
        results = []
        current_date = start_date
        
        while current_date <= end_date:
            try:
                # Use getTransactionCount as proxy for volume
                payload = {
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": "getTransactionCount",
                    "params": []
                }
                
                response = requests.post(self.rpc_url, json=payload, timeout=30)
                response.raise_for_status()
                
                data = response.json()
                tx_count = data.get("result", 0)
                
                results.append({
                    "timestamp": current_date,
                    "value": tx_count,
                    "metadata": {
                        "source": "solana_rpc",
                        "category": "transaction_volume"
                    }
                })
                
                # Respect rate limits
                time.sleep(0.5)
                
            except Exception as e:
                print(f"⚠️  Error fetching transaction data from RPC: {e}")
                results.append({
                    "timestamp": current_date,
                    "value": 0,
                    "metadata": {
                        "source": "solana_rpc",
                        "category": "transaction_volume",
                        "error": str(e)
                    }
                })
            
            current_date += timedelta(days=1)
        
        return results
    
    def get_active_wallets(self, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        """Get active wallet count via RPC (very slow, not recommended)."""
        # RPC doesn't provide direct wallet count
        # Would need to query all accounts and filter
        print("⚠️  RPC provider doesn't efficiently support active_wallets queries")
        return [{
            "timestamp": start_date + timedelta(days=i),
            "value": 0,
            "metadata": {
                "source": "solana_rpc",
                "category": "active_wallets",
                "note": "Not efficiently available via RPC"
            }
        } for i in range((end_date - start_date).days)]
    
    def get_program_deployments(self, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        """Get program deployments via RPC (very slow)."""
        import requests
        import time
        
        results = []
        current_date = start_date
        
        while current_date <= end_date:
            try:
                # Get all programs is expensive - approximate
                payload = {
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": "getProgramAccounts",
                    "params": [
                        "11111111111111111111111111111111",  # System program
                        {
                            "encoding": "base64",
                            "filters": [
                                {"dataSize": 0}
                            ]
                        }
                    ]
                }
                
                response = requests.post(self.rpc_url, json=payload, timeout=60)
                response.raise_for_status()
                
                data = response.json()
                program_count = len(data.get("result", []))
                
                results.append({
                    "timestamp": current_date,
                    "value": program_count,
                    "metadata": {
                        "source": "solana_rpc",
                        "category": "program_deployments"
                    }
                })
                
                time.sleep(1.0)  # Respect rate limits
                
            except Exception as e:
                print(f"⚠️  Error fetching program data from RPC: {e}")
                results.append({
                    "timestamp": current_date,
                    "value": 0,
                    "metadata": {
                        "source": "solana_rpc",
                        "category": "program_deployments",
                        "error": str(e)
                    }
                })
            
            current_date += timedelta(days=1)
        
        return results
    
    def get_tvl(self, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        """Get TVL via RPC (very slow and imprecise)."""
        print("⚠️  RPC provider doesn't efficiently support TVL queries")
        return [{
            "timestamp": start_date + timedelta(days=i),
            "value": 0,
            "metadata": {
                "source": "solana_rpc",
                "category": "tvl",
                "note": "Not efficiently available via RPC"
            }
        } for i in range((end_date - start_date).days)]


def get_onchain_provider(provider_name: str = None, **kwargs) -> OnchainProvider:
    """
    Factory function to get the appropriate onchain data provider.
    
    Args:
        provider_name: "helius" (recommended), "solana_rpc", or None (auto-detect)
        **kwargs: Arguments to pass to provider constructor
        
    Returns:
        Configured OnchainProvider instance
    """
    import os
    
    if provider_name is None:
        # Auto-detect based on available API keys
        if os.getenv("HELIUS_API_KEY"):
            provider_name = "helius"
        elif os.getenv("SOLANA_RPC_URL"):
            provider_name = "solana_rpc"
        else:
            raise ValueError(
                "No onchain provider configured. "
                "Set HELIUS_API_KEY (recommended) or SOLANA_RPC_URL"
            )
    
    if provider_name == "helius":
        return HeliusProvider(**kwargs)
    elif provider_name == "solana_rpc":
        return SolanaRPCProvider(**kwargs)
    else:
        raise ValueError(f"Unknown onchain provider: {provider_name}")
