# FILE REORGANIZATION GUIDE

All files have been flattened with this naming convention:
- `__SLASH__` = directory separator `/`
- `DOT_` prefix = hidden files starting with `.`

## Step-by-Step Reorganization

### 1. Create Directory Structure

```bash
mkdir -p agent-solana-narratives
cd agent-solana-narratives
mkdir -p agent/{collectors,signals,narratives,llm,reports}
mkdir -p docs
mkdir -p data/{raw,processed}
mkdir -p reports
```

### 2. Move Root Files

```bash
# Hidden files (rename DOT_ prefix to .)
mv DOT_env.example .env.example
mv DOT_gitignore .gitignore

# Regular root files
mv LICENSE LICENSE
mv PROJECT_OVERVIEW.md PROJECT_OVERVIEW.md
mv QUICKSTART.md QUICKSTART.md
mv README.md README.md
mv requirements.txt requirements.txt
mv verify_setup.py verify_setup.py
```

### 3. Move agent/ Files

```bash
# Main agent files
mv "agent__SLASH____init__.py" "agent/__init__.py"
mv "agent__SLASH__config.yaml" "agent/config.yaml"
mv "agent__SLASH__main.py" "agent/main.py"
```

### 4. Move agent/collectors/ Files

```bash
mv "agent__SLASH__collectors__SLASH____init__.py" "agent/collectors/__init__.py"
mv "agent__SLASH__collectors__SLASH__github.py" "agent/collectors/github.py"
mv "agent__SLASH__collectors__SLASH__onchain.py" "agent/collectors/onchain.py"
mv "agent__SLASH__collectors__SLASH__social.py" "agent/collectors/social.py"
```

### 5. Move agent/signals/ Files

```bash
mv "agent__SLASH__signals__SLASH____init__.py" "agent/signals/__init__.py"
mv "agent__SLASH__signals__SLASH__clustering.py" "agent/signals/clustering.py"
mv "agent__SLASH__signals__SLASH__momentum.py" "agent/signals/momentum.py"
mv "agent__SLASH__signals__SLASH__normalize.py" "agent/signals/normalize.py"
```

### 6. Move agent/narratives/ Files

```bash
mv "agent__SLASH__narratives__SLASH____init__.py" "agent/narratives/__init__.py"
mv "agent__SLASH__narratives__SLASH__detect.py" "agent/narratives/detect.py"
mv "agent__SLASH__narratives__SLASH__explain.py" "agent/narratives/explain.py"
mv "agent__SLASH__narratives__SLASH__ideas.py" "agent/narratives/ideas.py"
```

### 7. Move agent/llm/ Files

```bash
mv "agent__SLASH__llm__SLASH____init__.py" "agent/llm/__init__.py"
mv "agent__SLASH__llm__SLASH__base.py" "agent/llm/base.py"
mv "agent__SLASH__llm__SLASH__local.py" "agent/llm/local.py"
mv "agent__SLASH__llm__SLASH__openai.py" "agent/llm/openai.py"
```

### 8. Move agent/reports/ Files

```bash
mv "agent__SLASH__reports__SLASH__README.md" "agent/reports/README.md"
```

### 9. Move docs/ Files

```bash
mv "docs__SLASH__PRD.md" "docs/PRD.md"
```

## Quick Script (All at Once)

Save this as `reorganize.sh` and run it:

```bash
#!/bin/bash

# Create directories
mkdir -p agent-solana-narratives
cd agent-solana-narratives
mkdir -p agent/{collectors,signals,narratives,llm,reports}
mkdir -p docs data/{raw,processed} reports

# Move all files
cd ..
mv DOT_env.example agent-solana-narratives/.env.example
mv DOT_gitignore agent-solana-narratives/.gitignore
mv LICENSE agent-solana-narratives/
mv PROJECT_OVERVIEW.md agent-solana-narratives/
mv QUICKSTART.md agent-solana-narratives/
mv README.md agent-solana-narratives/
mv requirements.txt agent-solana-narratives/
mv verify_setup.py agent-solana-narratives/

# Agent root
mv "agent__SLASH____init__.py" "agent-solana-narratives/agent/__init__.py"
mv "agent__SLASH__config.yaml" "agent-solana-narratives/agent/config.yaml"
mv "agent__SLASH__main.py" "agent-solana-narratives/agent/main.py"

# Collectors
mv "agent__SLASH__collectors__SLASH____init__.py" "agent-solana-narratives/agent/collectors/__init__.py"
mv "agent__SLASH__collectors__SLASH__github.py" "agent-solana-narratives/agent/collectors/github.py"
mv "agent__SLASH__collectors__SLASH__onchain.py" "agent-solana-narratives/agent/collectors/onchain.py"
mv "agent__SLASH__collectors__SLASH__social.py" "agent-solana-narratives/agent/collectors/social.py"

# Signals
mv "agent__SLASH__signals__SLASH____init__.py" "agent-solana-narratives/agent/signals/__init__.py"
mv "agent__SLASH__signals__SLASH__clustering.py" "agent-solana-narratives/agent/signals/clustering.py"
mv "agent__SLASH__signals__SLASH__momentum.py" "agent-solana-narratives/agent/signals/momentum.py"
mv "agent__SLASH__signals__SLASH__normalize.py" "agent-solana-narratives/agent/signals/normalize.py"

# Narratives
mv "agent__SLASH__narratives__SLASH____init__.py" "agent-solana-narratives/agent/narratives/__init__.py"
mv "agent__SLASH__narratives__SLASH__detect.py" "agent-solana-narratives/agent/narratives/detect.py"
mv "agent__SLASH__narratives__SLASH__explain.py" "agent-solana-narratives/agent/narratives/explain.py"
mv "agent__SLASH__narratives__SLASH__ideas.py" "agent-solana-narratives/agent/narratives/ideas.py"

# LLM
mv "agent__SLASH__llm__SLASH____init__.py" "agent-solana-narratives/agent/llm/__init__.py"
mv "agent__SLASH__llm__SLASH__base.py" "agent-solana-narratives/agent/llm/base.py"
mv "agent__SLASH__llm__SLASH__local.py" "agent-solana-narratives/agent/llm/local.py"
mv "agent__SLASH__llm__SLASH__openai.py" "agent-solana-narratives/agent/llm/openai.py"

# Reports
mv "agent__SLASH__reports__SLASH__README.md" "agent-solana-narratives/agent/reports/README.md"

# Docs
mv "docs__SLASH__PRD.md" "agent-solana-narratives/docs/PRD.md"

echo "✅ Reorganization complete!"
echo "Run: cd agent-solana-narratives && python3 verify_setup.py"
```

## Final Directory Structure

```
agent-solana-narratives/
├── .env.example
├── .gitignore
├── LICENSE
├── PROJECT_OVERVIEW.md
├── QUICKSTART.md
├── README.md
├── requirements.txt
├── verify_setup.py
├── agent/
│   ├── __init__.py
│   ├── config.yaml
│   ├── main.py
│   ├── collectors/
│   │   ├── __init__.py
│   │   ├── github.py
│   │   ├── onchain.py
│   │   └── social.py
│   ├── signals/
│   │   ├── __init__.py
│   │   ├── clustering.py
│   │   ├── momentum.py
│   │   └── normalize.py
│   ├── narratives/
│   │   ├── __init__.py
│   │   ├── detect.py
│   │   ├── explain.py
│   │   └── ideas.py
│   ├── llm/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── local.py
│   │   └── openai.py
│   └── reports/
│       └── README.md
├── docs/
│   └── PRD.md
├── data/
│   ├── raw/
│   └── processed/
└── reports/
```

## Verification

After reorganizing, verify everything works:

```bash
cd agent-solana-narratives
python3 verify_setup.py
```

You should see:
```
✅ All imports successful!
```

Then you can run the agent:
```bash
cd agent
python main.py
```
