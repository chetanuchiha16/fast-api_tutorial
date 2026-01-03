from fastapi import FastAPI, HTTPException
from app.schema import Post
app = FastAPI()

posts = {
        1: {"title": "First Post", "content": "This is the first post."},
        2: {"title": "Second Post", "content": "This is the second post."},
        3: {"title": "Third Post", "content": "This is the third post."},
        4: {"title": "Fourth Post", "content": "This is the fourth post."}
}

@app.get("/all-posts")
def get_posts(limit: int = None):
    if limit:
        # return first `limit` posts as a dict
        # print (posts.items())
        return dict(list(posts.items())[:limit])
    
    return posts


@app.get("/post/{post_id}")
def get_post(post_id: int):
    if post_id not in posts:
        raise HTTPException(status_code=404, detail="post not found")
    return posts[post_id]

@app.post("/posts") 
def create_post(post: Post) -> Post:
    return {
        post.title,
        post.content
    }