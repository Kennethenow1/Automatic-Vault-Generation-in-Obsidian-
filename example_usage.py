"""
Example usage of the Obsidian Vault Generator
"""
from vault_generator import VaultGenerator
import os

# Example 1: Create a vault about Python Programming
print("Example 1: Creating Python Programming vault...")
generator = VaultGenerator(
    vault_base_path="~/Obsidian-Vaults",
    api_key=os.getenv("OPENAI_API_KEY")  # or None to use templates
)

vault_path = generator.create_interconnected_vault(
    vault_name="Python-Programming",
    main_topic="Python Programming",
    num_notes=35,
    connection_density=0.45  # Good balance for graph view
)

print(f"Created vault at: {vault_path}")

# Example 2: Create a smaller, highly connected vault about a specific topic
print("\nExample 2: Creating Machine Learning vault...")
vault_path2 = generator.create_interconnected_vault(
    vault_name="Machine-Learning-Basics",
    main_topic="Machine Learning",
    num_notes=25,
    connection_density=0.6  # Higher density = more connections
)

print(f"Created vault at: {vault_path2}")

# Example 3: Create a large knowledge base
print("\nExample 3: Creating comprehensive knowledge base...")
vault_path3 = generator.create_interconnected_vault(
    vault_name="Knowledge-Base",
    main_topic="General Knowledge",
    num_notes=50,
    connection_density=0.35  # Lower density for large vaults
)

print(f"Created vault at: {vault_path3}")

print("\n✅ All examples completed!")
print("Open Obsidian and add these vault folders to explore the graph views.")

