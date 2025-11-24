import sqlite3
from pathlib import Path

DB_PATH = Path("database.db")

class Database:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.conn.row_factory = sqlite3.Row
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            full_name TEXT,
            subscription_status TEXT DEFAULT 'inactive',
            plan TEXT DEFAULT NULL,
            expiry_date TEXT DEFAULT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS signals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pair TEXT,
            direction TEXT,
            entry_price REAL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS subscriptions (
            user_id INTEGER,
            plan TEXT,
            expiry_date TEXT,
            PRIMARY KEY (user_id)
        )
        """)

        self.conn.commit()

    def query(self, sql, params=()):
        cursor = self.conn.cursor()
        cursor.execute(sql, params)
        self.conn.commit()
        return cursor

db = Database()
