from .database import db

class SubscriptionModel:
    @staticmethod
    def set_subscription(user_id, plan, expiry_date):
        db.query("""
        INSERT OR REPLACE INTO subscriptions (user_id, plan, expiry_date)
        VALUES (?, ?, ?)
        """, (user_id, plan, expiry_date))

    @staticmethod
    def get_subscription(user_id):
        result = db.query("SELECT * FROM subscriptions WHERE user_id = ?", (user_id,))
        return result.fetchone()

    @staticmethod
    def remove_subscription(user_id):
        db.query("DELETE FROM subscriptions WHERE user_id = ?", (user_id,))
