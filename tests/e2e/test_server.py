"""End-to-end: a real MCP client talks to the server in-process.

Runs twice: on the stateless 2026-07-28 protocol ("auto") and on the legacy
initialize handshake ("legacy"), so older clients keep working.
"""

import json
from pathlib import Path

import pytest
from mcp import Client

SNAPSHOT = Path(__file__).parent.parent / "snapshots" / "tools.json"
MODES = ["auto", "legacy"]

pytestmark = pytest.mark.anyio


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


@pytest.mark.parametrize("mode", MODES)
async def test_lists_expected_tools(server, mode: str) -> None:  # type: ignore[no-untyped-def]
    async with Client(server, mode=mode) as client:
        result = await client.list_tools()
    names = sorted(t.name for t in result.tools)
    assert names == ["check_bin", "server_status"]
    for tool in result.tools:
        assert tool.annotations is not None and tool.annotations.read_only_hint is True
        assert tool.output_schema is not None, f"{tool.name} has no outputSchema"


@pytest.mark.parametrize("mode", MODES)
async def test_check_bin_valid_and_invalid(server, mode: str) -> None:  # type: ignore[no-untyped-def]
    async with Client(server, mode=mode) as client:
        bad = await client.call_tool("check_bin", {"value": "12345"})
        ok = await client.call_tool("check_bin", {"value": "000000000000"})
    assert bad.is_error is False
    assert bad.structured_content["valid"] is False
    assert "12 digits" in bad.structured_content["reason"]
    assert ok.structured_content == {"value": "000000000000", "valid": True, "reason": None}


@pytest.mark.parametrize("mode", MODES)
async def test_server_status_reports_mock(server, mode: str) -> None:  # type: ignore[no-untyped-def]
    async with Client(server, mode=mode) as client:
        res = await client.call_tool("server_status", {})
    assert res.structured_content["data_source"] == "mock"
    assert res.structured_content["token_configured"] is False


async def test_tool_schemas_match_snapshot(server) -> None:  # type: ignore[no-untyped-def]
    """Fails when a tool name, description or schema changes. Regenerate on purpose:
    UPDATE_SNAPSHOTS=1 uv run pytest tests/e2e -k snapshot"""
    import os

    async with Client(server) as client:
        result = await client.list_tools()
    current = [t.model_dump(mode="json", by_alias=True, exclude_none=True) for t in result.tools]
    current.sort(key=lambda t: t["name"])
    if os.environ.get("UPDATE_SNAPSHOTS") == "1" or not SNAPSHOT.exists():
        SNAPSHOT.write_text(json.dumps(current, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    assert current == json.loads(SNAPSHOT.read_text(encoding="utf-8"))
