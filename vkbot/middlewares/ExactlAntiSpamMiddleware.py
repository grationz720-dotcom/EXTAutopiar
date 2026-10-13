import os
from vkbottle.bot import ABCRule, Message
import redis.asyncio as aioredis

REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
redis_client = aioredis.from_url(REDIS_URL, decode_responses=True)

class CooldownRule(ABCRule[Message]):
    def __init__(self, cooldown: float):
        self.cooldown = cooldown

    async def check(self, event: Message) -> bool:
        redis_key = f"limit:{event.from_id}:{event.text}"
        
        # Пытаемся занять тайм-аут в Redis
        is_allowed = await redis_client.set(redis_key, "active", ex=self.cooldown, nx=True)
        
        if not is_allowed:
            await event.answer(f"⚠️ Эту команду можно вызывать раз в {self.cooldown} сек.!")
            return False # Хендлер даже не запустится
            
        return True