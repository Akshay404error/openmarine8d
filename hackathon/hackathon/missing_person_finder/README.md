# 🔍 AI Facial Recognition System for Missing Persons & Unidentified Bodies

A complete, **privacy-safe, local-only** facial recognition system built with Streamlit for identifying missing persons and matching unidentified bodies.

## 🎯 Features

### Core Functionality
- ✅ **100% Offline Operation** - No cloud APIs, complete privacy
- 🔍 **Face Detection & Recognition** - Powered by dlib and face_recognition
- 🚀 **Fast Similarity Search** - FAISS vector database for instant matching
- 📷 **Multiple Input Methods** - Upload images or capture from webcam
- 📊 **Confidence Scoring** - Detailed similarity scores for each match
- 👥 **Dynamic Database** - Add new people through the UI
- 📝 **Activity Logging** - Track all searches with timestamps
- 🖼️ **Visual Results** - Side-by-side comparison of matches

### User Interface
- 🎨 Modern, intuitive Streamlit interface
- 📱 Responsive design
- 🔄 Real-time face detection
- 📈 Database statistics and analytics
- 📥 Export logs to CSV

## 🛠️ Technology Stack

| Component | Technology |
|-----------|-----------|
| **Frontend/UI** | Streamlit |
| **Face Detection** | face_recognition (dlib) |
| **Face Encoding** | 128D embeddings via dlib |
| **Vector Search** | FAISS (Facebook AI Similarity Search) |
| **Image Processing** | OpenCV, Pillow |
| **Data Handling** | NumPy, Pandas |
| **Logging** | CSV files |

## 📁 Project Structure

```
missing_person_finder/
├── app.py                      # Main Streamlit application
├── embedding_utils.py          # Face encoding and FAISS utilities
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── data/
│   ├── known_faces/           # Stored face images
│   │   └── [person_name_timestamp.jpg]
│   └── index/                 # FAISS index and metadata
│       ├── faiss_index.bin    # FAISS vector index
│       └── metadata.pkl       # Person metadata
└── logs/
    └── search_logs.csv        # Search activity logs
```

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Webcam (optional, for camera capture)

### Step 1: Clone or Download
```bash
cd missing_person_finder
```

### Step 2: Install Dependencies

**Windows:**
```bash
pip install -r requirements.txt
```

**Linux/Mac:**
```bash
pip3 install -r requirements.txt
```

**Note:** Installing `dlib` may require additional system dependencies:

**Ubuntu/Debian:**
```bash
sudo apt-get install build-essential cmake
sudo apt-get install libopenblas-dev liblapack-dev
sudo apt-get install libx11-dev libgtk-3-dev
```

**macOS:**
```bash
brew install cmake
```

### Step 3: Run the Application
```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`

## 📖 Usage Guide

### 1. Adding People to Database

1. Navigate to **"➕ Add New Person"** page
2. Enter the person's name or ID (e.g., "John Doe" or "MP-2024-001")
3. Choose input method:
   - **Upload Image**: Select a JPG/PNG file
   - **Camera**: Capture live from webcam
4. Preview the image and verify face detection
5. Click **"Add to Database"**

**Best Practices:**
- Use clear, frontal face images
- Ensure good lighting
- One face per image
- High resolution images (recommended)

### 2. Searching for Matches

1. Navigate to **"🔎 Search Face"** page
2. Choose input method (Upload or Camera)
3. Provide the query image
4. Adjust number of results to show (1-20)
5. Click **"Search Database"**
6. Review ranked matches with similarity scores

### 3. Understanding Results

**Match Quality Indicators:**
- 🟢 **High Match** (Distance < 0.6): Strong confidence
- 🟡 **Medium Match** (Distance 0.6-0.8): Moderate confidence
- 🔴 **Low Match** (Distance > 0.8): Weak confidence

**Similarity Score:**
- 0-100% scale (higher = more similar)
- Based on L2 distance between face embeddings

**Distance:**
- Raw L2 distance metric
- Lower values indicate more similar faces
- Typical range: 0.0 (identical) to 1.0+ (different)

### 4. Viewing Database Statistics

Navigate to **"📊 Database Stats"** to see:
- Total number of people and faces
- Complete list of all entries
- Face gallery view
- Database management tools

**Rebuild Index:**
- Use if index becomes corrupted
- Recreates FAISS index from stored images
- Useful after manual file operations

### 5. Reviewing Search Logs

Navigate to **"📝 View Logs"** to:
- View all search activity
- See timestamps and query types
- Check top matches for each search
- Download logs as CSV

## 🔒 Privacy & Security

### Complete Privacy
- ✅ **No Internet Required** - Works entirely offline
- ✅ **No Cloud Storage** - All data stored locally
- ✅ **No External APIs** - No data leaves your machine
- ✅ **No Tracking** - No analytics or telemetry

### Data Storage
- Face images stored in `data/known_faces/`
- Face embeddings (128D vectors) stored in FAISS index
- Only metadata: name/ID and file path
- Search logs contain: timestamp, query type, match results

### Security Recommendations
- Keep the `data/` directory secure
- Regular backups of `data/` and `logs/`
- Restrict file system access appropriately
- Use encryption for sensitive deployments

## 🧪 How It Works

### 1. Face Detection
- Uses HOG (Histogram of Oriented Gradients) or CNN
- Detects face locations in images
- Extracts face regions for encoding

### 2. Face Encoding
- Converts face to 128-dimensional vector
- Uses deep learning model (ResNet)
- Captures unique facial features
- Invariant to lighting, angle (within limits)

### 3. Vector Indexing (FAISS)
- Stores embeddings in efficient index structure
- Uses L2 (Euclidean) distance metric
- Enables fast similarity search
- Scales to thousands of faces

### 4. Similarity Search
- Compares query embedding with database
- Finds k-nearest neighbors
- Returns ranked results with distances
- Converts distances to similarity scores

### 5. Logging
- Records every search operation
- Timestamps and query metadata
- Top match information
- CSV format for easy analysis

## 🎓 Technical Details

### Face Encoding
- **Dimensions:** 128D vector
- **Model:** dlib's ResNet-based face recognition model
- **Accuracy:** ~99.38% on LFW benchmark
- **Speed:** ~30ms per face on modern CPU

### FAISS Index
- **Type:** IndexFlatL2 (exact search)
- **Distance Metric:** L2 (Euclidean)
- **Search Complexity:** O(n) for n faces
- **Memory:** ~512 bytes per face

### Performance
- **Face Detection:** 100-500ms per image
- **Encoding:** 30-100ms per face
- **Search:** <10ms for 1000 faces
- **Total Query Time:** ~200-600ms

## 🔧 Configuration

### Adjusting Match Thresholds

Edit `embedding_utils.py` to customize thresholds:

```python
# Line ~150 in search_similar_faces()
"match_threshold": "High" if distance < 0.6 else "Medium" if distance < 0.8 else "Low"
```

### Changing Number of Results

Default is 5, adjustable in UI (1-20). To change default, edit `app.py`:

```python
# Line ~250 in search_face_page()
num_results = st.slider("Number of results to show:", 1, 20, 5)  # Last param is default
```

### Database Paths

Modify paths in `embedding_utils.py` initialization:

```python
def __init__(self, index_path: str = "data/index", known_faces_path: str = "data/known_faces"):
```

## 🐛 Troubleshooting

### Issue: "No face detected"
**Solutions:**
- Ensure face is clearly visible and frontal
- Check image quality and resolution
- Improve lighting conditions
- Try different image or angle

### Issue: "Poor match results"
**Solutions:**
- Add multiple images of the same person
- Use higher quality images
- Ensure consistent lighting
- Rebuild the index

### Issue: "Installation fails for dlib"
**Solutions:**
- Install CMake: `pip install cmake`
- Install build tools (see Installation section)
- Use pre-built wheels: `pip install dlib-binary`
- Try conda: `conda install -c conda-forge dlib`

### Issue: "FAISS index corrupted"
**Solutions:**
- Use "Rebuild Index" in Database Stats page
- Delete `data/index/` folder and restart app
- Check file permissions

### Issue: "Camera not working"
**Solutions:**
- Grant camera permissions to browser
- Check if camera is in use by another app
- Try different browser
- Use upload method instead

## 📊 Limitations

### Technical Limitations
- **Face Angle:** Works best with frontal faces (±45°)
- **Lighting:** Requires reasonable lighting conditions
- **Occlusion:** Masks, sunglasses reduce accuracy
- **Image Quality:** Low resolution affects performance
- **Age:** Significant aging may reduce match accuracy

### Scale Limitations
- **Database Size:** Optimized for 1,000-10,000 faces
- **Search Speed:** Linear with database size (IndexFlatL2)
- **Memory:** ~512 bytes per face + image storage

### Use Case Limitations
- Not suitable for real-time video surveillance
- Requires clear face images
- Not a replacement for professional forensic analysis
- Should be used as an investigative aid only

## 🚀 Future Enhancements

Potential improvements:
- [ ] Multiple face encodings per person
- [ ] Advanced FAISS indices (IVF, HNSW) for larger databases
- [ ] Batch upload functionality
- [ ] Export match reports as PDF
- [ ] Face quality assessment
- [ ] Age progression/regression
- [ ] Integration with case management systems
- [ ] Multi-user authentication
- [ ] Database encryption
- [ ] REST API for integration

## 📄 License

This project is provided as-is for educational and investigative purposes. Please ensure compliance with local privacy laws and regulations when deploying.

## ⚠️ Disclaimer

This system is designed as an investigative aid and should not be the sole basis for identification. Always verify matches through additional means and follow proper legal procedures. The accuracy of facial recognition can be affected by various factors including image quality, lighting, age, and facial expressions.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! This is an open-source project designed to help with missing persons cases.

## 📞 Support

For issues or questions:
1. Check this README
2. Review code documentation
3. Check troubleshooting section
4. Examine log files in `logs/`

## 🙏 Acknowledgments

- **dlib** - Face detection and recognition
- **FAISS** - Efficient similarity search
- **Streamlit** - Beautiful web interface
- **face_recognition** - Simplified face recognition API

---

**Built with ❤️ for helping find missing persons and identify unidentified individuals**

**Version:** 1.0.0  
**Last Updated:** November 2024
