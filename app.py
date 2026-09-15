import sqlite3

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


def search_users(query):
    """Search users by a free-text query against username or email."""
    conn = get_connection()
    try:
        cur = conn.cursor()
        like = "%" + query + "%"
        cur.execute(
            "SELECT id, username, email FROM users WHERE username LIKE ? OR email LIKE ?",
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
