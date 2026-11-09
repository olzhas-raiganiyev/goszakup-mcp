"""MCP server definition. Tools are read-only; every output has a schema."""

from __future__ import annotations

import inspect
from typing import Annotated

from mcp.server.mcpserver import MCPServer
from mcp_types import ToolAnnotations
from pydantic import BaseModel, Field

from goszakup_mcp import __version__, bin_iin
from goszakup_mcp.config import Settings, load_settings

SERVER_NAME = "goszakup-mcp"

INSTRUCTIONS = (
    "Read-only access to Kazakhstan public procurement data from the official "
    "goszakup.gov.kz open-data API. Identifiers of companies are 12-digit BINs; "
    "of individuals and sole proprietors, 12-digit IINs. Validate an identifier "
    "with check_bin before searching by it."
)


def describe(text: str) -> str:
    """Normalize a tool description so models see the same text on every Python version.

    The SDK sends a function's raw __doc__; Python 3.13+ strips docstring indentation
    at compile time while 3.11-3.12 keep it, so descriptions would differ by version.
    """
    return inspect.cleandoc(text)


READ_ONLY_LOCAL = ToolAnnotations(
    read_only_hint=True,
    destructive_hint=False,
    idempotent_hint=True,
    open_world_hint=False,
)


class BinCheck(BaseModel):
    """Result of validating a BIN or IIN."""

    value: str = Field(description="The identifier as received, trimmed.")
    valid: bool = Field(description="True when the format and check digit are correct.")
    reason: str | None = Field(default=None, description="Why the identifier is invalid; null when valid.")


class ServerStatus(BaseModel):
    """What this server instance is connected to."""

    name: str
    version: str
    data_source: str = Field(description="'mock' (offline sample data) or 'ows' (official live API).")
    token_configured: bool


def build_server(settings: Settings | None = None) -> MCPServer:
    """Create the server. Tests pass explicit settings; the CLI reads the environment."""
    settings = settings or load_settings()
    server = MCPServer(SERVER_NAME, version=__version__, instructions=INSTRUCTIONS)

    @server.tool(
        title="Validate BIN/IIN",
        annotations=READ_ONLY_LOCAL,
        description=describe(
            """
            Check that a Kazakhstan BIN or IIN has 12 digits and a correct check digit.

            Works offline. Use it before looking up a company or person by identifier.
            """
        ),
    )
    def check_bin(
        value: Annotated[str, Field(description="12-digit BIN or IIN, e.g. '123456789012'.")],
    ) -> BinCheck:
        result = bin_iin.check(value)
        return BinCheck(value=value.strip(), valid=result.valid, reason=result.reason)

    @server.tool(
        title="Server status",
        annotations=READ_ONLY_LOCAL,
        description=describe("Report the server version and whether it serves mock or live procurement data."),
    )
    def server_status() -> ServerStatus:
        return ServerStatus(
            name=SERVER_NAME,
            version=__version__,
            data_source=settings.source,
            token_configured=settings.has_token,
        )

    return server
