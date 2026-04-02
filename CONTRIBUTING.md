# Contributing to matocr8d

Thank you for your interest in contributing to matocr8d! This document provides guidelines and information for contributors.

## Getting Started

### Prerequisites

- Python 3.7 or higher
- Git
- Tesseract OCR installed on your system

### Development Setup

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/Akshay404error/OCR-library-python.git
   cd OCR-library-python
   ```

3. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. Install the package in development mode:
   ```bash
   pip install -e .[dev]
   ```

5. Run the tests to ensure everything is working:
   ```bash
   pytest
   ```

## How to Contribute

### Reporting Issues

1. Check existing issues to avoid duplicates
2. Use the issue templates when available
3. Provide clear and detailed information:
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment details (OS, Python version, etc.)
   - Sample code if applicable

### Submitting Pull Requests

1. Create a new branch for your feature or bugfix:
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/your-bugfix-name
   ```

2. Make your changes following the coding standards below

3. Add tests for new functionality:
   ```bash
   # Run tests
   pytest
   # Check coverage
   pytest --cov=matocr8d
   ```

4. Ensure all tests pass and maintain good coverage

5. Commit your changes with descriptive messages:
   ```bash
   git add .
   git commit -m "feat: add new text extraction feature"
   ```

6. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

7. Create a pull request to the main branch

## Coding Standards

### Code Style

We use the following tools to maintain code quality:

- **Black** for code formatting
- **flake8** for linting
- **mypy** for type checking

Run these tools before submitting:
```bash
black matocr8d tests
flake8 matocr8d tests
mypy matocr8d
```

### Code Structure

- Follow PEP 8 guidelines
- Use type hints where appropriate
- Write docstrings for all public functions and classes
- Keep functions focused and small
- Add comprehensive tests for new features

### Documentation

- Update README.md if adding significant features
- Update docstrings for modified functions
- Add examples for new functionality
- Update CHANGELOG.md for version changes

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=matocr8d

# Run specific test file
pytest tests/test_core.py

# Run with verbose output
pytest -v
```

### Writing Tests

- Write tests for all new functionality
- Use descriptive test names
- Test both success and error cases
- Use mocking for external dependencies
- Aim for high code coverage

## Release Process

Releases are automated through GitHub Actions:

1. Create a new release on GitHub
2. The CI/CD pipeline will automatically:
   - Run all tests
   - Build the package
   - Publish to PyPI
   - Create a git tag

Version numbers follow Semantic Versioning (MAJOR.MINOR.PATCH).

## Development Guidelines

### Feature Development

1. Create an issue to discuss the feature first
2. Break down large features into smaller PRs
3. Consider backward compatibility
4. Add appropriate error handling
5. Include documentation and examples

### Bug Fixes

1. Add a test that reproduces the bug
2. Fix the issue
3. Ensure the test passes
4. Check for similar issues in the codebase

### Performance

- Profile code changes that might affect performance
- Consider memory usage for large images
- Optimize critical paths
- Document any performance considerations

## Community

### Code of Conduct

Please be respectful and inclusive in all interactions. Follow the [Code of Conduct](CODE_OF_CONDUCT.md).

### Getting Help

- Check the documentation first
- Search existing issues
- Ask questions in GitHub Discussions
- Join our community channels (if available)

## Recognition

Contributors are recognized in:
- AUTHORS file
- Release notes
- GitHub contributor statistics

Thank you for contributing to matocr8d!
