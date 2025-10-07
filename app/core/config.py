import os


class Settings:
    DB_USER: str = os.getenv("DB_USER", '')
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", '')
    DB_HOST: str = os.getenv("DB_HOST", '')
    DB_PORT: str = os.getenv("DB_PORT", '')
    DB_NAME: str = os.getenv("DB_NAME", '')
    JWT_SECRET: str = os.getenv("JWT_SECRET", '')
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30

    @property
    def database_url(self):
        return f'postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'

settings = Settings()
