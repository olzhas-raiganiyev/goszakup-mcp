# 0004. Secrets handling

- Status: accepted
- Date: 2026-11-04

## Context

The server needs an API token and the repository is public. In an earlier personal project, a committed `.env` file exposed a database password in a public repository, and the password had to be rotated. Deleting a file does not remove it from git history.

## Decision

- The token is read only from the `GOSZAKUP_TOKEN` environment variable; it never appears in code or committed config.
- `.env` is git-ignored; `.env.example` documents the variables with empty values.
- gitleaks runs in pre-commit and as a required CI check; GitHub secret scanning and push protection are enabled.
- The server never logs or returns the token: `server_status` reports only `token_configured: true/false`.
- PyPI releases use trusted publishing (OIDC), so no long-lived publishing token exists.

## Alternatives considered

- **Config file in the user's home directory** — workable, but MCP clients already pass configuration as environment variables, and a second mechanism adds risk without benefit.
- **Rely on code review alone** — a single-maintainer project has no second reviewer to catch a leak.

## Consequences

- Contributors need pre-commit installed; CI catches what a missing hook lets through.
- If a secret is committed anyway: rotate it first, then remove it from history. Rotation is the fix; history cleanup is hygiene.
