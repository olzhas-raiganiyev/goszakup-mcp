"""Command-line entry point: `goszakup-mcp` (stdio) or `goszakup-mcp --transport streamable-http`."""

from __future__ import annotations

import argparse

from goszakup_mcp import __version__
from goszakup_mcp.server import build_server


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="goszakup-mcp", description=__doc__)
    parser.add_argument("--transport", choices=["stdio", "streamable-http"], default="stdio")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    args = parser.parse_args(argv)
    server = build_server()
    if args.transport == "stdio":
        server.run("stdio")
    else:  # pragma: no cover - exercised manually / by MCP Inspector
        server.run("streamable-http")


if __name__ == "__main__":  # pragma: no cover
    main()
