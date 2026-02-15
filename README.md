# Solana Narrative Detection Agent

An explainable, code-first agent that detects emerging narratives in the Solana ecosystem and generates actionable product ideas.

## What It Does

This tool automatically:

1. **Collects signals** from multiple sources (onchain, GitHub, social/offchain)
2. **Detects emerging narratives** using algorithmic pattern detection
3. **Explains why they matter** with evidence-backed reasoning
4. **Generates product ideas** that builders can implement

Unlike LLM-first approaches that hallucinate trends, this system uses **algorithms first, LLMs second** to ensure every narrative is backed by real data.

## Why It's Useful

For **builders**: Discover what to build next based on real ecosystem momentum, not speculation.

For **investors**: Identify emerging trends before they become obvious.

For **ecosystem teams**: Understand where developer attention and user activity is accelerating.

## How It Works

### Signal Collection
The agent collects three types of signals over a 14-day window:

- **Onchain**: Transaction volume, active wallets, program deployments, TVL
- **GitHub**: Repository activity, stars, commits, new projects
- **Social**: Blog posts, reports, community discourse (from curated sources)

### Narrative Detection (Algorithmic)
1. **Normalize** raw metrics into comparable scores
2. **Detect momentum** by comparing recent vs baseline activity
3. **Cluster** related signals using keyword similarity (TF-IDF)
4. **Filter** clusters that meet criteria:
   - Multiple signal types reinforce each other (e.g., onchain + GitHub + social)
   - Momentum score above threshold (≥15% growth)
   - Sufficient cluster quality

**No LLM reasoning at this stage** - narratives are detected purely from data patterns.

### LLM-Assisted Enhancement
Only after narratives are algorithmically detected, LLMs are used to:

1. **Label** clusters with clear narrative names
2. **Explain** why the narrative matters (evidence-backed)
3. **Generate** 3-5 concrete product ideas per narrative

## Data Sources

**Current implementation uses mock data** to demonstrate the pipeline. 

For production, replace with:
- **Onchain**: Solana RPC, Helius, SolanaFM, FlipsideCrypto
- **GitHub**: GitHub API tracking solana-labs and ecosystem repos
- **Social**: Self-hosted crawler (e.g., crawl4ai) for blogs, RSS, curated KOL sources

## Example Output

```markdown
## 1. AI Agent Explosion

**Momentum Score:** 72.5 / 100

### Why it matters
AI agents are becoming the fastest-growing vertical on Solana, with autonomous 
trading bots and chatbot frameworks seeing 40%+ growth in the past two weeks.

- Onchain: AI-related program deployments up 180% week-over-week
- GitHub: Solana AI agent frameworks gained 850+ stars in 7 days
- Social: "AI agents" mentions increased 350% across ecosystem media

### Build Ideas

1. **Conversational DeFi Assistant**
   An AI agent that helps users navigate Solana DeFi via natural language...

2. **Autonomous Portfolio Rebalancer**
   A trading bot that automatically rebalances portfolios based on...
```

## Web Interface 🌐

Scratchy now includes a modern web interface! Access the agent via your browser with a beautiful dashboard.

### Features:
- 🚀 One-click agent runs
- 📊 Real-time progress tracking
- 📄 Report viewer with markdown rendering
- 🎨 Modern Solana-themed UI
- 📱 Responsive design (mobile + desktop)

### Quick Start (Web Version):

```bash
# Install dependencies
pip install -r requirements.txt

# Configure .env with your API key
cp .env.example .env

# Run the web server
python app.py
```

Visit `http://localhost:8080` in your browser!

### Deploy to the Cloud:

Deploy to **Vercel** or **Render** for a public URL:

```bash
# Push to GitHub
git init && git add . && git commit -m "Initial commit"
git push

# Then deploy via:
# - Vercel: https://vercel.com (best for demos)
# - Render: https://render.com (best for production)
```

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions.

## Installation & Setup (CLI Version)

## Installation & Setup

### Prerequisites
- Python 3.9+
- OpenAI API key OR self-hosted LLM (Ollama, vLLM, etc.)

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your API keys:
   ```bash
   # For OpenAI
   LLM_PROVIDER=openai
   OPENAI_API_KEY=your-key-here
   
   # OR for local LLM
   LLM_PROVIDER=local
   LOCAL_LLM_BASE_URL=http://localhost:11434
   ```

3. (Optional) Adjust settings in `agent/config.yaml`

### Run the Agent

```bash
cd agent
python main.py
```

The agent will:
- Collect and process signals
- Detect narratives
- Generate explanations and ideas
- Save a report to `reports/narrative_brief_latest.md`

## Configuration

Edit `agent/config.yaml` to customize:

- **Time window**: Default 14 days (fortnightly)
- **Momentum threshold**: Minimum growth % to qualify (default 15%)
- **Signal weights**: How to balance onchain vs GitHub vs social
- **Max narratives**: Maximum narratives to output (default 7)
- **LLM settings**: Temperature, max tokens, ideas per narrative

## Project Structure

```
agent-solana-narratives/
├── agent/
│   ├── collectors/       # Signal collection (onchain, GitHub, social)
│   ├── signals/          # Processing (normalize, momentum, clustering)
│   ├── narratives/       # Detection, explanation, idea generation
│   ├── llm/              # LLM abstraction (OpenAI, local)
│   ├── config.yaml       # Configuration
│   └── main.py           # CLI entry point
├── data/
│   ├── raw/              # Raw collected signals
│   └── processed/        # Normalized and scored signals
├── reports/              # Generated narrative briefs
├── docs/                 # Documentation
│   └── PRD.md            # Product Requirements Document
├── .env.example          # Environment variable template
└── README.md             # This file
```

## Extending the System

### Replace Mock Data with Real APIs

1. **Onchain**: Edit `agent/collectors/onchain.py`
   - Replace `_mock_*` methods with real Solana RPC calls
   - Consider using Helius, FlipsideCrypto, or SolanaFM

2. **GitHub**: Edit `agent/collectors/github.py`
   - Implement GitHub API integration
   - Track solana-labs and curated ecosystem repos

3. **Social**: Edit `agent/collectors/social.py`
   - Integrate with self-hosted crawler (crawl4ai)
   - Or use RSS feed parsing

### Add New Signal Types

1. Create new collector in `agent/collectors/`
2. Ensure signals have required fields: `signal_type`, `metric`, `value`, `timestamp`, `metadata`
3. Add to pipeline in `main.py`

### Customize Narrative Detection

Edit thresholds in `agent/config.yaml`:
- `momentum_threshold_pct`: Minimum growth to qualify
- `min_signal_types`: Require more signal type reinforcement
- `min_momentum_score`: Raise the bar for narrative quality

## Future Enhancements

- Database-backed storage (currently file-based)
- Web dashboard for visualizing narratives
- Real-time streaming (currently batch processing)
- Multi-agent orchestration (currently single-process)
- Automated deployment tracking (monitor if ideas get built)

## License

MIT

## Contributing

This is a Superteam bounty submission. For production use, replace mock data with real integrations.

## Acknowledgments

Built for the Solana ecosystem as part of Superteam bounty program.
