from pydantic import BaseModel
from uuid import UUID
from typing import Any
class ImageKitConfig(BaseModel):
    private_key: str
    public_key: str
    url_endpoint: str

class PostModel(BaseModel):
    id: UUID
    caption: str
    url :  str
    file_type: str
    file_name : str
    created_at : Any