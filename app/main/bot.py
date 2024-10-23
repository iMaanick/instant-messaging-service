import asyncio
import os

from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message, BotCommand
from dotenv import load_dotenv


async def command_start_handler(message: Message) -> None:
    bot_message = "Hi! I will notify you of new messages if you are offline."
    await message.answer(bot_message)


async def set_commands(bot: Bot) -> None:
    commands = [
        BotCommand(command="/start", description="Start the bot"),
    ]
    await bot.set_my_commands(commands)


async def main() -> None:
    load_dotenv()
    dp = Dispatcher()
    bot = Bot(token=os.environ.get("TOKEN"), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp.message.register(command_start_handler, Command("start", prefix="/"))
    await set_commands(bot)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
