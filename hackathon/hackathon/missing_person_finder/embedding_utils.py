"""
Embedding utilities for face recognition and FAISS vector search
Handles face detection, encoding, and similarity search operations
"""

import face_recognition
import numpy as np
import faiss
import pickle
import os
from pathlib import Path
from typing import List, Tuple, Optional
import cv2
from PIL import Image


class FaceEmbeddingManager:
    """Manages face embeddings and FAISS index for similarity search"""
    
    def __init__(self, index_path: str = "data/index", known_faces_path: str = "data/known_faces"):
        self.index_path = Path(index_path)
        self.known_faces_path = Path(known_faces_path)
        self.index_file = self.index_path / "faiss_index.bin"
        self.metadata_file = self.index_path / "metadata.pkl"
        
        # Create directories if they don't exist
        self.index_path.mkdir(parents=True, exist_ok=True)
        self.known_faces_path.mkdir(parents=True, exist_ok=True)
        
        # Initialize FAISS index and metadata
        self.dimension = 128  # face_recognition produces 128D embeddings
        self.index = None
        self.metadata = []  # List of dicts: [{"name": "John Doe", "image_path": "path/to/image.jpg"}]
        
        # Load existing index if available
        self.load_index()
    
    def encode_face(self, image_array: np.ndarray) -> Optional[np.ndarray]:
        """
        Encode a face from an image array into a 128D embedding
        
        Args:
            image_array: RGB image as numpy array
            
        Returns:
            128D face encoding or None if no face detected
        """
        try:
            # Convert to RGB if needed
            if len(image_array.shape) == 2:  # Grayscale
                image_array = cv2.cvtColor(image_array, cv2.COLOR_GRAY2RGB)
            elif image_array.shape[2] == 4:  # RGBA
                image_array = cv2.cvtColor(image_array, cv2.COLOR_RGBA2RGB)
            
            # Detect faces and get encodings
            face_locations = face_recognition.face_locations(image_array)
            
            if len(face_locations) == 0:
                return None
            
            # Get encoding for the first face found
            face_encodings = face_recognition.face_encodings(image_array, face_locations)
            
            if len(face_encodings) > 0:
                return face_encodings[0]
            
            return None
            
        except Exception as e:
            print(f"Error encoding face: {e}")
            return None
    
    def detect_faces(self, image_array: np.ndarray) -> List[Tuple[int, int, int, int]]:
        """
        Detect all faces in an image
        
        Args:
            image_array: RGB image as numpy array
            
        Returns:
            List of face locations as (top, right, bottom, left)
        """
        try:
            return face_recognition.face_locations(image_array)
        except Exception as e:
            print(f"Error detecting faces: {e}")
            return []
    
    def add_face(self, name: str, image_array: np.ndarray, image_filename: str) -> bool:
        """
        Add a new face to the database
        
        Args:
            name: Person's name
            image_array: RGB image as numpy array
            image_filename: Filename to save the image
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Encode the face
            encoding = self.encode_face(image_array)
            
            if encoding is None:
                return False
            
            # Save the image
            image_path = self.known_faces_path / image_filename
            img = Image.fromarray(image_array)
            img.save(image_path)
            
            # Add to metadata
            self.metadata.append({
                "name": name,
                "image_path": str(image_path),
                "filename": image_filename
            })
            
            # Add to FAISS index
            if self.index is None:
                # Create new index
                self.index = faiss.IndexFlatL2(self.dimension)
            
            # Add encoding to index
            encoding_reshaped = encoding.reshape(1, -1).astype('float32')
            self.index.add(encoding_reshaped)
            
            # Save index and metadata
            self.save_index()
            
            return True
            
        except Exception as e:
            print(f"Error adding face: {e}")
            return False
    
    def search_similar_faces(self, query_encoding: np.ndarray, k: int = 5) -> List[dict]:
        """
        Search for similar faces in the database
        
        Args:
            query_encoding: 128D face encoding to search for
            k: Number of top matches to return
            
        Returns:
            List of dicts with match information
        """
        if self.index is None or self.index.ntotal == 0:
            return []
        
        try:
            # Ensure k doesn't exceed number of faces in database
            k = min(k, self.index.ntotal)
            
            # Search FAISS index
            query_reshaped = query_encoding.reshape(1, -1).astype('float32')
            distances, indices = self.index.search(query_reshaped, k)
            
            # Prepare results
            results = []
            for i, (distance, idx) in enumerate(zip(distances[0], indices[0])):
                if idx < len(self.metadata):
                    # Convert L2 distance to similarity score (0-100)
                    # Lower distance = higher similarity
                    # Typical face distance range: 0.0 (identical) to 1.0+ (different)
                    similarity = max(0, 100 * (1 - min(distance, 1.0)))
                    
                    results.append({
                        "rank": i + 1,
                        "name": self.metadata[idx]["name"],
                        "image_path": self.metadata[idx]["image_path"],
                        "distance": float(distance),
                        "similarity": float(similarity),
                        "match_threshold": "High" if distance < 0.6 else "Medium" if distance < 0.8 else "Low"
                    })
            
            return results
            
        except Exception as e:
            print(f"Error searching faces: {e}")
            return []
    
    def save_index(self):
        """Save FAISS index and metadata to disk"""
        try:
            if self.index is not None and self.index.ntotal > 0:
                faiss.write_index(self.index, str(self.index_file))
            
            with open(self.metadata_file, 'wb') as f:
                pickle.dump(self.metadata, f)
                
        except Exception as e:
            print(f"Error saving index: {e}")
    
    def load_index(self):
        """Load FAISS index and metadata from disk"""
        try:
            if self.index_file.exists():
                self.index = faiss.read_index(str(self.index_file))
            else:
                self.index = faiss.IndexFlatL2(self.dimension)
            
            if self.metadata_file.exists():
                with open(self.metadata_file, 'rb') as f:
                    self.metadata = pickle.load(f)
            else:
                self.metadata = []
                
        except Exception as e:
            print(f"Error loading index: {e}")
            self.index = faiss.IndexFlatL2(self.dimension)
            self.metadata = []
    
    def get_database_stats(self) -> dict:
        """Get statistics about the face database"""
        return {
            "total_faces": self.index.ntotal if self.index else 0,
            "total_people": len(self.metadata),
            "index_exists": self.index_file.exists(),
            "metadata_exists": self.metadata_file.exists()
        }
    
    def rebuild_index_from_images(self) -> Tuple[int, int]:
        """
        Rebuild FAISS index from images in known_faces directory
        Useful for recovery or initial setup
        
        Returns:
            Tuple of (successful_count, failed_count)
        """
        # Reset index and metadata
        self.index = faiss.IndexFlatL2(self.dimension)
        self.metadata = []
        
        successful = 0
        failed = 0
        
        # Process all images in known_faces directory
        for image_file in self.known_faces_path.glob("*"):
            if image_file.suffix.lower() in ['.jpg', '.jpeg', '.png', '.bmp']:
                try:
                    # Load image
                    img = Image.open(image_file)
                    img_array = np.array(img)
                    
                    # Encode face
                    encoding = self.encode_face(img_array)
                    
                    if encoding is not None:
                        # Extract name from filename (remove extension)
                        name = image_file.stem
                        
                        # Add to metadata
                        self.metadata.append({
                            "name": name,
                            "image_path": str(image_file),
                            "filename": image_file.name
                        })
                        
                        # Add to index
                        encoding_reshaped = encoding.reshape(1, -1).astype('float32')
                        self.index.add(encoding_reshaped)
                        
                        successful += 1
                    else:
                        failed += 1
                        
                except Exception as e:
                    print(f"Error processing {image_file}: {e}")
                    failed += 1
        
        # Save the rebuilt index
        if successful > 0:
            self.save_index()
        
        return successful, failed
