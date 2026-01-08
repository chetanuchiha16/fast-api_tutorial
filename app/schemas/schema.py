from pydantic import BaseModel, ConfigDict
from uuid import UUID
from typing import Any
class ImageKitConfig(BaseModel):
    private_key: str
    public_key: str
    url_endpoint: str

class BaseSchema(BaseModel):
    caption: str
    url :  str
    file_type: str
    file_name : str

class PostCreateSchema(BaseSchema):
    pass
class PostModel(BaseSchema):
    id: UUID
    created_at : Any

    model_config = ConfigDict(from_attributes=True)