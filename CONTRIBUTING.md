# Contributing to Threads

Thank you for your interest in contributing to Threads! This document provides guidelines and instructions for contributing to this FastAPI blog platform project.

## Introduction

Threads is a community-driven project, and we welcome contributions of all kinds: from bug reports and feature requests to documentation improvements and code contributions. This guide will help you get started with the contribution process.

## Code of Conduct

All contributors are expected to adhere to our Code of Conduct. We are committed to providing a welcoming and inclusive environment for everyone. By participating in this project, you agree to:

- Be respectful and considerate in all communications
- Be open to collaboration and different viewpoints
- Gracefully accept constructive criticism
- Focus on what is best for the community
- Show empathy towards other community members

Unacceptable behavior includes harassment, offensive comments, and any form of discrimination. Maintainers have the right to remove, edit, or reject any contributions that don't align with these standards.

## Getting Started

### Fork and Clone the Repository

1. Fork the repository on GitHub by clicking the "Fork" button at the top right of the repository page.
2. Clone your fork to your local machine:
   ```bash
   git clone https://github.com/YOUR_USERNAME/threads.git
   cd threads
   ```
3. Add the original repository as upstream:
   ```bash
   git remote add upstream https://github.com/ORIGINAL_OWNER/threads.git
   ```

### Set Up the Development Environment

1. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Install development dependencies:
   ```bash
   pip install pytest pytest-cov ruff black
   ```
4. Configure the database (see README.md for instructions)

## Development Workflow

1. Create a new branch for your feature or bugfix:
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/issue-you-are-fixing
   ```

2. Make your changes and commit them with clear, descriptive commit messages:
   ```bash
   git add .
   git commit -m "Add feature: short description of changes"
   ```

3. Keep your branch updated with the upstream main branch:
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

4. Run tests to ensure your changes don't break existing functionality:
   ```bash
   pytest
   ```

5. Run linting to ensure your code follows our style guidelines:
   ```bash
   ruff check .
   ```

## Pull Request Process

1. Push your branch to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

2. Open a pull request through the GitHub interface:
   - Navigate to your fork on GitHub
   - Click "New Pull Request"
   - Select your branch and fill out the PR template

3. Ensure your PR includes:
   - A clear title and description
   - Reference to any related issues
   - Tests for new functionality
   - Documentation updates if applicable

4. A maintainer will review your PR, possibly requesting changes
   - Be responsive to feedback
   - Make requested changes by adding new commits to your branch

5. Once approved, your PR will be merged

## Coding Standards

We follow Python's [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide with a few project-specific guidelines:

1. Use 4 spaces for indentation
2. Use 88 character line limit (compatible with Black formatter)
3. Use type hints for function parameters and return values
4. Document functions and classes with docstrings
5. Use descriptive variable names
6. Write clear comments for complex logic

Example:
```python
def get_post_by_slug(slug: str, db: Session) -> Optional[BlogPost]:
    """
    Retrieve a blog post by its URL slug.
    
    Args:
        slug: The URL slug of the post
        db: Database session
        
    Returns:
        The blog post if found, None otherwise
    """
    return db.query(BlogPost).filter(BlogPost.slug == slug).first()
```

## Testing Guidelines

1. Write tests for all new features and bug fixes
2. Aim for high test coverage (target: >80%)
3. Tests should be in the `tests/` directory with a structure mirroring the main code
4. Name test files with a `test_` prefix
5. Use pytest fixtures for reusable test setup
6. Mock external dependencies when appropriate

Example test:
```python
def test_get_post_by_slug_exists(db_session):
    # Arrange
    post = BlogPost(title="Test Post", slug="test-post", content="Test content")
    db_session.add(post)
    db_session.commit()
    
    # Act
    result = get_post_by_slug("test-post", db_session)
    
    # Assert
    assert result is not None
    assert result.title == "Test Post"
```

## Documentation

Good documentation is crucial for the project's usability:

1. Update the README.md when adding new features
2. Keep API documentation up-to-date
3. Document code with docstrings
4. Add usage examples for new features
5. Document configuration options

## Issue Reporting Guidelines

When reporting issues:

1. Use the GitHub issue tracker
2. Search existing issues before creating a new one
3. Include detailed information:
   - Steps to reproduce
   - Expected vs. actual behavior
   - Environment details (OS, Python version, etc.)
   - Error messages or screenshots
4. Use issue templates when available
5. Tag issues appropriately (bug, enhancement, etc.)

## Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Pytest Documentation](https://docs.pytest.org/)

Thank you for contributing to Threads!

