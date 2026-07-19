import asyncio
import logging

from aiogram import Dispatcher

from bot import bot
from handlers import router
from middleware import UserMiddleware

logging.basicConfig(level=logging.INFO)
logging.getLogger("aiogram.event").setLevel(logging.WARNING)

dp = Dispatcher()
dp.business_message.middleware(UserMiddleware())
dp.include_router(router)

async def main() -> None:
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
