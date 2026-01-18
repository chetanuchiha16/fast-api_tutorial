from pydantic_settings import BaseSettings, SettingsConfigDict
from app.schemas.imagekit import ImageKitConfig

class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_SERVER: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    IMAGEkit_PRIVATE_KEY:str
    IMAGEkit_PUBLIC_KEY:str
    IMAGEkit_URL:str

    @property
    def DATABASE_URI(self):
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
    
    @property
    def imagekit(self) -> ImageKitConfig:
        return ImageKitConfig(
            private_key = self.IMAGEkit_PRIVATE_KEY,
            # public_key = self.IMAGEkit_PUBLIC_KEY,
            url_endpoint = self.IMAGEkit_URL,
        )
    
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()