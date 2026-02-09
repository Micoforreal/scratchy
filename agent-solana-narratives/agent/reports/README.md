# Narrative Reports

This directory contains generated narrative briefs from the detection agent.

## Files

- `narrative_brief_YYYYMMDD_HHMMSS.md`: Timestamped reports
- `narrative_brief_latest.md`: Always points to the most recent report

## Report Structure

Each report includes:

1. **Metadata**: Date range, generation time, narrative count
2. **Narratives**: Ranked by strength score
3. **For each narrative:**
   - Name and momentum score
   - Why it matters (explanation)
   - Evidence points
   - 3-5 concrete build ideas

## Viewing Reports

Reports are in Markdown format and can be viewed in:
- Any text editor
- GitHub/GitLab (will render nicely)
- Markdown preview tools
- Converted to HTML (if enabled in config)

## Archival

Reports are automatically timestamped. You can keep historical reports to track how narratives evolve over time.
