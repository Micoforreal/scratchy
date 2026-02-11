"""
Onchain signal collector for Solana ecosystem.

Collects blockchain usage signals including transaction volume,
active wallets, program deployments, and TVL.

Currently uses mock data - replace with real Solana RPC calls for production.
"""

import random
from datetime import datetime, timedelta
from typing import Dict, List, Any
import os


class OnchainCollector:
    """
    Collects onchain usage signals from Solana blockchain.
    
    In production, this would query Solana RPC endpoints, block explorers,
    or analytics APIs. For now, generates realistic mock data.
    """
    
    def __init__(self, rpc_url: str = None):
        """
        Initialize onchain collector.
        
        Args:
            rpc_url: Solana RPC endpoint (reads from env if not provided)
        """
        self.rpc_url = rpc_url or os.getenv("SOLANA_RPC_URL", "https://api.mainnet-beta.solana.com")
        
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
        signals = []
        end_date = datetime.now()
        start_date = end_date - timedelta(days=window_days)
        
        # Mock data: simulate various onchain metrics
        # TODO: Replace with real Solana RPC/analytics API calls
        
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
