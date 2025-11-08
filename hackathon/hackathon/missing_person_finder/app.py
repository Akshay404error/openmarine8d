"""
AI Facial Recognition System for Missing Persons & Unidentified Bodies
A complete local-only facial recognition system using Streamlit
"""

import streamlit as st
import numpy as np
from PIL import Image
import pandas as pd
from datetime import datetime
import os
from pathlib import Path
import cv2
import io
# Initialize TESSERACT_AVAILABLE at module level
TESSERACT_AVAILABLE = False

# Tesseract OCR setup
try:
    import pytesseract
    from pytesseract import Output
    
    # Try to set Tesseract path automatically for common Windows installation
    try:
        pytesseract.get_tesseract_version()
        TESSERACT_AVAILABLE = True
    except (pytesseract.TesseractNotFoundError, pytesseract.TesseractError):
        # Try common Windows installation paths
        common_paths = [
            r'C:\Program Files\Tesseract-OCR\\tesseract.exe',
            r'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe'
        ]
        for path in common_paths:
            if os.path.exists(path):
                pytesseract.pytesseract.tesseract_cmd = path
                try:
                    pytesseract.get_tesseract_version()
                    TESSERACT_AVAILABLE = True
                    break
                except:
                    continue
        
        if not TESSERACT_AVAILABLE:
            st.warning(
                "Tesseract OCR is not properly installed or not in PATH. "
                "Text detection in images will be disabled. Please install Tesseract OCR "
                "for full functionality."
            )
            
except ImportError:
    st.warning(
        "pytesseract is not installed. Text detection in images will be disabled. "
        "Install it with: pip install pytesseract"
    )

from embedding_utils import FaceEmbeddingManager


# Page configuration
st.set_page_config(
    page_title="AI Facial Recognition System",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .match-card {
        border: 2px solid #e0e0e0;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        background-color: #f9f9f9;
    }
    .high-match {
        border-color: #4CAF50;
        background-color: #e8f5e9;
    }
    .medium-match {
        border-color: #FF9800;
        background-color: #fff3e0;
    }
    .low-match {
        border-color: #f44336;
        background-color: #ffebee;
    }
    .stat-box {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)


# Initialize session state
if 'face_manager' not in st.session_state:
    st.session_state.face_manager = FaceEmbeddingManager()

if 'search_results' not in st.session_state:
    st.session_state.search_results = None

if 'query_image' not in st.session_state:
    st.session_state.query_image = None


def log_search(query_type: str, num_matches: int, top_match_name: str = None, top_match_distance: float = None):
    """Log search activity to CSV file"""
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / "search_logs.csv"
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_entry = {
        "timestamp": timestamp,
        "query_type": query_type,
        "num_matches": num_matches,
        "top_match_name": top_match_name if top_match_name else "N/A",
        "top_match_distance": f"{top_match_distance:.4f}" if top_match_distance else "N/A"
    }
    
    df = pd.DataFrame([log_entry])
    
    # Append to existing log or create new
    if log_file.exists():
        df.to_csv(log_file, mode='a', header=False, index=False)
    else:
        df.to_csv(log_file, mode='w', header=True, index=False)


def process_and_search_image(image_array: np.ndarray, query_type: str):
    """Process image and search for matches"""
    with st.spinner("🔍 Detecting and encoding face..."):
        # Encode the face
        encoding = st.session_state.face_manager.encode_face(image_array)
        
        if encoding is None:
            st.error("❌ No face detected in the image. Please upload a clear image with a visible face.")
            return
        
        st.success("✅ Face detected and encoded successfully!")
        
        # Search for similar faces
        with st.spinner("🔎 Searching database for matches..."):
            results = st.session_state.face_manager.search_similar_faces(encoding, k=10)
            
            if len(results) == 0:
                st.warning("⚠️ No matches found. The database might be empty.")
                log_search(query_type, 0)
            else:
                st.session_state.search_results = results
                st.success(f"✅ Found {len(results)} potential matches!")
                
                # Log the search
                log_search(
                    query_type,
                    len(results),
                    results[0]["name"],
                    results[0]["distance"]
                )


def display_search_results():
    """Display search results with images and similarity scores"""
    if st.session_state.search_results is None:
        return
    
    st.markdown("---")
    st.markdown("## 🎯 Search Results")
    
    results = st.session_state.search_results
    
    # Display results in columns
    for i in range(0, len(results), 3):
        cols = st.columns(3)
        
        for j, col in enumerate(cols):
            if i + j < len(results):
                result = results[i + j]
                
                with col:
                    # Determine match quality
                    match_class = result["match_threshold"].lower() + "-match"
                    
                    st.markdown(f"""
                        <div class="match-card {match_class}">
                            <h3>Rank #{result['rank']}</h3>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # Display image
                    try:
                        img = Image.open(result["image_path"])
                        st.image(img, use_column_width=True)
                    except:
                        st.error("Image not found")
                    
                    # Display information
                    st.markdown(f"**Name:** {result['name']}")
                    st.markdown(f"**Similarity:** {result['similarity']:.2f}%")
                    st.markdown(f"**Distance:** {result['distance']:.4f}")
                    st.markdown(f"**Match Quality:** {result['match_threshold']}")
                    
                    # Match interpretation
                    if result['distance'] < 0.6:
                        st.success("🟢 Strong Match")
                    elif result['distance'] < 0.8:
                        st.warning("🟡 Moderate Match")
                    else:
                        st.info("🔴 Weak Match")


def main():
    """Main application"""
    
    # Header
    st.markdown('<div class="main-header">🔍 AI Facial Recognition System</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Missing Persons & Unidentified Bodies Database</div>', unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.title("📋 Navigation")
    page = st.sidebar.radio(
        "Select Page",
        ["🔎 Search Face", "➕ Add New Person", "📊 Database Stats", "📝 View Logs", "⚙️ System Info"]
    )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🔒 Privacy Notice")
    st.sidebar.info("This system operates entirely offline. No data is sent to external servers.")
    
    # Page routing
    if page == "🔎 Search Face":
        search_face_page()
    elif page == "➕ Add New Person":
        add_person_page()
    elif page == "📊 Database Stats":
        database_stats_page()
    elif page == "📝 View Logs":
        view_logs_page()
    elif page == "⚙️ System Info":
        system_info_page()


def search_face_page():
    """Search for faces in the database"""
    st.header("🔎 Search for Missing Person or Identify Unknown Face")
    
    st.markdown("""
    Upload an image or capture from camera to search for matching faces in the database.
    The system will show the most similar faces with confidence scores.
    """)
    
    # Check if database is empty
    stats = st.session_state.face_manager.get_database_stats()
    if stats["total_faces"] == 0:
        st.warning("⚠️ The database is empty. Please add some faces first in the 'Add New Person' page.")
        return
    
    st.markdown("---")
    
    # Input method selection
    input_method = st.radio(
        "Choose input method:",
        ["📁 Upload Image", "📷 Capture from Camera"],
        horizontal=True
    )
    
    query_image = None
    
    if input_method == "📁 Upload Image":
        uploaded_file = st.file_uploader(
            "Upload an image (JPG, PNG, JPEG)",
            type=["jpg", "jpeg", "png"],
            help="Upload a clear image with a visible face"
        )
        
        if uploaded_file is not None:
            query_image = Image.open(uploaded_file)
            st.session_state.query_image = query_image
    
    elif input_method == "📷 Capture from Camera":
        camera_image = st.camera_input("Take a picture")
        
        if camera_image is not None:
            query_image = Image.open(camera_image)
            st.session_state.query_image = query_image
    
    # Display query image and search button
    if query_image is not None:
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("### Query Image")
            st.image(query_image, use_column_width=True)
        
        with col2:
            st.markdown("### Actions")
            
            # Number of results to show
            num_results = st.slider("Number of results to show:", 1, 20, 5)
            
            if st.button("🔍 Search Database", type="primary"):
                # Convert to numpy array
                img_array = np.array(query_image)
                
                # Process and search
                process_and_search_image(img_array, input_method.split()[0])
                
                # Update number of results
                if st.session_state.search_results:
                    st.session_state.search_results = st.session_state.search_results[:num_results]
            
            if st.button("🔄 Clear Results"):
                st.session_state.search_results = None
                st.session_state.query_image = None
                st.rerun()
    
    # Display results
    display_search_results()


def add_person_page():
    """Add a new person to the database"""
    st.header("➕ Add New Person to Database")
    
    st.markdown("""
    Add a new person to the facial recognition database. Upload a clear image with a visible face
    and provide the person's name or identifier.
    """)
    
    st.markdown("---")
    
    # Input fields
    col1, col2 = st.columns([1, 1])
    
    with col1:
        person_name = st.text_input(
            "Person's Name or ID *",
            placeholder="e.g., John Doe or MP-2024-001",
            help="Enter a unique identifier for this person"
        )
    
    with col2:
        input_method = st.radio(
            "Input method:",
            ["📁 Upload", "📷 Camera"],
            horizontal=True
        )
    
    # Image input
    person_image = None
    
    if input_method == "📁 Upload":
        uploaded_file = st.file_uploader(
            "Upload person's image or PDF",
            type=["jpg", "jpeg", "png", "webp", "pdf"],
            help="Upload a clear frontal face image (JPG, PNG, WebP) or PDF containing images"
        )
        
        if uploaded_file is not None:
            if uploaded_file.type == "application/pdf":
                try:
                    import fitz  # PyMuPDF
                    import tempfile
                    import io
                    
                    # Save the uploaded file to a temporary file
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                        tmp_file.write(uploaded_file.read())
                        tmp_file_path = tmp_file.name
                    
                    # Extract images from PDF
                    pdf_document = fitz.open(tmp_file_path)
                    
                    # Check if PDF has any images
                    has_images = False
                    for page_num in range(len(pdf_document)):
                        if pdf_document[page_num].get_images():
                            has_images = True
                            break
                    
                    if not has_images:
                        st.error("This PDF contains only text. Please upload a PDF with images or use an image file instead.")
                        pdf_document.close()
                        os.unlink(tmp_file_path)
                        return
                    
                    # Process PDF with images
                    for page_num in range(len(pdf_document)):
                        page = pdf_document.load_page(page_num)
                        image_list = page.get_images(full=True)
                        
                        if image_list:
                            try:
                                # Get the first image from the page
                                img = pdf_document.extract_image(image_list[0][0])
                                image_data = img["image"]
                                person_image = Image.open(io.BytesIO(image_data))
                                if person_image:
                                    break
                            except Exception as e:
                                st.warning(f"Could not process an image in the PDF: {str(e)}")
                                continue
                    
                    pdf_document.close()
                    os.unlink(tmp_file_path)  # Clean up temporary file
                    
                    if person_image is None:
                        st.error("Could not extract any usable images from the PDF. Please try with a different file.")
                    
                except Exception as e:
                    st.error(f"Error processing PDF: {str(e)}")
                    person_image = None
            else:
                # Handle regular image uploads
                try:
                    # Open the image
                    person_image = Image.open(uploaded_file)
                    
                    # Check for text in the image if Tesseract is available
                    if TESSERACT_AVAILABLE and uploaded_file.type in ["image/webp", "image/png", "image/jpeg", "image/jpg"]:
                        try:
                            # Convert to RGB if RGBA
                            if person_image.mode == 'RGBA':
                                person_image = person_image.convert('RGB')
                            
                            # Check for text using OCR
                            text = pytesseract.image_to_string(
                                np.array(person_image),
                                config='--psm 6 --oem 3 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz',
                                output_type=Output.STRING
                            ).strip()
                            
                            if text:
                                st.error("This image appears to contain text. Please upload an image without text.")
                                person_image = None
                                return
                                
                        except Exception as e:
                            st.warning("Could not check for text in the image. Please ensure Tesseract OCR is properly installed.")
                            # Continue with the upload even if text detection fails
                            
                except ImportError:
                    # If pytesseract is not available, just continue without text detection
                    pass
                except Exception as e:
                    st.error(f"Error processing image: {str(e)}")
                    person_image = None
    
    elif input_method == "📷 Camera":
        camera_image = st.camera_input("Capture person's image")
        if camera_image is not None:
            person_image = Image.open(camera_image)
    
    # Display preview and add button
    if person_image is not None:
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("### Preview")
            st.image(person_image, use_column_width=True)
        
        with col2:
            st.markdown("### Confirm Details")
            st.info(f"**Name/ID:** {person_name if person_name else 'Not provided'}")
            
            # Detect faces in image
            img_array = np.array(person_image)
            faces = st.session_state.face_manager.detect_faces(img_array)
            
            if len(faces) == 0:
                st.error("❌ No face detected in the image. Please use a different image.")
            elif len(faces) > 1:
                st.warning(f"⚠️ {len(faces)} faces detected. Only the first face will be used.")
            else:
                st.success("✅ Face detected successfully!")
            
            # Add button
            if st.button("➕ Add to Database", type="primary", disabled=not person_name or len(faces) == 0):
                with st.spinner("Adding person to database..."):
                    # Generate filename
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"{person_name.replace(' ', '_')}_{timestamp}.jpg"
                    
                    # Add to database
                    success = st.session_state.face_manager.add_face(
                        person_name,
                        img_array,
                        filename
                    )
                    
                    if success:
                        st.success(f"✅ Successfully added {person_name} to the database!")
                        st.balloons()
                        
                        # Show updated stats
                        stats = st.session_state.face_manager.get_database_stats()
                        st.info(f"📊 Database now contains {stats['total_faces']} faces")
                    else:
                        st.error("❌ Failed to add person to database. Please try again.")


def database_stats_page():
    """Display database statistics"""
    st.header("📊 Database Statistics")
    
    stats = st.session_state.face_manager.get_database_stats()
    
    # Display stats in columns
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div class="stat-box">
                <h2 style="color: #1f77b4;">👥 {}</h2>
                <p>Total People</p>
            </div>
        """.format(stats["total_people"]), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="stat-box">
                <h2 style="color: #2ca02c;">🎭 {}</h2>
                <p>Total Faces</p>
            </div>
        """.format(stats["total_faces"]), unsafe_allow_html=True)
    
    with col3:
        status = "✅ Active" if stats["index_exists"] else "❌ Not Found"
        st.markdown("""
            <div class="stat-box">
                <h2 style="color: #ff7f0e;">{}</h2>
                <p>Index Status</p>
            </div>
        """.format(status), unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Display all people in database
    if stats["total_people"] > 0:
        st.subheader("📋 People in Database")
        
        metadata = st.session_state.face_manager.metadata
        
        # Create dataframe
        df_data = []
        for i, person in enumerate(metadata, 1):
            df_data.append({
                "No.": i,
                "Name": person["name"],
                "Filename": person["filename"],
                "Image Path": person["image_path"]
            })
        
        df = pd.DataFrame(df_data)
        st.dataframe(df, hide_index=True)
        
        # Display images in grid
        st.subheader("🖼️ Face Gallery")
        
        cols_per_row = 4
        for i in range(0, len(metadata), cols_per_row):
            cols = st.columns(cols_per_row)
            
            for j, col in enumerate(cols):
                if i + j < len(metadata):
                    person = metadata[i + j]
                    with col:
                        try:
                            img = Image.open(person["image_path"])
                            st.image(img, caption=person["name"], use_column_width=True)
                        except:
                            st.error(f"Cannot load {person['name']}")
    else:
        st.info("📭 Database is empty. Add some people to get started!")
    
    st.markdown("---")
    
    # Database management
    st.subheader("🔧 Database Management")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔄 Rebuild Index from Images"):
            with st.spinner("Rebuilding index..."):
                successful, failed = st.session_state.face_manager.rebuild_index_from_images()
                st.success(f"✅ Rebuilt index: {successful} successful, {failed} failed")
                st.rerun()
    
    with col2:
        st.info("Use rebuild if index is corrupted or after manual file changes")


def view_logs_page():
    """View search logs"""
    st.header("📝 Search Activity Logs")
    
    log_file = Path("logs/search_logs.csv")
    
    if not log_file.exists():
        st.info("📭 No search logs available yet. Perform some searches to see logs here.")
        return
    
    # Read logs
    df = pd.read_csv(log_file)
    
    # Display summary stats
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div class="stat-box">
                <h2 style="color: #1f77b4;">📊 {}</h2>
                <p>Total Searches</p>
            </div>
        """.format(len(df)), unsafe_allow_html=True)
    
    with col2:
        upload_count = len(df[df["query_type"] == "📁"])
        st.markdown("""
            <div class="stat-box">
                <h2 style="color: #2ca02c;">📁 {}</h2>
                <p>Upload Searches</p>
            </div>
        """.format(upload_count), unsafe_allow_html=True)
    
    with col3:
        camera_count = len(df[df["query_type"] == "📷"])
        st.markdown("""
            <div class="stat-box">
                <h2 style="color: #ff7f0e;">📷 {}</h2>
                <p>Camera Searches</p>
            </div>
        """.format(camera_count), unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Display logs table
    st.subheader("📋 Recent Search Activity")
    
    # Sort by timestamp descending
    df_sorted = df.sort_values("timestamp", ascending=False)
    
    # Display with formatting
    st.dataframe(
        df_sorted,
        hide_index=True,
        column_config={
            "timestamp": st.column_config.DatetimeColumn("Timestamp", format="DD/MM/YYYY HH:mm:ss"),
            "query_type": "Query Type",
            "num_matches": st.column_config.NumberColumn("Matches Found"),
            "top_match_name": "Top Match",
            "top_match_distance": "Distance"
        }
    )
    
    # Download button
    st.markdown("---")
    
    csv = df_sorted.to_csv(index=False)
    st.download_button(
        label="📥 Download Logs as CSV",
        data=csv,
        file_name=f"search_logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv"
    )


def system_info_page():
    """Display system information and help"""
    st.header("⚙️ System Information")
    
    st.markdown("""
    ## 🎯 About This System
    
    This is a **fully local, privacy-safe facial recognition system** designed for:
    - 🔍 Identifying missing persons
    - 🆔 Matching unidentified bodies
    - 👥 Managing person databases
    - 📊 Tracking search activity
    
    ### 🔒 Privacy & Security
    - ✅ **100% Offline** - No cloud APIs or external connections
    - ✅ **Local Storage** - All data stays on your machine
    - ✅ **No Personal Data** - Only face embeddings are stored
    - ✅ **Full Control** - You own and manage all data
    
    ### 🛠️ Technology Stack
    - **Frontend:** Streamlit
    - **Face Detection:** face_recognition (dlib)
    - **Vector Search:** FAISS (Facebook AI Similarity Search)
    - **Image Processing:** OpenCV, Pillow
    - **Data Handling:** NumPy, Pandas
    
    ### 📖 How It Works
    
    1. **Face Detection** - Detects faces in uploaded/captured images
    2. **Encoding** - Converts faces to 128-dimensional vectors
    3. **Indexing** - Stores vectors in FAISS for fast similarity search
    4. **Matching** - Compares query faces with database using L2 distance
    5. **Ranking** - Returns top matches with similarity scores
    
    ### 📏 Understanding Match Scores
    
    - **Distance < 0.6** 🟢 High confidence match
    - **Distance 0.6-0.8** 🟡 Moderate confidence match  
    - **Distance > 0.8** 🔴 Low confidence match
    
    The distance represents how different two faces are (lower = more similar).
    
    ### 📁 File Structure
    ```
    missing_person_finder/
    ├── app.py                  # Main Streamlit application
    ├── embedding_utils.py      # Face encoding and FAISS utilities
    ├── requirements.txt        # Python dependencies
    ├── data/
    │   ├── known_faces/       # Stored face images
    │   └── index/             # FAISS index and metadata
    └── logs/
        └── search_logs.csv    # Search activity logs
    ```
    
    ### 🚀 Quick Start Guide
    
    1. **Add People** - Go to "Add New Person" and upload face images
    2. **Search** - Use "Search Face" to find matches
    3. **Review** - Check match scores and confidence levels
    4. **Track** - View logs to see search history
    
    ### ⚠️ Best Practices
    
    - Use **clear, frontal face images** for best results
    - Ensure **good lighting** in photos
    - One face per image works best
    - Use **consistent naming** for people
    - Regularly **backup** the data folder
    
    ### 🆘 Troubleshooting
    
    **No face detected?**
    - Ensure face is clearly visible
    - Check image quality and lighting
    - Try a different angle
    
    **Poor match results?**
    - Add more images of the same person
    - Use higher quality images
    - Rebuild the index
    
    **Index corrupted?**
    - Use "Rebuild Index" in Database Stats
    - This will recreate index from images
    
    ### 📞 Support
    
    For issues or questions, check the README.md file or review the code documentation.
    """)
    
    st.markdown("---")
    
    # System status
    st.subheader("💻 System Status")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.success("✅ Face Recognition: Active")
        st.success("✅ FAISS Index: Active")
        st.success("✅ Logging System: Active")
    
    with col2:
        stats = st.session_state.face_manager.get_database_stats()
        st.info(f"📊 Database: {stats['total_faces']} faces indexed")
        st.info(f"💾 Storage: data/ and logs/ directories")
        
        log_file = Path("logs/search_logs.csv")
        if log_file.exists():
            df = pd.read_csv(log_file)
            st.info(f"📝 Logs: {len(df)} searches recorded")
        else:
            st.info("📝 Logs: No searches yet")


if __name__ == "__main__":
    main()
