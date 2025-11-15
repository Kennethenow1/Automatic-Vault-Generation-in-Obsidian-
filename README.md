# Obsidian Vault Generator with MCP


**If you ever need to use the Obsidian MCP server for generating full notes** – for research, learning, knowledge bases, or exploring topics – this tool provides automated vault generation with rich interconnections optimized for Obsidian's graph view.

<img width="1823" height="980" alt="Screenshot from 2025-11-15 00-05-17" src="https://github.com/user-attachments/assets/ee71c40b-49dd-4c76-ad00-c69a4ec73807" />
**File structure that was generated**
<img width="1823" height="980" alt="Screenshot from 2025-11-15 00-05-29" src="https://github.com/user-attachments/assets/08a5c369-a9dc-4453-a5cf-ee0a8f4f7173" />
**Picture of one of the enteries**
<img width="1470" height="962" alt="Screenshot from 2025-11-15 00-05-39" src="https://github.com/user-attachments/assets/915f15e6-e136-4a56-996b-18d614be228d" />
**Picture of the obsidian map**

## Features


- **Automated Vault Creation**: Generate entire vaults from a single topic prompt
- **Rich Interconnections**: Creates bidirectional links between related notes for graph visualization
- **AI-Powered Content**: Uses OpenAI or other LLM APIs to generate note content (templates available as fallback)
- **Graph View Optimized**: Configured for Obsidian's graph view with proper link formatting
- **MCP Integration**: Built on the Obsidian MCP server for direct vault manipulation

## Setup

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Set your API key** (optional, for AI-generated content):
```bash
export OPENAI_API_KEY="your-api-key-here"
```

Or use Anthropic:
```bash
export ANTHROPIC_API_KEY="your-api-key-here"
```

The generator will use template-based content if no API key is provided.

## Usage

### Basic Usage

```bash
python vault_generator.py --topic "Machine Learning" --vault-name "ML-Knowledge-Base"
```

### Advanced Options

```bash
python vault_generator.py \
  --topic "Quantum Computing" \
  --vault-name "Quantum-Vault" \
  --notes 50 \
  --density 0.5 \
  --vault-path ~/Obsidian-Vaults \
  --api-key your-api-key
```

### Parameters

- `--topic`: Main topic for the vault (required)
- `--vault-name`: Name of the vault folder (default: "Knowledge-Vault")
- `--notes`: Number of notes to create (default: 30)
- `--density`: Connection density between 0.0 and 1.0 (default: 0.4)
  - Higher = more interconnected
  - Recommended: 0.3-0.6 for good graph visualization
- `--vault-path`: Base directory for vaults (default: ~/Obsidian-Vaults)
- `--api-key`: LLM API key (or use environment variable)

### Programmatic Usage

```python
from vault_generator import VaultGenerator

generator = VaultGenerator(
    vault_base_path="~/Obsidian-Vaults",
    api_key="your-api-key"  # optional
)

vault_path = generator.create_interconnected_vault(
    vault_name="My-Knowledge-Vault",
    main_topic="Artificial Intelligence",
    num_notes=40,
    connection_density=0.45
)
```

## How It Works

1. **Structure Generation**: Creates a network of topics with interconnections
2. **Content Generation**: Uses the Obsidian MCP server to generate full notes with content (or templates)
3. **Link Creation**: Establishes bidirectional links between related notes
4. **Hub Notes**: Creates central hub notes connecting to multiple topics
5. **Configuration**: Sets up Obsidian configuration optimized for graph view

## Graph View

After generating your vault:

1. Open the vault in Obsidian
2. Press `Ctrl+G` (or `Cmd+G` on Mac) to open graph view
3. Use filter options to explore:
   - Tags
   - Orphans
   - Unlinked mentions
4. Click nodes to navigate between notes
5. Adjust graph settings in `.obsidian/graph.json` for customization

## Output

A typical vault contains:

- **README.md**: Index note with links to all topics
- **Knowledge Hubs.md**: Central interconnection points
- **30+ interconnected notes**: Each with multiple bidirectional links
- **Obsidian configuration**: Optimized for graph visualization

## API Providers

Currently supports:
- **OpenAI** (default) - via `openai` package
- **Anthropic** - via `anthropic` package (extend `content_generator.py`)

To add more providers, extend the `ContentGenerator` class.

## Requirements

- Python 3.8+
- Obsidian installed (to view the vault)
- LLM API key (optional, falls back to templates)

## Troubleshooting

**No API key?** The generator will use template-based content generation.

**Graph view not showing connections?** Ensure:
- Notes use `[[double brackets]]` for links
- Graph view is enabled in Obsidian
- Check `.obsidian/graph.json` configuration

**Too many/few connections?** Adjust the `--density` parameter:
- Lower (0.2-0.3) = fewer connections, cleaner graph
- Higher (0.5-0.7) = more connections, denser web
- Recommended: 0.3-0.6

## About

**If you ever need to use the Obsidian MCP server for generating full notes** – for research, learning, knowledge bases, or exploring topics – this tool provides automated vault generation with rich interconnections.

The Obsidian MCP server handles vault manipulation, allowing you to focus on content exploration rather than manual setup.

## License

MIT License - feel free to modify and use as needed

