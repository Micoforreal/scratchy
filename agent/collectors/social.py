"""
Social and offchain signal collector for Solana ecosystem.

Collects signals from blogs, reports, KOL posts, and curated sources.
Uses optional crawler integration for content fetching.

Supports both mock data and live API calls via crawler or RSS.
"""

import random
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import os


class SocialCollector:
    """
    Collects offchain/social signals from curated sources.
    
    Supports:
    - Mock data (for development/testing - always works)
    - Live data via self-hosted crawler (e.g., crawl4ai)
    - Live data via RSS feeds
    """
    
    def __init__(self, crawler_url: str = None, sources: List[str] = None, use_mock: bool = None):
        """
        Initialize social collector.
        
        Args:
            crawler_url: Base URL for self-hosted crawler (reads from env if not provided)
            sources: List of curated sources to monitor
            use_mock: Force mock data (True) or live data (False).
                     If None, reads USE_MOCK_DATA env var (default: True)
        """
        self.crawler_url = crawler_url or os.getenv("CRAWLER_BASE_URL")
        self.crawler_enabled = os.getenv("CRAWLER_ENABLED", "false").lower() == "true"
        self.sources = sources or [
            "https://solana.com/news",
            "https://www.helius.dev/blog",
            "https://www.coindesk.com/",
        ]
        
        # Determine if we should use mock data
        if use_mock is None:
            use_mock = os.getenv("USE_MOCK_DATA", "true").lower() == "true"
        self.use_mock = use_mock
        
        # Validate setup for live data
        if not self.use_mock and not (self.crawler_enabled and self.crawler_url):
            print("⚠️  No crawler configured and CRAWLER_ENABLED is false. Falling back to mock data.")
            self.use_mock = True
        
    def collect(self, window_days: int = 14) -> List[Dict[str, Any]]:
        """
        Collect social/offchain signals for the specified time window.
        
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
        """Collect mock social signals for testing/development."""
        return self._generate_mock_social_signals(window_days)
    
    def _collect_live(self, window_days: int) -> List[Dict[str, Any]]:
        """Collect live social signals from crawler or RSS feeds."""
        signals = []
        
        if self.crawler_enabled and self.crawler_url:
            print(f"   🌐 Fetching live social data from crawler...")
            signals.extend(self._fetch_from_crawler(window_days))
        
        # Also try RSS feeds as fallback/supplement
        print(f"   🌐 Fetching live social data from RSS feeds...")
        signals.extend(self._fetch_from_rss(window_days))
        
        if not signals:
            print("   ⚠️  No live data collected. Falling back to mock data.")
            return self._collect_mock(window_days)
        
        return signals
    
    def _fetch_from_crawler(self, window_days: int) -> List[Dict[str, Any]]:
        """Fetch content from self-hosted crawler (crawl4ai format)."""
        import requests
        
        signals = []
        end_date = datetime.now()
        start_date = end_date - timedelta(days=window_days)
        
        try:
            for source_url in self.sources:
                try:
                    # Call crawl4ai API with proper format
                    response = requests.post(
                        f"{self.crawler_url}/crawl",
                        json={
                            "urls": [source_url],
                            "crawler_config": {
                                "type": "CrawlerRunConfig",
                                "params": {
                                    "scraping_strategy": {
                                        "type": "LXMLWebScrapingStrategy",
                                        "params": {}
                                    },
                                    "stream": False  # Use batch mode
                                }
                            }
                        },
                        timeout=60
                    )
                    response.raise_for_status()
                    
                    data = response.json()
                    
                    # Handle crawl4ai response structure
                    # crawl4ai returns results in different format
                    results = data.get("results", [])
                    
                    for result in results:
                        try:
                            # Handle crawl4ai response - content can be dict or string
                            content = result.get("markdown", result.get("html", ""))
                            if isinstance(content, dict):
                                content = str(content)
                            elif not isinstance(content, str):
                                content = str(content)
                            
                            title = result.get("title", source_url)
                            if isinstance(title, dict):
                                title = str(title)
                            elif not isinstance(title, str):
                                title = str(title)
                            
                            # Extract mentions of key topics
                            mentions = self._extract_topic_mentions(title + " " + content)
                            
                            for topic, count in mentions.items():
                                signals.append({
                                    "signal_type": "social",
                                    "metric": "content_mentions",
                                    "value": count,
                                    "timestamp": end_date,
                                    "metadata": {
                                        "source": "crawl4ai",
                                        "topic": topic,
                                        "url": source_url,
                                        "title": title
                                    }
                                })
                        except Exception as e:
                            print(f"      ⚠️  Error processing crawl4ai result: {e}")
                            continue
                    
                except requests.exceptions.Timeout:
                    print(f"      ⚠️  Timeout crawling {source_url} (> 60s)")
                    continue
                except requests.exceptions.ConnectionError:
                    print(f"      ⚠️  Could not connect to crawler at {self.crawler_url}")
                    continue
                except Exception as e:
                    print(f"      ⚠️  Error crawling {source_url}: {e}")
                    continue
        
        except Exception as e:
            print(f"   ⚠️  Crawler error: {e}")
        
        return signals
    
    def _fetch_from_rss(self, window_days: int) -> List[Dict[str, Any]]:
        """Fetch content from RSS feeds."""
        try:
            import feedparser
        except ImportError:
            print("   ⚠️  feedparser not installed. Install with: pip install feedparser")
            return []
        
        signals = []
        end_date = datetime.now()
        start_date = end_date - timedelta(days=window_days)
        
        for feed_url in self.sources:
            try:
                feed = feedparser.parse(feed_url)
                
                for entry in feed.entries[:10]:  # Get last 10 entries
                    try:
                        # Extract date
                        if hasattr(entry, 'published_parsed') and entry.published_parsed:
                            pub_date = datetime.fromtimestamp(
                                __import__('time').mktime(entry.published_parsed)
                            )
                        else:
                            pub_date = end_date
                        
                        # Skip if outside time window
                        if pub_date < start_date:
                            continue
                        
                        # Extract content
                        title = entry.get('title', '')
                        summary = entry.get('summary', '')
                        content = title + " " + summary
                        
                        # Extract topic mentions
                        mentions = self._extract_topic_mentions(content)
                        
                        for topic, count in mentions.items():
                            signals.append({
                                "signal_type": "social",
                                "metric": "content_mentions",
                                "value": count,
                                "timestamp": pub_date,
                                "metadata": {
                                    "source": "rss",
                                    "topic": topic,
                                    "feed": feed_url,
                                    "title": title
                                }
                            })
                    
                    except Exception as e:
                        print(f"      ⚠️  Error processing RSS entry: {e}")
                        continue
            
            except Exception as e:
                print(f"   ⚠️  Error parsing feed {feed_url}: {e}")
                continue
        
        return signals
    
    def _extract_topic_mentions(self, text: str) -> Dict[str, int]:
        """Extract topic mentions from text."""
        topics = {
            "ai_agents": ["ai", "agent", "bot", "autonomous", "chatbot"],
            "defi": ["defi", "dex", "yield", "liquidity", "amm", "perps"],
            "gaming": ["game", "nft", "metaverse", "p2e", "play-to-earn"],
            "payments": ["payment", "usdc", "stablecoin", "merchant", "commerce"],
        }
        
        text_lower = text.lower()
        mentions = {}
        
        for topic, keywords in topics.items():
            count = sum(1 for keyword in keywords if keyword in text_lower)
            if count > 0:
                mentions[topic] = count
        
        return mentions
    
    
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
