# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Reverse API Engineer is a CLI tool that captures browser traffic (HAR files) and uses AI to automatically generate production-ready Python API clients. It supports three modes: manual browser capture, autonomous AI agent browsing, and re-engineering from previous captures.

## Core Architecture

### SDK Dispatch Pattern
The project uses a **dual-SDK architecture** controlled by `config.json`:

- **Claude SDK** (`engineer.py` → `ClaudeEngineer`): Uses `claude-agent-sdk` for direct Claude API integration
- **OpenCode SDK** (`opencode_engineer.py` → `OpenCodeEngineer`): Uses httpx to communicate with local OpenCode server (http://127.0.0.1:4096)

Both inherit from `BaseEngineer` (abstract base class) which defines the common interface and shared prompt building logic. The SDK selection is determined by the `sdk` field in config.

### Key Components

- **CLI Layer** (`cli.py`): Main entry point with mode cycling (manual/engineer/agent), slash commands, and interactive prompts
- **Browser** (`browser.py`): Playwright-based HAR recording with stealth mode and anti-detection measures
  - `ManualBrowser`: User-controlled browser with HAR capture
  - `run_agent_browser()`: Autonomous agent browsing (browser-use or stagehand)
- **Configuration** (`config.py`): JSON-based config manager at `~/.reverse-api/config.json`
- **Session Management** (`session.py`): Tracks run history with costs and metadata
- **Message Store** (`messages.py`): Persists full conversation logs per run
- **UI** (`tui.py`, `opencode_ui.py`): Rich-based terminal UI for progress tracking

### Data Flow
1. Browser captures HAR → saved to `~/.reverse-api/runs/{run_id}/har/`
2. Engineer analyzes HAR with LLM → generates Python scripts
3. Scripts saved to:
   - `~/.reverse-api/runs/{run_id}/scripts/` (permanent)
   - `./scripts/{descriptive_name}/` (local copy)

## Development Commands

### Setup
```bash
# Clone and install dependencies
git clone https://github.com/kalil0321/reverse-api-engineer.git
cd reverse-api-engineer
uv sync
playwright install chromium

# Run locally (development mode)
uv run reverse-api-engineer
```

### Building
```bash
# Clean build (removes all caches and artifacts)
./scripts/clean_build.sh

# Manual build
uv build
```

### Testing
```bash
# Test as installed package (creates isolated venv)
python -m venv test_env
test_env/bin/pip install dist/*.whl
test_env/bin/reverse-api-engineer

# Test with uv tool
uv tool install .
reverse-api-engineer
```

## Release Process

**Single source of truth: `pyproject.toml`**

1. Update version in `pyproject.toml` only
2. Update `CHANGELOG.md`
3. Run `./scripts/clean_build.sh`
4. Commit and tag:
   ```bash
   git add pyproject.toml CHANGELOG.md
   git commit -m "release: vX.Y.Z - description"
   git tag vX.Y.Z
   git push origin main
   git push origin vX.Y.Z
   ```
5. Publish to PyPI:
   ```bash
   source .env  # contains UV_PUBLISH_TOKEN or PYPI_TOKEN
   uv publish
   ```

**Important:** Never edit `src/reverse_api/__init__.py` for versioning—it reads from package metadata via `importlib.metadata`.

## Configuration System

### Config Location
`~/.reverse-api/config.json` with these fields:

```json
{
  "claude_code_model": "claude-sonnet-4-5",    // For Claude SDK
  "opencode_provider": "anthropic",            // For OpenCode SDK
  "opencode_model": "claude-sonnet-4-5",       // For OpenCode SDK
  "sdk": "claude",                             // "claude" or "opencode"
  "agent_provider": "browser-use",             // "browser-use" or "stagehand"
  "browser_use_model": "bu-llm",               // Browser-use agent model
  "stagehand_model": "openai/computer-use-preview-2025-03-11",
  "output_dir": null                           // Custom output dir (null = use ~/.reverse-api/runs)
}
```

### Model Naming
- **Claude models**: `claude-sonnet-4-5`, `claude-opus-4-5`, `claude-haiku-4-5`
- **Gemini models**: `gemini-3-flash`, `gemini-3-pro`, `gemini-3-pro-low`, `gemini-3-pro-high`
- **Antigravity models** (free tier): Require OpenCode SDK with `opencode_provider: "google"`
- **Agent models**: Format varies by provider
  - Browser-use: `bu-llm` or `{provider}/{model}` (e.g., `openai/gpt-4`)
  - Stagehand: `{provider}/{model}` (e.g., `openai/computer-use-preview-2025-03-11`)

## Pricing System

### Three-tier fallback for cost calculation:
1. **Local pricing** (`pricing.py`): Built-in prices for Claude/Gemini models
2. **LiteLLM pricing** (optional `[pricing]` extra): Extended coverage for 100+ models
3. **Default pricing**: Falls back to Claude Sonnet 4.5 pricing

Pricing tracks:
- Input/output tokens
- Cache creation/read tokens
- Reasoning tokens (for thinking models)

## Agent Mode

### Requirements
Agent mode requires browser-use from specific git commit (has HAR recording support):
```bash
uv tool install 'reverse-api-engineer[agent]' --with 'browser-use @ git+https://github.com/browser-use/browser-use.git@49a345fb19e9f12befc5cc1658e0033873892455'
```

### Agent Providers
- **browser-use**: Multi-model support (Browser-Use LLM, OpenAI, Google)
- **stagehand**: Computer Use models only (OpenAI, Anthropic)

API keys via environment variables: `BROWSER_USE_API_KEY`, `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `GOOGLE_API_KEY`

## Code Style Conventions

- **Type hints**: Use throughout (`from typing import Optional, Dict, Any`)
- **Async/await**: Engineers use async for LLM streaming
- **Error handling**: Wrap external calls in try-except with user-friendly messages
- **UI consistency**: Use Rich for all terminal output (no plain print statements)
- **Config migration**: `config.py` includes backward compatibility logic for renamed keys

## Common Tasks

### Adding a new model
1. Add pricing to `pricing.py` MODEL_PRICING dict (if not in LiteLLM)
2. Update model choices in `tui.py` get_model_choices() if needed
3. Update README.md model list

### Adding a new agent provider
1. Add provider logic to `browser.py` run_agent_browser()
2. Add config fields to `config.py` DEFAULT_CONFIG
3. Update settings menu in `cli.py`
4. Document in README.md

### Debugging
- **OpenCode**: Set `OPENCODE_DEBUG=1` for detailed logs
- **Stagehand logs**: Suppressed by `_suppress_stagehand_logs()` in `browser.py`
- **Message logs**: All LLM interactions saved to `~/.reverse-api/runs/{run_id}/messages/`

## File Structure Notes

```
src/reverse_api/
├── cli.py              # Main entry point, mode cycling, slash commands
├── base_engineer.py    # Abstract base for SDK implementations
├── engineer.py         # Claude SDK implementation
├── opencode_engineer.py # OpenCode SDK implementation
├── browser.py          # Playwright HAR capture + agent mode
├── config.py           # Configuration manager
├── session.py          # Run history and metadata
├── messages.py         # Message persistence
├── pricing.py          # Model pricing database
├── tui.py              # Terminal UI (Rich-based)
├── opencode_ui.py      # OpenCode-specific UI extensions
└── utils.py            # Path helpers, run ID generation

~/.reverse-api/
├── config.json         # User configuration
├── history.json        # Run history with costs
└── runs/{run_id}/      # Per-run data
    ├── har/            # Captured traffic
    ├── scripts/        # Generated API clients
    └── messages/       # LLM conversation logs
```

## Dependencies Management

Uses `uv` for dependency management:
- **Core deps**: playwright, claude-agent-sdk, rich, questionary, anthropic
- **Optional [agent]**: stagehand (browser-use must be installed separately from git)
- **Optional [pricing]**: litellm (for extended model pricing)

Always use `uv sync` after pulling changes.
