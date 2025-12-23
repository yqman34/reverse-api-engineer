# 🔄 Reverse API

[![PyPI version](https://badge.fury.io/py/reverse-api.svg)](https://badge.fury.io/py/reverse-api)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Reverse API** is an AI-powered tool that captures browser traffic and automatically generates production-ready Python API clients. No more manual reverse engineering—just browse, capture, and get clean API code.

## ✨ Features

- 🌐 **Browser Automation**: Built on Playwright with stealth mode for realistic browsing
- 📊 **HAR Recording**: Captures all network traffic in HTTP Archive format
- 🤖 **AI-Powered Generation**: Uses Claude 4.5 to analyze traffic and generate clean Python code
- 💻 **Interactive CLI**: Minimalist terminal interface with mode cycling (Shift+Tab)
- 📦 **Production Ready**: Generated scripts include error handling, type hints, and documentation
- 💾 **Session History**: All runs saved locally with full message logs
- 💰 **Cost Tracking**: Detailed token usage and cost estimation with cache support

## 🚀 Installation

### Using pip
```bash
pip install reverse-api
```

### Using uv (recommended)
```bash
uv tool install reverse-api
```

### From source
```bash
git clone https://github.com/kalil0321/reverse-api.git
cd reverse-api
uv sync
```

### Post-installation
Install Playwright browsers:
```bash
playwright install chromium
```

## 📖 Usage

### Quick Start

Launch the interactive CLI:
```bash
reverse-api
```

The CLI has two modes (cycle with **Shift+Tab**):
- **manual**: Full pipeline (browser capture + AI generation)
- **engineer**: Reverse engineer from existing run_id

### Manual Mode (Full Pipeline)

1. Start the CLI: `reverse-api`
2. Enter your task description (e.g., "Fetch Apple job listings")
3. Optionally provide a starting URL
4. Browse and interact with the website
5. Close the browser when done
6. AI automatically generates the API client

Generated scripts are saved to:
- `~/.reverse-api/runs/scripts/{run_id}/` (permanent storage)
- `./scripts/{descriptive_name}/` (local copy with readable name)

### Engineer Mode (Re-process existing captures)

Re-run AI generation on a previous capture:
```bash
# In CLI, switch to engineer mode (Shift+Tab) and enter run_id
# Or use command line:
reverse-api engineer <run_id>
```

### CLI Commands

While in the CLI, use these slash commands:
- `/settings` - Configure model and output directory
- `/history` - View past runs with costs
- `/messages <run_id>` - View detailed message logs
- `/help` - Show all commands
- `/exit` - Quit

### Model Selection

Choose from Claude 4.5 models:
- **Sonnet 4.5** (default): Balanced performance and cost
- **Opus 4.5**: Maximum capability for complex APIs
- **Haiku 4.5**: Fastest and most economical

Change model in `/settings` or via CLI:
```bash
reverse-api manual --model claude-sonnet-4-5
```

## 🔧 Configuration

Settings are stored in `~/.reverse-api/config.json`:
```json
{
  "model": "claude-sonnet-4-5",
  "output_dir": null
}
```

## 📁 Project Structure

```
~/.reverse-api/
├── config.json          # User settings
├── history.json         # Run history with metadata
└── runs/
    ├── har/{run_id}/    # Captured HAR files
    ├── scripts/{run_id}/ # Generated API clients
    └── messages/{run_id}.jsonl # Full message logs
```

## 💡 Examples

### Example: Reverse Engineering a Job Board API

```bash
$ reverse-api
> fetch all apple jobs from their careers page

# Browser opens, you navigate and interact
# Close browser when done

# AI generates:
# - api_client.py (full API implementation)
# - README.md (documentation)
# - example_usage.py (usage examples)

# Scripts copied to: ./scripts/apple_jobs_api/
```

Generated `api_client.py` includes:
- Authentication handling
- Clean function interfaces
- Type hints and docstrings
- Error handling
- Production-ready code

## 🛠️ Development

### Setup
```bash
git clone https://github.com/kalil0321/reverse-api.git
cd reverse-api
uv sync
```

### Run locally
```bash
uv run reverse-api
```

### Build
```bash
uv build
```

## 🔐 Requirements

- Python 3.10+
- Anthropic API key (set as `ANTHROPIC_API_KEY` environment variable)
- Playwright browsers installed

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
