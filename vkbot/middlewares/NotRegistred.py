import os
from vkbottle.bot import Message
from vkbot.database.user import UserCRUD
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.environ.get('database_url')

engine = create_async_engine(
    DATABASE_URL, 
    echo=False,
    future=True
)

async_session = sessionmaker(
    bind=engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session

users = UserCRUD()

from vkbottle.bot import ABCRule, Message

class NotRegistred(ABCRule[Message]):
    async def check(self, event: Message) -> bool:
        user_id = event.from_id

        async with async_session() as session:
            db_user = await users.read(session, vk_id=user_id)

            if not db_user:
                return True

            return False