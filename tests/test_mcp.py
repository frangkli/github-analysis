import asyncio
from unittest.mock import patch

import pytest

from github_analysis.client.client import GitHubAnalysisClient

owner = "frangkli"
repo = "github-analysis"


class TestMessageContextProcessor:
    @pytest.fixture(scope="session", autouse=True)
    def client(self):
        return GitHubAnalysisClient()

    @pytest.fixture(scope="session", autouse=True)
    def no_tool_client(self):
        return GitHubAnalysisClient(disable_tools=True)

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
    @pytest.mark.parametrize(
        "user_prompt",
        [
            "Who is the author of this repo?",
            "Tell me about this repo concisely.",
            "How does this repo use the MCP protocol?",
            "How is this repository structured?",
            "What programming language does this codebase use?",
            "What is the most recent commit about?",
            "Who authored the latest commit and when?",
            "How is the weather today?",
            "What license is this repository using?",
            "Give me the exact description of this repository.",
        ],
    )
    @patch("questionary.text")
    async def test_handle_custom_analysis(
        self,
        mock_questionary,
        client: GitHubAnalysisClient,
        no_tool_client: GitHubAnalysisClient,
        user_prompt: str,
    ):
        print("")
        print("------------------------------------------------")
        print(f"Query: {user_prompt}")
        print("------------------------------------------------")
        # Connect clients to MCP server
        await client.connect_to_server()
        await no_tool_client.connect_to_server()

        # Mock the questionary prompt
        mock_questionary.return_value.ask_async.return_value = asyncio.Future()
        mock_questionary.return_value.ask_async.return_value.set_result(user_prompt)

        # Call the function and get real ollama response
        print("------------------------------------------------")
        print("Client with tools enabled:")
        await client.handle_custom_analysis(owner, repo)
        print("------------------------------------------------")
        print("Client with tools disabled:")
        await no_tool_client.handle_custom_analysis(owner, repo)
        print("------------------------------------------------")
