# User search

## Problem

The admin panel needs a way to look up users by a free-text query instead of an exact username
match. `get_user_by_username` only supports an exact match, which isn't useful for a search box.

## Design

Add `search_users(query)` to `app.py`, alongside the existing `get_user_by_username` /
`create_user` helpers, via a shared `_connection()` context manager all three now use for
connection lifecycle (open, commit-on-success where applicable, always close) — this PR also
migrates `get_user_by_username` and `create_user` onto it, since leaving them on the old
manual-`close()` pattern while adding a third copy of it for `search_users` would have meant
three near-identical open/close blocks instead of one shared one. `search_users` runs a single
parameterized `LIKE` query against `username` and `email`, matching either field as a substring
of `query`. `%` and `_` in `query` are escaped before being embedded in the `LIKE` pattern (both
are wildcard characters in SQL `LIKE`), so a literal search term matches literally rather than
being interpreted as a wildcard.

A `python app.py <query>` CLI entry point (`if __name__ == "__main__"`) is the interim caller
that exercises `search_users` end-to-end until the real admin-panel route exists — intentionally
minimal, it only prints matching rows.

Out of scope: pagination, ranking/relevance, and the actual admin-panel UI/route — those are
follow-up work once the underlying query helper exists; the CLI entry point above is not a
substitute for that route, just a way to invoke the helper directly in the meantime.

## Testing

Unit tests in `test_app.py` cover an exact-substring match, a query containing `%`/`_` (asserting
they're treated literally, not as wildcards), and an empty-result case.
