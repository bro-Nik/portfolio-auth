import os


class Settings:
    # DB_USER: str = os.getenv('DB_USER', '')
    # DB_PASSWORD: str = os.getenv('DB_PASSWORD', '')
    # DB_HOST: str = os.getenv('DB_HOST', '')
    # DB_PORT: str = os.getenv('DB_PORT', '')
    # DB_NAME: str = os.getenv('DB_NAME', '')
    DB_ECHO: bool = os.getenv('DB_ECHO', 'false').lower() in ('true', '1')
    DB_POOL_SIZE: int = int(os.getenv('DB_POOL_SIZE', '5'))
    DB_MAX_OVERFLOW: int = int(os.getenv('DB_MAX_OVERFLOW', '10'))

    JWT_SECRET: str = os.getenv('JWT_SECRET', '')
    JWT_ALGORITHM: str = os.getenv('JWT_ALGORITHM', '')
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30

    DATABASE_URL: str = os.getenv('DATABASE_URL', '')

    @property
    def database_url(self):
        return self.DATABASE_URL

        return f'postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'


settings = Settings()
