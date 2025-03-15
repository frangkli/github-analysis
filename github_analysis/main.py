"""Main module for GitHub repository analysis."""

import asyncio
import sys

from github_analysis.client.client import main as client_main
from github_analysis.server.server import main as server_main


def main() -> None:
    """Run the application."""
    if len(sys.argv) < 2:
        print("Usage: github-analysis [server|client] [args...]")
        sys.exit(1)

    mode = sys.argv[1]
    sys.argv.pop(1)  # Remove the mode argument

    try:
        if mode == "server":
            server_main()  # Server's main function handles its own event loop
        elif mode == "client":
            asyncio.run(client_main())
        else:
            print("Invalid mode. Use 'server' or 'client'.")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\nApplication stopped by user")
        sys.exit(0)


if __name__ == "__main__":
    main()
