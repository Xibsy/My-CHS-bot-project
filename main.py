import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types import Message
from bot import TOKEN, ADMIN_CHAT_ID  # Consider using environment variables instead



# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stdout
)

bot = Bot(
        token=TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    exit_ids = []
    with open('chat_ids.txt', 'r') as ids:
        for id in ids.readline().split():
            exit_ids.append(id)

    with open('chat_ids.txt', 'a') as ids:
        new_id = str(message.chat.id)
        if new_id not in exit_ids:
            ids.write(f'{str(new_id)} ')
    user_name = html.bold(message.from_user.full_name)
    await message.answer(
        f"Hello, {user_name}!\n\n"
        f"Welcome to the bot! Use /help to see available commands."
    )


@dp.message(Command('br'))
async def broadcast_text(message: Message) -> None:
    if str(message.chat.id) == ADMIN_CHAT_ID:
        with open('chat_ids.txt', 'r') as ids:
            users_chats = [id for id in ids.readline().split() if id != ' ']
            for id in users_chats:
                if id == ADMIN_CHAT_ID:
                    continue
                await bot.send_message(id, message.text.strip('/br '))
    await message.answer(f'Вы отправили всем сообщение {html.bold(message.text.strip('/br '))}')


@dp.message(Command("help"))
async def command_help_handler(message: Message) -> None:
    """
    Handler for /help command
    """
    help_text = """
Available commands:
/start - Start the bot
/help - Show this help message

Just send me any message and I'll echo it back!
    """
    await message.answer(help_text)


@dp.message()
async def echo(message: Message) -> None:
    if message.chat.id != ADMIN_CHAT_ID:
        await bot.send_message(ADMIN_CHAT_ID, f'{message.from_user.full_name}: {message.text}')


async def main() -> None:
    logger = logging.getLogger(__name__)
    logger.info("Starting bot...")

    try:
        # Start polling
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Error occurred: {e}")
    finally:
        await bot.session.close()
        logger.info("Bot stopped")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nBot stopped by user")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")