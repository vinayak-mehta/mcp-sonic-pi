"""Command-line interface for Sonic Pi MCP."""

import asyncio
import sys

from .client import main as client_main


def main() -> None:
    """Entry point for the CLI."""
    try:
        asyncio.run(client_main())
    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == "__main__":
    main()
