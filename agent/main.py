#!/usr/bin/env python3
"""
Solana Narrative Detection Agent - Main Entry Point

This is the primary CLI for running the narrative detection pipeline.
"""

import os
import sys
import yaml
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any

# Load environment variables from .env file
from dotenv import load_dotenv
env_file = Path(__file__).parent.parent / ".env"
load_dotenv(env_file)

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from collectors import OnchainCollector, GitHubCollector, SocialCollector
from signals import SignalNormalizer, MomentumDetector, SignalClusterer
from narratives import NarrativeDetector, NarrativeExplainer, IdeaGenerator
from llm import get_llm_client, LLMError


def load_config() -> Dict[str, Any]:
    """
    Load configuration from config.yaml.
    
    Returns:
        Configuration dictionary
    """
    config_path = Path(__file__).parent / "config.yaml"
    
    if not config_path.exists():
        print(f"❌ Error: config.yaml not found at {config_path}")
        sys.exit(1)
    
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def check_required_env_vars() -> None:
    """
    Check that required environment variables are set.
    
    Exits with error if critical vars are missing.
    """
    llm_provider = os.getenv("LLM_PROVIDER", "openai")
    
    required_vars = []
    
    if llm_provider == "openai":
        if not os.getenv("OPENAI_API_KEY"):
            required_vars.append("OPENAI_API_KEY")
    elif llm_provider == "local":
        if not os.getenv("LOCAL_LLM_BASE_URL"):
            required_vars.append("LOCAL_LLM_BASE_URL")
    
    if required_vars:
        print("❌ Error: Missing required environment variables:")
        for var in required_vars:
            print(f"   - {var}")
        print("\nPlease set these in your .env file or environment.")
        print("See .env.example for reference.")
        sys.exit(1)


def ensure_directories(config: Dict[str, Any]) -> None:
    """
    Ensure required directories exist.
    
    Args:
        config: Configuration dictionary
    """
    paths = config.get("paths", {})
    
    for path_name, path_value in paths.items():
        path = Path(__file__).parent.parent / path_value
        path.mkdir(parents=True, exist_ok=True)


def save_signals(signals: list, config: Dict[str, Any], stage: str) -> None:
    """
    Save signals to file for inspection.
    
    Args:
        signals: List of signals
        config: Configuration dictionary
        stage: Processing stage name
    """
    data_path = Path(__file__).parent.parent / config["paths"]["processed_data"]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = data_path / f"{stage}_{timestamp}.json"
    
    with open(filename, 'w') as f:
        json.dump(signals, f, indent=2, default=str)
    
    print(f"   Saved {stage} data to {filename}")


def generate_report(narratives: list, config: Dict[str, Any]) -> str:
    """
    Generate narrative report in Markdown format.
    
    Args:
        narratives: List of final narratives
        config: Configuration dictionary
        
    Returns:
        Path to generated report
    """
    # Calculate date range
    window_days = config["window"]["duration_days"]
    end_date = datetime.now()
    start_date = end_date - timedelta(days=window_days)
    
    # Format dates
    date_range = f"{start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}"
    
    # Build report content
    lines = [
        f"# Solana Ecosystem Narrative Brief",
        f"",
        f"**Period:** {date_range} ({window_days} days)",
        f"**Generated:** {end_date.strftime('%Y-%m-%d %H:%M:%S')}",
        f"**Narratives Detected:** {len(narratives)}",
        f"",
        f"---",
        f""
    ]
    
    for idx, narrative in enumerate(narratives, 1):
        name = narrative.get("name", narrative.get("narrative_name", "Unnamed"))
        explanation = narrative.get("explanation", "No explanation available")
        momentum = narrative.get("momentum_score", 0.0)
        why_matters = narrative.get("why_it_matters", [])
        ideas = narrative.get("build_ideas", [])
        
        lines.append(f"## {idx}. {name}")
        lines.append(f"")
        lines.append(f"**Momentum Score:** {momentum:.1f} / 100")
        lines.append(f"")
        lines.append(f"### Why it matters")
        lines.append(f"")
        lines.append(explanation)
        lines.append(f"")
        
        if why_matters:
            for point in why_matters:
                lines.append(f"- {point}")
            lines.append(f"")
        
        lines.append(f"### Build Ideas")
        lines.append(f"")
        
        if ideas:
            for idea_idx, idea in enumerate(ideas, 1):
                title = idea.get("title", f"Idea {idea_idx}")
                description = idea.get("description", "")
                lines.append(f"{idea_idx}. **{title}**")
                lines.append(f"   {description}")
                lines.append(f"")
        else:
            lines.append("*No ideas generated*")
            lines.append(f"")
        
        lines.append(f"---")
        lines.append(f"")
    
    # Write report
    reports_path = Path(__file__).parent.parent / config["paths"]["reports"]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = reports_path / f"narrative_brief_{timestamp}.md"
    
    with open(report_file, 'w') as f:
        f.write("\n".join(lines))
    
    # Create "latest" symlink/copy
    if config.get("output", {}).get("create_latest_alias", True):
        latest_file = reports_path / "narrative_brief_latest.md"
        with open(latest_file, 'w') as f:
            f.write("\n".join(lines))
    
    return str(report_file)


def main():
    """
    Main execution pipeline.
    """
    print("🚀 Solana Narrative Detection Agent")
    print("=" * 50)
    
    # Load configuration
    print("\n📋 Loading configuration...")
    config = load_config()
    print("   ✅ Config loaded")
    
    # Check environment
    print("\n🔍 Checking environment variables...")
    check_required_env_vars()
    print("   ✅ Environment OK")
    
    # Ensure directories exist
    print("\n📁 Setting up directories...")
    ensure_directories(config)
    print("   ✅ Directories ready")
    
    # Initialize LLM client
    print("\n🤖 Initializing LLM client...")
    try:
        llm_client = get_llm_client()
        print(f"   ✅ LLM client ready ({os.getenv('LLM_PROVIDER', 'openai')})")
    except LLMError as e:
        print(f"   ❌ Failed to initialize LLM: {str(e)}")
        sys.exit(1)
    
    # Stage 1: Collect Signals
    print("\n" + "=" * 50)
    print("📡 STAGE 1: SIGNAL COLLECTION")
    print("=" * 50)
    
    window_days = config["window"]["duration_days"]
    
    print(f"\n   Collecting onchain signals...")
    onchain = OnchainCollector()
    onchain_signals = onchain.collect(window_days)
    print(f"   ✅ Collected {len(onchain_signals)} onchain signals")
    
    print(f"\n   Collecting GitHub signals...")
    github = GitHubCollector(repo_limit=config["collection"]["github_repo_limit"])
    github_signals = github.collect(window_days)
    print(f"   ✅ Collected {len(github_signals)} GitHub signals")
    
    print(f"\n   Collecting social signals...")
    social = SocialCollector(sources=config["collection"]["social_sources"])
    social_signals = social.collect(window_days)
    print(f"   ✅ Collected {len(social_signals)} social signals")
    
    all_signals = onchain_signals + github_signals + social_signals
    print(f"\n   📊 Total signals: {len(all_signals)}")
    save_signals(all_signals, config, "01_raw_signals")
    
    # Stage 2: Process Signals
    print("\n" + "=" * 50)
    print("⚙️  STAGE 2: SIGNAL PROCESSING")
    print("=" * 50)
    
    print("\n   Normalizing signals...")
    normalizer = SignalNormalizer(method=config["signals"]["normalization_method"])
    normalized_signals = normalizer.normalize_signals(all_signals)
    print(f"   ✅ Normalized {len(normalized_signals)} signals")
    
    print("\n   Detecting momentum...")
    momentum_detector = MomentumDetector(
        threshold_pct=config["signals"]["momentum_threshold_pct"],
        window_days=window_days
    )
    momentum_signals = momentum_detector.detect_momentum(normalized_signals)
    signals_with_momentum = sum(1 for s in momentum_signals if s.get("has_momentum", False))
    print(f"   ✅ Found {signals_with_momentum} signals with momentum")
    save_signals(momentum_signals, config, "02_momentum_signals")
    
    print("\n   Clustering signals...")
    clusterer = SignalClusterer(min_cluster_size=3)
    initial_clusters = clusterer.cluster_signals(momentum_signals)
    enriched_clusters = clusterer.enrich_clusters(initial_clusters, momentum_signals)
    print(f"   ✅ Formed {len(enriched_clusters)} signal clusters")
    
    # Stage 3: Detect Narratives
    print("\n" + "=" * 50)
    print("🔍 STAGE 3: NARRATIVE DETECTION")
    print("=" * 50)
    
    print("\n   Detecting narratives from clusters...")
    detector = NarrativeDetector(
        min_signal_types=config["narratives"]["min_signal_types"],
        min_momentum_score=config["narratives"]["min_momentum_score"],
        max_narratives=config["narratives"]["max_narratives"]
    )
    narratives = detector.detect_narratives(enriched_clusters)
    print(f"   ✅ Detected {len(narratives)} qualifying narratives")
    
    if not narratives:
        print("\n   ⚠️  No narratives met the criteria.")
        print("   Try adjusting thresholds in config.yaml")
        return
    
    # Stage 4: Explain Narratives (LLM)
    print("\n" + "=" * 50)
    print("💡 STAGE 4: NARRATIVE EXPLANATION (LLM)")
    print("=" * 50)
    
    print("\n   Generating explanations...")
    explainer = NarrativeExplainer(llm_client)
    explained_narratives = explainer.explain_narratives(narratives)
    print(f"   ✅ Generated explanations for {len(explained_narratives)} narratives")
    
    # Stage 5: Generate Ideas (LLM)
    print("\n" + "=" * 50)
    print("💡 STAGE 5: IDEA GENERATION (LLM)")
    print("=" * 50)
    
    print("\n   Generating build ideas...")
    idea_generator = IdeaGenerator(
        llm_client,
        ideas_per_narrative=config["llm"]["ideas_per_narrative"]
    )
    final_narratives = idea_generator.generate_ideas_batch(explained_narratives)
    print(f"   ✅ Generated ideas for {len(final_narratives)} narratives")
    
    # Stage 6: Generate Report
    print("\n" + "=" * 50)
    print("📄 STAGE 6: REPORT GENERATION")
    print("=" * 50)
    
    print("\n   Creating narrative brief...")
    report_path = generate_report(final_narratives, config)
    print(f"   ✅ Report saved to {report_path}")
    
    # Print Summary
    print("\n" + "=" * 50)
    print("✨ PIPELINE COMPLETE")
    print("=" * 50)
    print(f"\n📊 Summary:")
    print(f"   - Signals collected: {len(all_signals)}")
    print(f"   - Signals with momentum: {signals_with_momentum}")
    print(f"   - Narratives detected: {len(final_narratives)}")
    print(f"   - Report: {report_path}")
    print("\n🎉 Done!\n")


if __name__ == "__main__":
    main()
