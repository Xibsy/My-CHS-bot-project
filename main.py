import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from bot import TOKEN, ADMIN_CHAT_ID, AI_TOKEN
from generate_on_api import Bot_AI# Consider using environment variables instead


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stdout
)

ai = Bot_AI(AI_TOKEN)

bot = Bot(
    token=TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    exit_ids = []
    with open('chat_ids.txt', 'r', encoding="utf-8") as ids:
        for id in ids.readline().split(';'):
            try:
                exit_ids.append(id.split(',')[1])
            except IndexError:
                continue

    with open('chat_ids.txt', 'a', encoding="utf-8") as ids:
        new_id = str(message.chat.id)
        if new_id not in exit_ids:
            ids.write(f'{message.from_user.full_name},{str(new_id)};')
    user_name = html.bold(message.from_user.full_name)
    await message.answer(
        f"Привет, {user_name}!\n\n"
        f"Отправь команду {html.bold('/chs')}, чтобы оповестить всех о ЧС"
    )


@dp.message(Command('br'))
async def broadcast_text(message: Message) -> None:
    if str(message.chat.id) == ADMIN_CHAT_ID:
        with open('chat_ids.txt', 'r', encoding="utf-8") as ids:
            users_chats = [id.split(',')[1] for id in ids.readline().split(';') if id != '']
            for id in users_chats:
                if id == ADMIN_CHAT_ID:
                    continue
                await bot.send_message(id, message.text.strip('/br '))
        await message.answer(f'Вы отправили всем сообщение {html.bold(message.text.strip('/br '))}')


@dp.message(Command("help"))
async def command_help_handler(message: Message) -> None:
    help_text = f"""
Доступные команды:
/start - Перезапустить бота
/help - Получить подсказку
/chs ({html.italic('Черезвычайная ситуация')}) - Отправить всем действия при указанной ЧС

    """
    await message.answer(help_text)


@dp.message(Command('chs'))
async def chs_command(message: Message) -> None:
    ai_answer = ai.answer(message.text.strip('/chs '))
    with open('chat_ids.txt', 'r', encoding="utf-8") as ids:
        users_chats = [id.split(',')[1] for id in ids.readline().split(';') if id != '']
        for id in users_chats:
            await bot.send_message(id, (
                    f'{html.bold('Черезвычайная ситуация')}\n\n'
                    f'{html.bold(message.text.strip('/chs '))}\n\n'
                    f'{ai_answer}'
                ))


@dp.message()
async def echo(message: Message) -> None:
    if message.chat.id != ADMIN_CHAT_ID:
        await bot.send_message(message.chat.id, f'Напишите команту {html.bold('/chs')} '
                                                f'чтобы отправить черезвычайную ситуацию')
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
