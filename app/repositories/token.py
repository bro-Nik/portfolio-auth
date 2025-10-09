from app.models.token import RefreshTokenCreate


class TokenRepository:
    def __init__(self, db_pool):
        self.db_pool = db_pool

    async def create_refresh_token(self, token_data: RefreshTokenCreate) -> None:
        async with self.db_pool.acquire() as conn:
            await conn.execute(
                "INSERT INTO refresh_tokens (user_id, token, expires_at) VALUES ($1, $2, $3)",
                token_data.user_id, token_data.token, token_data.expires_at
            )

    async def get_refresh_token(self, token: str) -> RefreshTokenCreate:
        async with self.db_pool.acquire() as conn:
            result = await conn.fetchrow(
                "SELECT user_id, token, expires_at FROM refresh_tokens WHERE token = $1",
                token
            )
            return RefreshTokenCreate(**result)
    #
    # async def update_refresh_token(self, token_id: int, new_token: str, expires_at) -> None:
    #     async with self.db_pool.acquire() as conn:
    #         await conn.execute(
    #             "UPDATE refresh_tokens SET token = $1, expires_at = $2 WHERE id = $3",
    #             new_token, expires_at, token_id
    #         )
    #
    # async def delete_user_refresh_tokens(self, user_id: int) -> None:
    #     async with self.db_pool.acquire() as conn:
    #         await conn.execute(
    #             "DELETE FROM refresh_tokens WHERE user_id = $1",
    #             user_id
    #         )
    #
    async def delete_refresh_token(self, token: str) -> None:
        async with self.db_pool.acquire() as conn:
            await conn.execute(
                "DELETE FROM refresh_tokens WHERE token = $1",
                token
            )
