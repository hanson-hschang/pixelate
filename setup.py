#!/usr/bin/env python3

from setuptools import setup, find_packages

# Read the README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read version from package
exec(open("pixelate/__init__.py").read())

setup(
    name="pixelate",
    version=__version__,
    author="Heng-Sheng Chang",
    description="A CLI tool that generates pixel art PNG images from markdown files with TOML front-matter",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hanson-hschang/pixelate",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Multimedia :: Graphics",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.7",
    install_requires=[
        "toml>=0.10.2",
        "pillow>=10.0.0",
        "click>=8.0.0",
    ],
    entry_points={
        "console_scripts": [
            "pixelate=pixelate.cli:main",
        ],
    },
)