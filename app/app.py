from fastapi import FastAPI, HTTPException

app = FastAPI()

posts = {1: {"title": "First Post", "content": "This is the first post."}}

@app.get("/all-posts")
def get_posts():
    return posts

@app.get("/post/{post_id}")
def ged_post(id:int):
    if id not in posts:
        raise HTTPException(status_code=404, detail="post not found")
    return posts.get(id)