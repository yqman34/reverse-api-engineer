# Release v0.2.0 - Instructions

## ✅ Completed Steps

1. ✅ Updated version to 0.2.0 in `pyproject.toml`
2. ✅ Updated version to 0.2.0 in `src/reverse_api/__init__.py`
3. ✅ Created `CHANGELOG.md` with release notes
4. ✅ Created git commit with version bump
5. ✅ Created git tag `v0.2.0`

## 📦 Next Steps

### 1. Push to GitHub

```bash
# Push the commit and tag to GitHub
git push origin feat/browser-agent
git push origin v0.2.0

# Or if you want to merge to main first:
# git checkout main
# git merge feat/browser-agent
# git push origin main
# git push origin v0.2.0
```

### 2. Create GitHub Release

1. Go to: https://github.com/kalil0321/reverse-api-engineer/releases/new
2. Select tag: `v0.2.0`
3. Release title: `v0.2.0 - OpenCode Support, Agent Mode & UX Improvements`
4. Description (copy from CHANGELOG.md):

```markdown
## [0.2.0] - 2024-12-XX

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

### Fixed
- Various bug fixes and improvements based on user feedback
```

5. Click "Publish release"

### 3. Build and Publish to PyPI

```bash
# Make sure you're in the project root
cd /Users/kalilbouzigues/Projects/browgents/reverse-api

# Clean previous builds
rm -rf dist/ build/ *.egg-info

# Build the package
uv build

# Verify the build
ls -lh dist/

# Upload to PyPI (requires PyPI credentials)
# Option 1: Using twine (recommended)
pip install twine
twine upload dist/*

# Option 2: Using uv
uv publish

# You'll be prompted for PyPI credentials
# Username: __token__
# Password: your-pypi-api-token
```

### 4. Verify Release

After publishing:

1. **PyPI**: Check https://pypi.org/project/reverse-api-engineer/
2. **GitHub**: Check https://github.com/kalil0321/reverse-api-engineer/releases
3. **Test installation**:
   ```bash
   pip install --upgrade reverse-api-engineer
   reverse-api-engineer --version  # Should show 0.2.0
   ```

## 📝 Notes

- Make sure you have PyPI API token ready (create at https://pypi.org/manage/account/token/)
- The tag `v0.2.0` has been created locally and needs to be pushed
- Consider merging `feat/browser-agent` branch to `main` before creating the release

