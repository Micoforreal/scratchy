# Product Requirements Document (PRD)
## Solana Narrative Detection Agent

**Version:** 1.0  
**Last Updated:** 2025-02-09  
**Status:** Initial Implementation

---

## Problem Statement

Builders, investors, and ecosystem teams in Solana need to identify emerging trends early to make informed decisions about what to build, where to invest, and how to allocate resources.

Current approaches have critical flaws:
- **Manual research**: Time-intensive, not scalable, subject to bias
- **LLM-first detection**: Prone to hallucination, lacks transparency
- **Volume-only metrics**: Miss nuanced narratives, favor established projects

**What's missing**: A systematic, explainable way to detect emerging narratives from real ecosystem data, with automatic idea generation.

---

## Target Users

### Primary
1. **Solana builders/founders**
   - Need: Discover what to build next based on real momentum
   - Outcome: Launch products that capitalize on emerging trends

2. **VCs/investors**
   - Need: Identify narrative trends before they become consensus
   - Outcome: Early position in high-growth sectors

3. **Ecosystem teams** (Solana Foundation, infrastructure providers)
   - Need: Understand where developer attention is flowing
   - Outcome: Better resource allocation and ecosystem support

### Secondary
- Researchers analyzing ecosystem dynamics
- Media/analysts covering Solana trends
- Developer relations teams at major protocols

---

## Non-Goals

This system explicitly does NOT:

- **Real-time monitoring**: This is batch processing (fortnightly windows), not streaming
- **Prediction/forecasting**: Detects current acceleration, doesn't predict future
- **Sentiment analysis**: Uses momentum, not sentiment scoring
- **Comprehensive coverage**: Focuses on quality signals from curated sources
- **Database**: V1 uses file-based storage for simplicity and inspectability
- **Web interface**: CLI-first, dashboard is future work

---

## System Overview

### Architecture Philosophy

**Algorithms first, LLMs second**

The system is designed as a **logical multi-agent pipeline** with clear separation of concerns:

1. **Signal Harvester** (No LLM)
   - Collects raw data from onchain, GitHub, and social sources
   - Stores structured signals with metadata
   - Completely deterministic and reproducible

2. **Narrative Analyst** (Limited LLM)
   - Normalizes signals into comparable scores
   - Detects momentum algorithmically
   - Clusters related signals using TF-IDF
   - Filters clusters into qualified narratives
   - Uses LLM only for labeling/naming clusters

3. **Synthesis Agent** (LLM-heavy)
   - Explains why narratives matter (evidence-backed)
   - Generates concrete product ideas
   - Operates only on already-validated narratives

**Critical design principle**: LLMs cannot hallucinate narratives end-to-end. They can only enhance algorithmically-detected patterns.

### Data Flow

```
Raw Sources → Signals → Normalization → Momentum → Clustering → Narratives → Explanation → Ideas → Report
     ↓            ↓           ↓             ↓           ↓            ↓             ↓          ↓         ↓
  Onchain     Structured   0-1 scale   Growth %    Proto-      Filtered    LLM labels  LLM ideas  Markdown
  GitHub       signals                              narratives   by rules
  Social
```

### Storage Strategy (V1)

**File-based only** for:
- Reproducibility (judges can inspect all intermediate outputs)
- Simplicity (no database setup required)
- Auditability (JSON files can be diff'd between runs)

**Directory structure:**
```
/data/raw/              # Raw collected signals (timestamped)
/data/processed/        # Normalized, momentum-scored signals
/reports/               # Final narrative briefs (Markdown + optional HTML)
```

---

## Signal Definitions

### 1. Onchain Signals
Metrics that reflect actual blockchain usage:

| Metric | Definition | Source | Momentum Calculation |
|--------|-----------|--------|---------------------|
| Transaction Volume | Daily tx count | RPC/Block explorer | Growth vs 14-day baseline |
| Active Wallets | Unique addresses | RPC | Growth vs baseline |
| Program Deployments | New programs deployed | On-chain analysis | Week-over-week change |
| TVL | Total value locked | DeFi aggregators | Growth % |

**V1 Implementation**: Mock data with realistic patterns

### 2. GitHub Signals
Development activity metrics:

| Metric | Definition | Source | Momentum Calculation |
|--------|-----------|--------|---------------------|
| Repository Stars | Star count growth | GitHub API | Week-over-week delta |
| Commit Activity | Commit frequency | GitHub API | Recent vs baseline |
| PR/Issue Activity | Development velocity | GitHub API | Acceleration |
| New Projects | Repos created | GitHub API | Count increase |

**Repo curation**: Track top 50 Solana ecosystem repos (configurable)

**V1 Implementation**: Mock data categorized by narrative themes

### 3. Social/Offchain Signals
Discourse and attention metrics:

| Metric | Definition | Source | Momentum Calculation |
|--------|-----------|--------|---------------------|
| Topic Mentions | Keyword frequency | Curated blogs/RSS | Growth in mentions |
| Content Volume | Articles/posts | Crawler | Publication increase |
| Engagement | Shares/comments | Social APIs | Engagement growth |

**Source curation**: Whitelist of high-signal sources (Solana blog, Helius, key ecosystem blogs)

**V1 Implementation**: Mock data with topic-based signals

---

## Narrative Detection Logic

### Stage 1: Signal Processing

**Normalization**
- Method: Min-max scaling (0-1)
- Applied per (signal_type, metric) group
- Ensures different scales are comparable

**Momentum Detection**
- Split time series: first half (baseline) vs second half (recent)
- Calculate growth: `((recent_avg - baseline_avg) / baseline_avg) * 100`
- Classify trend: accelerating, growing, flat, declining
- Flag signals with momentum ≥ threshold (default 15%)

**Clustering**
- Extract keywords from signal metadata (category, topics, tags)
- Group signals with shared keywords using co-occurrence
- Minimum cluster size: 3 signals
- Method: TF-IDF-like keyword similarity (no embeddings in V1)

### Stage 2: Narrative Qualification

A cluster becomes a **narrative** if:

1. **Multi-signal reinforcement**: At least 2 different signal types (e.g., onchain + GitHub)
2. **Sufficient momentum**: Average momentum ≥ 20%
3. **Cluster quality**: Cluster score ≥ 30/100
4. **Recency**: Signals from the current window

### Stage 3: Ranking

Narratives ranked by **strength score** (0-100):
- 60% momentum score (normalized)
- 40% cluster quality score

Top N narratives (default 7) are selected.

### Stage 4: LLM Enhancement

For each qualified narrative, LLM:
1. Generates clear narrative name (2-4 words)
2. Writes explanation (why it matters)
3. Lists 3-4 evidence points
4. Creates 3-5 concrete product ideas

**Prompts are structured** to ensure LLM stays grounded in provided evidence.

---

## Configuration Parameters

### `config.yaml` Structure

```yaml
window:
  duration_days: 14  # Fortnightly

signals:
  normalization_method: "minmax"
  momentum_threshold_pct: 15.0
  weights:
    onchain: 0.33
    github: 0.33
    social: 0.34

narratives:
  min_signal_types: 2
  min_momentum_score: 20
  max_narratives: 7
  
llm:
  temperature: 0.7
  max_tokens: 1500
  ideas_per_narrative: 5
```

### Environment Variables (`.env`)

**Required:**
- `LLM_PROVIDER`: "openai" or "local"
- `OPENAI_API_KEY` (if using OpenAI)
- `LOCAL_LLM_BASE_URL` (if using local LLM)

**Optional:**
- `GITHUB_TOKEN`: For real GitHub API access
- `SOLANA_RPC_URL`: For real onchain data
- `CRAWLER_BASE_URL`: For self-hosted crawler integration

---

## Output Format

### Narrative Brief (Markdown)

```markdown
# Solana Ecosystem Narrative Brief

**Period:** 2025-01-26 to 2025-02-09 (14 days)
**Generated:** 2025-02-09 14:32:15
**Narratives Detected:** 3

---

## 1. AI Agent Explosion

**Momentum Score:** 72.5 / 100

### Why it matters
[LLM-generated explanation...]

- Evidence point 1
- Evidence point 2
- Evidence point 3

### Build Ideas

1. **Idea Title**
   Description...

2. **Idea Title**
   Description...
```

### Intermediate Files (for inspection)

- `data/processed/01_raw_signals_TIMESTAMP.json`
- `data/processed/02_momentum_signals_TIMESTAMP.json`
- `reports/narrative_brief_TIMESTAMP.md`
- `reports/narrative_brief_latest.md` (always points to most recent)

---

## Known Limitations

### V1 Limitations (By Design)

1. **Mock data**: Current implementation uses placeholder data
   - Real API integration is straightforward replacement
   - Structure is designed for easy swapping

2. **File-based storage**: No database
   - Sufficient for fortnightly reports
   - Database can be added later without architecture changes

3. **Batch processing**: Not real-time
   - By design - narratives need time to develop
   - Real-time streaming is scope creep

4. **Single-process**: No true multi-agent orchestration
   - Code structure allows future split
   - Agent boundaries are logical, not physical

5. **TF-IDF clustering**: Simple keyword matching
   - Embeddings/semantic search can improve clustering
   - But TF-IDF is transparent and debuggable

### Technical Debt / Future Work

1. **Data quality**: Real APIs needed for production
2. **Source curation**: Needs human input to maintain signal quality
3. **Threshold tuning**: Current values are estimates, need real data to optimize
4. **Error handling**: Basic error handling, could be more robust
5. **Rate limiting**: Not implemented (needed for real APIs)
6. **Caching**: No caching of API results (would speed up development)

### Risks & Mitigations

**Risk**: LLM costs could be high  
**Mitigation**: LLM only called for qualified narratives (typically <10 per run), cost is bounded

**Risk**: Signal quality depends on source curation  
**Mitigation**: File-based storage allows easy auditing of signal quality

**Risk**: Thresholds might not work on real data  
**Mitigation**: All thresholds are configurable in `config.yaml`

**Risk**: GitHub rate limiting  
**Mitigation**: Use authenticated API calls, implement exponential backoff

---

## Success Metrics

### System Quality
- **Reproducibility**: Same input signals → same narratives (for non-LLM components)
- **Inspectability**: All intermediate outputs saved to files
- **Explainability**: Every narrative traceable to specific signals

### Output Quality
- **Relevance**: Narratives align with known ecosystem activity
- **Novelty**: Detects trends before they're widely recognized
- **Actionability**: Ideas are concrete and buildable

### For Bounty Submission
- **Code quality**: Type hints, docstrings, clear structure
- **Documentation**: README, PRD, inline comments
- **Configurability**: No hardcoded values

---

## Implementation Notes

### Dependencies

**Core:**
- Python 3.9+
- PyYAML (config parsing)
- NumPy (signal processing)
- Requests (API calls)

**Future (when replacing mocks):**
- `solana-py` or `anchorpy` for Solana RPC
- `PyGithub` for GitHub API
- `beautifulsoup4` for crawling (if not using self-hosted crawler)

### Code Standards

- Type hints for all functions
- Docstrings (Google style)
- Clear variable names
- Comments for non-obvious logic
- Fail loudly with helpful errors

### Testing Strategy (Future)

- Unit tests for signal processing (normalization, momentum)
- Integration tests for pipeline end-to-end
- Snapshot tests for LLM prompts
- Mock external APIs in tests

---

## Changelog

### V1.0 (2025-02-09)
- Initial implementation
- Mock data collectors
- Complete pipeline (collect → detect → explain → generate → report)
- File-based storage
- Configurable via YAML + env vars
- Full documentation

---

## Next Steps (Post-V1)

1. Replace mock collectors with real API integrations
2. Tune thresholds on real data
3. Add error handling and retry logic
4. Implement caching for API responses
5. Build web dashboard for visualization
6. Add database option for historical analysis
7. Implement true multi-agent orchestration (optional)
8. Add A/B testing for different prompt strategies

---

## Questions & Decisions

### Open Questions
- What's the optimal momentum threshold for Solana's pace?
- How to balance signal types (equal weight or onchain-heavy)?
- Should we detect negative narratives (declining trends)?

### Design Decisions
- **Why fortnightly?** Balance between signal quality and timeliness
- **Why TF-IDF over embeddings?** Transparency and debuggability for V1
- **Why file-based storage?** Inspectability for judges, simplicity for V1
- **Why OpenAI default?** Most accessible, but local LLM supported
