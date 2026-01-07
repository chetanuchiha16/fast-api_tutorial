from app.crud.base import CrudBase
from app.db import Post
from app.schemas.schema import PostModel


class PostCrud(CrudBase[Post, PostModel]):
    pass

post_crud = PostCrud(Post)