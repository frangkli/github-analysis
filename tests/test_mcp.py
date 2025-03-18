import asyncio
from unittest.mock import patch

import pytest

from github_analysis.client.client import GitHubAnalysisClient

owner = "frangkli"
repo = "github-analysis"


class TestMessageContextProcessor:
    @pytest.fixture
    def client(self):
        return GitHubAnalysisClient()

    @pytest.mark.parametrize(
        "prompt,expected",
        [
            ("Show me recent commits", True),
            ("What changed in the last update?", True),
            ("How is the code structured?", False),
            ("What does this function do?", False),
        ],
    )
    def test_needs_commit_info(self, client: GitHubAnalysisClient, prompt, expected):
        assert client._needs_commit_info(prompt) == expected

    @pytest.mark.parametrize(
        "prompt,expected",
        [
            ("Show me the repo structure", True),
            ("How are the files organized?", True),
            ("What was the last commit?", False),
            ("Explain this function", False),
        ],
    )
    def test_needs_repo_info(self, client: GitHubAnalysisClient, prompt, expected):
        assert client._needs_repo_info(prompt) == expected

    @pytest.mark.asyncio
    @patch("questionary.text")
    async def test_handle_custom_analysis_with_no_context(
        self, mock_questionary, client: GitHubAnalysisClient
    ):
        # Mock the questionary prompt
        await client.connect_to_server()
        mock_questionary.return_value.ask_async.return_value = asyncio.Future()
        mock_questionary.return_value.ask_async.return_value.set_result(
            "Tell me something about this repository."
        )

        # Call the function and get real ollama response
        await client.handle_custom_analysis(owner, repo)
