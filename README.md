# Amazon ML Challenge 2025 - Smart Product Pricing Solution

## 🏆 Competition Results
**SMAPE Score:** 48.834%  
**Rank:** Top 750 out of 84,000+ registered students  
**Event:** 3-day Amazon ML Hackathon  

## 📋 Project Overview

This project was developed during the 3-day Amazon ML hackathon focused on predicting product prices using multimodal data (text and images). Our solution achieved a SMAPE score of 48.834%, placing us in the top 750 teams out of over 84,000 registered students.

## 🎯 Strategy & Approach

### Primary Strategy (48.834% SMAPE)
Our winning approach focused **exclusively on text data** from the `catalog_content` field:

1. **Text Embedding:** Used Sentence Transformers to create semantic embeddings of product descriptions
2. **Feature Engineering:** Extracted statistical features from text (length, word count, numerical patterns, etc.)
3. **Gradient Boosting Ensemble:** Trained XGBoost, CatBoost, and LightGBM models
4. **Ensemble Learning:** Combined predictions using stacking with Ridge regression as meta-model

### Alternative Approaches Attempted

#### 🖼️ Image Processing Pipeline
- **Goal:** Increase image resolution from SD to HD and use CLIP (OpenAI) for image embeddings
- **Challenge:** Insufficient compute resources caused repeated notebook crashes
- **Status:** Incomplete due to computational constraints

#### 🧠 MLP-Based Model
- **Goal:** Transition from gradient boosting to neural network architecture
- **Challenge:** Late pivot meant insufficient time for complete training
- **Status:** Could not submit due to time constraints

## 📁 Project Structure

### Models Directory (`student_resource/models/`)
All our experimental models and approaches are stored in the `models/` directory:

- **`text-optimised.ipynb`** ⭐ - **BEST PERFORMING MODEL** (48.834% SMAPE)
  - Uses only text data with Sentence Transformers + Gradient Boosting
  - Comprehensive feature engineering and ensemble learning
  
- **`advanced-ensemble-tfidf.ipynb`** - Advanced ensemble with TF-IDF and gradient boosting
- **`autogluon.ipynb`** - AutoML approach using AutoGluon framework
- **`candidate1.ipynb`** - Feature engineering experiments and improvements
- **`tailor.ipynb`** - Custom model architecture experiments
- **`heavy_image_text.ipynb`** - Multimodal approach with CLIP embeddings
- **`light-weight-tokenizer.ipynb`** - Lightweight text processing experiments
- **`meta-learning-layer.ipynb`** - Meta-learning approach experiments

### ⚠️ Important Note on Price Scraper
- **`price-scraper.ipynb`** - **NEVER USED IN TRAINING OR TESTING**
- This notebook was built purely out of curiosity to explore web scraping
- **The scraper is incomplete and non-functional**
- **We understand that using scraped data would violate competition rules**
- **Our final model used ONLY the provided dataset**

## 🚀 Getting Started

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Best Model:**
   ```bash
   jupyter notebook student_resource/models/text-optimised.ipynb
   ```

3. **Data Structure:**
   - Training data: `student_resource/dataset/train.csv`
   - Test data: `student_resource/dataset/test.csv`
   - Images: `student_resource/images/` (downloaded separately)

## 📊 Key Insights

- **Text-only approach outperformed multimodal attempts** due to computational constraints
- **Ensemble methods** (XGBoost + CatBoost + LightGBM) provided robust predictions
- **Feature engineering** from catalog content was crucial for performance
- **Semantic embeddings** (Sentence Transformers) captured product characteristics better than TF-IDF alone

## 🏅 Competition Context

- **Total Participants:** 84,000+ students
- **Our Rank:** Top 750 (top 0.8%)
- **Approach:** Text-only with advanced feature engineering and ensemble learning

## 📝 Documentation

- **Problem Statement:** `student_resource/README.md` (provided by organizers)
- **Technical Details:** `student_resource/Documentation_template.md`
- **Image Storage:** `student_resource/images/README.md`

---

*This project demonstrates the power of focused feature engineering and ensemble methods in achieving competitive results within computational constraints.*
