from fastapi import APIRouter, UploadFile, Form, File, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.db import get_async_session
from app.schemas.post import PostCreateSchema, PostModel
from app.crud.post import post_crud
from app.db.users import User
from app.users import current_active_users
import uuid
router = APIRouter()


@router.post("/upload", response_model=PostModel)
async def upload_file(
    caption: str = Form(""),
    file: UploadFile = File(...),
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_users),
):

    post = PostCreateSchema(
        user_id=user.id,
        caption=caption,
        url="qewe",
        file_type="image",
        file_name="jkjjkj"
    )
    
    return await post_crud.create(session, post)

@router.get("/feed", response_model=list[PostModel])
async def get_feed(limit:int, session:AsyncSession = Depends(get_async_session), user:User = Depends(current_active_users)):
    # result = await session.execute(select(Post).order_by(Post.created_at))
    # posts = result.scalars().all()
    # # posts = [row for row in result]
    # print(posts)
    # posts_data = []
    # for post in posts:
    #     posts_data.routerend({
    #         "id": post.id,
    #         "caption": post.caption,
    #         "url": post.url,
    #         "file_type": post.file_type,
    #         "file_name": post.file_name,
    #         "created_at": post.created_at
            
    #     })
    return await post_crud.list(session,limit)
    # return {"posts": posts_data}

@router.delete("/delete", status_code=200, response_model=PostModel)
async def delete_feed(id:uuid.UUID, session:AsyncSession = Depends(get_async_session), user: User = Depends(current_active_users)):
    deleted_post = await post_crud.delete(session, id)

    if  not deleted_post:
        raise HTTPException(404, detail=f"post {id} not found")
    
    if user.id != deleted_post.user_id:
        raise HTTPException(403, "You do not have permition to delete this post")
        
    # return {"message": f"post Deleted successfully"}
    return deleted_post