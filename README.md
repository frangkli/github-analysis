# GitHub Repository Analysis

Analyze GitHub repositories and their commit histories using Ollama with Qwen 2.5.

## Features

- 🎯 Interactive CLI with arrow key navigation
- 🔄 Commit history analysis
- 📊 Repository statistics
- 🔍 Custom analysis queries
- 🎨 Beautiful terminal interface

## Project Structure

```
github-analysis/
├── github_analysis/       # Source code directory
│   ├── __init__.py       # Package initialization
│   ├── main.py           # Main application code
│   └── exceptions.py     # Custom exceptions
├── .python-version       # Python version specification (3.12.0)
├── pyproject.toml        # Project metadata and dependencies
└── uv.lock              # Locked dependencies
```

## Setup

1. Install `uv`:
```bash
pip install uv
```

2. Set up development environment:
```bash
# Create virtual environment with Python 3.12
uv venv

# Activate it
source .venv/bin/activate  # Unix/macOS
# or
.venv\Scripts\activate    # Windows

# Install dependencies
uv sync
```

## Managing Dependencies

Add new packages:
```bash
# Production dependencies
uv add requests
uv add 'ollama>=0.4.7'
uv add 'questionary>=2.0.1'

# Development dependencies
uv add --dev ruff
```

Update dependencies:
```bash
# Update a specific package
uv add --upgrade package_name

# Update all dependencies
uv pip compile pyproject.toml --upgrade
```

## Usage

1. Set your GitHub token (optional, but recommended):
```bash
export GITHUB_TOKEN="your-token-here"
```

2. Run the analysis with repository information:
```bash
github-analysis OWNER REPO

# Example:
github-analysis microsoft TypeScript
```

3. Interactive Menu:
   Use arrow keys (↑/↓) to select from:
   - 🔄 Analyze recent commits
   - 📊 Analyze repository information
   - 🔍 Custom analysis prompt
   - 👋 Exit

Example usage:
```bash
# Analyze the TypeScript repository
github-analysis microsoft TypeScript

# Analyze a specific repository
github-analysis facebook react
```

## Development

Format and lint code:
```bash
ruff format .
ruff check .
```