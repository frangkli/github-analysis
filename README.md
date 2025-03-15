# GitHub Repository Analysis Tool

A tool for analyzing GitHub repositories using Model Context Protocol (MCP) and LLM-powered insights.

## Features

- 🔍 Repository information analysis
- 🔄 Commit history analysis
- 🤖 AI-powered insights using Ollama
- 🎨 Beautiful command-line interface
- 🔌 MCP-based client-server architecture

## Architecture

The application uses a client-server architecture based on the Model Context Protocol (MCP):

- **Server**: Provides tools for fetching GitHub data through a standardized MCP interface
  - `get_repo_info`: Fetches repository information
  - `get_commit_history`: Fetches commit history

- **Client**: Connects to the server and provides analysis features
  - Communicates with the server using MCP's stdio transport
  - Uses Ollama for AI-powered analysis
  - Provides an interactive command-line interface

## Prerequisites

- Python 3.10 or higher
- [Ollama](https://ollama.ai) installed with the `qwen2.5:7b` model
- GitHub personal access token (for higher API rate limits)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/github-analysis.git
cd github-analysis
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install the package:
```bash
pip install -e .
```

4. Set up your GitHub token (optional but recommended):
```bash
export GITHUB_TOKEN=your_token_here
```

## Usage

The tool can be run in two modes: server and client.

1. First, start the server:
```bash
github-analysis server
```

2. Then, in another terminal, run the client:
```bash
github-analysis client <owner> <repo>
```

You can also run the client in Ollama-only mode, which bypasses the MCP server and tools:
```bash
github-analysis client <owner> <repo> --disable-tools
```

### Analysis Options

The tool provides three types of analysis:

1. **Repository Analysis**: Analyzes repository metadata, languages, and statistics
2. **Commit Analysis**: Analyzes recent commit history and patterns
3. **Custom Analysis**: Allows you to ask custom questions about the repository

When running in Ollama-only mode (`--disable-tools`), the analysis will be based on general knowledge rather than real-time repository data.

## Development

### Project Structure

```
github_analysis/
├── client/
│   └── client.py     # MCP client implementation
├── server/
│   ├── server.py     # MCP server implementation
│   └── exceptions.py # Custom exceptions
└── main.py          # CLI entry point
```

### Architecture Details

- **MCP Server**:
  - Implements the Model Context Protocol
  - Provides tools for GitHub API interaction
  - Uses stdio transport for communication

- **MCP Client**:
  - Connects to the server using stdio transport
  - Manages tool calls and response handling
  - Integrates with Ollama for analysis

### Adding New Features

1. **New Server Tools**:
   - Add new functions with the `@mcp.tool()` decorator in `server.py`
   - Implement the tool's functionality using GitHub's API

2. **New Analysis Types**:
   - Add new handler methods in the client class
   - Create appropriate system prompts for Ollama
   - Update the menu options

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.