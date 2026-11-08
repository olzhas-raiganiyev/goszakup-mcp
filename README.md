# goszakup-mcp

MCP server for Kazakhstan public procurement data ([goszakup.gov.kz](https://goszakup.gov.kz)), with an open evaluation of how well LLMs use it.

> **Status: pre-alpha.** Only offline tools work today. Procurement tools arrive with access to the official open-data API.

<!-- Ownership proof for the MCP Registry. Do not remove. -->
mcp-name: io.github.olzhas-raiganiyev/goszakup-mcp

## What works now

| Tool | What it does |
| --- | --- |
| `check_bin` | Validates a 12-digit BIN/IIN: format and check digit. Offline. |
| `server_status` | Shows the version and whether the server uses mock or live data. |

All tools are read-only and return structured output with a JSON schema. The server speaks MCP revision 2026-07-28 and still serves older clients.

## Run locally

```bash
uv sync
uv run goszakup-mcp                       # stdio
uv run goszakup-mcp --transport streamable-http
```

Claude Desktop (`claude_desktop_config.json`), from a local checkout:

```json
{
  "mcpServers": {
    "goszakup": {
      "command": "uv",
      "args": ["--directory", "/path/to/goszakup-mcp", "run", "goszakup-mcp"]
    }
  }
}
```

## Configuration

| Variable | Default | Meaning |
| --- | --- | --- |
| `GOSZAKUP_SOURCE` | `mock` | `mock` for offline sample data, `ows` for the official API |
| `GOSZAKUP_TOKEN` | — | Token for the official API, issued by the Ministry of Finance of Kazakhstan. Required when `GOSZAKUP_SOURCE=ows`. |

Never commit a token. `.env` is git-ignored and CI scans every push with gitleaks.

## Development

```bash
uv sync
uv run pytest --cov      # unit + end-to-end over both protocol modes
uv run ruff check . && uv run ruff format --check . && uv run mypy
uv run pre-commit install
```

Tool schemas are snapshot-tested. After an intended change: `UPDATE_SNAPSHOTS=1 uv run pytest -k snapshot`.

Design decisions live in [`docs/adr/`](docs/adr/).

## License

MIT
