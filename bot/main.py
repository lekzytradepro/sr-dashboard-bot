import asyncio
import logging
import os
from aiohttp import web
from aiogram import Bot, Dispatcher

from config.settings import BOT_TOKEN
from bot.handlers import router as handlers_router
from core.scheduler import AutoEngine

logging.basicConfig(level=logging.INFO)

async def health_check(request):
    """Simple health check endpoint for Render"""
    return web.Response(text="✅ Bot is running!")

async def start_web_server():
    """Start minimal web server for port binding"""
    app = web.Application()
    app.router.add_get('/', health_check)
    app.router.add_get('/health', health_check)
    
    port = int(os.environ.get("PORT", 10000))
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    logging.info(f"🌐 Web server running on port {port}")
    return runner

async def main():
    # Start web server for Render port binding
    web_runner = await start_web_server()
    
    bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
    dp = Dispatcher()

    # Register handlers
    dp.include_router(handlers_router)

    # Start auto signal engine (background task)
    auto_engine = AutoEngine(bot)
    asyncio.create_task(auto_engine.start())  # runs forever in background

    logging.info("🚀 Bot is running...")

    try:
        # Start bot
        await dp.start_polling(bot)
    except Exception as e:
        logging.error(f"Bot error: {e}")
    finally:
        # Cleanup web server
        await web_runner.cleanup()

if __name__ == "__main__":
    asyncio.run(main())
