# User search

## Problem

The admin panel needs a way to look up users by a free-text query instead of an exact username
match. `get_user_by_username` only supports an exact match, which isn't useful for a search box.

## Design

Add `search_users(query)` to `app.py`, alongside the existing `get_user_by_username` /
`create_user` helpers. It runs a single parameterized `LIKE` query against `username` and
`email`, matching either field as a substring of `query`. `%` and `_` in `query` are escaped
before being embedded in the `LIKE` pattern (both are wildcard characters in SQL `LIKE`), so a
literal search term matches literally rather than being interpreted as a wildcard.

Out of scope: pagination, ranking/relevance, and the actual admin-panel UI/route that will call
this helper — those are follow-up work once the underlying query helper exists.

## Testing

Unit tests in `test_app.py` cover an exact-substring match, a query containing `%`/`_` (asserting
they're treated literally, not as wildcards), and an empty-result case.
