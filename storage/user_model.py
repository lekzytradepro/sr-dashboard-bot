from .database import db

class UserModel:
    @staticmethod
    def create_user(user_id, username, full_name):
        db.query("""
        INSERT OR IGNORE INTO users (user_id, username, full_name)
        VALUES (?, ?, ?)
        """, (user_id, username, full_name))

    @staticmethod
    def get_user(user_id):
        result = db.query("SELECT * FROM users WHERE user_id = ?", (user_id,))
        return result.fetchone()

    @staticmethod
    def update_subscription(user_id, plan, expiry_date):
        db.query("""
        UPDATE users SET subscription_status='active', plan=?, expiry_date=?
        WHERE user_id=?
        """, (plan, expiry_date, user_id))

    @staticmethod
    def deactivate(user_id):
        db.query("""
        UPDATE users SET subscription_status='inactive', plan=NULL, expiry_date=NULL
        WHERE user_id=?
        """, (user_id,))
