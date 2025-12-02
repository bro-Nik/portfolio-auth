from typing import Optional, List
from app.models.user import User


class UserRepository:
    def __init__(self, db_pool):
        self.db_pool = db_pool

    async def get_user_by_email(self, email: str) -> Optional[User]:
        async with self.db_pool.acquire() as conn:
            result = await conn.fetchrow(
                """
                SELECT id, email, password_hash, is_active,
                    COALESCE(roles, ARRAY['user']) as roles
                FROM users WHERE email = $1
                """,
                email
            )
            return User(**result) if result else None

    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        async with self.db_pool.acquire() as conn:
            result = await conn.fetchrow(
                """
                SELECT id, email, is_active,
                    COALESCE(roles, ARRAY['user']) as roles
                FROM users WHERE id = $1
                """,
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

    async def get_all_users(self) -> List[User]:
        """Получить всех пользователей"""
        async with self.db_pool.acquire() as conn:
            results = await conn.fetch(
                """
                SELECT id, email, password_hash, is_active,
                    COALESCE(roles, ARRAY['user']) as roles
                FROM users ORDER BY id
                """
            )
            return [User(**result) for result in results]
