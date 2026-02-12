# 📊 Mock Data vs Live Data - Complete Guide

## Current Status: **ALWAYS MOCK**

Right now, the system **100% uses mock data** with no option to switch to live data.

## 🎯 When Mock Data is Used

### ✅ Always (Current Implementation)

All three collectors **always** generate mock data:

1. **Onchain Collector** → Mock Solana blockchain data
2. **GitHub Collector** → Mock repository activity
3. **Social Collector** → Mock blog/social signals

### Why Mock Data?

Mock data is included so the system:
- ✅ Works out-of-the-box (no API setup required)
- ✅ Demonstrates the full pipeline end-to-end
- ✅ Can be tested without rate limits or costs
- ✅ Shows realistic signal patterns and narratives

## 🌐 How to Add Live Data Support

The current code is **designed** to make switching to live data easy, but you need to implement the actual API calls.

### Step 1: Add USE_MOCK_DATA Flag

Add to `.env`:
```bash
# Data source configuration
USE_MOCK_DATA=true   # Set to false for live data
```

Add to `agent/config.yaml`:
```yaml
# Data collection mode
data:
  use_mock: true  # Override with USE_MOCK_DATA env var
```

### Step 2: Modify Each Collector

For each collector (`onchain.py`, `github.py`, `social.py`), add:

```python
def __init__(self, ..., use_mock: bool = None):
    # Check environment variable
    if use_mock is None:
        use_mock = os.getenv("USE_MOCK_DATA", "true").lower() == "true"
    self.use_mock = use_mock

def collect(self, window_days: int = 14):
    if self.use_mock:
        return self._collect_mock(window_days)
    else:
        return self._collect_live(window_days)

def _collect_mock(self, window_days):
    # Existing mock code
    pass

def _collect_live(self, window_days):
    # NEW: Real API calls
    raise NotImplementedError("Live data not implemented yet")
```

### Step 3: Implement Live Data Methods

#### For Onchain Data:

**Option A: Use Helius API** (Recommended)
```python
def _collect_live(self, window_days):
    import requests
    
    # Get Helius API key from env
    helius_key = os.getenv("HELIUS_API_KEY")
    
    # Call Helius endpoints
    response = requests.get(
        f"https://api.helius.xyz/v0/addresses/stats",
        params={"api-key": helius_key}
    )
    
    data = response.json()
    # Convert to signals format...
```

**Option B: Use Solana RPC**
```python
def _collect_live(self, window_days):
    from solana.rpc.api import Client
    
    client = Client(self.rpc_url)
    
    # Get transaction count
    tx_count = client.get_transaction_count()
    
    # Convert to signals...
```

#### For GitHub Data:

```python
def _collect_live(self, window_days):
    from github import Github
    
    g = Github(self.github_token)
    
    # Track key repos
    repos = [
        "solana-labs/solana",
        "coral-xyz/anchor",
        "project-serum/anchor",
    ]
    
    signals = []
    for repo_name in repos:
        repo = g.get_repo(repo_name)
        
        # Get recent commits
        commits = repo.get_commits(since=datetime.now() - timedelta(days=window_days))
        
        signals.append({
            "signal_type": "github",
            "metric": "repo_activity",
            "value": commits.totalCount,
            "metadata": {
                "repo": repo_name,
                "stars": repo.stargazers_count,
                "commits_14d": commits.totalCount
            }
        })
    
    return signals
```

#### For Social Data:

```python
def _collect_live(self, window_days):
    import requests
    
    # Option A: Use self-hosted crawler
    if self.crawler_url:
        response = requests.post(
            f"{self.crawler_url}/crawl",
            json={"urls": self.sources}
        )
        content = response.json()
        # Parse and extract signals...
    
    # Option B: Use RSS feeds
    import feedparser
    
    signals = []
    for feed_url in self.sources:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries:
            # Extract signals from feed entries...
            pass
    
    return signals
```

## 🔀 Switching Between Mock and Live

### Via Environment Variable
```bash
# .env
USE_MOCK_DATA=false  # Use live data
```

### Via Code (main.py)
```python
# Force mock data
onchain = OnchainCollector(use_mock=True)

# Force live data
onchain = OnchainCollector(use_mock=False)

# Use environment variable (default)
onchain = OnchainCollector()
```

## 📋 Required Dependencies for Live Data

Add to `requirements.txt`:

```txt
# For live onchain data
solana>=0.30.0          # Solana RPC
# OR
requests>=2.28.0        # For Helius API

# For live GitHub data
PyGithub>=2.1.0

# For live social data
feedparser>=6.0.0       # RSS feeds
beautifulsoup4>=4.12.0  # Web scraping
# OR
requests>=2.28.0        # For crawler API
```

## 🔑 Required API Keys for Live Data

Add to `.env`:

```bash
# For live data
USE_MOCK_DATA=false

# Onchain data (choose one)
HELIUS_API_KEY=your-helius-key        # Recommended
# OR
SOLANA_RPC_URL=https://api.mainnet-beta.solana.com

# GitHub data
GITHUB_TOKEN=your-github-token

# Social data (optional)
CRAWLER_BASE_URL=http://localhost:8000
```

## 🎯 Recommended Approach

### Phase 1: Mock Data (Current - ✅ Done)
- Works out-of-the-box
- No API setup needed
- Demonstrates pipeline

### Phase 2: Add Toggle (Quick - ~1 hour)
- Add `USE_MOCK_DATA` env var
- Modify collectors to check flag
- Keep mock as default

### Phase 3: Implement Live Data (Full - ~1 day)
- Implement `_collect_live()` methods
- Add error handling
- Add rate limiting
- Test with real APIs

### Phase 4: Hybrid Mode (Advanced)
- Use live data where available
- Fall back to mock for missing data
- Log data source for each signal

## 🧪 Testing Strategy

```python
# Test with mock data (fast, free)
USE_MOCK_DATA=true python main.py

# Test with live data (slow, may cost)
USE_MOCK_DATA=false python main.py

# Test hybrid (some live, some mock)
# Implement per-collector override
```

## 📊 Data Quality Comparison

### Mock Data
✅ Fast and free
✅ Consistent results
✅ No rate limits
❌ Not real trends
❌ Static patterns

### Live Data
✅ Real ecosystem trends
✅ Actual market signals
✅ Up-to-date information
❌ Costs money (API calls)
❌ Rate limits
❌ Requires setup

## 🎯 Summary

**Current State:**
- Always uses mock data
- No live data option

**To Add Live Data:**
1. Add `USE_MOCK_DATA` env var
2. Modify collectors to check flag
3. Implement `_collect_live()` methods
4. Add required dependencies
5. Set up API keys

**Recommended:**
- Start with mock (current)
- Add toggle when ready to test with real data
- Implement live data one collector at a time
- Keep mock as fallback for development

See `EXAMPLE_MOCK_VS_LIVE_PATTERN.py` for implementation pattern!
