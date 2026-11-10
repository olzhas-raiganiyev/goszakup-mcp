# 0003. Data sources behind adapters

- Status: accepted (adapter structure); zakup.gov.kz source: proposed
- Date: 2026-11-04

## Context

The official source is the goszakup.gov.kz open-data API (ows.goszakup.gov.kz, V3 GraphQL). Access requires a token issued by the Ministry of Finance on written request, with no known response time. Procurement has moved to zakup.gov.kz; third-party reports say the old interface, which links to the API, stays available until 28.02.2027, and one developer reported HTTP 403 from ows for every token since 29.10.2026. The project must be buildable, testable and evaluable without a token.

## Decision

Tools depend on a `DataSource` interface, never on a specific API. Implementations:

- `OwsSource` — official V3 GraphQL API, requires `GOSZAKUP_TOKEN`.
- `MockSource` — frozen sample data built from real response shapes; used by tests and the eval.

The source is selected with `GOSZAKUP_SOURCE`. Public zakup.gov.kz endpoints are undocumented: a candidate third adapter that needs its own ADR before use. HTML scraping is not allowed.

## Alternatives considered

- **Call the API directly from tools** — couples every tool to one API that may change or close, and nothing can be tested without a token.
- **Scrape portal HTML** — fragile, may breach the portal's terms of use.
- **Wait for the token before building** — blocks the whole project on an external answer.

## Consequences

- Switching or adding a source does not change tool code or tool schemas.
- The eval runs on frozen data, so results are reproducible and comparable across models.
- The mock can drift from the real API: it is built from real payloads, and a nightly contract test against the live schema runs once a token exists.
