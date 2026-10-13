from vkbot.database.user import UserCRUD

from vkbot.keyboards.reply.TOS import TOSKeyboard

from middlewares.AntiSpamMiddleware import AntiSpamMiddleware
from middlewares.NotRegistred import NotRegistred

from vkbottle.bot import BotLabeler, Message
from vkbottle_types.events import GroupEventType

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession

import os
from loguru import logger

logger.add('vkbot/logs/bot.log', mode='INFO')

DATABASE_URL = os.environ.get("database_url")

if not DATABASE_URL:
    raise ValueError("Критическая ошибка: DATABASE_URL не задан!")

engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    pool_size=10,
    max_overflow=20
)

async_session = sessionmaker(
    engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

# --------------------------------------------------------------------
users = UserCRUD()

bot = BotLabeler()
bot.labeler.message_view.register_middleware(AntiSpamMiddleware)

@bot.on.private_message(text='Начать', rules=[NotRegistred()])
async def start_handle(message: Message):
    await message.answer(message="""
⚖️ Здравствуйте! Для продолжения вам нужно принять следующие документы\n(клавиатура снизу, вы можете взаимодействовать):

• ToS (Terms of Service): https://vk.ru/@extpiar-usloviya-ispolzovaniya-servisa-extautopiar
""", keyboard=TOSKeyboard)

@bot.on.private_message(text="✓ Принять", rules=[NotRegistred()])
async def see_tos_handle(message: Message):
    async with async_session() as session:
        meow = await message.ctx_api.users.get(user_ids=[message.from_id])
        
        if meow:
            username = f"{meow[0].first_name} {meow[0].last_name}"
        else:
            username = "Пользователь"

        result_registration = await users.create(session, vk_id=message.from_id, username=username)

        if result_registration:
            await message.answer("✓ Вы успешно зарегистрированы в боте и приняли документы!")