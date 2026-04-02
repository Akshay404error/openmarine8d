"""
Setup script for matocr8d library
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="matocr8d",
    version="0.1.0",
    author="matocr8d Contributors",
    author_email="contributors@matocr8d.dev",
    description="A simple OCR library for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Akshay404error/OCR-library-python",
    packages=find_packages(),
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
        "Topic :: Scientific/Engineering :: Image Recognition",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    include_package_data=True,
    keywords="ocr, text extraction, image processing, tesseract",
    project_urls={
        "Bug Reports": "https://github.com/Akshay404error/OCR-library-python/issues",
        "Source": "https://github.com/Akshay404error/OCR-library-python",
        "Documentation": "https://github.com/Akshay404error/OCR-library-python/wiki",
    },
)
