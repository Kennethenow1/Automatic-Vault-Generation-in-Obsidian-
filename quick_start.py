#!/usr/bin/env python3
"""
Quick start script - interactive vault generation
"""
import os
from vault_generator import VaultGenerator

def main():
    print("=" * 60)
    print("  Obsidian Vault Generator - Quick Start")
    print("=" * 60)
    print()
    
    # Get vault details
    topic = input("Enter the main topic for your vault: ").strip()
    if not topic:
        print("Error: Topic is required!")
        return
    
    vault_name = input(f"Enter vault name (default: {topic.replace(' ', '-')}): ").strip()
    if not vault_name:
        vault_name = topic.replace(' ', '-')
    
    # Get number of notes
    num_notes_input = input("Number of notes to create (default: 30): ").strip()
    try:
        num_notes = int(num_notes_input) if num_notes_input else 30
    except ValueError:
        num_notes = 30
        print("Invalid input, using default: 30")
    
    # Get connection density
    density_input = input("Connection density 0.0-1.0 (default: 0.4): ").strip()
    try:
        density = float(density_input) if density_input else 0.4
        density = max(0.0, min(1.0, density))  # Clamp between 0 and 1
    except ValueError:
        density = 0.4
        print("Invalid input, using default: 0.4")
    
    # Get vault path
    vault_path_input = input("Vault base path (default: ~/Obsidian-Vaults): ").strip()
    vault_base_path = os.path.expanduser(vault_path_input) if vault_path_input else os.path.expanduser("~/Obsidian-Vaults")
    
    # Check for API key
    api_key = os.getenv("OPENAI_API_KEY")
    use_ai = bool(api_key)
    
    if not use_ai:
        print("\n  No OPENAI_API_KEY found. Using template-based generation.")
        print("   Set OPENAI_API_KEY environment variable for AI-generated content.")
    else:
        print("\n✓ OpenAI API key found. Will use AI for content generation.")
    
    print("\n" + "=" * 60)
    print("  Generating Vault...")
    print("=" * 60)
    print()
    
    # Create generator
    generator = VaultGenerator(
        vault_base_path=vault_base_path,
        api_key=api_key
    )
    
    # Generate vault
    vault_path = generator.create_interconnected_vault(
        vault_name=vault_name,
        main_topic=topic,
        num_notes=num_notes,
        connection_density=density
    )
    
    print("\n" + "=" * 60)
    print("   Vault Created Successfully!")
    print("=" * 60)
    print(f"\n Location: {vault_path}")
    print(f"\n Next Steps:")
    print(f"   1. Open Obsidian")
    print(f"   2. Click 'Open another vault'")
    print(f"   3. Select: {vault_path}")
    print(f"   4. Press Ctrl+G (Cmd+G on Mac) to view the graph!")
    print()

if __name__ == "__main__":
    main()

