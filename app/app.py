from fastapi import FastAPI, HTTPException, Form, File, UploadFile, Depends
from app.schemas.schema import PostModel, PostCreateSchema
from contextlib import asynccontextmanager
from app.db import create_db_and_tables, get_async_session, AsyncSession, Post
from sqlalchemy import select
from app.crud.PostCrud import post_crud

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

@app.post("/upload")
async def upload_file(
    caption: str = Form(""),
    file: UploadFile = File(...),
    session: AsyncSession = Depends(get_async_session),
):

    post = PostCreateSchema(
        caption=caption,
        url="qewe",
        file_type="image",
        file_name="jkjjkj"
    )

    
    return await post_crud.post(session, post)

@app.get("/feed", response_model=list[PostModel])
async def get_feed(limit:int, session:AsyncSession = Depends(get_async_session)):
    # result = await session.execute(select(Post).order_by(Post.created_at))
    # posts = result.scalars().all()
    # # posts = [row for row in result]
    # print(posts)
    # posts_data = []
    # for post in posts:
    #     posts_data.append({
    #         "id": post.id,
    #         "caption": post.caption,
    #         "url": post.url,
    #         "file_type": post.file_type,
    #         "file_name": post.file_name,
    #         "created_at": post.created_at
            
    #     })
    return await post_crud.get(session,limit)
    # return {"posts": posts_data}