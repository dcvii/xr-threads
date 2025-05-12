from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, DateTime, BigInteger
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False, unique=True)
    email = Column(String(100), nullable=False, unique=True)
    password_hash = Column(Text, nullable=False)
    display_name = Column(String(100))
    bio = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    posts = relationship('BlogPost', back_populates='author')
    comments = relationship('Comment', back_populates='author')

class BlogPost(Base):
    __tablename__ = 'blog_posts'

    post_id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    title = Column(String(200), nullable=False)
    slug = Column(String(200), nullable=False, unique=True)
    content = Column(Text, nullable=False)
    published = Column(Boolean, default=False)
    published_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    author = relationship('User', back_populates='posts')
    comments = relationship('Comment', back_populates='post')
    metadata = relationship('PostMetadata', uselist=False, back_populates='post')

class Comment(Base):
    __tablename__ = 'comments'

    comment_id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey('blog_posts.post_id'), nullable=False)
    author_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    parent_comment_id = Column(Integer, ForeignKey('comments.comment_id'), nullable=True)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    post = relationship('BlogPost', back_populates='comments')
    author = relationship('User', back_populates='comments')
    parent_comment = relationship('Comment', remote_side=[comment_id])

class Tag(Base):
    __tablename__ = 'tags'

    tag_id = Column(Integer, primary_key=True)
    tag_name = Column(String(50), nullable=False, unique=True)

class PostTag(Base):
    __tablename__ = 'post_tags'

    post_id = Column(Integer, ForeignKey('blog_posts.post_id'), primary_key=True)
    tag_id = Column(Integer, ForeignKey('tags.tag_id'), primary_key=True)

class PostMetadata(Base):
    __tablename__ = 'post_metadata'

    post_id = Column(Integer, ForeignKey('blog_posts.post_id'), primary_key=True)
    view_count = Column(BigInteger, default=0)
    like_count = Column(BigInteger, default=0)
    comment_count = Column(BigInteger, default=0)
    last_viewed_at = Column(DateTime(timezone=True))
    last_liked_at = Column(DateTime(timezone=True))

    post = relationship('BlogPost', back_populates='metadata')

class Engagement(Base):
    __tablename__ = 'engagements'

    engagement_id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey('blog_posts.post_id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=True)
    engagement_type = Column(String(20), nullable=False)
    engagement_time = Column(DateTime(timezone=True), server_default=func.now())
