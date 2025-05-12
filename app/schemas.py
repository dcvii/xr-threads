from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# User Schema (Response Model)
class UserOut(BaseModel):
    user_id: int
    username: str
    display_name: Optional[str] = None
    bio: Optional[str] = None

    class Config:
        orm_mode = True

# Comment Schema (Response Model)
class CommentOut(BaseModel):
    comment_id: int
    post_id: int
    author: UserOut
    content: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# Comment Create (Request Model)
class CommentCreate(BaseModel):
    post_id: int
    author_id: int
    content: str
