"""
Onchain signal collector for Solana ecosystem.

Collects blockchain usage signals including transaction volume,
active wallets, program deployments, and TVL.

Supports both mock data and live API calls via pluggable providers.
"""

import random
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import os

from .onchain_provider import get_onchain_provider


class OnchainCollector:
    """
    Collects onchain usage signals from Solana blockchain.
    
    Supports:
    - Mock data (for development/testing - always works)
    - Live data via Helius API (recommended)
    - Live data via Solana RPC (free but slower)
    """
    
    def __init__(self, rpc_url: str = None, use_mock: bool = None, provider: str = None):
        """
        Initialize onchain collector.
        
        Args:
            rpc_url: Solana RPC endpoint (reads from env if not provided)
            use_mock: Force mock data (True) or live data (False). 
                     If None, reads USE_MOCK_DATA env var (default: True)
            provider: Onchain provider to use ("helius", "solana_rpc").
                     If None, auto-detects based on available API keys.
        """
        self.rpc_url = rpc_url or os.getenv("SOLANA_RPC_URL", "https://api.mainnet-beta.solana.com")
        
        # Determine if we should use mock data
        if use_mock is None:
            use_mock = os.getenv("USE_MOCK_DATA", "true").lower() == "true"
        self.use_mock = use_mock
        
        # Initialize live provider (only if not using mock)
        self.provider = None
        if not self.use_mock:
            try:
                self.provider = get_onchain_provider(provider)
            except ValueError as e:
                print(f"⚠️  Could not initialize live onchain provider: {e}")
                print("   Falling back to mock data")
                self.use_mock = True
    
    def collect(self, window_days: int = 14) -> List[Dict[str, Any]]:
        """
        Collect onchain signals for the specified time window.
        
        Args:
            window_days: Number of days to collect data for
            
        Returns:
            List of signal dictionaries with keys:
                - signal_type: Type of signal (e.g., "onchain")
                - metric: Specific metric name
                - value: Raw metric value
                - timestamp: When the signal was recorded
                - metadata: Additional context
        """
        if self.use_mock:
            return self._collect_mock(window_days)
        else:
            return self._collect_live(window_days)
    
    def _collect_mock(self, window_days: int) -> List[Dict[str, Any]]:
        """Collect mock onchain signals for testing/development."""
        signals = []
        end_date = datetime.now()
        start_date = end_date - timedelta(days=window_days)
        
        # Mock data: simulate various onchain metrics
        metrics = {
            "transaction_volume": self._mock_transaction_volume(start_date, end_date),
            "active_wallets": self._mock_active_wallets(start_date, end_date),
            "program_deployments": self._mock_program_deployments(start_date, end_date),
            "tvl": self._mock_tvl(start_date, end_date),
        }
        
        for metric_name, data in metrics.items():
            for entry in data:
                signals.append({
                    "signal_type": "onchain",
                    "metric": metric_name,
                    "value": entry["value"],
                    "timestamp": entry["timestamp"],
                    "metadata": entry.get("metadata", {})
                })
        
        return signals
    
    def _collect_live(self, window_days: int) -> List[Dict[str, Any]]:
        """Collect live onchain signals from configured provider."""
        try:
            # Get the provider (will auto-detect based on available API keys)
            provider = get_onchain_provider()
            
            signals = []
            end_date = datetime.now()
            start_date = end_date - timedelta(days=window_days)
            
            print(f"   🌐 Fetching live onchain data from {provider.__class__.__name__}...")
            
            # Collect different onchain metrics
            metrics = {
                "transaction_volume": provider.get_transaction_volume(start_date, end_date),
                "active_wallets": provider.get_active_wallets(start_date, end_date),
                "program_deployments": provider.get_program_deployments(start_date, end_date),
                "tvl": provider.get_tvl(start_date, end_date),
            }
            
            # Convert to signal format
            for metric_name, data in metrics.items():
                for entry in data:
                    signals.append({
                        "signal_type": "onchain",
                        "metric": metric_name,
                        "value": entry["value"],
                        "timestamp": entry["timestamp"],
                        "metadata": entry.get("metadata", {})
                    })
            
            return signals
        
        except Exception as e:
            print(f"   ⚠️  Error in live onchain collection: {e}")
            print("   Falling back to mock data")
            # Fall back to mock data on any error
            return self._collect_mock(window_days)
    
    def _mock_transaction_volume(self, start_date: datetime, end_date: datetime) -> List[Dict]:
        """Generate mock transaction volume data with trends."""
        # Simulate DeFi surge narrative
        base_volume = 50_000_000
        growth_rate = 1.15  # 15% growth (above momentum threshold)
        
        return [{
            "value": int(base_volume * (growth_rate ** (i / 7))),
            "timestamp": start_date + timedelta(days=i),
            "metadata": {"category": "defi_activity"}
        } for i in range((end_date - start_date).days)]
    
    def _mock_active_wallets(self, start_date: datetime, end_date: datetime) -> List[Dict]:
        """Generate mock active wallet data."""
        base_wallets = 1_200_000
        growth_rate = 1.12  # 12% growth (below threshold - less momentum)
        
        return [{
            "value": int(base_wallets * (growth_rate ** (i / 7))),
            "timestamp": start_date + timedelta(days=i),
            "metadata": {"category": "user_growth"}
        } for i in range((end_date - start_date).days)]
    
    def _mock_program_deployments(self, start_date: datetime, end_date: datetime) -> List[Dict]:
        """Generate mock program deployment data."""
        # Simulate AI agent deployment spike
        deployments = []
        for i in range((end_date - start_date).days):
            # Spike in AI-related programs
            if i > 7:  # Second week
                base_count = 45
                ai_programs = random.randint(15, 25)
            else:
                base_count = 30
                ai_programs = random.randint(3, 8)
            
            deployments.append({
                "value": base_count + ai_programs,
                "timestamp": start_date + timedelta(days=i),
                "metadata": {
                    "category": "program_deployments",
                    "ai_related": ai_programs,
                    "tags": ["ai", "agents"] if i > 7 else []
                }
            })
        
        return deployments
    
    def _mock_tvl(self, start_date: datetime, end_date: datetime) -> List[Dict]:
        """Generate mock TVL data."""
        base_tvl = 5_000_000_000  # $5B
        growth_rate = 1.18  # 18% growth (strong momentum)
        
        return [{
            "value": int(base_tvl * (growth_rate ** (i / 7))),
            "timestamp": start_date + timedelta(days=i),
            "metadata": {"category": "liquidity"}
        } for i in range((end_date - start_date).days)]
