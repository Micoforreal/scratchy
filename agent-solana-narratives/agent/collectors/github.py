"""
GitHub signal collector for Solana ecosystem.

Collects repository activity signals including stars, commits,
PRs, issues, and contributor activity.

Currently uses mock data - replace with real GitHub API calls for production.
"""

import random
from datetime import datetime, timedelta
from typing import Dict, List, Any
import os


class GitHubCollector:
    """
    Collects development activity signals from GitHub.
    
    In production, this would query GitHub API for Solana ecosystem repos.
    For now, generates realistic mock data representing trending topics.
    """
    
    def __init__(self, github_token: str = None, repo_limit: int = 50):
        """
        Initialize GitHub collector.
        
        Args:
            github_token: GitHub API token (reads from env if not provided)
            repo_limit: Maximum number of repos to track
        """
        self.github_token = github_token or os.getenv("GITHUB_TOKEN")
        self.repo_limit = repo_limit
        
    def collect(self, window_days: int = 14) -> List[Dict[str, Any]]:
        """
        Collect GitHub activity signals for the specified time window.
        
        Args:
            window_days: Number of days to collect data for
            
        Returns:
            List of signal dictionaries
        """
        signals = []
        end_date = datetime.now()
        start_date = end_date - timedelta(days=window_days)
        
        # Mock data: simulate trending repo categories
        # TODO: Replace with real GitHub API calls to track solana-labs and ecosystem repos
        
        repo_categories = [
            self._mock_ai_agent_repos(start_date, end_date),
            self._mock_defi_repos(start_date, end_date),
            self._mock_gaming_repos(start_date, end_date),
            self._mock_infrastructure_repos(start_date, end_date),
        ]
        
        for repo_data in repo_categories:
            signals.extend(repo_data)
        
        return signals
    
    def _mock_ai_agent_repos(self, start_date: datetime, end_date: datetime) -> List[Dict]:
        """Generate mock data for AI agent repos (hot narrative)."""
        signals = []
        
        # Simulate spike in AI agent framework activity
        for i in range((end_date - start_date).days):
            # Stars growing rapidly
            base_stars = 500 if i < 7 else 850  # Spike in second week
            
            # Commits increasing
            base_commits = 15 if i < 7 else 35
            
            signals.append({
                "signal_type": "github",
                "metric": "repo_activity",
                "value": base_stars + base_commits,
                "timestamp": start_date + timedelta(days=i),
                "metadata": {
                    "category": "ai_agents",
                    "repos": ["solana-ai-agent-kit", "eliza-solana"],
                    "stars_delta": 25 if i >= 7 else 8,
                    "commits": base_commits,
                    "contributors": 12 if i >= 7 else 6,
                    "topics": ["ai", "agents", "automation", "chatbots"]
                }
            })
        
        return signals
    
    def _mock_defi_repos(self, start_date: datetime, end_date: datetime) -> List[Dict]:
        """Generate mock data for DeFi repos."""
        signals = []
        
        for i in range((end_date - start_date).days):
            # Steady growth
            base_activity = 800
            growth = i * 15
            
            signals.append({
                "signal_type": "github",
                "metric": "repo_activity",
                "value": base_activity + growth,
                "timestamp": start_date + timedelta(days=i),
                "metadata": {
                    "category": "defi",
                    "repos": ["jupiter-core", "marinade-finance"],
                    "stars_delta": 12,
                    "commits": 28,
                    "contributors": 18,
                    "topics": ["defi", "dex", "yield", "staking"]
                }
            })
        
        return signals
    
    def _mock_gaming_repos(self, start_date: datetime, end_date: datetime) -> List[Dict]:
        """Generate mock data for gaming repos."""
        signals = []
        
        for i in range((end_date - start_date).days):
            # Moderate activity, no major spike
            base_activity = 300 + random.randint(-20, 20)
            
            signals.append({
                "signal_type": "github",
                "metric": "repo_activity",
                "value": base_activity,
                "timestamp": start_date + timedelta(days=i),
                "metadata": {
                    "category": "gaming",
                    "repos": ["solana-game-sdk", "star-atlas-dao"],
                    "stars_delta": 5,
                    "commits": 12,
                    "contributors": 8,
                    "topics": ["gaming", "nft", "metaverse"]
                }
            })
        
        return signals
    
    def _mock_infrastructure_repos(self, start_date: datetime, end_date: datetime) -> List[Dict]:
        """Generate mock data for infrastructure repos."""
        signals = []
        
        for i in range((end_date - start_date).days):
            # Consistent activity
            base_activity = 600 + i * 5
            
            signals.append({
                "signal_type": "github",
                "metric": "repo_activity",
                "value": base_activity,
                "timestamp": start_date + timedelta(days=i),
                "metadata": {
                    "category": "infrastructure",
                    "repos": ["solana", "jito-solana"],
                    "stars_delta": 8,
                    "commits": 45,
                    "contributors": 25,
                    "topics": ["validator", "rpc", "indexer", "infrastructure"]
                }
            })
        
        return signals
