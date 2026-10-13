import os
from vkbottle import BaseMiddleware
from vkbottle.bot import Message
import redis.asyncio as aioredis

REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
redis_client = aioredis.from_url(REDIS_URL, decode_responses=True)

class AntiSpamMiddleware(BaseMiddleware[Message]):
    def __init__(self, default_cooldown: float = 0.5):
        self.default_cooldown = default_cooldown

    async def pre(self):
        user_id = self.event.from_id
        cooldown = self.default_cooldown
        
        if cooldown <= 0:
            return

        redis_key = f"limit:{user_id}"

        is_allowed = await redis_client.set(redis_key, "active", ex=cooldown, nx=True)

        if not is_allowed:
            await self.event.answer(
                message=f"⚠️ Пожалуйста, не спамьте! Лимит между сообщениями: {cooldown} сек."
            )
            return False