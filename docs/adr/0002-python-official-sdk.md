# 0002. Python and the official MCP Python SDK 2.x

- Status: accepted
- Date: 2026-11-04

## Context

The server must speak MCP revision 2026-07-28 (stateless, no initialize handshake) and still serve older clients that use the legacy handshake. Tools must return structured output with a JSON schema. The author's primary language is Python, and the planned eval harness and data tooling are Python too.

## Decision

Python 3.11+ with the official `mcp` SDK 2.x (`MCPServer`), pinned to `mcp>=2.3,<3`. Tool inputs and outputs are Pydantic models, so every tool publishes an `outputSchema`.

## Alternatives considered

- **FastMCP 4** — more built-in features, but an extra layer over the same protocol and not the reference SDK; we prefer to track the spec through the official implementation.
- **TypeScript SDK** — the most common choice for MCP servers, but it would split the project across two languages, since the eval harness stays in Python.

## Consequences

- End-to-end tests run the real client in both protocol modes (`Client(server, mode="auto")` and `mode="legacy"`), so backward compatibility is tested, not assumed.
- SDK 2.x is young: we pin the major version and read release notes before upgrading.
- Found in practice: the SDK sends a function's raw `__doc__` as the tool description. Python 3.13 strips docstring indentation at compile time while 3.11–3.12 keep it, so models saw different descriptions on different Python versions. Fixed in PR #1 with `inspect.cleandoc` and a regression test; worth reporting upstream.
