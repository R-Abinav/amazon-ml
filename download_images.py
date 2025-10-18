#!/usr/bin/env python3
"""
Complete standalone script to download all images locally
Downloads to:
  - <root>/student_resource/dataset/train_images/
  - <root>/student_resource/dataset/test_images/
Automatically skips already downloaded images.
"""

import pandas as pd
import os
import requests
from pathlib import Path
from tqdm import tqdm
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import warnings
warnings.filterwarnings('ignore')

# SSL handling
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ==================== CONFIGURATION ====================
CONFIG = {
    'max_workers': 16,  # Parallel downloads
    'timeout': 15,
    'max_retries': 3,
    'retry_delay': 2,
}

# ==================== DOWNLOAD FUNCTION ====================
def download_single_image(args):
    """Download a single image with retry logic"""
    sample_id, url, output_dir, retries, timeout = args
    
    # Check if already exists (all common extensions)
    for ext in ['.jpg', '.jpeg', '.png', '.webp', '.gif']:
        filepath = os.path.join(output_dir, f"{sample_id}{ext}")
        if os.path.exists(filepath) and os.path.getsize(filepath) > 0:
            return (sample_id, True, "exists")
    
    # Try downloading
    for attempt in range(retries):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'image/avif,image/webp,image/apng,image/*,*/*;q=0.8',
                'Referer': 'https://www.amazon.com/',
            }
            
            response = requests.get(
                url,
                headers=headers,
                timeout=timeout,
                verify=False,  # Disable SSL verification for problematic URLs
                stream=True
            )
            
            if response.status_code == 200:
                # Determine extension
                content_type = response.headers.get('content-type', '').lower()
                if 'jpeg' in content_type or 'jpg' in content_type:
                    ext = '.jpg'
                elif 'png' in content_type:
                    ext = '.png'
                elif 'webp' in content_type:
                    ext = '.webp'
                elif 'gif' in content_type:
                    ext = '.gif'
                else:
                    # Fallback to URL extension or default to .jpg
                    url_ext = Path(url.split('?')[0]).suffix.lower()
                    ext = url_ext if url_ext in ['.jpg', '.jpeg', '.png', '.webp', '.gif'] else '.jpg'
                
                filepath = os.path.join(output_dir, f"{sample_id}{ext}")
                
                # Write file
                with open(filepath, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                
                # Verify not empty
                if os.path.getsize(filepath) > 0:
                    return (sample_id, True, None)
                else:
                    os.remove(filepath)
                    raise Exception("Empty file")
            else:
                raise Exception(f"HTTP {response.status_code}")
        
        except Exception as e:
            if attempt == retries - 1:
                return (sample_id, False, str(e)[:50])
            time.sleep(CONFIG['retry_delay'])
    
    return (sample_id, False, "Max retries exceeded")

def get_existing_images(output_dir):
    """Get set of sample_ids that are already downloaded"""
    existing = set()
    if not os.path.exists(output_dir):
        return existing
    
    for ext in ['.jpg', '.jpeg', '.png', '.webp', '.gif']:
        for filepath in Path(output_dir).glob(f"*{ext}"):
            # Extract sample_id (filename without extension)
            existing.add(filepath.stem)
    
    return existing

def download_dataset_images(csv_path, output_dir, dataset_name):
    """Download all images for a dataset"""
    print(f"\n{'='*70}")
    print(f"📥 Downloading {dataset_name}")
    print(f"{'='*70}")
    
    # Load CSV
    try:
        df = pd.read_csv(csv_path)
        print(f"✓ Loaded CSV: {len(df):,} samples")
    except Exception as e:
        print(f"❌ Error loading {csv_path}: {e}")
        return 0, 0
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Check existing images
    existing = get_existing_images(output_dir)
    already_downloaded = len(existing)
    
    print(f"📊 Already downloaded: {already_downloaded:,}")
    print(f"📥 Remaining to download: {len(df) - already_downloaded:,}")
    
    # Prepare tasks (only for missing images)
    tasks = []
    for _, row in df.iterrows():
        sample_id = str(row['sample_id'])
        
        # Skip if already exists
        if sample_id in existing:
            continue
        
        url = row.get('image_link', '')
        if pd.isna(url) or not url or url == '':
            continue
        
        tasks.append((
            sample_id,
            url,
            output_dir,
            CONFIG['max_retries'],
            CONFIG['timeout']
        ))
    
    if not tasks:
        print(f"🎉 All images already downloaded!")
        coverage = (already_downloaded / len(df)) * 100
        print(f"🎯 Coverage: {coverage:.2f}%")
        return already_downloaded, 0
    
    # Download in parallel
    print(f"\n🚀 Starting download: {len(tasks):,} images...")
    print(f"   Workers: {CONFIG['max_workers']}")
    est_time_min = (len(tasks) / (CONFIG['max_workers'] * 2)) / 60
    print(f"   Est. time: ~{est_time_min:.1f} minutes")
    
    successful = 0
    failed = 0
    failed_list = []
    
    with ThreadPoolExecutor(max_workers=CONFIG['max_workers']) as executor:
        futures = {executor.submit(download_single_image, task): task for task in tasks}
        
        with tqdm(total=len(tasks), desc="Downloading", unit="img") as pbar:
            for future in as_completed(futures):
                sample_id, success, error = future.result()
                
                if success and error != "exists":
                    successful += 1
                elif error == "exists":
                    successful += 1  # Count as successful
                else:
                    failed += 1
                    failed_list.append((sample_id, error))
                
                pbar.update(1)
                pbar.set_postfix({'✓': successful, '✗': failed})
    
    total_available = already_downloaded + successful
    coverage = (total_available / len(df)) * 100
    
    print(f"\n{'='*70}")
    print(f"📊 Results for {dataset_name}")
    print(f"{'='*70}")
    print(f"✅ New downloads: {successful:,}")
    print(f"❌ Failed: {failed:,}")
    print(f"📈 Total available: {total_available:,} / {len(df):,}")
    print(f"🎯 Coverage: {coverage:.2f}%")
    
    if failed_list and len(failed_list) <= 20:
        print(f"\n⚠️  Failed images (showing first 20):")
        for sid, err in failed_list[:20]:
            print(f"   • {sid}: {err}")
    elif failed_list:
        print(f"\n⚠️  {len(failed_list):,} images failed to download")
    
    return total_available, failed

# ==================== MAIN ====================
def main():
    """Main execution"""
    print("="*80)
    print("🚀 LOCAL IMAGE DOWNLOADER (Skip Existing)")
    print("="*80)
    
    # Setup paths
    script_dir = Path(__file__).parent
    dataset_dir = script_dir / "student_resource" / "dataset"
    
    train_csv = dataset_dir / "train.csv"
    test_csv = dataset_dir / "test.csv"
    train_images_dir = dataset_dir / "train_images"
    test_images_dir = dataset_dir / "test_images"
    
    print(f"📁 Root directory: {script_dir}")
    print(f"📁 Dataset directory: {dataset_dir}")
    print(f"📁 Train images → {train_images_dir}")
    print(f"📁 Test images → {test_images_dir}")
    
    # Check CSVs exist
    if not train_csv.exists():
        print(f"\n❌ train.csv not found at: {train_csv}")
        return
    if not test_csv.exists():
        print(f"\n❌ test.csv not found at: {test_csv}")
        return
    
    print(f"\n✓ Found train.csv and test.csv")
    
    # Download train images
    print(f"\n[1/2] Processing training images...")
    train_count, train_failed = download_dataset_images(
        train_csv,
        str(train_images_dir),
        "Training Images"
    )
    
    # Download test images
    print(f"\n[2/2] Processing test images...")
    test_count, test_failed = download_dataset_images(
        test_csv,
        str(test_images_dir),
        "Test Images"
    )
    
    # Final summary
    total = train_count + test_count
    total_failed = train_failed + test_failed
    
    print(f"\n{'='*80}")
    print(f"🎉 DOWNLOAD COMPLETE!")
    print(f"{'='*80}")
    print(f"📊 Summary:")
    print(f"   Train: {train_count:,} images → {train_images_dir}")
    print(f"   Test: {test_count:,} images → {test_images_dir}")
    print(f"   Total: {total:,} images")
    print(f"   Failed: {total_failed:,}")
    
    if total_failed > 0:
        print(f"\n💡 Tip: Re-run this script to retry failed downloads")
    
    print(f"{'='*80}")

if __name__ == "__main__":
    main()