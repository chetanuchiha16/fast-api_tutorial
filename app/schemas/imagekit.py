from pydantic import BaseModel

class ImageKitConfig(BaseModel):
    private_key: str
    # public_key: str
    # url_endpoint: str
