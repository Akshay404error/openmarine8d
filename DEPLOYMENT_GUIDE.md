# Deployment Guide: Publishing matocr8d to PyPI

This guide walks you through setting up PyPI publishing for the matocr8d library.

## Step 1: Create PyPI Account

1. Go to https://pypi.org
2. Click **"Register"** in the top right corner
3. Fill in your details:
   - Username (will be public)
   - Email address
   - Password
4. Verify your email address
5. Complete the registration process

## Step 2: Generate PyPI API Token

### Method 1: Through PyPI Website (Recommended)

1. **Log in** to https://pypi.org
2. Click on your **username** in the top right corner
3. Select **"Account settings"** from the dropdown
4. Scroll down to **"API tokens"** section
5. Click **"Add API token"**
6. Fill in the token details:
   - **Name**: `matocr8d-github-actions` (or descriptive name)
   - **Scope**: Select **"Entire account"** (for publishing) or **"Only specific projects"**
7. Click **"Create token"**
8. **IMPORTANT**: Copy the token immediately - you won't see it again!

### Method 2: Using PyPI CLI (Advanced)

```bash
# Install twine if not already installed
pip install twine

# Upload a package to get prompted for credentials
# This will create a .pypirc file with your token
twine upload dist/*
```

## Step 3: Add API Token to GitHub Secrets

1. **Go to your GitHub repository**: https://github.com/matocr8d/matocr8d
2. Click on **"Settings"** tab
3. In the left sidebar, click **"Secrets and variables"** → **"Actions"**
4. Click **"New repository secret"**
5. Fill in the details:
   - **Name**: `PYPI_API_TOKEN`
   - **Secret**: Paste your PyPI API token here
6. Click **"Add secret"**

## Step 4: Test the Publishing Workflow

### Option A: Create a Test Release

1. Go to your repository on GitHub
2. Click **"Releases"** tab
3. Click **"Create a new release"**
4. Create a **test release**:
   - **Tag**: `v0.1.0-test`
   - **Title**: `Test Release v0.1.0`
   - **Description**: `Test release for PyPI publishing`
   - **Set as a pre-release**: ✅ Check this box
5. Click **"Publish release"**
6. Monitor the **Actions** tab to see the publishing process

### Option B: Manual Local Testing

```bash
# Build the package locally
python -m build

# Check the package
twine check dist/*

# Test upload to TestPyPI (recommended first)
pip install twine
twine upload --repository testpypi dist/*

# If successful, upload to real PyPI
twine upload dist/*
```

## Step 5: Publish the Official Release

Once testing is successful:

1. Go to **Releases** tab on GitHub
2. Click **"Create a new release"**
3. Create the **official release**:
   - **Tag**: `v0.1.0`
   - **Title**: `matocr8d v0.1.0 - Initial Release`
   - **Description**: 
     ```
     ## matocr8d v0.1.0 - Initial Release
     
     🎉 First public release of matocr8d OCR library!
     
     ### Features:
     - Simple OCR functionality with Tesseract integration
     - Support for multiple image formats
     - Text extraction with confidence scores
     - Multi-language support
     - Comprehensive error handling
     
     ### Installation:
     ```bash
     pip install matocr8d
     ```
     
     ### Quick Start:
     ```python
     from matocr8d import MatOCR8D
     
     ocr = MatOCR8D()
     text = ocr.extract_text("image.jpg")
     print(text)
     ```
     ```
4. **Do NOT** check "Set as a pre-release"
5. Click **"Publish release"**

## Step 6: Verify the Publication

1. **Check GitHub Actions**: Go to Actions tab and ensure the workflow completed successfully
2. **Check PyPI**: Go to https://pypi.org/project/matocr8d/ to verify it's published
3. **Test installation**:
   ```bash
   pip install matocr8d
   python -c "from matocr8d import MatOCR8D; print('Installation successful!')"
   ```

## Troubleshooting

### Common Issues

1. **"Invalid token" error**:
   - Double-check the token was copied correctly
   - Ensure the secret name in GitHub is exactly `PYPI_API_TOKEN`

2. **"Project name already exists" error**:
   - The project name `matocr8d` might be taken
   - You'll need to choose a different name

3. **"Upload failed" error**:
   - Check the package metadata in `pyproject.toml`
   - Ensure all required fields are filled

4. **"Permission denied" error**:
   - Ensure the API token has proper permissions
   - Check that you're the owner of the project

### Debug Commands

```bash
# Check package structure
python -m build --sdist --wheel .

# Validate package
twine check dist/*

# Test PyPI connection
twine upload --repository testpypi --skip-existing dist/*
```

## Security Notes

- **Never** commit your API token to git
- **Never** share your API token publicly
- **Regenerate** token if accidentally exposed
- Use **TestPyPI** for initial testing

## Next Steps

After successful publication:

1. **Update documentation** with PyPI badge
2. **Share on social media** and relevant communities
3. **Monitor downloads** and user feedback
4. **Respond to issues** and pull requests promptly

## TestPyPI vs PyPI

- **TestPyPI**: For testing packages (https://test.pypi.org)
- **PyPI**: For production packages (https://pypi.org)

To use TestPyPI, modify the workflow to use the test repository:

```yaml
- name: Publish to TestPyPI
  run: |
    twine upload --repository testpypi dist/*
```

And users would install with:
```bash
pip install --index-url https://test.pypi.org/simple/ matocr8d
```
