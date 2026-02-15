#!/usr/bin/env python3
"""
Scratchy Web Application
Flask web server for the Solana Narrative Detection Agent
"""

import os
import sys
import json
import threading
from datetime import datetime
from pathlib import Path
from flask import Flask, render_template, jsonify, request, send_file
from flask_cors import CORS
import markdown2

# Add agent directory to path
sys.path.insert(0, str(Path(__file__).parent / "agent"))

# Import agent components
from agent.main import load_config, check_required_env_vars, ensure_directories
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Global state for tracking runs
runs = {}
current_run_id = None

def run_agent_pipeline(run_id):
    """
    Run the agent pipeline in a background thread.
    
    Args:
        run_id: Unique identifier for this run
    """
    global runs
    
    try:
        runs[run_id]["status"] = "running"
        runs[run_id]["progress"] = "Initializing..."
        
        # Import here to avoid circular imports
        from agent.main import main as run_main_pipeline
        import io
        from contextlib import redirect_stdout
        
        # Capture stdout
        output = io.StringIO()
        
        # Run the pipeline
        with redirect_stdout(output):
            try:
                # Import and run the pipeline components
                from agent.main import (
                    load_config, ensure_directories, get_llm_client,
                    OnchainCollector, GitHubCollector, SocialCollector,
                    SignalNormalizer, MomentumDetector, SignalClusterer,
                    NarrativeDetector, NarrativeExplainer, IdeaGenerator,
                    generate_report
                )
                
                config = load_config()
                ensure_directories(config)
                
                runs[run_id]["progress"] = "Loading LLM client..."
                llm_client = get_llm_client()
                
                # Stage 1: Collect Signals
                runs[run_id]["progress"] = "Collecting signals..."
                window_days = config["window"]["duration_days"]
                use_mock_data = os.getenv("USE_MOCK_DATA", "true").lower() == "true"
                
                onchain = OnchainCollector(use_mock=use_mock_data)
                github = GitHubCollector(
                    repo_limit=config["collection"]["github_repo_limit"],
                    use_mock=use_mock_data
                )
                social = SocialCollector(
                    sources=config["collection"]["social_sources"],
                    use_mock=use_mock_data
                )
                
                onchain_signals = onchain.collect(window_days)
                github_signals = github.collect(window_days)
                social_signals = social.collect(window_days)
                
                all_signals = onchain_signals + github_signals + social_signals
                
                if not all_signals:
                    raise Exception("No signals collected")
                
                # Stage 2: Process Signals
                runs[run_id]["progress"] = "Processing signals..."
                normalizer = SignalNormalizer(method=config["signals"]["normalization_method"])
                normalized_signals = normalizer.normalize_signals(all_signals)
                
                momentum_detector = MomentumDetector(
                    threshold_pct=config["signals"]["momentum_threshold_pct"],
                    window_days=window_days
                )
                momentum_signals = momentum_detector.detect_momentum(normalized_signals)
                
                clusterer = SignalClusterer(min_cluster_size=3)
                initial_clusters = clusterer.cluster_signals(momentum_signals)
                enriched_clusters = clusterer.enrich_clusters(initial_clusters, momentum_signals)
                
                # Stage 3: Detect Narratives
                runs[run_id]["progress"] = "Detecting narratives..."
                detector = NarrativeDetector(
                    min_signal_types=config["narratives"]["min_signal_types"],
                    min_momentum_score=config["narratives"]["min_momentum_score"],
                    max_narratives=config["narratives"]["max_narratives"]
                )
                narratives = detector.detect_narratives(enriched_clusters)
                
                if not narratives:
                    runs[run_id]["status"] = "completed"
                    runs[run_id]["progress"] = "No narratives detected"
                    runs[run_id]["result"] = "No narratives met the criteria"
                    return
                
                # Stage 4: Explain Narratives
                runs[run_id]["progress"] = "Generating explanations..."
                explainer = NarrativeExplainer(llm_client)
                explained_narratives = explainer.explain_narratives(narratives)
                
                # Stage 5: Generate Ideas
                runs[run_id]["progress"] = "Generating build ideas..."
                idea_generator = IdeaGenerator(
                    llm_client,
                    ideas_per_narrative=config["llm"]["ideas_per_narrative"]
                )
                final_narratives = idea_generator.generate_ideas_batch(explained_narratives)
                
                # Stage 6: Generate Report
                runs[run_id]["progress"] = "Creating report..."
                report_path = generate_report(final_narratives, config)
                
                runs[run_id]["status"] = "completed"
                runs[run_id]["progress"] = "Complete!"
                runs[run_id]["result"] = f"Generated {len(final_narratives)} narratives"
                runs[run_id]["report_path"] = report_path
                
            except Exception as e:
                raise e
        
    except Exception as e:
        runs[run_id]["status"] = "failed"
        runs[run_id]["progress"] = f"Error: {str(e)}"
        runs[run_id]["error"] = str(e)


@app.route('/')
def index():
    """Render the main dashboard."""
    return render_template('index.html')


@app.route('/api/run', methods=['POST'])
def trigger_run():
    """Trigger a new agent run."""
    global current_run_id, runs
    
    # Generate run ID
    run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    current_run_id = run_id
    
    # Initialize run state
    runs[run_id] = {
        "id": run_id,
        "status": "queued",
        "progress": "Queued",
        "started_at": datetime.now().isoformat(),
        "result": None,
        "error": None
    }
    
    # Start background thread
    thread = threading.Thread(target=run_agent_pipeline, args=(run_id,))
    thread.daemon = True
    thread.start()
    
    return jsonify({
        "success": True,
        "run_id": run_id,
        "message": "Agent run started"
    })


@app.route('/api/status/<run_id>')
def get_status(run_id):
    """Get status of a specific run."""
    if run_id not in runs:
        return jsonify({"error": "Run not found"}), 404
    
    return jsonify(runs[run_id])


@app.route('/api/status')
def get_current_status():
    """Get status of the current/latest run."""
    if not current_run_id or current_run_id not in runs:
        return jsonify({"status": "idle", "message": "No runs yet"})
    
    return jsonify(runs[current_run_id])


@app.route('/api/reports')
def list_reports():
    """List all generated reports."""
    try:
        config = load_config()
        reports_path = Path(__file__).parent / config["paths"]["reports"]
        
        if not reports_path.exists():
            return jsonify({"reports": []})
        
        reports = []
        for file in reports_path.glob("narrative_brief_*.md"):
            if file.name == "narrative_brief_latest.md":
                continue
            
            stats = file.stat()
            reports.append({
                "filename": file.name,
                "path": str(file),
                "size": stats.st_size,
                "modified": datetime.fromtimestamp(stats.st_mtime).isoformat()
            })
        
        # Sort by modified time, newest first
        reports.sort(key=lambda x: x["modified"], reverse=True)
        
        return jsonify({"reports": reports})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/reports/<filename>')
def get_report(filename):
    """Get a specific report."""
    try:
        config = load_config()
        reports_path = Path(__file__).parent / config["paths"]["reports"]
        report_file = reports_path / filename
        
        if not report_file.exists():
            return jsonify({"error": "Report not found"}), 404
        
        # Read markdown content
        with open(report_file, 'r', encoding='utf-8') as f:
            markdown_content = f.read()
        
        # Convert to HTML
        html_content = markdown2.markdown(markdown_content, extras=['tables', 'fenced-code-blocks'])
        
        return jsonify({
            "filename": filename,
            "markdown": markdown_content,
            "html": html_content
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/latest')
def get_latest_report():
    """Get the latest report."""
    try:
        config = load_config()
        reports_path = Path(__file__).parent / config["paths"]["reports"]
        latest_file = reports_path / "narrative_brief_latest.md"
        
        if not latest_file.exists():
            return jsonify({"error": "No reports generated yet"}), 404
        
        # Read markdown content
        with open(latest_file, 'r', encoding='utf-8') as f:
            markdown_content = f.read()
        
        # Convert to HTML
        html_content = markdown2.markdown(markdown_content, extras=['tables', 'fenced-code-blocks'])
        
        return jsonify({
            "filename": "narrative_brief_latest.md",
            "markdown": markdown_content,
            "html": html_content
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/health')
def health():
    """Health check endpoint."""
    return jsonify({"status": "healthy", "service": "scratchy-agent"})


if __name__ == '__main__':
    # Check environment on startup
    try:
        check_required_env_vars()
        config = load_config()
        ensure_directories(config)
        print("✅ Environment check passed")
    except Exception as e:
        print(f"❌ Environment check failed: {e}")
        print("Please configure your .env file properly")
    
    # Run the app
    port = int(os.getenv('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=os.getenv('DEBUG', 'false').lower() == 'true')
