# 🔄 Live Data Integration Guide

This document explains how to use the live API integrations in the Solana Narrative Detection Agent.

## Quick Start: Switch to Live Data

### 1. Update `.env` file

```bash
# Enable live data mode
USE_MOCK_DATA=false

# Choose ONE onchain provider:
# Option A: Helius API (Recommended)
HELIUS_API_KEY=your-helius-api-key

# Option B: Solana RPC
SOLANA_RPC_URL=https://api.mainnet-beta.solana.com

# GitHub API (for live repository data)
GITHUB_TOKEN=your-github-personal-access-token
```

### 2. Install Optional Dependencies

```bash
# Install live data support
pip install PyGithub feedparser

# Optional: If using Solana RPC
pip install solana
```

### 3. Run with Live Data

```bash
cd agent
python main.py
```

You'll see output like:
```
Data Mode: 🌐 LIVE
   Collecting onchain signals...
   🌐 Fetching live onchain data from HeliusProvider...
   ✅ Collected XX onchain signals
```

---

## Data Source Options

### 📊 Mock Data (Default)

**Best for:** Development, testing, demonstrations

- ✅ Always works - no API setup needed
- ✅ Fast execution
- ✅ Consistent/reproducible results
- ❌ Not real market data
- ❌ Static patterns

**Enable:**
```bash
USE_MOCK_DATA=true  # Default
python main.py
```

---

### 🌐 Live Data

**Best for:** Production, real market analysis

- ✅ Real ecosystem trends
- ✅ Actual on-chain metrics
- ✅ Current development activity
- ❌ Requires API setup
- ❌ API rate limits/costs

---

## Onchain Data Providers

### Option 1: Helius API ⭐ (Recommended)

**Why choose Helius:**
- Fast API responses
- Rich data (NFTs, tokens, programs, accounts)
- Free tier: 100 requests/second
- No credit card needed for sign-up
- Better data accuracy than RPC

**Setup:**

1. Sign up at https://www.helius.dev/
2. Create an API key
3. Add to `.env`:
   ```bash
   HELIUS_API_KEY=your-key-here
   ```

4. Update `USE_MOCK_DATA=false` in `.env`

**Features:**
- Transaction volume tracking
- Active wallet detection
- Program deployment monitoring
- TVL estimation (via account balances)

**Rate Limits:**
- Free tier: 100 requests/second
- Good for production use

---

### Option 2: Solana RPC

**Why choose Solana RPC:**
- Completely free
- No sign-up required
- Direct blockchain access
- Self-hostable

**Setup:**

1. Use default: `https://api.mainnet-beta.solana.com`
2. Or self-host a node
3. Add to `.env`:
   ```bash
   SOLANA_RPC_URL=https://api.mainnet-beta.solana.com
   ```

4. Install Solana SDK:
   ```bash
   pip install solana
   ```

5. Update `USE_MOCK_DATA=false` in `.env`

**Limitations:**
- Rate limited (~40 req/10 seconds on public RPC)
- Slower than Helius
- Limited query capabilities
- Not all metrics available efficiently

**Note:** We recommend Helius for production use.

---

## GitHub Data Integration

Collects real repository activity for Solana ecosystem projects.

**Setup:**

1. Go to https://github.com/settings/tokens
2. Create a Personal Access Token with `repo` scope
3. Add to `.env`:
   ```bash
   GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxx
   ```

4. Install PyGithub:
   ```bash
   pip install PyGithub
   ```

5. Update `USE_MOCK_DATA=false` in `.env`

**Tracked Repositories:**
- `solana-labs/solana` - Core Solana
- `coral-xyz/anchor` - Anchor framework
- `project-serum/anchor` - Serum Anchor
- `raydium-io/raydium-clmm` - Raydium DEX
- `marinade-finance/liquid-staking-program` - Marinade staking

**Data Collected:**
- Commit counts
- Pull request activity
- Issue tracking
- Star count changes
- Contributor activity
- Repository trends

**Auto-categorization:**
- AI agents
- DeFi/DEX projects
- Gaming/NFT projects
- Infrastructure/tools

---

## Social/Content Data Integration

Collects signals from blogs, news, and RSS feeds.

### Option 1: RSS Feeds

**Best for:** Free, low-setup content monitoring

**Setup:**

1. Install feedparser:
   ```bash
   pip install feedparser
   ```

2. Configure sources in `config.yaml`:
   ```yaml
   collection:
     social_sources:
       - "https://solana.com/news"
       - "https://www.helius.dev/blog"
       - "https://www.coindesk.com/"
   ```

3. Update `USE_MOCK_DATA=false` in `.env`

**Features:**
- Automatic topic mention extraction
- Publication date tracking
- Sentiment analysis ready
- No rate limits

**Tracked Topics:**
- AI agents
- DeFi innovations
- Gaming/NFTs
- Payment systems

---

### Option 2: Self-Hosted Crawler (Advanced)

**Best for:** Custom sources, API-protected content

**Setup:**

1. Install a crawler (e.g., crawl4ai):
   ```bash
   pip install crawl4ai
   ```

2. Start crawler server:
   ```bash
   python -m crawl4ai.server
   ```

3. Configure in `.env`:
   ```bash
   CRAWLER_BASE_URL=http://localhost:8000
   CRAWLER_ENABLED=true
   ```

4. Add your custom sources to `config.yaml`

5. Update `USE_MOCK_DATA=false` in `.env`

**Features:**
- JavaScript content rendering
- Custom crawling rules
- Rate limiting/backoff
- Data extraction pipelines

---

## Configuration Examples

### Example 1: Development (Mock Data)

```bash
# .env
USE_MOCK_DATA=true
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-...
```

**Result:** Runs with demo data, fast, no API setup needed ✅

---

### Example 2: Production (Helius + GitHub)

```bash
# .env
USE_MOCK_DATA=false
HELIUS_API_KEY=your-key
GITHUB_TOKEN=ghp_...
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-...
```

**Result:** Real on-chain data + real GitHub activity

---

### Example 3: Free Setup (RPC + GitHub)

```bash
# .env
USE_MOCK_DATA=false
SOLANA_RPC_URL=https://api.mainnet-beta.solana.com
GITHUB_TOKEN=ghp_...
LLM_PROVIDER=local
LOCAL_LLM_BASE_URL=http://localhost:11434
LOCAL_LLM_MODEL=llama3
```

**Result:** Free APIs, local LLM, minimal costs

---

### Example 4: Hybrid (Mock Onchain + Live GitHub)

Not currently supported, but can be added per-collector basis.

---

## How It Works: Architecture

### Data Flow

```
┌─────────────────────────────┐
│   USE_MOCK_DATA Env Var     │
└────────────┬────────────────┘
             │
    ┌────────▼────────┐
    │  use_mock=True? │
    └────────┬────────┘
             │
     ┌───────┴──────────┐
     │                  │
  YES│                  │NO
     ▼                  ▼
  ┌──────┐        ┌──────────────┐
  │ MOCK │        │ LIVE PROVIDER│
  └──────┘        └──────────────┘
     │                  │
     ▼                  ▼
  [SIGNALS] ◄────────[SIGNALS]
```

### Collector Logic

Each collector follows this pattern:

```python
class Collector:
    def __init__(self, use_mock=None):
        # Check USE_MOCK_DATA env var if not specified
        if use_mock is None:
            use_mock = os.getenv("USE_MOCK_DATA", "true") == "true"
        self.use_mock = use_mock
    
    def collect(self, window_days):
        if self.use_mock:
            return self._collect_mock(window_days)
        else:
            return self._collect_live(window_days)
```

### Error Handling

- ✅ If live API fails, automatically falls back to mock
- ✅ Missing API keys → fallback to mock
- ✅ Network errors → graceful degradation
- ✅ Rate limits → included in signal metadata

---

## Testing

### Test with Mock Data

```bash
# Always works, fast (~5-10 seconds)
export USE_MOCK_DATA=true
python main.py
```

### Test with Live Data

```bash
# Requires API keys, slower (~30-60 seconds)
export USE_MOCK_DATA=false
export HELIUS_API_KEY=your-key
export GITHUB_TOKEN=ghp_...
python main.py
```

### Compare Results

```bash
# Run both modes and compare outputs
bash compare_mock_vs_live.sh  # (if available)
```

---

## Troubleshooting

### Problem: "HELIUS_API_KEY environment variable not set"

**Solution:**
```bash
# Make sure .env has:
HELIUS_API_KEY=your-actual-key
USE_MOCK_DATA=false

# Or set directly:
export HELIUS_API_KEY=your-key
python main.py
```

### Problem: "Failed to resolve 'helius' (getaddrinfo failed)"

**Solution:**
- Check internet connection
- Verify API key is valid
- Check Helius API status page
- Fall back to mock: `USE_MOCK_DATA=true`

### Problem: "PyGithub not installed"

**Solution:**
```bash
pip install PyGithub
```

### Problem: GitHub rate limiting

**Solution:**
- Use authenticated requests (requires token)
- Already implemented - just add `GITHUB_TOKEN`
- Rate limits: 60 requests/hour (unauthenticated), 5000/hour (authenticated)

### Problem: Live data is incomplete

**Possible causes:**
- API is down/rate limited
- API key has insufficient permissions
- Network connectivity issue
- Data not available for time period

**Solution:**
- Check API status pages
- Verify API key scopes
- Check network connection
- Try mock mode to verify agent works

---

## Adding Custom Data Sources

### Add a New Collector

1. Create `agent/collectors/custom.py`:

```python
from typing import Dict, List, Any
from datetime import datetime, timedelta

class CustomCollector:
    def __init__(self, api_key=None, use_mock=None):
        import os
        self.api_key = api_key or os.getenv("CUSTOM_API_KEY")
        if use_mock is None:
            use_mock = os.getenv("USE_MOCK_DATA", "true").lower() == "true"
        self.use_mock = use_mock
    
    def collect(self, window_days: int = 14) -> List[Dict[str, Any]]:
        if self.use_mock:
            return self._collect_mock(window_days)
        else:
            return self._collect_live(window_days)
    
    def _collect_mock(self, window_days):
        # Mock implementation
        pass
    
    def _collect_live(self, window_days):
        # Live API implementation
        pass
```

2. Update `agent/main.py` to use it:

```python
from collectors import CustomCollector

custom = CustomCollector(use_mock=use_mock_data)
custom_signals = custom.collect(window_days)
all_signals.extend(custom_signals)
```

---

## Performance & Costs

### Mock Data
- Runtime: ~5-10 seconds
- Cost: Free
- API calls: 0

### Live Data (Helius)
- Runtime: ~30-120 seconds (depending on data volume)
- Cost: Free (for 100 req/sec)
- API calls: ~200-500 per run

### Live Data (RPC)
- Runtime: ~60-300 seconds (slow)
- Cost: Free
- API calls: ~100-300 per run

### Live Data (GitHub)
- Runtime: ~10-30 seconds
- Cost: Free (with token)
- API calls: ~5-10 per run

---

## Production Deployment

### Recommended Setup

```bash
# Production .env
USE_MOCK_DATA=false
HELIUS_API_KEY=your-production-key
GITHUB_TOKEN=your-bot-token
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-...
```

### Environment Variables to Rotate/Secure

```bash
# Use secrets management:
- OPENAI_API_KEY
- HELIUS_API_KEY
- GITHUB_TOKEN
```

### Scheduling

```bash
# Run daily at 2 AM
0 2 * * * cd /app && USE_MOCK_DATA=false python main.py
```

---

## Summary

| Feature | Mock | Helius | RPC | GitHub | RSS |
|---------|------|--------|-----|--------|-----|
| Onchain data | ✅ | ✅✅ | ✅ | ❌ | ❌ |
| GitHub data | ✅ | ❌ | ❌ | ✅✅ | ❌ |
| Social data | ✅ | ❌ | ❌ | ❌ | ✅✅ |
| Setup time | <1min | 5min | 1min | 5min | 1min |
| Cost | Free | Free* | Free | Free | Free |
| Speed | Fast | Slow | Slower | Medium | Medium |
| Accuracy | Demo | High | Medium | High | Medium |

*Free tier available for Helius

---

## Questions?

See `MOCK_VS_LIVE_DATA_GUIDE.md` for implementation details.
