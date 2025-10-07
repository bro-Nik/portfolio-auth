from typing import Optional
from app.models.user import User


class UserRepository:
    def __init__(self, db_pool):
        self.db_pool = db_pool

    async def get_user_by_email(self, email: str) -> Optional[User]:
        async with self.db_pool.acquire() as conn:
            result = await conn.fetchrow(
                "SELECT id, email, password_hash, is_active FROM users WHERE email = $1",
                email
            )
            return User(**result) if result else None

    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        async with self.db_pool.acquire() as conn:
            result = await conn.fetchrow(
                "SELECT id, email, is_active FROM users WHERE id = $1",
                user_id
            )
            return User(**result) if result else None

    async def create_user(self, email: str, password_hash: str) -> User:
        async with self.db_pool.acquire() as conn:
            result = await conn.fetchrow(
                "INSERT INTO users (email, password_hash) VALUES ($1, $2) RETURNING id, email",
                email, password_hash
            )
            return User(**result)
