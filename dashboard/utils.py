from dashboard.models import ADMIN_USERS

def is_admin(username: str):
    return username in ADMIN_USERS

def register_admin(username: str, password: str):
    ADMIN_USERS.add(username)
    return True
