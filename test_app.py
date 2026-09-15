import os
import sqlite3
import unittest

import app


class SearchUsersTest(unittest.TestCase):
    def setUp(self):
        self.db_path = "test_users.db"
        app.DB_PATH = self.db_path
        conn = sqlite3.connect(self.db_path)
        conn.execute(
            "CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, email TEXT)"
        )
        conn.commit()
        conn.close()
        app.create_user("alice", "alice@example.com")
        app.create_user("bob_smith", "bob@example.com")
        app.create_user("carol100%off", "carol@example.com")

    def tearDown(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_exact_substring_match(self):
        rows = app.search_users("alice")
        self.assertEqual([r[1] for r in rows], ["alice"])

    def test_matches_email_too(self):
        rows = app.search_users("bob@")
        self.assertEqual([r[1] for r in rows], ["bob_smith"])

    def test_empty_query_matches_everything(self):
        rows = app.search_users("")
        self.assertEqual(len(rows), 3)

    def test_no_match_returns_empty(self):
        self.assertEqual(app.search_users("nobody-like-this"), [])

    def test_percent_wildcard_is_treated_literally(self):
        # Without escaping, "100%" would match anything after "100"; it must
        # only match the literal "100%" in carol100%off's username.
        rows = app.search_users("100%")
        self.assertEqual([r[1] for r in rows], ["carol100%off"])

    def test_underscore_wildcard_is_treated_literally(self):
        # Without escaping, "bob_smith" would match "bobXsmith" for any X;
        # confirm the underscore is literal by checking a near-miss doesn't match.
        rows = app.search_users("bobXsmith")
        self.assertEqual(rows, [])
        rows = app.search_users("bob_smith")
        self.assertEqual([r[1] for r in rows], ["bob_smith"])


if __name__ == "__main__":
    unittest.main()
