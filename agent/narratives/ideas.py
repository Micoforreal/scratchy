"""
Product idea generation module.

Uses LLM to generate concrete, realistic product ideas from detected narratives.
This is LLM-heavy but operates only on already-validated narratives.
"""

from typing import Dict, Any, List

try:
    from ..llm import LLMClient
except ImportError:
    from llm import LLMClient


class IdeaGenerator:
    """
    Generates product/build ideas from narratives using LLM.
    
    Takes explained narratives and produces actionable product ideas
    that builders could actually implement.
    """
    
    def __init__(self, llm_client: LLMClient, ideas_per_narrative: int = 5):
        """
        Initialize idea generator.
        
        Args:
            llm_client: Configured LLM client
            ideas_per_narrative: Number of ideas to generate per narrative
        """
        self.llm = llm_client
        self.ideas_per_narrative = ideas_per_narrative
        
    def generate_ideas(self, narrative: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate product ideas for a single narrative.
        
        Args:
            narrative: Explained narrative dictionary
            
        Returns:
            Narrative with added 'build_ideas' field
        """
        # Build prompt
        prompt = self._build_ideas_prompt(narrative)
        
        # Generate ideas
        response = self.llm.generate(prompt, temperature=0.8, max_tokens=1200)
        
        # Parse response
        ideas = self._parse_ideas_response(response)
        
        # Add to narrative
        narrative["build_ideas"] = ideas
        
        return narrative
    
    def generate_ideas_batch(self, narratives: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Generate ideas for multiple narratives.
        
        Args:
            narratives: List of explained narratives
            
        Returns:
            Narratives with build ideas added
        """
        for narrative in narratives:
            self.generate_ideas(narrative)
        return narratives
    
    def _build_ideas_prompt(self, narrative: Dict[str, Any]) -> str:
        """
        Build LLM prompt for idea generation.
        
        Args:
            narrative: Narrative dictionary
            
        Returns:
            Formatted prompt string
        """
        name = narrative.get("name", narrative.get("narrative_name", "Unknown"))
        explanation = narrative.get("explanation", "")
        why_matters = narrative.get("why_it_matters", [])
        keywords = ", ".join(narrative.get("keywords", []))
        
        why_matters_text = "\n".join(f"- {point}" for point in why_matters)
        
        prompt = f"""You are a product strategist helping Solana builders identify opportunities.

Narrative: {name}

Overview: {explanation}

Why it matters:
{why_matters_text}

Related keywords: {keywords}

Generate {self.ideas_per_narrative} concrete, realistic product ideas that builders could create to capitalize on this narrative.

Requirements for each idea:
- Must be specific and actionable (not vague)
- Should be realistic for a small team to build
- Should directly address the narrative/trend
- Mix of new products and improvements to existing solutions
- Avoid generic ideas - be creative and practical

Format your response EXACTLY as:
IDEA 1: <Title>
<2-3 sentence description of what to build and why>

IDEA 2: <Title>
<2-3 sentence description>

[Continue for all {self.ideas_per_narrative} ideas]

Make each idea specific enough that a developer could start building."""

        return prompt
    
    def _parse_ideas_response(self, response: str) -> List[Dict[str, str]]:
        """
        Parse LLM response into structured ideas.
        
        Args:
            response: Raw LLM response
            
        Returns:
            List of idea dictionaries with 'title' and 'description'
        """
        ideas = []
        lines = response.strip().split("\n")
        
        current_idea = None
        current_description = []
        
        for line in lines:
            line = line.strip()
            
            # Check if this is a new idea header
            if line.startswith("IDEA "):
                # Save previous idea if exists
                if current_idea:
                    ideas.append({
                        "title": current_idea,
                        "description": " ".join(current_description).strip()
                    })
                
                # Start new idea
                parts = line.split(":", 1)
                if len(parts) == 2:
                    current_idea = parts[1].strip()
                    current_description = []
            elif current_idea and line:
                # Add to current idea description
                current_description.append(line)
        
        # Don't forget the last idea
        if current_idea:
            ideas.append({
                "title": current_idea,
                "description": " ".join(current_description).strip()
            })
        
        return ideas[:self.ideas_per_narrative]
