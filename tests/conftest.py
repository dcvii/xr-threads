import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

from main import app as main_app
from models import Base, User, BlogPost
from database import get_db
from passlib.context import CryptContext

# Create in-memory SQLite database for testing
TEST_SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    TEST_SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Password hashing context for creating test users
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@pytest.fixture(scope="function")
def db():
    """
    Create a fresh database for each test.
    """
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db: Session):
    """
    Create a test client using the test database.
    """
    def override_get_db():
        try:
            yield db
        finally:
            pass

    main_app.dependency_overrides[get_db] = override_get_db
    with TestClient(main_app) as test_client:
        yield test_client
    
    # Reset the dependency override after the test
    main_app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def test_user(db: Session):
    """
    Create a test user in the database.
    """
    user = User(
        username="testuser",
        email="test@example.com",
        password_hash=pwd_context.hash("testpassword"),
        display_name="Test User"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture(scope="function")
def authenticated_client(client: TestClient, test_user: User):
    """
    Create a test client with an authenticated session.
    """
    # Simulate login by directly setting the session cookie
    client.post(
        "/login",
        data={"username": "testuser", "password": "testpassword"}
    )
    return client


@pytest.fixture(scope="function")
def test_posts(db: Session, test_user: User):
    """
    Create some test blog posts in the database.
    """
    posts = []
    for i in range(3):
        post = BlogPost(
            title=f"Test Post {i}",
            slug=f"test-post-{i}",
            content=f"This is test post content {i}",
            author_id=test_user.user_id,
            published=True
        )
        db.add(post)
        posts.append(post)
    
    db.commit()
    
    for post in posts:
        db.refresh(post)
    
    return posts

