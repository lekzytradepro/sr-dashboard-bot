# core/session_manager.py

import time

class SessionManager:
    def __init__(self, timeout_minutes=30):
        self.sessions = {}
        self.timeout = timeout_minutes * 60  # convert to seconds

    def create_session(self, user_id):
        now = time.time()
        self.sessions[user_id] = {
            "created_at": now,
            "last_active": now
        }
        return True

    def update_activity(self, user_id):
        if user_id in self.sessions:
            self.sessions[user_id]["last_active"] = time.time()

    def is_active(self, user_id):
        if user_id not in self.sessions:
            return False
        
        last_active = self.sessions[user_id]["last_active"]
        if time.time() - last_active > self.timeout:
            self.destroy_session(user_id)
            return False

        return True

    def destroy_session(self, user_id):
        if user_id in self.sessions:
            del self.sessions[user_id]
