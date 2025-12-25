# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2025-12-25

### Added
- **OpenCode SDK Support**: Native integration with OpenCode SDK for more flexibility in reverse engineering workflows
- **Agent Mode**: Fully automated browser interaction using AI agents (browser-use) with support for multiple LLM providers
  - Browser-Use LLM (default)
  - OpenAI models (gpt-4, gpt-3.5-turbo, etc.)
  - Google models (gemini-pro, gemini-1.5-pro, etc.)
- **Multi-Provider Agent Support**: Configure agent models via settings with automatic API key detection

### Changed
- Improved UX with better CLI interactions and mode cycling
- Enhanced settings management for model, agent model, SDK, and output directory configuration
- Better error handling and user feedback throughout the application

## [0.1.0] - 2025-12-22

### Added
- Initial release
- Browser automation with Playwright and stealth mode
- HAR recording and capture
- AI-powered API client generation using Claude
- Interactive CLI with manual and engineer modes
- Session history and cost tracking
- Production-ready code generation with type hints and documentation

