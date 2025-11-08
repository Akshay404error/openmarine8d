# 🚀 Quick Start Guide

## Installation (5 minutes)

### 1. Install Python Dependencies

```bash
cd missing_person_finder
pip install -r requirements.txt
```

**Note:** If `dlib` installation fails, try:
```bash
pip install cmake
pip install dlib
```

### 2. Run the Application

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

## First Steps

### Step 1: Add Your First Person (2 minutes)

1. Click **"➕ Add New Person"** in the sidebar
2. Enter a name (e.g., "John Doe")
3. Upload an image or use camera
4. Click **"Add to Database"**

### Step 2: Search for a Match (1 minute)

1. Click **"🔎 Search Face"** in the sidebar
2. Upload a test image or capture from camera
3. Click **"Search Database"**
4. View ranked matches with similarity scores

### Step 3: Explore Features

- **📊 Database Stats** - View all people in database
- **📝 View Logs** - See search history
- **⚙️ System Info** - Learn about the system

## Understanding Results

- **🟢 High Match** (Distance < 0.6): Strong confidence
- **🟡 Medium Match** (Distance 0.6-0.8): Moderate confidence
- **🔴 Low Match** (Distance > 0.8): Weak confidence

## Tips for Best Results

✅ Use clear, frontal face images
✅ Ensure good lighting
✅ One face per image
✅ High resolution preferred

## Troubleshooting

**No face detected?**
- Ensure face is visible and frontal
- Check image quality

**Installation issues?**
- See README.md for detailed instructions
- Check system dependencies

## Need Help?

See the full **README.md** for comprehensive documentation.

---

**You're ready to go! 🎉**
