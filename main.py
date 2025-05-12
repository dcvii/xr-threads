from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Base, BlogPost, User
from database import engine, get_db
from pydantic import BaseModel
from typing import List, Optional

# DB setup
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Threads Blog API")

# Pydantic Schemas
class BlogPostCreate(BaseModel):
    title: str
    slug: str
    content: str
    author_id: int

class BlogPostOut(BaseModel):
    post_id: int
    title: str
    slug: str
    content: str
    published: bool
    published_at: Optional[str]
    created_at: str
    updated_at: str

    class Config:
        orm_mode = True

# Routes
@app.post("/posts/", response_model=BlogPostOut)
def create_post(post: BlogPostCreate, db: Session = Depends(get_db)):
    db_post = BlogPost(**post.dict())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

@app.get("/posts/", response_model=List[BlogPostOut])
def read_posts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    posts = db.query(BlogPost).offset(skip).limit(limit).all()
    return posts

@app.get("/posts/{post_id}", response_model=BlogPostOut)
def read_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(BlogPost).filter(BlogPost.post_id == post_id).first()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@app.put("/posts/{post_id}", response_model=BlogPostOut)
def update_post(post_id: int, post_data: BlogPostCreate, db: Session = Depends(get_db)):
    post = db.query(BlogPost).filter(BlogPost.post_id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    for field, value in post_data.dict().items():
        setattr(post, field, value)
    db.commit()
    db.refresh(post)
    return post

@app.delete("/posts/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(BlogPost).filter(BlogPost.post_id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    db.delete(post)
    db.commit()
    return {"detail": "Post deleted"}
