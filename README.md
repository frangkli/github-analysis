# GitHub Repository Analysis Tool

A powerful tool for analyzing GitHub repositories using the Model Context Protocol (MCP) and AI-powered insights from Large Language Models (LLMs).

## Features

- 🔍 **Repository Information Analysis**: Fetch detailed information about GitHub repositories.
- 🔄 **Commit History Analysis**: Analyze commit histories to identify patterns and insights.
- 🤖 **AI-Powered Insights**: Utilize Ollama to generate intelligent responses and analyses based on repository data.
- 🎨 **Beautiful Command-Line Interface**: Enjoy a user-friendly CLI for seamless interaction.
- 🔌 **MCP-Based Client-Server Architecture**: Leverage a modular architecture for efficient data fetching and analysis.

## Architecture

The application employs a client-server architecture based on the Model Context Protocol (MCP):

- **Server**: Provides tools for fetching GitHub data through a standardized MCP interface.
  - `get_repo_info`: Fetches repository information.
  - `get_commit_history`: Retrieves commit history for analysis.

- **Client**: Connects to the server and provides analysis features
  - Communicates with the server using MCP's stdio transport
  - Uses Ollama for AI-powered analysis
  - Provides an interactive command-line interface

## Prerequisites

- Python 3.10 or higher
- [Ollama](https://ollama.ai) installed with the `qwen2.5:7b` model
- GitHub personal access token (for higher API rate limits)

## Installation

To get started with the GitHub Repository Analysis Tool, follow these steps:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/frangkli/github-analysis.git
   cd github-analysis
   ```

2. **Set Up Environment and Dependencies**:
   ```bash
   uv sync
   ```

3. **Activate Virtual Environment**:
   ```bash
   source .venv/bin/activate
   ```

4. **Install Ollama**: Ensure you have [Ollama](https://ollama.ai) installed with the `qwen2.5:7b` model for AI-powered insights.

5. **Set Up GitHub Personal Access Token**: For higher API rate limits, create a GitHub personal access token and set it as an environment variable:
   ```bash
   export GITHUB_TOKEN=your_token_here  # On Windows use `set GITHUB_TOKEN=your_token_here`
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
└── main.py           # CLI entry point
tests/
└── test_mcp.py       # Some sample tests to test LLM output
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

## Contributing

Contributions are welcome. If you have suggestions or improvements, please open an issue or submit a pull request.

- **New Server Tools**:
   - Add new functions with the `@mcp.tool()` decorator in `server.py`
   - Implement the tool's functionality using GitHub's API

- **New Analysis Types**:
   - Add new handler methods in the client class
   - Create appropriate system prompts for Ollama
   - Update the menu options


## License

This project is licensed under the MIT License - see the LICENSE file for details.