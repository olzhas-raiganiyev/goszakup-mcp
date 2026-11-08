# 0001. Record architecture decisions

- Status: accepted
- Date: 2026-11-04

## Context

This project is built partly with AI coding agents. A reviewer, and the author in an interview, must be able to explain why each significant choice was made, not only what the code does.

## Decision

Every decision that is costly to reverse gets a short ADR in `docs/adr/`, numbered in order, using `0000-template.md`. The author writes ADRs personally; agents may draft code, not decisions.

## Alternatives considered

- **Decisions in commit messages only** — hard to find, no alternatives recorded.
- **A single DESIGN.md** — grows into a wall of text, loses the history of why.

## Consequences

Small overhead per decision. The ADR list becomes the map of the project for reviewers.
