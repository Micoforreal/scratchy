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