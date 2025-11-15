"""
MCP Client for interacting with Obsidian MCP Server
Handles communication with the Obsidian vault through MCP protocol
"""
from typing import List, Optional
from pathlib import Path


class ObsidianMCPClient:
    """Client for interacting with Obsidian MCP server"""
    
    def __init__(self):
        """
        Initialize the MCP client
        """
        pass
    
    def create_note(self, vault_path: str, note_name: str, content: str) -> bool:
        """
        Create a new note in the Obsidian vault
        
        Args:
            vault_path: Path to the Obsidian vault
            note_name: Name of the note (without .md extension)
            content: Markdown content for the note
            
        Returns:
            True if successful, False otherwise
        """
        note_path = Path(vault_path) / f"{note_name}.md"
        note_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            note_path.write_text(content, encoding='utf-8')
            return True
        except Exception as e:
            print(f"Error creating note {note_name}: {e}")
            return False
    
    def create_note_with_path(self, note_path: str, content: str) -> bool:
        """
        Create a note at a specific path
        
        Args:
            note_path: Full path to the note file
            content: Markdown content for the note
            
        Returns:
            True if successful, False otherwise
        """
        path = Path(note_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            path.write_text(content, encoding='utf-8')
            return True
        except Exception as e:
            print(f"Error creating note at {note_path}: {e}")
            return False
    
    def read_note(self, vault_path: str, note_name: str) -> Optional[str]:
        """
        Read a note from the vault
        
        Args:
            vault_path: Path to the Obsidian vault
            note_name: Name of the note (without .md extension)
            
        Returns:
            Note content or None if not found
        """
        note_path = Path(vault_path) / f"{note_name}.md"
        
        if note_path.exists():
            return note_path.read_text(encoding='utf-8')
        return None
    
    def list_notes(self, vault_path: str) -> List[str]:
        """
        List all notes in the vault
        
        Args:
            vault_path: Path to the Obsidian vault
            
        Returns:
            List of note names
        """
        vault = Path(vault_path)
        notes = []
        
        for md_file in vault.rglob("*.md"):
            if ".obsidian" not in str(md_file):
                relative = md_file.relative_to(vault)
                notes.append(str(relative.with_suffix("")))
        
        return notes
    
    def update_note(self, vault_path: str, note_name: str, content: str) -> bool:
        """
        Update an existing note
        
        Args:
            vault_path: Path to the Obsidian vault
            note_name: Name of the note (without .md extension)
            content: New markdown content
            
        Returns:
            True if successful, False otherwise
        """
        return self.create_note(vault_path, note_name, content)
    
    def link_notes(self, source_note: str, target_notes: List[str], vault_path: str) -> bool:
        """
        Add links to other notes in a source note
        
        Args:
            source_note: Name of the source note
            target_notes: List of target note names to link to
            vault_path: Path to the Obsidian vault
            
        Returns:
            True if successful, False otherwise
        """
        content = self.read_note(vault_path, source_note)
        if content is None:
            return False
        
        # Check if links section exists
        if "## Links" not in content:
            content += "\n\n## Links\n"
        
        # Add links
        for target in target_notes:
            link = f"- [[{target}]]"
            if link not in content:
                content += f"\n{link}"
        
        return self.update_note(vault_path, source_note, content)

