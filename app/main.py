from fastapi import FastAPI, Form, Depends, HTTPException, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from app.models import Base, BlogPost, User, Comment
from app.database import engine, get_db
from typing import List, Optional
from pydantic import BaseModel
from starlette_sessions.middleware import SessionMiddleware
from app.auth import get_current_user
import secrets
from passlib.context import CryptContext
import uvicorn
import typer
import sys



# DB setup
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Threads Blog API")
app.add_middleware(SessionMiddleware, secret_key=secrets.token_hex(16))
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

templates = Jinja2Templates(directory="templates")

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


# Landing page: list posts
@app.get("/", response_class=HTMLResponse)
def read_root(request: Request, db: Session = Depends(get_db)):
    posts = db.query(BlogPost).filter(BlogPost.published).all()
    return templates.TemplateResponse("index.html", {"request": request, "posts": posts})


# Update post detail view to include comments
@app.get("/posts/{slug}", response_class=HTMLResponse)
def read_post(slug: str, request: Request, db: Session = Depends(get_db)):
    post = db.query(BlogPost).filter(BlogPost.slug == slug).first()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    comments = db.query(Comment).filter(Comment.post_id == post.post_id).all()
    return templates.TemplateResponse("post_detail.html", {"request": request, "post": post, "comments": comments})

# Routes
#
# # Handle new post submission
@app.post("/new-post")
def create_post(request: Request, title: str = Form(...), slug: str = Form(...), content: str = Form(...), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not current_user:
        return RedirectResponse(url="/login", status_code=303)
    new_post = BlogPost(title=title, slug=slug, content=content, author_id=current_user.user_id, published=True)
    db.add(new_post)
    db.commit()
    return RedirectResponse(url="/", status_code=303)

# Show new post form
@app.get("/new-post", response_class=HTMLResponse)
def new_post_form(request: Request):
    return templates.TemplateResponse("new_post.html", {"request": request})

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

@app.post("/posts/{slug}/comments")
def add_comment(slug: str, post_id: int = Form(...), author_id: int = Form(...), content: str = Form(...), db: Session = Depends(get_db)):
    post = db.query(BlogPost).filter(BlogPost.slug == slug).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    new_comment = Comment(post_id=post_id, author_id=author_id, content=content)
    db.add(new_comment)
    db.commit()
    return RedirectResponse(url=f"/posts/{slug}", status_code=303)


# Show login form
@app.get("/login", response_class=HTMLResponse)
def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

# Handle login submission
@app.post("/login")
def login(request: Request, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user or not pwd_context.verify(password, user.password_hash):
        raise HTTPException(status_code=400, detail="Invalid username or password")

    request.session["user_id"] = user.user_id
    return RedirectResponse(url="/", status_code=303)

# Handle logout
@app.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/", status_code=303)

    """
    Run the FastAPI application with uvicorn.
    
    Args:
        host: Host to bind the server to
        port: Port to bind the server to
        reload: Enable auto-reload for development
        workers: Number of worker processes
        log_level: Logging level
    """
    try:
        uvicorn.run(
            "main:app",
            host=host,
            port=port,
            reload=reload,
            workers=workers,
            log_level=log_level
        )
    except Exception as e:
        print(f"Error starting server: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    # Create a Typer CLI app for command line usage
    cli = typer.Typer()
    
    @cli.command()
    def start(
        host: str = typer.Option("0.0.0.0", help="Host to bind the server to"),
        port: int = typer.Option(8000, help="Port to bind the server to"),
        reload: bool = typer.Option(False, help="Enable auto-reload for development"),
        workers: int = typer.Option(1, help="Number of worker processes"),
        log_level: str = typer.Option("info", help="Logging level")
    ):
        """Run the Threads blog application server"""
        run_app(host, port, reload, workers, log_level)
    
    # Run the CLI app if called directly
    cli()
