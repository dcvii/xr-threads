import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from models import User, BlogPost


def test_home_page(client: TestClient, test_posts):
    """
    Test that the home page returns a 200 status code and contains the test posts.
    """
    response = client.get("/")
    assert response.status_code == 200
    content = response.text
    
    # Check if all post titles are in the response
    for post in test_posts:
        assert post.title in content
    
    # Check if we're getting HTML
    assert "<html" in content
    assert "<body" in content


def test_view_post_exists(client: TestClient, test_posts):
    """
    Test viewing a post that exists.
    """
    # Get the first test post from the fixture
    post = test_posts[0]
    
    response = client.get(f"/posts/{post.slug}")
    assert response.status_code == 200
    
    # Check if the post content is in the response
    assert post.title in response.text
    assert post.content in response.text


def test_view_post_not_found(client: TestClient):
    """
    Test viewing a post that doesn't exist returns a 404 error.
    """
    response = client.get("/posts/non-existent-post")
    assert response.status_code == 404
    assert "Not Found" in response.text


def test_login_page(client: TestClient):
    """
    Test that the login page loads correctly.
    """
    response = client.get("/login")
    assert response.status_code == 200
    assert "login" in response.text.lower()
    assert "<form" in response.text


def test_successful_login(client: TestClient, test_user: User):
    """
    Test successful login with valid credentials.
    """
    response = client.post(
        "/login",
        data={"username": "testuser", "password": "testpassword"}
    )
    # Should redirect after successful login
    assert response.status_code == 303
    assert response.headers["location"] == "/"


def test_failed_login(client: TestClient, test_user: User):
    """
    Test failed login with invalid credentials.
    """
    response = client.post(
        "/login",
        data={"username": "testuser", "password": "wrongpassword"}
    )
    # Should return 400 Bad Request for invalid credentials
    assert response.status_code == 400
    assert "Invalid username or password" in response.text


def test_logout(authenticated_client: TestClient):
    """
    Test that logout clears the session.
    """
    # First verify we're logged in by accessing a protected page
    initial_response = authenticated_client.get("/new-post")
    assert initial_response.status_code == 200
    
    # Now logout
    logout_response = authenticated_client.get("/logout")
    assert logout_response.status_code == 303  # Redirect
    
    # Verify we're logged out by trying to access the protected page again
    post_logout_response = authenticated_client.get("/new-post")
    assert "login" in post_logout_response.url.lower()


def test_create_post_authenticated(authenticated_client: TestClient, db: Session):
    """
    Test creating a new post when authenticated.
    """
    response = authenticated_client.post(
        "/new-post",
        data={
            "title": "New Test Post",
            "slug": "new-test-post",
            "content": "This is a new test post content."
        }
    )
    
    # Should redirect after post creation
    assert response.status_code == 303
    
    # Verify the post was created in the database
    post = db.query(BlogPost).filter(BlogPost.slug == "new-test-post").first()
    assert post is not None
    assert post.title == "New Test Post"
    assert post.content == "This is a new test post content."


def test_create_post_unauthenticated(client: TestClient):
    """
    Test that unauthenticated users cannot create posts.
    """
    response = client.post(
        "/new-post",
        data={
            "title": "Unauthorized Post",
            "slug": "unauthorized-post",
            "content": "This post should not be created."
        }
    )
    
    # Should redirect to login
    assert response.status_code == 303
    assert "login" in response.headers["location"].lower()


def test_new_post_form_authenticated(authenticated_client: TestClient):
    """
    Test that authenticated users can access the new post form.
    """
    response = authenticated_client.get("/new-post")
    assert response.status_code == 200
    assert "new post" in response.text.lower()
    assert "<form" in response.text


def test_new_post_form_unauthenticated(client: TestClient):
    """
    Test that unauthenticated users are redirected to login.
    """
    response = client.get("/new-post", follow_redirects=False)
    assert response.status_code == 303  # Redirect
    assert "login" in response.headers["location"].lower()

