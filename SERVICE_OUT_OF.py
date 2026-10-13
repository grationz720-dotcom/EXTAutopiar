import asyncio
from vkbottle import Bot
from vkbottle.bot import Message
from dotenv import load_dotenv
import os
from AntiSpamMiddleware import AntiSpamMiddleware

config_status = load_dotenv('extconfig.env')
VK_TOKEN = None

if config_status:
    VK_TOKEN = os.environ.get("token")
    DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite+aiosqlite:///database.db")

    if not VK_TOKEN:
        print("Критическая ошибка: Переменная 'token' не найдена внутри файла extconfig.env")
        exit(1)
else:
    print("Критическая ошибка: Не удалось найти или загрузить файл extconfig.env")
    exit(1)

bot = Bot(token=VK_TOKEN)
bot.labeler.message_view.register_middleware(AntiSpamMiddleware)

@bot.on.private_message()
async def message_ext_handle(message: Message):
    await message.answer(message="⚠️ Бот сейчас на разработке. Пожалуйста, подождите.\n\n📱 Контакт менеджера-разработчика: https://vk.com/lessro.\nС уважением, автоответчик.")

if __name__ == '__main__':
    print("Бот успешно запущен и слушает сообщения...")
    asyncio.run(bot.run_polling())