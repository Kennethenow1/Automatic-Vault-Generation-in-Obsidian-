"""
Main vault generator that uses MCP client and content generator
to create interconnected Obsidian vaults
"""
import os
import json
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

from mcp_obsidian_client import ObsidianMCPClient
from content_generator import ContentGenerator


class VaultGenerator:
    """Generate complete interconnected Obsidian vaults"""
    
    def __init__(
        self,
        vault_base_path: str,
        api_key: Optional[str] = None,
        provider: str = "openai"
    ):
        """
        Initialize the vault generator
        
        Args:
            vault_base_path: Base directory where vaults will be created
            api_key: LLM API key (optional, can use env var)
            provider: LLM provider name
        """
        self.vault_base_path = Path(vault_base_path)
        self.vault_base_path.mkdir(parents=True, exist_ok=True)
        
        self.mcp_client = ObsidianMCPClient()
        self.content_generator = ContentGenerator(api_key=api_key, provider=provider)
    
    def create_interconnected_vault(
        self,
        vault_name: str,
        main_topic: str,
        num_notes: int = 30,
        connection_density: float = 0.4,
        use_ai: bool = True
    ) -> Path:
        """
        Create a complete interconnected vault
        
        Args:
            vault_name: Name for the new vault
            main_topic: Central topic of the vault
            num_notes: Number of notes to create
            connection_density: How interconnected (0.0 to 1.0)
            use_ai: Whether to use AI for content generation
            
        Returns:
            Path to the created vault
        """
        vault_path = self.vault_base_path / vault_name
        vault_path.mkdir(parents=True, exist_ok=True)
        
        print(f"Creating vault: {vault_name}")
        print(f"Main topic: {main_topic}")
        print(f"Generating {num_notes} interconnected notes...")
        
        # Generate vault structure
        structure = self.content_generator.generate_vault_structure(
            main_topic,
            num_nodes=num_notes,
            connection_density=connection_density
        )
        
        # Create index/README note
        self._create_index_note(vault_path, main_topic, list(structure.keys()))
        
        # Create all notes with their connections
        created_notes = {}
        for topic, metadata in structure.items():
            print(f"  Creating note: {topic}")
            content = self.content_generator.generate_note_content(
                topic=topic,
                related_topics=metadata["related"],
                note_type=metadata["note_type"]
            )
            
            # Clean topic name for filename
            note_name = self._sanitize_filename(topic)
            success = self.mcp_client.create_note(
                str(vault_path),
                note_name,
                content
            )
            
            if success:
                created_notes[topic] = note_name
        
        # Create additional hub notes for better connectivity
        self._create_hub_notes(vault_path, structure, created_notes)
        
        # Setup Obsidian configuration
        self._setup_obsidian_config(vault_path)
        
        print(f"\n✓ Vault created successfully at: {vault_path}")
        print(f"  Total notes: {len(created_notes)}")
        print(f"  Open this path in Obsidian to explore the graph!")
        
        return vault_path
    
    def _create_index_note(self, vault_path: Path, main_topic: str, all_topics: List[str]):
        """Create an index/README note with links to all other notes"""
        index_content = f"""# {main_topic} - Knowledge Vault

**Created:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Overview

This vault contains interconnected knowledge about **{main_topic}**. Use the graph view in Obsidian to explore the connections between concepts.

## Quick Navigation

### Main Topic
- [[{self._sanitize_filename(main_topic)}]]

### All Topics

"""
        # Group topics for better organization
        for topic in sorted(all_topics):
            note_name = self._sanitize_filename(topic)
            index_content += f"- [[{note_name}]]\n"
        
        index_content += f"""
## Graph View

Open the graph view in Obsidian (Ctrl+G / Cmd+G) to visualize the connections between all notes.

## Statistics

- **Total Notes:** {len(all_topics)}
- **Main Topic:** {main_topic}
- **Connection Density:** High - all notes are interconnected

## How to Use

1. Open this vault in Obsidian
2. Explore notes by clicking links
3. Use graph view to see connections
4. Add your own notes and connections
"""
        
        self.mcp_client.create_note(str(vault_path), "README", index_content)
    
    def _create_hub_notes(self, vault_path: Path, structure: Dict, created_notes: Dict):
        """Create hub notes that connect multiple related topics"""
        # Find highly connected nodes (hubs)
        connection_counts = {topic: len(meta["related"]) for topic, meta in structure.items()}
        sorted_topics = sorted(connection_counts.items(), key=lambda x: x[1], reverse=True)
        
        # Create a hub note for top connections
        if sorted_topics:
            hub_content = """# Knowledge Hubs

These are the most interconnected nodes in the vault - excellent starting points for exploration.

## Central Hubs

"""
            for topic, count in sorted_topics[:10]:
                note_name = created_notes.get(topic, self._sanitize_filename(topic))
                hub_content += f"- [[{note_name}]] ({count} connections)\n"
            
            self.mcp_client.create_note(str(vault_path), "Knowledge Hubs", hub_content)
    
    def _setup_obsidian_config(self, vault_path: Path):
        """Setup basic Obsidian configuration"""
        obsidian_dir = vault_path / ".obsidian"
        obsidian_dir.mkdir(exist_ok=True)
        
        # Basic app configuration
        app_config = {
            "newFileLocation": "folder",
            "newFileFolderPath": "",
            "attachmentFolderPath": "attachments",
            "showLineNumber": True,
            "spellcheck": True,
            "alwaysUpdateLinks": True,
            "strictLineBreaks": False
        }
        
        app_json = obsidian_dir / "app.json"
        with open(app_json, "w") as f:
            json.dump(app_config, f, indent=2)
        
        # Graph view configuration for better visualization
        graph_config = {
            "collapse-filter": True,
            "search": "",
            "showTags": True,
            "showAttachments": True,
            "hideUnresolved": False,
            "showOrphans": True,
            "collapse-color-groups": True,
            "colorGroups": [],
            "collapse-display": True,
            "showArrow": True,
            "textFadeMultiplier": 0,
            "nodeSizeMultiplier": 1,
            "lineSizeMultiplier": 1,
            "collapse-forces": True,
            "centerStrength": 0.518713248970312,
            "repelStrength": 10,
            "linkStrength": 1,
            "linkDistance": 250,
            "scale": 1.0
        }
        
        graph_json = obsidian_dir / "graph.json"
        with open(graph_json, "w") as f:
            json.dump(graph_config, f, indent=2)
        
        print("  ✓ Obsidian configuration created")
    
    def _sanitize_filename(self, name: str) -> str:
        """Sanitize a name for use as a filename"""
        # Remove invalid characters
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            name = name.replace(char, '_')
        
        # Remove leading/trailing dots and spaces
        name = name.strip('. ')
        
        # Limit length
        if len(name) > 100:
            name = name[:100]
        
        return name


def main():
    """Example usage"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate interconnected Obsidian vaults")
    parser.add_argument("--vault-name", default="Knowledge-Vault", help="Name for the vault")
    parser.add_argument("--topic", required=True, help="Main topic for the vault")
    parser.add_argument("--notes", type=int, default=30, help="Number of notes to create")
    parser.add_argument("--density", type=float, default=0.4, help="Connection density (0.0-1.0)")
    parser.add_argument("--vault-path", default="~/Obsidian-Vaults", help="Base path for vaults")
    parser.add_argument("--api-key", help="LLM API key (or use OPENAI_API_KEY env var)")
    
    args = parser.parse_args()
    
    # Expand user path
    vault_base = os.path.expanduser(args.vault_path)
    
    generator = VaultGenerator(
        vault_base_path=vault_base,
        api_key=args.api_key
    )
    
    vault_path = generator.create_interconnected_vault(
        vault_name=args.vault_name,
        main_topic=args.topic,
        num_notes=args.notes,
        connection_density=args.density
    )
    
    print(f"\n🎉 Done! Open Obsidian and add this vault: {vault_path}")


if __name__ == "__main__":
    main()

