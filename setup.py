from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="sphinx-pitch",
    version="0.1.0",
    author="sphinx-pitch authors",
    author_email="",
    description="A Sphinx extension for creating presentations with GitPitch-compatible syntax",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tetsuo-koyama/sphinx-pitch",
    packages=find_packages(),
    package_data={
        "sphinx_pitch": ["static/*.css"],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Framework :: Sphinx :: Extension",
        "Topic :: Documentation :: Sphinx",
        "Topic :: Multimedia :: Graphics :: Presentation",
    ],
    python_requires=">=3.7",
    install_requires=[
        "sphinx>=3.0",
        "docutils>=0.16",
        "sphinx-revealjs>=2.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.800",
        ],
    },
    keywords="sphinx extension presentation slides gitpitch markdown",
    project_urls={
        "Bug Reports": "https://github.com/tetsuo-koyama/sphinx-pitch/issues",
        "Source": "https://github.com/tetsuo-koyama/sphinx-pitch",
    },
)
