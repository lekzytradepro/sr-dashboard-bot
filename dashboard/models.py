from datetime import datetime

# Simple in-memory storage (replace later with database)
USERS = {}
ADMIN_USERS = set()
SIGNAL_LOGS = []
SETTINGS = {
    "auto_signal_enabled": True,
    "timezone": "UTC",
}


class User:
    def __init__(self, user_id):
        self.user_id = user_id
        self.created_at = datetime.utcnow()
        self.last_signal_time = None


class Admin:
    def __init__(self, username, password):
        self.username = username
        self.password = password  # (Plain text for now, later hashed)
