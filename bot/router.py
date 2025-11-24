# bot/router.py

from aiogram import Router
from bot.handlers.admin import admin_router
from bot.handlers.menu import menu_router
from bot.handlers.signals import signal_router

def create_main_router() -> Router:
    """
    Collect and merge all bot routers.
    """
    main = Router()

    # Attach sub routers
    main.include_router(admin_router)
    main.include_router(menu_router)
    main.include_router(signal_router)

    return main
