import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web
import structlog

from src.core.config import settings
from src.core.database.connection import create_tables
from src.bot.handlers import basic, automation, ai
from src.bot.middleware.auth import AuthMiddleware
from src.bot.middleware.rate_limit import RateLimitMiddleware

# Configure structured logging
structlog.configure(
    processors=[
        structlog.processors.JSONRenderer()
    ],
    wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
    logger_factory=structlog.WriteLoggerFactory(),
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

async def create_bot():
    """Initialize bot and dispatcher"""
    bot = Bot(token=settings.telegram_bot_token)
    
    # Storage selection based on environment
    if settings.environment == "production":
        storage = RedisStorage.from_url(settings.redis_url)
    else:
        storage = MemoryStorage()
    
    dp = Dispatcher(storage=storage)
    
    # Register middleware
    dp.message.middleware(AuthMiddleware())
    dp.message.middleware(RateLimitMiddleware())
    
    # Register handlers
    dp.include_router(basic.router)
    dp.include_router(automation.router)
    dp.include_router(ai.router)
    
    return bot, dp

async def on_startup(bot: Bot):
    """Bot startup handler"""
    logger.info("Bot starting up...")
    
    # Create database tables
    create_tables()
    
    # Set webhook if configured
    if settings.telegram_webhook_url:
        await bot.set_webhook(settings.telegram_webhook_url)
        logger.info("Webhook set", url=settings.telegram_webhook_url)
    
    logger.info("Bot started successfully")

async def on_shutdown(bot: Bot):
    """Bot shutdown handler"""
    logger.info("Bot shutting down...")
    await bot.session.close()

async def main():
    """Main application entry point"""
    bot, dp = await create_bot()
    
    # Register startup/shutdown handlers
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    
    if settings.telegram_webhook_url:
        # Webhook mode
        app = web.Application()
        
        # Setup webhook handling
        webhook_requests_handler = SimpleRequestHandler(
            dispatcher=dp,
            bot=bot,
        )
        webhook_requests_handler.register(app, path="/webhook")
        setup_application(app, dp, bot=bot)
        
        # Start webhook server
        web.run_app(app, host="0.0.0.0", port=8000)
    else:
        # Polling mode (development)
        logger.info("Starting bot in polling mode")
        await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())