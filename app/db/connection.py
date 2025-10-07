import asyncpg
from app.core.config import settings


class Database:
    def __init__(self):
        self.pool = None

    async def connect(self):
        self.pool = await asyncpg.create_pool(settings.database_url)

    async def disconnect(self):
        if self.pool:
            await self.pool.close()


db = Database()
