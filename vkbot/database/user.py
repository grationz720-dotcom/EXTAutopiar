from sqlmodel import select, update
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.sql import func
from vkbot.database.models.user import User
from typing import Any

class UserCRUD:
    @staticmethod
    async def create(session: AsyncSession, vk_id: int, username: str) -> User:
        db_user = User(vk_id=vk_id, username=username)
        session.add(db_user)
        await session.commit()
        await session.refresh(db_user)
        return db_user

    @staticmethod
    async def read(session: AsyncSession, vk_id: int) -> User:
        statement = select(User).where(User.vk_id==vk_id)
        result = await session.execute(statement)
        return result.scalar_one_or_none()

    @staticmethod
    async def update(session: AsyncSession, vk_id: int, **kwargs) -> bool:
        if not kwargs:
            return False

        statement = (
            update(User)
            .where(User.vk_id == vk_id)
            .values(**kwargs)
        )
        
        result = await session.execute(statement)
        await session.commit()

    @staticmethod
    async def delete(session: AsyncSession, vk_id: int) -> bool:
        statement = delete(User).where(User.vk_id == vk_id)
        
        result = await session.execute(statement)
        await session.commit()

    @staticmethod
    async def update_metadata_key(session: AsyncSession, vk_id: int, key: str, value: Any) -> bool:
        statement = (
            update(User)
            .where(User.vk_id == vk_id)
            .values(
                metadata_json=func.json_set(
                    User.metadata_json, 
                    f"$.{key}", 
                    func.json(f"'{value}'") if isinstance(value, (dict, list)) else value
                )
            )
        )
        
        result = await session.execute(statement)
        await session.commit()
        return result.rowcount > 0