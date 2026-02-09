#!/usr/bin/env python3
"""
Quick verification test to ensure all modules can be imported.
Run this to verify the installation is correct.
"""

import sys
from pathlib import Path

# Add agent directory to path
agent_dir = Path(__file__).parent / "agent"
sys.path.insert(0, str(agent_dir))

print("🔍 Testing imports...\n")

try:
    print("   Testing collectors...")
    from collectors import OnchainCollector, GitHubCollector, SocialCollector
    print("   ✅ Collectors OK")
    
    print("   Testing signals...")
    from signals import SignalNormalizer, MomentumDetector, SignalClusterer
    print("   ✅ Signals OK")
    
    print("   Testing narratives...")
    from narratives import NarrativeDetector, NarrativeExplainer, IdeaGenerator
    print("   ✅ Narratives OK")
    
    print("   Testing LLM...")
    from llm import get_llm_client, LLMClient, OpenAIClient, LocalLLMClient
    print("   ✅ LLM OK")
    
    print("\n✅ All imports successful!")
    print("\nℹ️  The system is ready to use.")
    print("   Run 'cd agent && python main.py' to execute the pipeline.")
    print("   (Make sure to set up your .env file first)")
    
except ImportError as e:
    print(f"\n❌ Import error: {e}")
    sys.exit(1)
