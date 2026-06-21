import sqlite3

def save_user(username, password):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users VALUES (?, ?)",
        (username, password)
    )
    conn.commit()