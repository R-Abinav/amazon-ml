# ML Challenge 2025: Smart Product Pricing Solution Template

**Team Name:** TEAM Baked
**Team Members:** R. Abinav, Kishore K, Sree Balaji, Monissh Balaji
**Submission Date:** 13/10/2025

---

## 1. Executive Summary
Our solution achieved a **SMAPE score of 48.834%**, placing us in the **top 700 out of 84,000+ registered students**. We focused exclusively on text data from the `catalog_content` field, using Sentence Transformers for semantic embeddings combined with comprehensive feature engineering and gradient boosting ensemble methods.

---

## 2. Methodology Overview

### 2.1 Problem Analysis
We interpreted the pricing challenge as a multimodal regression problem where product prices depend on both textual descriptions and visual features. Through exploratory data analysis, we discovered that:

**Key Observations:**
- Text data (`catalog_content`) contains rich information about product specifications, quantities, and brand indicators
- Product titles extracted from catalog content provide strong semantic signals
- Numerical patterns (pack sizes, unit measurements) are crucial price indicators
- Brand keywords and product categories significantly influence pricing
- Image data, while available, posed computational challenges that prevented full utilization

### 2.2 Solution Strategy
**Approach Type:** Text-only ensemble with semantic embeddings  
**Core Innovation:** Combining Sentence Transformers (semantic understanding) with proven engineered features and gradient boosting ensemble

Our strategy involved:
1. **Semantic Embeddings:** Using Sentence Transformers to capture product semantics
2. **Feature Engineering:** Extracting numerical patterns, brand indicators, and structural features
3. **Ensemble Learning:** Training XGBoost, CatBoost, and LightGBM models with stacking meta-model
4. **Target Encoding:** Encoding categorical features using cross-validation

---

## 3. Model Architecture

### 3.1 Architecture Overview
```
Input: catalog_content (text)
    ↓
[Text Preprocessing & Feature Extraction]
    ↓
┌─────────────────┬─────────────────┬─────────────────┐
│   Sentence      │   Engineered    │   Target        │
│   Transformers  │   Features      │   Encoding      │
│   (384D)        │   (50+ features)│   (4 features)   │
└─────────────────┴─────────────────┴─────────────────┘
    ↓
[Feature Concatenation: ~450 total features]
    ↓
┌─────────────────┬─────────────────┬─────────────────┐
│   LightGBM      │   XGBoost       │   CatBoost      │
│   (5000 trees)  │   (5000 trees)  │   (5000 trees)  │
└─────────────────┴─────────────────┴─────────────────┘
    ↓
[Meta-Model: Ridge Regression]
    ↓
Output: Price Prediction
```

### 3.2 Model Components

**Text Processing Pipeline:**
- [x] Preprocessing steps: Text cleaning, title extraction, truncation to 150 words
- [x] Model type: Sentence Transformers (all-MiniLM-L6-v2, 384 dimensions)
- [x] Key parameters: Batch size 64, L2 normalization, max length 256

**Feature Engineering Pipeline:**
- [x] Preprocessing steps: Regex extraction of pack quantities, unit measurements, brand indicators
- [x] Model type: Custom feature extraction functions
- [x] Key parameters: 50+ engineered features including pack info, unit conversions, brand signals

**Image Processing Pipeline:**
- [x] Preprocessing steps: N/A (images not used in final model)
- [x] Model type: N/A
- [x] Key parameters: N/A

---

## 4. Model Performance

### 4.1 Validation Results
- **SMAPE Score:** 48.834%
- **Other Metrics:** Cross-validation mean: 48.9% ± 0.3%
- **Rank:** Top 700 out of 84,000+ participants (top 0.8%)

### 4.2 Model Components Performance
- **LightGBM:** Individual SMAPE ~49.2%
- **XGBoost:** Individual SMAPE ~49.0%
- **CatBoost:** Individual SMAPE ~49.1%
- **Ensemble:** Combined SMAPE 48.834%

---

## 5. Conclusion
Our text-only approach successfully achieved a competitive SMAPE score of 48.834% by leveraging semantic embeddings from Sentence Transformers combined with comprehensive feature engineering. The ensemble of gradient boosting models with stacking meta-learning proved effective for this e-commerce pricing challenge. While we experimented with image processing using CLIP embeddings, computational constraints prevented full implementation, demonstrating that focused text-based approaches can achieve strong results.

---

## Appendix

### A. Code artefacts
Complete code available in the `student_resource/models/` directory:
- **`text-optimised.ipynb`** - Final winning model (48.834% SMAPE)
- **`advanced-ensemble-tfidf.ipynb`** - Advanced ensemble with TF-IDF
- **`autogluon.ipynb`** - AutoML experiments
- **`heavy_image_text.ipynb`** - Multimodal CLIP experiments (incomplete)
- **`price-scraper.ipynb`** - Web scraping experiments (NOT USED)

### B. Additional Results
- **Baseline Comparison:** Improved from ~50% baseline to 48.834%
- **Feature Importance:** Pack quantities, unit measurements, and brand indicators were most predictive
- **Computational Notes:** Image processing attempts failed due to resource constraints
- **Alternative Approaches:** MLP-based models were attempted but couldn't complete training in time

---

**Note:** This solution demonstrates the effectiveness of semantic text embeddings combined with traditional feature engineering for e-commerce price prediction, achieving competitive results within computational constraints.
