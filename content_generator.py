"""
Content Generator using LLM API to create interconnected notes
Supports OpenAI API and can be extended for other providers
"""
import os
import json
import random
from typing import Dict, List, Optional

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


class ContentGenerator:
    """Generate interconnected content for Obsidian vaults using LLM API"""
    
    def __init__(self, api_key: Optional[str] = None, provider: str = "openai"):
        """
        Initialize the content generator
        
        Args:
            api_key: API key for the LLM provider (defaults to OPENAI_API_KEY env var)
            provider: LLM provider ("openai", "anthropic", etc.)
        """
        self.provider = provider
        self.api_key = api_key or os.getenv("OPENAI_API_KEY", "")
        
        if provider == "openai" and self.api_key and OPENAI_AVAILABLE:
            self.openai_client = OpenAI(api_key=self.api_key)
        else:
            self.openai_client = None
    
    def generate_note_content(
        self,
        topic: str,
        related_topics: List[str],
        note_type: str = "concept"
    ) -> str:
        """
        Generate content for a single note
        
        Args:
            topic: Main topic of the note
            related_topics: List of related topics to create links to
            note_type: Type of note (concept, person, event, etc.)
            
        Returns:
            Markdown content for the note
        """
        # Create links section
        links_section = "\n\n## Related Topics\n"
        for related in related_topics:
            links_section += f"- [[{related}]]\n"
        
        # If API key is available, use LLM to generate content
        if self.api_key and self.provider == "openai" and self.openai_client:
            return self._generate_with_openai(topic, related_topics, note_type)
        else:
            # Fallback to template-based generation
            return self._generate_template(topic, related_topics, note_type)
    
    def _generate_with_openai(
        self,
        topic: str,
        related_topics: List[str],
        note_type: str
    ) -> str:
        """Generate content using OpenAI API"""
        if not self.openai_client:
            return self._generate_template(topic, related_topics, note_type)
        
        try:
            related_str = ", ".join(related_topics)
            prompt = f"""Create a comprehensive Obsidian note about "{topic}".

Note type: {note_type}
Related topics: {related_str}

Include:
1. A clear introduction explaining the topic
2. Key concepts and definitions
3. Important details and context
4. Examples or applications if relevant
5. A "Related Topics" section with links to: {related_str}

Format as clean markdown. Use [[double brackets]] for internal links.
Keep it informative and well-structured."""

            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a knowledge management expert creating interconnected notes for an Obsidian vault."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            content = response.choices[0].message.content
            
            # Ensure links section is included
            if "## Related Topics" not in content:
                links_section = "\n\n## Related Topics\n"
                for related in related_topics:
                    links_section += f"- [[{related}]]\n"
                content += links_section
            
            return content
        except Exception as e:
            print(f"Error generating with OpenAI: {e}")
            return self._generate_template(topic, related_topics, note_type)
    
    def _generate_template(
        self,
        topic: str,
        related_topics: List[str],
        note_type: str
    ) -> str:
        """Generate content using templates (fallback)"""
        content = f"""# {topic}

## Overview

This note covers {topic} as a {note_type}.

## Key Points

- Add your key insights here
- Important information about {topic}
- Connections to other concepts

## Details

Expand on the topic here with relevant information and context.

## Related Topics

"""
        for related in related_topics:
            content += f"- [[{related}]]\n"
        
        content += f"\n## Tags\n#{note_type} #{topic.replace(' ', '').lower()}\n"
        
        return content
    
    def generate_vault_structure(
        self,
        main_topic: str,
        num_nodes: int = 20,
        connection_density: float = 0.3
    ) -> Dict[str, Dict]:
        """
        Generate a complete vault structure with interconnected nodes
        
        Args:
            main_topic: Central topic of the vault
            num_nodes: Number of notes to create
            connection_density: How interconnected (0.0 to 1.0)
            
        Returns:
            Dictionary mapping note names to their metadata and connections
        """
        # Generate topics
        topics = self._generate_topic_list(main_topic, num_nodes)
        
        # Create connections
        structure = {}
        
        # Initialize structure for all topics
        for topic in topics:
            structure[topic] = {"related": [], "note_type": self._determine_note_type(topic)}
        
        # Calculate target connections per node
        target_connections = max(2, int(num_nodes * connection_density))
        
        # Create connections
        for i, topic in enumerate(topics):
            # Get potential connections (all other topics)
            potential = [t for t in topics if t != topic]
            
            # Select connections: prefer nearby topics but add some randomness
            related = []
            for j, other_topic in enumerate(topics):
                if i != j:
                    distance = abs(i - j)
                    # Higher probability for closer topics, but allow some distant ones
                    max_distance = max(1, int(num_nodes * connection_density * 2))
                    if distance <= max_distance:
                        # Probability decreases with distance
                        prob = connection_density * (1.0 - (distance / max_distance) * 0.5)
                        if random.random() < prob:
                            related.append(other_topic)
            
            # Ensure minimum connections
            if len(related) < 2:
                # Add closest topics if we don't have enough
                remaining = [t for t in potential if t not in related]
                remaining.sort(key=lambda t: abs(topics.index(t) - i))
                related.extend(remaining[:2 - len(related)])
            
            # Limit to target connections
            related = related[:target_connections]
            
            # Update structure and ensure bi-directional connections
            structure[topic]["related"] = related
            for other_topic in related:
                if topic not in structure[other_topic]["related"]:
                    structure[other_topic]["related"].append(topic)
        
        return structure
    
    def _generate_topic_list(self, main_topic: str, count: int) -> List[str]:
        """Generate a list of related topics"""
        if self.api_key and self.provider == "openai" and self.openai_client:
            return self._generate_topics_with_ai(main_topic, count)
        else:
            return self._generate_topics_template(main_topic, count)
    
    def _generate_topics_with_ai(self, main_topic: str, count: int) -> List[str]:
        """Generate topics using AI"""
        if not self.openai_client:
            return self._generate_topics_template(main_topic, count)
        
        try:
            prompt = f"""Generate {count} interconnected topics related to "{main_topic}" for a knowledge base.

Return a JSON array of topic names (strings only, no other text).
Topics should be:
- Diverse and interesting
- Naturally interconnected
- Suitable for a knowledge graph
- Clear and specific

Example format: ["Topic 1", "Topic 2", "Topic 3", ...]"""

            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a knowledge base architect. Return only valid JSON arrays."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8,
                max_tokens=500
            )
            
            content = response.choices[0].message.content.strip()
            # Extract JSON array
            if content.startswith("```"):
                content = content.split("```")[1]
                if content.startswith("json"):
                    content = content[4:]
            content = content.strip()
            
            topics = json.loads(content)
            return [main_topic] + [t for t in topics if t != main_topic][:count-1]
        except Exception as e:
            print(f"Error generating topics with AI: {e}")
            return self._generate_topics_template(main_topic, count)
    
    def _generate_topics_template(self, main_topic: str, count: int) -> List[str]:
        """Generate topics using templates"""
        base_topics = [
            main_topic,
            f"{main_topic} Fundamentals",
            f"{main_topic} Applications",
            f"{main_topic} History",
            f"{main_topic} Best Practices",
            f"{main_topic} Advanced Concepts",
            f"{main_topic} Examples",
            f"{main_topic} Resources",
        ]
        
        # Generate additional topics
        extensions = [
            "Key Concepts",
            "Important Principles",
            "Common Patterns",
            "Use Cases",
            "Related Technologies",
            "Future Trends",
            "Getting Started",
            "Deep Dive",
            "Quick Reference",
            "Troubleshooting"
        ]
        
        all_topics = base_topics[:count]
        while len(all_topics) < count:
            all_topics.append(f"{main_topic} - {extensions[len(all_topics) % len(extensions)]}")
        
        return all_topics[:count]
    
    def _determine_note_type(self, topic: str) -> str:
        """Determine the type of note based on topic"""
        topic_lower = topic.lower()
        if any(word in topic_lower for word in ["person", "author", "scientist"]):
            return "person"
        elif any(word in topic_lower for word in ["event", "meeting", "conference"]):
            return "event"
        elif any(word in topic_lower for word in ["project", "case study"]):
            return "project"
        else:
            return "concept"

