"""
Example: How to modify collectors to support both mock and live data

This shows the pattern you should follow for each collector.
"""

import os
from typing import List, Dict, Any

class OnchainCollector:
    """Modified to support both mock and live data."""
    
    def __init__(self, rpc_url: str = None, use_mock: bool = None):
        self.rpc_url = rpc_url or os.getenv("SOLANA_RPC_URL")
        # Check environment variable if not explicitly set
        if use_mock is None:
            use_mock = os.getenv("USE_MOCK_DATA", "true").lower() == "true"
        self.use_mock = use_mock
        
    def collect(self, window_days: int = 14) -> List[Dict[str, Any]]:
        """Collect signals - routes to mock or live based on config."""
        if self.use_mock:
            print("   📊 Using MOCK onchain data")
            return self._collect_mock(window_days)
        else:
            print("   🌐 Using LIVE onchain data")
            return self._collect_live(window_days)
    
    def _collect_mock(self, window_days: int) -> List[Dict[str, Any]]:
        """Mock data collection (current implementation)."""
        signals = []
        # ... existing mock code ...
        return signals
    
    def _collect_live(self, window_days: int) -> List[Dict[str, Any]]:
        """Live data collection from Solana RPC."""
        signals = []
        
        # Example: Real API calls
        # from solana.rpc.api import Client
        # client = Client(self.rpc_url)
        # 
        # # Get transaction count
        # response = client.get_transaction_count()
        # tx_count = response['result']
        #
        # signals.append({
        #     "signal_type": "onchain",
        #     "metric": "transaction_volume",
        #     "value": tx_count,
        #     "timestamp": datetime.now(),
        #     "metadata": {"source": "solana_rpc"}
        # })
        
        raise NotImplementedError("Live data collection not yet implemented")
        # return signals


class GitHubCollector:
    """Modified to support both mock and live data."""
    
    def __init__(self, github_token: str = None, use_mock: bool = None):
        self.github_token = github_token or os.getenv("GITHUB_TOKEN")
        if use_mock is None:
            use_mock = os.getenv("USE_MOCK_DATA", "true").lower() == "true"
        self.use_mock = use_mock
        
    def collect(self, window_days: int = 14) -> List[Dict[str, Any]]:
        """Collect signals - routes to mock or live based on config."""
        if self.use_mock:
            print("   📊 Using MOCK GitHub data")
            return self._collect_mock(window_days)
        else:
            print("   🌐 Using LIVE GitHub data")
            return self._collect_live(window_days)
    
    def _collect_mock(self, window_days: int) -> List[Dict[str, Any]]:
        """Mock data (current implementation)."""
        signals = []
        # ... existing mock code ...
        return signals
    
    def _collect_live(self, window_days: int) -> List[Dict[str, Any]]:
        """Live data from GitHub API."""
        signals = []
        
        # Example: Real GitHub API calls
        # from github import Github
        # g = Github(self.github_token)
        #
        # # Track Solana repos
        # repos = [
        #     "solana-labs/solana",
        #     "coral-xyz/anchor",
        #     # etc...
        # ]
        #
        # for repo_name in repos:
        #     repo = g.get_repo(repo_name)
        #     signals.append({
        #         "signal_type": "github",
        #         "metric": "repo_activity",
        #         "value": repo.stargazers_count,
        #         "timestamp": datetime.now(),
        #         "metadata": {
        #             "repo": repo_name,
        #             "stars": repo.stargazers_count,
        #             "forks": repo.forks_count
        #         }
        #     })
        
        raise NotImplementedError("Live data collection not yet implemented")
        # return signals


class SocialCollector:
    """Modified to support both mock and live data."""
    
    def __init__(self, crawler_url: str = None, use_mock: bool = None):
        self.crawler_url = crawler_url or os.getenv("CRAWLER_BASE_URL")
        if use_mock is None:
            use_mock = os.getenv("USE_MOCK_DATA", "true").lower() == "true"
        self.use_mock = use_mock
        
    def collect(self, window_days: int = 14) -> List[Dict[str, Any]]:
        """Collect signals - routes to mock or live based on config."""
        if self.use_mock:
            print("   📊 Using MOCK social data")
            return self._collect_mock(window_days)
        else:
            print("   🌐 Using LIVE social data")
            return self._collect_live(window_days)
    
    def _collect_mock(self, window_days: int) -> List[Dict[str, Any]]:
        """Mock data (current implementation)."""
        return self._generate_mock_social_signals(window_days)
    
    def _collect_live(self, window_days: int) -> List[Dict[str, Any]]:
        """Live data from crawler or RSS."""
        signals = []
        
        # Example: Real crawler calls
        # import requests
        #
        # sources = [
        #     "https://solana.com/news",
        #     "https://www.helius.dev/blog",
        # ]
        #
        # for source_url in sources:
        #     response = requests.post(
        #         f"{self.crawler_url}/crawl",
        #         json={"url": source_url}
        #     )
        #     content = response.json()
        #     # Parse content and extract signals...
        
        raise NotImplementedError("Live data collection not yet implemented")
        # return signals


# Usage in main.py would be:
# onchain = OnchainCollector(use_mock=True)   # Force mock
# onchain = OnchainCollector(use_mock=False)  # Force live
# onchain = OnchainCollector()                # Use USE_MOCK_DATA env var
