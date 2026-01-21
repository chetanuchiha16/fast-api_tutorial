from pydantic_settings import BaseSettings, SettingsConfigDict
from app.schemas.imagekit import ImageKitConfig

class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_SERVER: str
    POSTGRES_PORT: int
    POSTGRES_DB: str

    AUTH_SECRET:str
    IMAGEKIT_PRIVATE_KEY:str
    IMAGEKIT_PUBLIC_KEY:str
    IMAGEKIT_URL:str

    @property
    def DATABASE_URI(self):
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
    
    # @property
    # def AUTH_SECRET(self):
    #     return self.AUTH_SECRET
    
    @property
    def imagekit(self) -> ImageKitConfig:
        return ImageKitConfig(
            private_key = self.IMAGEKIT_PRIVATE_KEY,
            # public_key = self.IMAGEKIT_PUBLIC_KEY,
            # url_endpoint = self.IMAGEKIT_URL,
        )
    
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()