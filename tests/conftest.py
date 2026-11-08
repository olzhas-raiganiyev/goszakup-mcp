import pytest

from goszakup_mcp.config import Settings
from goszakup_mcp.server import build_server


@pytest.fixture
def server():  # type: ignore[no-untyped-def]
    return build_server(Settings(source="mock", token=None))
