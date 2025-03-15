"""Main module for GitHub repository analysis."""

import argparse
import json
import os
from typing import Literal

import ollama
import questionary
import requests
from rich.console import Console

from github_analysis.exceptions import GitHubAPIError

console = Console()


def get_github_headers() -> dict[str, str]:
    """Get headers for GitHub API requests."""
    headers = {"Accept": "application/vnd.github.v3+json"}
    token = os.getenv("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"token {token}"
    return headers


def get_github_repo_info(repo_owner: str, repo_name: str) -> dict[str, object]:
    """Fetch repository information from GitHub API."""
    with console.status("[bold green]Fetching repository info...", spinner="dots"):
        url = f"https://api.github.com/repos/{repo_owner}/{repo_name}"
        response = requests.get(url, headers=get_github_headers())
        if response.status_code != 200:
            raise GitHubAPIError(
                f"Failed to fetch repo info: {response.json().get('message')}"
            )
        return response.json()


def get_commit_history(
    repo_owner: str, repo_name: str, limit: int = 5
) -> list[dict[str, object]]:
    """Fetch commit history from GitHub API."""
    with console.status("[bold green]Fetching commit history...", spinner="dots"):
        url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/commits"
        response = requests.get(
            url, headers=get_github_headers(), params={"per_page": limit}
        )
        if response.status_code != 200:
            raise GitHubAPIError(
                f"Failed to fetch commit history: {response.json().get('message')}"
            )
        return response.json()


def analyze_with_ollama(context: str, system_prompt: str) -> str:
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


def handle_commit_analysis(repo_owner: str, repo_name: str) -> None:
    """Handle commit analysis workflow."""
    try:
        commits = get_commit_history(repo_owner, repo_name)
        context = json.dumps(commits, indent=2)
        system_prompt = """Analyze these GitHub commits and provide insights about:
        1. Common themes in commit messages
        2. Code areas frequently modified
        3. Notable changes or patterns
        Please format your response in a clear, structured way."""

        analysis = analyze_with_ollama(context, system_prompt)
        console.print("\n[bold cyan]📊 Commit Analysis Results:[/]\n")
        console.print(analysis)

    except GitHubAPIError as e:
        console.print(f"\n[bold red]❌ Error:[/] {e!s}")


def handle_repo_analysis(repo_owner: str, repo_name: str) -> None:
    """Handle repository analysis workflow."""
    try:
        repo_info = get_github_repo_info(repo_owner, repo_name)
        context = json.dumps(repo_info, indent=2)
        system_prompt = """Analyze this GitHub repository information and provide insights about:
        1. Repository size and activity level
        2. Main programming languages
        3. Notable features (stars, forks, etc.)
        Please format your response in a clear, structured way."""

        analysis = analyze_with_ollama(context, system_prompt)
        console.print("\n[bold cyan]📊 Repository Analysis Results:[/]\n")
        console.print(analysis)

    except GitHubAPIError as e:
        console.print(f"\n[bold red]❌ Error:[/] {e!s}")


def handle_custom_analysis(repo_owner: str, repo_name: str) -> None:
    """Handle custom analysis workflow."""
    try:
        repo_info = get_github_repo_info(repo_owner, repo_name)
        commits = get_commit_history(repo_owner, repo_name)

        prompt = questionary.text("Enter your analysis prompt:").ask()
        if not prompt:
            return

        context = json.dumps({"repo": repo_info, "commits": commits}, indent=2)
        analysis = analyze_with_ollama(context, prompt)
        console.print("\n[bold cyan]📊 Custom Analysis Results:[/]\n")
        console.print(analysis)

    except GitHubAPIError as e:
        console.print(f"\n[bold red]❌ Error:[/] {e!s}")


MenuChoice = Literal["commits", "repo", "custom", "exit"]


def get_menu_choice() -> MenuChoice:
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

    choice = questionary.select(
        "Select an analysis option:",
        choices=list(choices.values()),
        style=style,
    ).ask()

    return next(k for k, v in choices.items() if v == choice) if choice else "exit"  # type: ignore


def main() -> None:
    """Main function."""
    parser = argparse.ArgumentParser(description="GitHub Repository Analysis Tool")
    parser.add_argument("owner", help="Repository owner")
    parser.add_argument("repo", help="Repository name")
    args = parser.parse_args()

    console.print(
        f"\n[bold green]🔍 Analyzing repository:[/] {args.owner}/{args.repo}\n"
    )

    while True:
        choice = get_menu_choice()

        if choice == "commits":
            handle_commit_analysis(args.owner, args.repo)
        elif choice == "repo":
            handle_repo_analysis(args.owner, args.repo)
        elif choice == "custom":
            handle_custom_analysis(args.owner, args.repo)
        else:
            console.print("\n[bold green]👋 Thanks for using the analysis tool![/]")
            break

        console.print("\n" + "─" * 50 + "\n")


if __name__ == "__main__":
    main()
