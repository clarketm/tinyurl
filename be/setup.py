from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="tinyurl",
    version="0.0.1",
    author="Travis Clarke",
    author_email="travis.m.clarke@gmail.com",
    description="Tiny URL API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=["fastapi", "pybase62", "python-dotenv", "redis", "cassandra-driver", "gunicorn", "uvicorn"],
    extras_require={"dev": ["black", "pyment", "pytest", "pytest-cov", "tox",]},
    entry_points={"console_scripts": ["tinyurl=app.main:app"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Framework :: FastAPI",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
