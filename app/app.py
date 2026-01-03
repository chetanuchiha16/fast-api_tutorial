from fastapi import FastAPI, HTTPException, Form, File, UploadFile, Depends
from app.schemas.schema import PostModel
from contextlib import asynccontextmanager
from app.db import create_db_and_tables, get_async_session, AsyncSession, Post
from sqlalchemy import select

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
) -> PostModel:

    post = Post(
        caption=caption,
        url="qewe",
        file_type="image",
        file_name=""
    )

    session.add(post)
    await session.commit()
    await session.refresh(post)
    return post

@app.get("/feed")
async def get_feed(session:AsyncSession = Depends(get_async_session)) -> dict[str,list[PostModel]]:
    result = await session.execute(select(Post).order_by(Post.created_at))
    posts = result.scalars().all()
    # posts = [row for row in result]
    print(posts)
    posts_data = []
    for post in posts:
        posts_data.append({
            "id": post.id,
            "caption": post.caption,
            "url": post.url,
            "file_type": post.file_type,
            "file_name": post.file_name,
            "created_at": post.created_at
            
        })

    return {"posts": posts_data}