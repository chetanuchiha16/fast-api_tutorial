from pydantic import BaseModel

class PostCreate(BaseModel):
    title: str
    content: str

post = PostCreate(title="Hello", content="World")
post.title  # <-- Put your cursor here and press Ctrl+Space (or Cmd+Space on Mac)

def some_function():
    data = {"title": "Hello", "content": "World"}
    data.  # <-- Put your cursor her