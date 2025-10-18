# Images Directory

This directory contains the downloaded product images from the Amazon ML Challenge dataset.

## Purpose
- **Storage Location:** All product images referenced in the training and test datasets
- **Usage:** Images were downloaded for experimental multimodal approaches
- **Note:** Our final winning model (`text-optimised.ipynb`) used **only text data** and did not utilize these images

## Image Processing Attempts
We experimented with:
- **Resolution Enhancement:** Attempting to upscale images from SD to HD
- **CLIP Embeddings:** Using OpenAI's CLIP model for image feature extraction
- **Multimodal Fusion:** Combining image and text embeddings

## Status
- **Images Downloaded:** ✅ Complete
- **Image Processing:** ❌ Incomplete (computational constraints)
- **Final Model:** Used text-only approach due to resource limitations

## Technical Details
- **Download Script:** `download_images.py` (in parent directory)
- **Image Format:** JPG/PNG files
- **Naming Convention:** Matches sample_id from dataset
- **Total Count:** ~50,000+ product images

*Note: Despite having access to images, our best performing model achieved 48.834% SMAPE using only text data from catalog_content.*
