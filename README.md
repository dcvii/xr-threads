# Threads - A FastAPI Blog Platform

A modern, lightweight blog platform built with FastAPI, SQLAlchemy, and Jinja2 templates. Threads provides a simple yet powerful system for creating and managing blog posts with nested comments, user authentication, and rich engagement analytics.

## Features

- 📝 **Blog Post Management**: Create, read, update, and delete blog posts
- 💬 **Nested Comments**: Support for threaded comment discussions
- 👤 **User Authentication**: Secure login and user management
- 🔍 **SEO-friendly URLs**: Uses slugs for better search engine optimization
- 📊 **Engagement Tracking**: Tracks views, likes, and comment statistics
- 🏷️ **Tagging System**: Organize content with a flexible tagging system
- 🎨 **Template-based Views**: Server-side rendering with Jinja2 templates
- 📱 **API-first Design**: RESTful API for all operations

## Technology Stack

- **Backend**: FastAPI (Python 3.12+)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: Session-based auth with password hashing (Passlib)
- **Templates**: Jinja2 templating engine
- **Form Handling**: FastAPI form handling with python-multipart
- **API Documentation**: Auto-generated with FastAPI Swagger UI

## Installation and Setup

### Prerequisites

- Python 3.12 or higher
- PostgreSQL
- Git

### Step 1: Clone the repository

```bash
git clone https://github.com/yourusername/threads.git
cd threads
```

### Step 2: Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### Step 3: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure the database

Update the database connection string in `database.py`:

```python
DATABASE_URL = "postgresql+psycopg2://username:password@localhost/threads_db"
```

Create the database:

```bash
# Connect to PostgreSQL
psql -U postgres

# In PostgreSQL console
CREATE DATABASE threads_db;
CREATE USER username WITH ENCRYPTED PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE threads_db TO username;
```

Set up database schema:

```bash
# Execute the DDL script
psql -U username -d threads_db -f db/ddl/threads_pg_ddl.sql
```

### Step 5: Run the application

```bash
uvicorn main:app --reload
```

The application will be available at `http://localhost:8000`

## Usage Examples

### Creating a new blog post

1. Visit `http://localhost:8000/new-post` in your browser
2. Fill in the title, slug, and content
3. Click "Submit" to publish your post

### Viewing a blog post

Visit `http://localhost:8000/posts/{slug}` where `{slug}` is the URL-friendly identifier for the post.

### Adding a comment

1. Navigate to a blog post
2. Scroll to the comment section
3. Enter your comment and click "Post Comment"

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Home page with list of posts |
| GET | `/posts/{slug}` | View a specific post by its slug |
| GET | `/new-post` | Form to create a new post |
| POST | `/new-post` | Submit a new post |
| POST | `/posts/` | Create a new post (API) |
| GET | `/posts/` | List all posts (API) |
| PUT | `/posts/{post_id}` | Update a post (API) |
| DELETE | `/posts/{post_id}` | Delete a post (API) |
| POST | `/posts/{slug}/comments` | Add a comment to a post |
| GET | `/login` | Login form |
| POST | `/login` | Process login |
| GET | `/logout` | Log out user |

## Development Guidelines

### Project Structure

```
threads/
├── main.py          # Application entry point and route definitions
├── database.py      # Database connection and session management
├── models.py        # SQLAlchemy models
├── schemas.py       # Pydantic schemas for data validation
├── requirements.txt # Project dependencies
├── db/              # Database scripts and migrations
│   └── ddl/         # Data Definition Language scripts
└── templates/       # Jinja2 HTML templates
    ├── index.htm    # Home page template
    ├── login.htm    # Login form
    ├── new_post.htm # New post form
    └── post_detail.htm # Single post view
```

### Coding Standards

- Follow PEP 8 style guidelines for Python code
- Use type hints for function parameters and return values
- Document functions and classes with docstrings
- Write unit tests for new features

### Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature-name`
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- FastAPI for the excellent web framework
- SQLAlchemy for the powerful ORM
- The open-source community for continuous inspiration

