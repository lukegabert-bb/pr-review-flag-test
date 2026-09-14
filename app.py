import sqlite3

DB_PATH = "users.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def get_user_by_username(username):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, username, email FROM users WHERE username = ?", (username,))
    row = cur.fetchone()
    conn.close()
    return row


def create_user(username, email):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO users (username, email) VALUES (?, ?)",
        (username, email),
    )
    conn.commit()
    conn.close()
