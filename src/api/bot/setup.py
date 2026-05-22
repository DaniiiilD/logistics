from aiogram import Bot, Dispatcher
from src.core.config import settings
from src.api.middlewares.bot_db_session import DBSessionMiddleware
from src.api.handlers.user import create_user_service_manual
from src.api.handlers.company.order import create_order_service_manual
from src.api.handlers.driver.offer import create_offer_service_manual
from src.api.bot.handlers.start import router as start_router
from src.api.bot.handlers.menu_processing import router as menu_router
from src.api.bot.handlers.auth import router as auth_router
from src.api.bot.handlers.orders import router as orders_router

TELEGRAM_TOKEN = settings.TELEGRAM_TOKEN
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

dp.update.middleware(DBSessionMiddleware())

user_service = create_user_service_manual()
dp["user_service"] = user_service

order_service = create_order_service_manual()
dp["order_service"] = order_service

offer_service = create_offer_service_manual()
dp["offer_service"] = offer_service

dp.include_router(start_router)
dp.include_router(menu_router)
dp.include_router(auth_router)
dp.include_router(orders_router)
