import sqlite3
import sys

DB_PATH = "users.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def get_user_by_username(username):
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("SELECT id, username, email FROM users WHERE username = ?", (username,))
        return cur.fetchone()
    finally:
        conn.close()


def _escape_like(value):
    """Escape LIKE wildcards (% and _) so a literal search term matches literally."""
    return value.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")


def search_users(query):
    """Search users by a free-text query against username or email."""
    conn = get_connection()
    try:
        cur = conn.cursor()
        like = "%" + _escape_like(query) + "%"
        cur.execute(
            "SELECT id, username, email FROM users WHERE username LIKE ? ESCAPE '\\' OR email LIKE ? ESCAPE '\\'",
            (like, like),
        )
        return cur.fetchall()
    finally:
        conn.close()


def create_user(username, email):
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO users (username, email) VALUES (?, ?)",
            (username, email),
        )
        conn.commit()
    finally:
        conn.close()


if __name__ == "__main__":
    # Minimal CLI entry point for the admin panel's upcoming search box to
    # call into; wires search_users() up so it's not dead code ahead of the
    # real route (out of scope for this change, see docs/design/user-search.md).
    if len(sys.argv) > 1:
        for row in search_users(sys.argv[1]):
            print(row)
