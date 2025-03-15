"""Client module for GitHub repository analysis."""

import argparse
import asyncio
import json
import os
from contextlib import AsyncExitStack
from typing import Any

import ollama
import questionary
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.types import TextContent
from rich.console import Console

console = Console()


class GitHubAnalysisClient:
    """Client for GitHub repository analysis."""

    def __init__(self) -> None:
        """Initialize the client."""
        self.session: ClientSession | None = None
        self.exit_stack = AsyncExitStack()

    async def connect_to_server(self) -> None:
        """Connect to the MCP server and list available tools."""
        try:
            console.print("[bold green]🔌 Connecting to GitHub Analysis Server...[/]")

            # Get the server script path
            current_dir = os.path.dirname(os.path.abspath(__file__))
            server_script = os.path.join(
                os.path.dirname(current_dir), "server", "server.py"
            )

            if not os.path.exists(server_script):
                raise FileNotFoundError(f"Server script not found at {server_script}")

            # Set up environment variables
            env = os.environ.copy()
            env.update(
                {
                    "PYTHONUNBUFFERED": "1",
                    "PYTHONPATH": os.path.dirname(os.path.dirname(current_dir)),
                }
            )

            # Connect to the server
            server_params = StdioServerParameters(
                command="python", args=[server_script], env=env
            )

            # Set up the transport and session
            transport = await self.exit_stack.enter_async_context(
                stdio_client(server_params)
            )
            self.session = await self.exit_stack.enter_async_context(
                ClientSession(*transport)
            )

            # Initialize the session
            await self.session.initialize()

            # List available tools
            response = await self.session.list_tools()
            console.print("\n[bold cyan]Available tools:[/]")
            for tool in response.tools:
                console.print(f"  • [bold]{tool.name}[/]: {tool.description}")
            console.print()

        except Exception as e:
            console.print(f"\n[bold red]❌ Failed to connect to server:[/] {e!s}")
            await self.exit_stack.aclose()
            raise

    async def get_repo_info(self, owner: str, repo: str) -> dict[str, Any] | None:
        """Get repository information."""
        try:
            if not self.session:
                raise RuntimeError("Not connected to server")

            result = await self.session.call_tool(
                "get_repo_info", arguments={"owner": owner, "repo": repo}
            )
            if isinstance(result.content, list) and result.content:
                first_content = result.content[0]
                if isinstance(first_content, TextContent):
                    return json.loads(first_content.text)
            return None
        except Exception as e:
            console.print(f"\n[bold red]❌ Error:[/] {e!s}")
            return None

    async def get_commits(
        self, owner: str, repo: str, limit: int = 5
    ) -> dict[str, Any] | None:
        """Get commit history."""
        try:
            if not self.session:
                raise RuntimeError("Not connected to server")

            result = await self.session.call_tool(
                "get_commit_history",
                arguments={"owner": owner, "repo": repo, "limit": limit},
            )
            if isinstance(result.content, list) and result.content:
                first_content = result.content[0]
                if isinstance(first_content, TextContent):
                    return json.loads(first_content.text)
            return None
        except Exception as e:
            console.print(f"\n[bold red]❌ Error:[/] {e!s}")
            return None

    def analyze_with_ollama(self, context: str, system_prompt: str) -> str:
        """Use Ollama to analyze GitHub data."""
        with console.status("[bold green]Analyzing with Ollama...", spinner="moon"):
            messages = [
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {"role": "user", "content": context},
            ]

            response = ollama.chat(model="qwen2.5:7b", messages=messages)
            return response["message"]["content"]

    async def handle_commit_analysis(self, owner: str, repo: str) -> None:
        """Handle commit analysis workflow."""
        commits = await self.get_commits(owner, repo)
        if not commits:
            return

        context = json.dumps(commits, indent=2)
        system_prompt = """Analyze these GitHub commits and provide insights about:
        1. Common themes in commit messages
        2. Code areas frequently modified
        3. Notable changes or patterns
        Please format your response in a clear, structured way."""

        analysis = self.analyze_with_ollama(context, system_prompt)
        console.print("\n[bold cyan]📊 Commit Analysis Results:[/]\n")
        console.print(analysis)

    async def handle_repo_analysis(self, owner: str, repo: str) -> None:
        """Handle repository analysis workflow."""
        repo_info = await self.get_repo_info(owner, repo)
        if not repo_info:
            return

        context = json.dumps(repo_info, indent=2)
        system_prompt = """
        Analyze this GitHub repository information and provide insights about:
        1. Repository size and activity level
        2. Main programming languages
        3. Notable features (stars, forks, etc.)
        Please format your response in a clear, structured way.
        """

        analysis = self.analyze_with_ollama(context, system_prompt)
        console.print("\n[bold cyan]📊 Repository Analysis Results:[/]\n")
        console.print(analysis)

    async def handle_custom_analysis(self, owner: str, repo: str) -> None:
        """Handle custom analysis workflow."""
        repo_info = await self.get_repo_info(owner, repo)
        commits = await self.get_commits(owner, repo)
        if not repo_info or not commits:
            return

        prompt = await questionary.text("Enter your analysis prompt:").ask_async()
        if not prompt:
            return

        context = json.dumps({"repo": repo_info, "commits": commits}, indent=2)
        analysis = self.analyze_with_ollama(context, prompt)
        console.print("\n[bold cyan]📊 Custom Analysis Results:[/]\n")
        console.print(analysis)

    async def get_menu_choice(self) -> str:
        """Get user's menu choice."""
        choices = {
            "commits": "🔄 Analyze recent commits",
            "repo": "📊 Analyze repository information",
            "custom": "🔍 Custom analysis prompt",
            "exit": "👋 Exit",
        }

        style = questionary.Style(
            [
                ("qmark", "fg:ansigreen bold"),
                ("question", "bold"),
                ("answer", "fg:ansiblue bold"),
                ("pointer", "fg:ansiyellow bold"),
                ("highlighted", "fg:ansiyellow bold"),
                ("selected", "fg:ansigreen"),
            ]
        )

        choice = await questionary.select(
            "Select an analysis option:",
            choices=list(choices.values()),
            style=style,
        ).ask_async()

        return next(k for k, v in choices.items() if v == choice) if choice else "exit"

    async def start(self, owner: str, repo: str) -> None:
        """Start the client."""
        console.print(f"\n[bold green]🔍 Analyzing repository:[/] {owner}/{repo}\n")

        while True:
            choice = await self.get_menu_choice()

            if choice == "commits":
                await self.handle_commit_analysis(owner, repo)
            elif choice == "repo":
                await self.handle_repo_analysis(owner, repo)
            elif choice == "custom":
                await self.handle_custom_analysis(owner, repo)
            else:
                console.print("\n[bold green]👋 Thanks for using the analysis tool![/]")
                break

            console.print("\n" + "─" * 50 + "\n")


async def main() -> None:
    """Run the client."""
    parser = argparse.ArgumentParser(description="GitHub Repository Analysis Tool")
    parser.add_argument("owner", help="Repository owner")
    parser.add_argument("repo", help="Repository name")
    args = parser.parse_args()

    client = GitHubAnalysisClient()
    try:
        await client.connect_to_server()
        await client.start(args.owner, args.repo)
    finally:
        await client.exit_stack.aclose()


if __name__ == "__main__":
    asyncio.run(main())
