"""
GitHub signal collector for Solana ecosystem.

Collects repository activity signals including stars, commits,
PRs, issues, and contributor activity.

Supports both mock data and live API calls via GitHub API.
"""

import random
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import os


class GitHubCollector:
    """
    Collects development activity signals from GitHub.
    
    Supports:
    - Mock data (for development/testing - always works)
    - Live data via GitHub API (requires token)
    """
    
    def __init__(self, github_token: str = None, repo_limit: int = 5, use_mock: bool = None):
        """
        Initialize GitHub collector.
        
        Args:
            github_token: GitHub API token (reads from env if not provided)
            repo_limit: Maximum number of repos to track
            use_mock: Force mock data (True) or live data (False).
                     If None, reads USE_MOCK_DATA env var (default: True)
        """
        self.github_token = github_token or os.getenv("GITHUB_TOKEN")
        self.repo_limit = repo_limit
        
        # Determine if we should use mock data
        if use_mock is None:
            use_mock = os.getenv("USE_MOCK_DATA", "true").lower() == "true"
        self.use_mock = use_mock
        
        # Validate token if using live data
        if not self.use_mock and not self.github_token:
            print("⚠️  GITHUB_TOKEN not set. Falling back to mock data.")
            self.use_mock = True
        
        # Solana ecosystem repos to track
        self.tracked_repos = [
            "solana-labs/solana",
            "coral-xyz/anchor",
            "project-serum/anchor",
            "raydium-io/raydium-clmm",
            "marinade-finance/liquid-staking-program",
        ][:repo_limit]
        
    def collect(self, window_days: int = 14) -> List[Dict[str, Any]]:
        """
        Collect GitHub activity signals for the specified time window.
        
        Args:
            window_days: Number of days to collect data for
            
        Returns:
            List of signal dictionaries
        """
        if self.use_mock:
            return self._collect_mock(window_days)
        else:
            return self._collect_live(window_days)
    
    def _collect_mock(self, window_days: int) -> List[Dict[str, Any]]:
        """Collect mock GitHub signals for testing/development."""
        signals = []
        end_date = datetime.now()
        start_date = end_date - timedelta(days=window_days)
        
        # Mock data: simulate trending repo categories
        repo_categories = [
            self._mock_ai_agent_repos(start_date, end_date),
            self._mock_defi_repos(start_date, end_date),
            self._mock_gaming_repos(start_date, end_date),
            self._mock_infrastructure_repos(start_date, end_date),
        ]
        
        for repo_data in repo_categories:
            signals.extend(repo_data)
        
        return signals
    
    def _collect_live(self, window_days: int) -> List[Dict[str, Any]]:
        """Collect live GitHub signals from tracked repositories."""
        try:
            from github import Github
        except ImportError:
            print("⚠️  PyGithub not installed. Install with: pip install PyGithub")
            print("   Falling back to mock data.")
            self.use_mock = True
            return self._collect_mock(window_days)
        
        signals = []
        end_date = datetime.now()
        start_date = end_date - timedelta(days=window_days)
        
        print(f"   🌐 Fetching live GitHub data for {len(self.tracked_repos)} repositories...")
        
        try:
            g = Github(self.github_token)
            
            for repo_name in self.tracked_repos:
                try:
                    repo = g.get_repo(repo_name)
                    
                    # Get commits in time window
                    commits = repo.get_commits(since=start_date, until=end_date)
                    commit_count = commits.totalCount
                    
                    # Get recent PRs
                    prs = repo.get_pulls(state='closed', sort='updated', direction='desc')
                    pr_count = prs.totalCount
                    
                    # Get issues
                    issues = repo.get_issues(state='closed', sort='updated', direction='desc')
                    issue_count = issues.totalCount
                    
                    # Determine category based on repo name
                    category = self._categorize_repo(repo_name)
                    
                    for i in range(window_days):
                        daily_timestamp = start_date + timedelta(days=i)
                        
                        signals.append({
                            "signal_type": "github",
                            "metric": "repo_activity",
                            "value": commit_count + (pr_count // window_days) + (issue_count // window_days),
                            "timestamp": daily_timestamp,
                            "metadata": {
                                "category": category,
                                "repo": repo_name,
                                "stars": repo.stargazers_count,
                                "commits": commit_count,
                                "prs": pr_count,
                                "issues": issue_count,
                                "forks": repo.forks_count,
                                "source": "github_api"
                            }
                        })
                    
                except Exception as e:
                    print(f"   ⚠️  Error fetching {repo_name}: {e}")
                    continue
            
        except Exception as e:
            print(f"   ⚠️  GitHub API error: {e}")
            print("   Falling back to mock data.")
            self.use_mock = True
            return self._collect_mock(window_days)
        
        return signals
    
    def _categorize_repo(self, repo_name: str) -> str:
        """Categorize a repo based on its name."""
        name_lower = repo_name.lower()
        
        if any(word in name_lower for word in ["ai", "agent", "bot"]):
            return "ai_agents"
        elif any(word in name_lower for word in ["dex", "amm", "swap", "jupiter", "raydium"]):
            return "defi"
        elif any(word in name_lower for word in ["game", "gaming", "star-atlas"]):
            return "gaming"
        elif any(word in name_lower for word in ["anchor", "solana-labs"]):
            return "infrastructure"
        else:
            return "other"
    
    
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
