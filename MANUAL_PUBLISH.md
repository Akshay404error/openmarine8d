# Manual Publishing Instructions

If the GitHub Actions workflow fails, follow these steps to publish manually:

## Step 1: Build the Package

```bash
cd "c:\github files\OCR-library-python"

# Install build tools
pip install build twine

# Build the package
python -m build
```

## Step 2: Check the Package

```bash
# Validate the package
twine check dist/*
```

## Step 3: Upload to PyPI

```bash
# Upload using your token
twine upload --username __token__ --password YOUR_PYP_API_TOKEN_HERE dist/*
```

## Step 4: Verify Installation

```bash
# Install your package
pip install matocr8d

# Test it
python -c "from matocr8d import MatOCR8D; print('✅ Success!')"
```

## If Package Name Exists

If `matocr8d` is already taken, change the name in:

1. `pyproject.toml` - line 4: `name = "matocr8d"`
2. `setup.py` - line 14: `name="matocr8d"`

Try alternative names like:
- `matocr8d-lib`
- `matocr8d-ocr`
- `python-matocr8d`
- `matocr8d-py`
