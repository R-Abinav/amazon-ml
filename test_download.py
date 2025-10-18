#!/usr/bin/env python3
"""
Test script to verify the improved download functionality with a small batch
"""

import pandas as pd
import os
import sys
from pathlib import Path

# Add the src directory to the path to import utils
sys.path.append(os.path.join(os.path.dirname(__file__), 'student_resource', 'src'))

from utils import download_images

def test_download():
    # Define paths
    root_dir = Path(__file__).parent
    dataset_dir = root_dir / "student_resource" / "dataset"
    test_csv_path = dataset_dir / "test.csv"
    test_images_folder = dataset_dir / "test_images_test"
    
    print("Loading test.csv dataset...")
    
    # Load the test.csv file
    try:
        df = pd.read_csv(test_csv_path)
        print(f"Loaded dataset with {len(df)} rows")
    except Exception as e:
        print(f"Error loading test.csv: {e}")
        return
    
    # Test with just the first 10 images that previously failed
    # Let's get some sample URLs that might have failed before
    sample_urls = [
        "https://m.media-amazon.com/images/I/71v60uN3WZL.jpg",
        "https://m.media-amazon.com/images/I/51jc1GAOStL.jpg", 
        "https://m.media-amazon.com/images/I/81UbHWTrriL.jpg",
        "https://m.media-amazon.com/images/I/811lNGLn3HL.jpg",
        "https://m.media-amazon.com/images/I/71ffrldN0DL.jpg"
    ]
    
    # Also get first 5 from the dataset
    first_five = df['image_link'].head(5).tolist()
    
    # Combine for testing
    test_links = sample_urls + first_five
    
    print(f"Testing download with {len(test_links)} images...")
    print(f"Test images will be saved to: {test_images_folder}")
    
    # Create test images folder if it doesn't exist
    test_images_folder.mkdir(parents=True, exist_ok=True)
    
    # Download test images using the improved utility function
    try:
        download_images(test_links, str(test_images_folder))
        print("Test download completed!")
        
        # Count downloaded images
        downloaded_count = len([f for f in test_images_folder.glob("*.jpg")])
        print(f"Total test images downloaded: {downloaded_count}")
        
        if downloaded_count > 0:
            print("✅ Test successful! The improved download method is working.")
            print("You can now run the main download script with confidence.")
        else:
            print("❌ Test failed. No images were downloaded.")
            
    except Exception as e:
        print(f"Error during test download: {e}")

if __name__ == "__main__":
    test_download()

