import asyncio
import logging
import os
import sys
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

# Load local environment variables
load_dotenv()

# Dictionary to store user data (e.g., video info before selection)
# In production, use Redis or a database.
user_data = {}

async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    TOKEN = os.getenv("BOT_TOKEN")
    if not TOKEN:
        print("Error: BOT_TOKEN not found in .env file")
        return

    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()

    # Import handlers here to avoid circular imports
    from handlers import router
    dp.include_router(router)

    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
