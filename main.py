from aiogram import Bot, Dispatcher
from aiohttp import ClientSession
from aiohttp_socks import ProxyConnector
from bot import PROXY_URL, TOKEN

async def create_bot():
    # Создаем прокси-коннектор
    connector = ProxyConnector.from_url(PROXY_URL)

    # Создаем сессию с прокси
    session = ClientSession(connector=connector)

    # Создаем бота с сессией через прокси
    bot = Bot(token=TOKEN, session=session)
    dp = Dispatcher()

    return bot, dp

async def main():
    bot, dp = await create_bot()

    @dp.message(commands=['start'])
    async def start_command(message):
        await message.answer("Привет! Это бот с поддержкой прокси.")

    # Запускаем поллинг
    await dp.start_polling(bot)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())

if __name__ == '__main__':
    asyncio.run(main())