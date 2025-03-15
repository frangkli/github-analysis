"""Server module for GitHub repository analysis."""

import os
from typing import Any

import requests
from mcp.server.fastmcp import FastMCP
from rich.console import Console

from github_analysis.server.exceptions import GitHubAPIError

# Create console for stderr output
console = Console(stderr=True)

# Create FastMCP instance with proper configuration
mcp = FastMCP(
    "GitHub Analysis",
    description="GitHub repository analysis tools",
    version="0.1.0",
)


@mcp.tool()
def get_repo_info(owner: str, repo: str) -> dict[str, Any]:
    """Fetch repository information from GitHub API."""
    with console.status("[bold green]Fetching repository info...", spinner="dots"):
        headers = {"Accept": "application/vnd.github.v3+json"}
        token = os.getenv("GITHUB_TOKEN")
        if token:
            headers["Authorization"] = f"token {token}"

        url = f"https://api.github.com/repos/{owner}/{repo}"
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise GitHubAPIError(
                f"Failed to fetch repo info: {response.json().get('message')}"
            )
        return response.json()


@mcp.tool()
def get_commit_history(owner: str, repo: str, limit: int = 5) -> list[dict[str, Any]]:
    """Fetch commit history from GitHub API."""
    with console.status("[bold green]Fetching commit history...", spinner="dots"):
        headers = {"Accept": "application/vnd.github.v3+json"}
        token = os.getenv("GITHUB_TOKEN")
        if token:
            headers["Authorization"] = f"token {token}"

        url = f"https://api.github.com/repos/{owner}/{repo}/commits"
        response = requests.get(url, headers=headers, params={"per_page": limit})
        if response.status_code != 200:
            raise GitHubAPIError(
                f"Failed to fetch commit history: {response.json().get('message')}"
            )
        return response.json()


def main() -> None:
    """Run the server."""
    try:
        # Print startup message to stderr
        console.print("[bold green]✨ Starting GitHub Analysis Server...[/]")

        # Run the server with stdio transport
        mcp.run(transport="stdio")
    except KeyboardInterrupt:
        console.print("\n[bold yellow]Server stopped by user[/]")


if __name__ == "__main__":
    main()
