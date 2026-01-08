from app.crud.base import CrudBase
from app.db.posts import Post
from app.schemas.schema import PostModel, PostCreateSchema


class PostCrud(CrudBase[Post, PostCreateSchema]):
    pass

post_crud = PostCrud(Post)