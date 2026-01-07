from typing import AsyncGenerator
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import AsyncSessionLocal


@asynccontextmanager
async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    """Асинхронный контекстный менеджер для сессии БД."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency для получения асинхронной сессии БД."""
    async with get_async_db() as session:
        yield session
