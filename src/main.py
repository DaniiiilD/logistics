from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.api.views import api_router
from src.api.bot.setup import bot, dp
import asyncio


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Заупуск приложения и Telegram бота...")

    polling_task = asyncio.create_task(dp.start_polling(bot))

    yield

    print("Остановка прилодения и Telegram - бота...")

    polling_task.cancel()
    await bot.session.close()


app = FastAPI(title="Logistics App", lifespan=lifespan)
app.include_router(api_router)
