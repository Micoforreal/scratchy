"""
Narrative explanation module.

Uses LLM to generate clear, evidence-backed explanations for why each narrative matters.
This is the first LLM-heavy component - used only AFTER narratives are algorithmically detected.
"""

from typing import Dict, Any, List

try:
    from ..llm import LLMClient
except ImportError:
    from llm import LLMClient


class NarrativeExplainer:
    """
    Generates explanations for detected narratives using LLM.
    
    Takes algorithmically-detected narratives and produces:
    - Better narrative names/labels
    - Why the narrative matters
    - Key evidence points
    """
    
    def __init__(self, llm_client: LLMClient):
        """
        Initialize narrative explainer.
        
        Args:
            llm_client: Configured LLM client
        """
        self.llm = llm_client
        
    def explain_narrative(self, narrative: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate explanation for a single narrative.
        
        Args:
            narrative: Narrative dictionary from detector
            
        Returns:
            Narrative with added 'explanation' and refined 'name' fields
        """
        # Build prompt with narrative evidence
        prompt = self._build_explanation_prompt(narrative)
        
        # Generate explanation
        response = self.llm.generate(prompt, temperature=0.7, max_tokens=800)
        
        # Parse response
        parsed = self._parse_explanation_response(response)
        
        # Update narrative with explanation
        narrative["name"] = parsed.get("name", narrative["narrative_name"])
        narrative["explanation"] = parsed.get("explanation", "")
        narrative["why_it_matters"] = parsed.get("why_it_matters", [])
        
        return narrative
    
    def explain_narratives(self, narratives: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Generate explanations for multiple narratives.
        
        Args:
            narratives: List of narrative dictionaries
            
        Returns:
            Narratives with explanations added
        """
        explained = []
        for narrative in narratives:
            explained.append(self.explain_narrative(narrative))
        return explained
    
    def _build_explanation_prompt(self, narrative: Dict[str, Any]) -> str:
        """
        Build LLM prompt for narrative explanation.
        
        Args:
            narrative: Narrative dictionary
            
        Returns:
            Formatted prompt string
        """
        keywords = ", ".join(narrative.get("keywords", []))
        signal_types = ", ".join(narrative.get("signal_types", []))
        momentum = narrative.get("momentum_score", 0.0)
        evidence = narrative.get("evidence", {})
        
        # Format evidence
        evidence_text = self._format_evidence(evidence)
        
        prompt = f"""You are analyzing emerging narratives in the Solana ecosystem.

A narrative has been detected with the following characteristics:

Keywords: {keywords}
Signal Types: {signal_types}
Momentum Score: {momentum:.1f}%

Evidence:
{evidence_text}

Your task:
1. Give this narrative a clear, concise name (2-4 words)
2. Explain why this narrative matters for the Solana ecosystem
3. Provide 3-4 evidence-backed bullet points

Format your response EXACTLY as:
NAME: <narrative name>
EXPLANATION: <1-2 sentence overview>
WHY IT MATTERS:
- <bullet point 1>
- <bullet point 2>
- <bullet point 3>
- <bullet point 4 (optional)>

Be specific and reference the actual evidence. Keep it concise and actionable."""

        return prompt
    
    def _format_evidence(self, evidence: Dict[str, Any]) -> str:
        """
        Format evidence dictionary into readable text.
        
        Args:
            evidence: Evidence dictionary
            
        Returns:
            Formatted evidence string
        """
        parts = []
        
        for signal_type, items in evidence.items():
            if not items:
                continue
            
            parts.append(f"\n{signal_type.upper()}:")
            
            # Take top 3 items per signal type
            for item in items[:3]:
                metric = item.get("metric", "unknown")
                momentum = item.get("momentum", 0.0)
                metadata = item.get("metadata", {})
                
                # Extract relevant metadata
                category = metadata.get("category", "")
                topic = metadata.get("topic", "")
                keywords = metadata.get("keywords", [])
                
                detail = f"  - {metric}: {momentum:.1f}% growth"
                if category:
                    detail += f" ({category})"
                if topic:
                    detail += f" [topic: {topic}]"
                if keywords:
                    detail += f" [keywords: {', '.join(keywords[:3])}]"
                
                parts.append(detail)
        
        return "\n".join(parts)
    
    def _parse_explanation_response(self, response: str) -> Dict[str, Any]:
        """
        Parse LLM response into structured format.
        
        Args:
            response: Raw LLM response
            
        Returns:
            Parsed dictionary with name, explanation, and why_it_matters
        """
        result = {
            "name": "",
            "explanation": "",
            "why_it_matters": []
        }
        
        lines = response.strip().split("\n")
        current_section = None
        
        for line in lines:
            line = line.strip()
            
            if line.startswith("NAME:"):
                result["name"] = line.replace("NAME:", "").strip()
            elif line.startswith("EXPLANATION:"):
                result["explanation"] = line.replace("EXPLANATION:", "").strip()
            elif line.startswith("WHY IT MATTERS:"):
                current_section = "why"
            elif current_section == "why" and line.startswith("-"):
                bullet = line.lstrip("- ").strip()
                if bullet:
                    result["why_it_matters"].append(bullet)
        
        return result
