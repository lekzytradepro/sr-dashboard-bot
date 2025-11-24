from .database import db

class SignalStorage:
    @staticmethod
    def save_signal(pair, direction, entry_price):
        db.query("""
        INSERT INTO signals (pair, direction, entry_price)
        VALUES (?, ?, ?)
        """, (pair, direction, entry_price))

    @staticmethod
    def get_latest_signal():
        result = db.query("""
        SELECT * FROM signals ORDER BY id DESC LIMIT 1
        """)
        return result.fetchone()

    @staticmethod
    def get_all():
        result = db.query("SELECT * FROM signals ORDER BY id DESC")
        return result.fetchall()
