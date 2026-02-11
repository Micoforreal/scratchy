# Quick Start Guide

Get the Solana Narrative Detection Agent running in under 5 minutes.

## Prerequisites

- Python 3.9 or higher
- pip (Python package manager)

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 2: Set Up Environment

### Option A: Use OpenAI (Recommended for First Run)

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your OpenAI API key:
   ```bash
   LLM_PROVIDER=openai
   OPENAI_API_KEY=your-actual-api-key-here
   OPENAI_MODEL=gpt-4o-mini
   ```

3. Get an API key from: https://platform.openai.com/api-keys

### Option B: Use Local LLM (Free, No API Key Required)

1. Install Ollama: https://ollama.ai/
2. Pull a model:
   ```bash
   ollama pull llama3
   ```

3. Edit `.env`:
   ```bash
   LLM_PROVIDER=local
   LOCAL_LLM_BASE_URL=http://localhost:11434
   LOCAL_LLM_MODEL=llama3
   ```

4. Ensure Ollama is running:
   ```bash
   ollama serve
   ```

## Step 3: Verify Setup

Run the verification script:

```bash
python3 verify_setup.py
```

You should see:
```
✅ All imports successful!
```

## Step 4: Run the Agent

# Navigate to the agent directory
cd d:\github\scratchy\agent-solana-narratives\agent

# Run the agent with your virtual environment's Python
D:/github/scratchy/agent-solana-narratives/.venv/Scripts/python.exe main.py




## What to Expect

The agent will:
1. **Collect signals** (using mock data - takes ~2 seconds)
2. **Process signals** (normalize, detect momentum, cluster - ~3 seconds)
3. **Detect narratives** (algorithmic filtering - ~1 second)
4. **Generate explanations** (LLM calls - ~10-30 seconds depending on model)
5. **Generate ideas** (more LLM calls - ~20-60 seconds)
6. **Create report** (save to `reports/` directory - instant)

**Total runtime**: 30 seconds to 2 minutes (depending on LLM)

## Viewing Results

The final report is saved to:
- `reports/narrative_brief_latest.md` (always the most recent)
- `reports/narrative_brief_TIMESTAMP.md` (timestamped version)

Open in any markdown viewer or text editor.

Example output structure:
```markdown
# Solana Ecosystem Narrative Brief

## 1. AI Agent Explosion
**Momentum Score:** 72.5 / 100

### Why it matters
[Explanation]

### Build Ideas
1. **Idea Title**
   Description...
```

## Customizing the Agent

Edit `agent/config.yaml` to adjust:

- **Time window**: Change `duration_days` (default: 14)
- **Momentum threshold**: Change `momentum_threshold_pct` (default: 15%)
- **Max narratives**: Change `max_narratives` (default: 7)
- **Ideas per narrative**: Change `ideas_per_narrative` (default: 5)

## Troubleshooting

### "OPENAI_API_KEY environment variable not set"
→ Make sure you created `.env` file with your API key

### "Local LLM request failed"
→ Check that Ollama is running (`ollama serve`)

### No narratives detected
→ Try lowering thresholds in `agent/config.yaml`:
- `momentum_threshold_pct: 10` (instead of 15)
- `min_momentum_score: 15` (instead of 20)

### LLM responses are weird
→ Try adjusting temperature in `agent/config.yaml`:
- Lower (0.5) = more focused
- Higher (0.9) = more creative

## Next Steps

1. **Read the full README**: `README.md` for complete documentation
2. **Check the PRD**: `docs/PRD.md` for system design details
3. **Inspect intermediate outputs**: Look in `data/processed/` to see signal processing
4. **Customize mock data**: Edit collectors in `agent/collectors/` to simulate different scenarios
5. **Replace with real data**: See README for API integration instructions

## Cost Estimate (OpenAI)

With default settings (7 narratives, 5 ideas each):
- **gpt-4o-mini**: ~$0.05 - $0.10 per run
- **gpt-4o**: ~$0.50 - $1.00 per run

Using a local LLM is **free** but slower.

## Need Help?

- Check `README.md` for detailed documentation
- Check `docs/PRD.md` for technical details
- Review example outputs in `reports/` after first run
