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
