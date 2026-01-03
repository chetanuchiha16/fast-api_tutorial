from app.config import settings
from imagekitio import ImageKit

imagekit = ImageKit(**settings.imagekit.model_dump())
