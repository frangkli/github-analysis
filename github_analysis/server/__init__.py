"""Server package for GitHub repository analysis."""

from github_analysis.server.server import get_commit_history, get_repo_info, main

__all__ = ["get_commit_history", "get_repo_info", "main"]
