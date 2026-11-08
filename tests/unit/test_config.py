import pytest

from goszakup_mcp.config import load_settings


def test_defaults_to_mock_without_token() -> None:
    s = load_settings({})
    assert s.source == "mock"
    assert not s.has_token


def test_ows_requires_token() -> None:
    with pytest.raises(ValueError, match="requires GOSZAKUP_TOKEN"):
        load_settings({"GOSZAKUP_SOURCE": "ows"})


def test_ows_with_token() -> None:
    s = load_settings({"GOSZAKUP_SOURCE": "OWS", "GOSZAKUP_TOKEN": "x"})
    assert s.source == "ows"
    assert s.has_token


def test_unknown_source_rejected() -> None:
    with pytest.raises(ValueError, match="must be 'mock' or 'ows'"):
        load_settings({"GOSZAKUP_SOURCE": "scrape"})
