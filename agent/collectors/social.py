"""
Social and offchain signal collector for Solana ecosystem.

Collects signals from blogs, reports, KOL posts, and curated sources.
Uses optional crawler integration for content fetching.

Currently uses mock data - replace with real crawler/RSS integration for production.
"""

import random
from datetime import datetime, timedelta
from typing import Dict, List, Any
import os


class SocialCollector:
    """
    Collects offchain/social signals from curated sources.
    
    In production, this would integrate with a self-hosted crawler (e.g., crawl4ai)
    or RSS feeds. For now, generates realistic mock data.
    """
    
    def __init__(self, crawler_url: str = None, sources: List[str] = None):
        """
        Initialize social collector.
        
        Args:
            crawler_url: Base URL for self-hosted crawler (reads from env if not provided)
            sources: List of curated sources to monitor
        """
        self.crawler_url = crawler_url or os.getenv("CRAWLER_BASE_URL")
        self.crawler_enabled = os.getenv("CRAWLER_ENABLED", "false").lower() == "true"
        self.sources = sources or [
            "https://solana.com/news",
            "https://www.helius.dev/blog",
            "placeholder-kol-feed"
        ]
        
    def collect(self, window_days: int = 14) -> List[Dict[str, Any]]:
        """
        Collect social/offchain signals for the specified time window.
        
        Args:
            window_days: Number of days to collect data for
            
        Returns:
            List of signal dictionaries
        """
        if self.crawler_enabled and self.crawler_url:
            # TODO: Implement real crawler integration
            # For now, fall back to mock data
            pass
        
        return self._generate_mock_social_signals(window_days)
    
    def _generate_mock_social_signals(self, window_days: int) -> List[Dict[str, Any]]:
        """
        Generate mock social signals representing trending narratives.
        
        This simulates content from blogs, reports, and social media
        showing discourse around emerging topics.
        """
        signals = []
        end_date = datetime.now()
        start_date = end_date - timedelta(days=window_days)
        
        # Mock trending topics with varying momentum
        topics = {
            "ai_agents": {
                "mentions": [5, 6, 8, 12, 15, 22, 30, 35, 42, 48, 55, 62, 70, 75],  # Strong growth
                "sentiment": "positive",
                "keywords": ["AI agents", "autonomous trading", "chatbots", "automation"],
            },
            "defi_innovation": {
                "mentions": [20, 22, 21, 23, 25, 27, 28, 30, 31, 33, 35, 36, 38, 40],  # Steady growth
                "sentiment": "positive",
                "keywords": ["DeFi", "yield", "liquidity", "AMM", "perps"],
            },
            "gaming": {
                "mentions": [10, 11, 9, 10, 12, 11, 10, 9, 11, 10, 12, 11, 10, 9],  # Flat
                "sentiment": "neutral",
                "keywords": ["gaming", "NFT", "play-to-earn", "metaverse"],
            },
            "payments": {
                "mentions": [8, 9, 11, 13, 16, 20, 24, 28, 32, 36, 40, 44, 48, 52],  # Growing
                "sentiment": "positive",
                "keywords": ["payments", "USDC", "stablecoin", "merchant adoption"],
            }
        }
        
        for day_idx in range(window_days):
            current_date = start_date + timedelta(days=day_idx)
            
            for topic_name, topic_data in topics.items():
                # Get mentions for this day
                mentions = topic_data["mentions"][day_idx] if day_idx < len(topic_data["mentions"]) else topic_data["mentions"][-1]
                
                signals.append({
                    "signal_type": "social",
                    "metric": "topic_mentions",
                    "value": mentions,
                    "timestamp": current_date,
                    "metadata": {
                        "topic": topic_name,
                        "sentiment": topic_data["sentiment"],
                        "keywords": topic_data["keywords"],
                        "sources": self._mock_sources(mentions),
                        "engagement": random.randint(100, 1000) * mentions,
                    }
                })
        
        return signals
    
    def _mock_sources(self, mention_count: int) -> List[Dict[str, str]]:
        """Generate mock source attributions."""
        source_types = ["blog_post", "twitter_thread", "research_report", "podcast"]
        sources = []
        
        for _ in range(min(mention_count // 3, 10)):  # Cap at 10 sources
            sources.append({
                "type": random.choice(source_types),
                "title": f"Mock content about Solana trends",
                "url": "https://example.com/mock",
                "author": f"mock_kol_{random.randint(1, 50)}"
            })
        
        return sources
    
    def fetch_with_crawler(self, url: str) -> Dict[str, Any]:
        """
        Fetch content using self-hosted crawler.
        
        This is a placeholder for future crawler integration.
        
        Args:
            url: URL to crawl
            
        Returns:
            Crawled content and metadata
        """
        if not self.crawler_enabled or not self.crawler_url:
            raise NotImplementedError("Crawler is not enabled")
        
        # TODO: Implement actual crawler HTTP calls
        # Example:
        # response = requests.post(f"{self.crawler_url}/crawl", json={"url": url})
        # return response.json()
        
        return {
            "url": url,
            "content": "Mock crawled content",
            "timestamp": datetime.now().isoformat()
        }
