from dashboard.middleware import require_admin
from dashboard.models import USERS, SIGNAL_LOGS, SETTINGS

async def get_users(request):
    return {"users": list(USERS.keys())}


@require_admin
async def toggle_auto_signal(request):
    SETTINGS["auto_signal_enabled"] = not SETTINGS["auto_signal_enabled"]
    return {"status": "success", "auto_signal": SETTINGS["auto_signal_enabled"]}


@require_admin
async def get_signal_logs(request):
    return {"history": SIGNAL_LOGS}
