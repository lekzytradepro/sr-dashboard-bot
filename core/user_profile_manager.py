# core/user_profile_manager.py

class UserProfileManager:
    def __init__(self):
        # User profiles stored in memory (later we will integrate database)
        self.users = {}

    def create_user(self, user_id, username=None):
        if user_id not in self.users:
            self.users[user_id] = {
                "username": username,
                "subscription": None,
                "plan_expiry": None,
                "preferences": {
                    "signal_asset": None,
                    "timezone": "UTC",
                    "notify_entry": True,
                    "notify_pre_entry": True
                }
            }
        return self.users[user_id]

    def set_subscription(self, user_id, plan_name, expiry_date):
        if user_id in self.users:
            self.users[user_id]["subscription"] = plan_name
            self.users[user_id]["plan_expiry"] = expiry_date

    def update_preference(self, user_id, key, value):
        if user_id in self.users:
            self.users[user_id]["preferences"][key] = value

    def get_user(self, user_id):
        return self.users.get(user_id, None)

    def is_subscribed(self, user_id):
        user = self.users.get(user_id)
        if not user:
            return False

        return user["subscription"] is not None
