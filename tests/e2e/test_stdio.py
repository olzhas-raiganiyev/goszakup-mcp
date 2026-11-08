"""Smoke test of the real entry point over stdio, the way Claude Desktop launches it."""

import sys

import pytest
from mcp import Client, StdioServerParameters

pytestmark = pytest.mark.anyio


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


async def test_cli_serves_over_stdio() -> None:
    params = StdioServerParameters(
        command=sys.executable,
        args=["-m", "goszakup_mcp"],
        env={"GOSZAKUP_SOURCE": "mock"},
    )
    async with Client(params) as client:
        result = await client.call_tool("server_status", {})
    assert result.structured_content["data_source"] == "mock"
