from fastapi import APIRouter, UploadFile, Form, File, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.db import get_async_session
from app.schemas.post import PostCreateSchema, PostModel
from app.crud.post import post_crud
from app.db.users import User
from app.users import current_active_users
import uuid
import os
import tempfile
import shutil
from app.imagekit import imagekit
import datetime

router = APIRouter()

# This is the background task function
def log_post_creation(user_email: str, post_caption: str):
    with open("post_audit.log", "a") as log_file:
        timestamp = datetime.datetime.now().isoformat()
        log_file.write(f"[{timestamp}] User {user_email} created a post: {post_caption}\n")


@router.post("/upload", response_model=PostModel)
async def upload_file(
    background_task: BackgroundTasks,
    caption: str = Form(""),
    file: UploadFile = File(...),
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_users),
):
    temp_file_path = None

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as temp_file:
            temp_file_path = temp_file.name
            shutil.copyfileobj(file.file, temp_file)

        # v5.0.0 Syntax
        upload_result = imagekit.files.upload(
            file=open(temp_file_path, "rb"),
            file_name=file.filename,
            folder="/posts",            # Pass options directly here
            use_unique_file_name=True,   # No need for a separate 'options' class
            tags=["backend-upload"]
        )

        background_task.add_task(log_post_creation, user.email, caption)
        # if upload_result.response_metadata.http_status_code == 200:
                
        post = PostCreateSchema(
            user_id=user.id,
            caption=caption,
            url=upload_result.url,
            file_type="image",
            file_name=upload_result.name
        )
        
        return await post_crud.create(session, post)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            os.unlink(temp_file_path)
        file.file.close()

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
    if user.id != deleted_post.user_id:
        raise HTTPException(403, "You do not have permition to delete this post")
    
    deleted_post = await post_crud.delete(session, id)

    if  not deleted_post:
        raise HTTPException(404, detail=f"post {id} not found")
    
        
    # return {"message": f"post Deleted successfully"}
    return deleted_post