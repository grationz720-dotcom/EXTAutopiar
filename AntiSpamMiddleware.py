import time
from vkbottle import BaseMiddleware
from vkbottle.bot import Message

LAST_TIME = {}
COOLDOWN = 2.0  

class AntiSpamMiddleware(BaseMiddleware[Message]):
    async def pre(self):
        user_id = self.event.from_id
        current_time = time.time()

        if user_id in LAST_TIME:
            time_passed = current_time - LAST_TIME[user_id]
            
            if time_passed < COOLDOWN:
                LAST_TIME[user_id] = current_time 

                self.stop("Spam detected")
                return

        LAST_TIME[user_id] = current_time