from dashboard.utils import is_admin


def require_admin(handler):
    async def wrapper(request):
        username = request.headers.get("X-Admin")

        if not username or not is_admin(username):
            return {"status": "error", "message": "Unauthorized"}

        return await handler(request)

    return wrapper
