from setuptools import setup, find_packages
import os

# Read requirements
with open('requirements.txt') as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

# Read long description from README
with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="xr_threads-blog",
    version="0.1.0",
    description="A modern, lightweight blog platform built with FastAPI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="xr_threads Contributors",
    author_email="mdcb@cubegeek.com",
    url="https://github.com/yourusername/xr_threads",
    packages=find_packages(exclude=["tests*"]),
    include_package_data=True,
    install_requires=requirements,
    python_requires=">=3.12",
    entry_points={
        "console_scripts": [
            "xr_threads-server=main:run_app",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Framework :: FastAPI",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.12",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Internet :: WWW/HTTP :: WSGI",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
    ],
    keywords="fastapi, blog, web, api, rest, xr_threads",
    project_urls={
        "Documentation": "https://github.com/yourusername/xr_threads",
        "Source": "https://github.com/yourusername/xr_threads",
        "Tracker": "https://github.com/yourusername/xr_threads/issues",
    },
)
