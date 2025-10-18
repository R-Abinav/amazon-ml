import re
import os
import pandas as pd
import multiprocessing
from time import time as timer
from tqdm import tqdm
import numpy as np
from pathlib import Path
from functools import partial
import requests
import urllib
import ssl
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def create_session():
    """Create a requests session with retry strategy and SSL configuration"""
    session = requests.Session()
    
    # Configure retry strategy
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["HEAD", "GET", "OPTIONS"]
    )
    
    # Mount adapter with retry strategy
    adapter = HTTPAdapter(max_retries=retry_strategy, pool_connections=20, pool_maxsize=20)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    
    # Configure headers to mimic a real browser
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    })
    
    return session

def download_image(image_link, savefolder, session=None):
    """Download a single image with robust error handling and retry logic"""
    if not isinstance(image_link, str) or not image_link.strip():
        return False
        
    filename = Path(image_link).name
    image_save_path = os.path.join(savefolder, filename)
    
    # Skip if file already exists
    if os.path.exists(image_save_path):
        return True
    
    # Create session if not provided
    if session is None:
        session = create_session()
    
    max_retries = 3
    retry_delay = 1
    
    for attempt in range(max_retries):
        try:
            response = session.get(
                image_link, 
                timeout=(10, 30),  # (connect timeout, read timeout)
                stream=True,
                verify=True  # Enable SSL verification
            )
            response.raise_for_status()
            
            # Save the image
            with open(image_save_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            return True
            
        except requests.exceptions.SSLError as e:
            print(f'SSL Error (attempt {attempt + 1}/{max_retries}) - {image_link}: {str(e)[:100]}')
            if attempt < max_retries - 1:
                time.sleep(retry_delay * (2 ** attempt))  # Exponential backoff
                continue
            else:
                print(f'Failed to download after {max_retries} attempts - {image_link}')
                return False
                
        except requests.exceptions.ConnectionError as e:
            print(f'Connection Error (attempt {attempt + 1}/{max_retries}) - {image_link}: {str(e)[:100]}')
            if attempt < max_retries - 1:
                time.sleep(retry_delay * (2 ** attempt))
                continue
            else:
                print(f'Failed to download after {max_retries} attempts - {image_link}')
                return False
                
        except requests.exceptions.Timeout as e:
            print(f'Timeout Error (attempt {attempt + 1}/{max_retries}) - {image_link}: {str(e)[:100]}')
            if attempt < max_retries - 1:
                time.sleep(retry_delay * (2 ** attempt))
                continue
            else:
                print(f'Failed to download after {max_retries} attempts - {image_link}')
                return False
                
        except requests.exceptions.RequestException as e:
            print(f'Request Error (attempt {attempt + 1}/{max_retries}) - {image_link}: {str(e)[:100]}')
            if attempt < max_retries - 1:
                time.sleep(retry_delay * (2 ** attempt))
                continue
            else:
                print(f'Failed to download after {max_retries} attempts - {image_link}')
                return False
                
        except Exception as e:
            print(f'Unexpected Error (attempt {attempt + 1}/{max_retries}) - {image_link}: {str(e)[:100]}')
            if attempt < max_retries - 1:
                time.sleep(retry_delay * (2 ** attempt))
                continue
            else:
                print(f'Failed to download after {max_retries} attempts - {image_link}')
                return False
    
    return False

def download_images(image_links, download_folder):
    """Download multiple images with improved error handling and progress tracking"""
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)
    
    print(f"Starting download of {len(image_links)} images...")
    print("Using improved download method with SSL support and retry logic")
    
    # Use fewer processes to avoid overwhelming the server
    num_processes = min(20, multiprocessing.cpu_count() * 2)
    
    results = []
    download_image_partial = partial(download_image, savefolder=download_folder)
    
    successful_downloads = 0
    failed_downloads = 0
    
    with multiprocessing.Pool(num_processes) as pool:
        for result in tqdm(pool.imap(download_image_partial, image_links), total=len(image_links), desc="Downloading images"):
            results.append(result)
            if result:
                successful_downloads += 1
            else:
                failed_downloads += 1
        pool.close()
        pool.join()
    
    print(f"\nDownload completed!")
    print(f"Successfully downloaded: {successful_downloads}")
    print(f"Failed downloads: {failed_downloads}")
    print(f"Success rate: {(successful_downloads/len(image_links)*100):.1f}%")
    
    return results