# 🌿 PlantVision AI — Plant Disease Detection System

**PlantVision AI** is a computer vision-powered web application built with **Streamlit, Python, Plotly, and SQLite** to detect plant diseases from leaf images across three core agricultural crops: **Potato, Tomato, and Apple**, with specialized backend models for each plant.

---

## 🚀 Key Features

1. **User Authentication & Profiles:** Secure registration, login with hashed passwords, and personal scan history sessions.
2. **Plant Disease Scanner:**
   * Select **Potato**, **Tomato**, or **Apple**.
   * Upload JPG/JPEG/PNG or use 1-click test sample leaves.
   * Automatic image preprocessing to standard **224 × 224 × 3 RGB**.
   * Multi-class confidence score and latency meter.
3. **AI Diagnosis & Prescription:**
   * Condition status: **Early Blight**, **Late Blight**, **Apple Scab**, **Black Rot**, **Cedar Rust**, **Septoria**, or **Healthy**.
   * Disease severity tags (🟢 Healthy, 🟡 Moderate, 🔴 Severe).
   * 3-tier treatment recommendations: **Organic Remedies**, **Chemical Fungicides with Dosages**, and **Prevention Tips**.
4. **Personal Scan History:** Automatically logs all scans to the user's account in SQLite database with search and filtering by plant and status.
5. **Interactive Analytics Dashboard:** Real-time Plotly charts for total scan volume, healthy vs. diseased ratios, and disease distribution.
6. **Plant Disease Library:** Comprehensive offline encyclopedia covering symptoms, pathogens, causes, and management for all 3 plants.
7. **Diagnostic PDF Report Generation:** 1-click downloadable pathology report for farmers and agronomists.

---

## 🛠️ System Architecture

`	ext
plantvision-ai/
├── app.py                     # Main Streamlit application entry point & router
├── config.py                  # App settings, constants, USE_MOCK flag, Google Drive IDs
├── database.py                # SQLite database management (Users, Scans, Analytics)
├── auth.py                    # Authentication, password hashing, session state
├── preprocessor.py            # Image preprocessing pipeline (224x224x3 RGB)
├── report_generator.py        # PDF diagnostic report generator
├── requirements.txt           # Python dependencies
├── models/
│   ├── model_loader.py        # Google Drive downloader & cached loader
│   ├── potato_model.py        # Potato inference handler
│   ├── tomato_model.py        # Tomato inference handler
│   └── apple_model.py         # Apple inference handler
├── data/
│   ├── disease_library.py     # Plant disease knowledge base
│   └── mock_predictions.py    # Realistic mock inference engine
└── static/
    ├── style.css              # Custom styling & badges
    └── samples/               # Preloaded sample leaf images
`

---

## 📦 Installation & Setup

1. **Install Python dependencies:**
`ash
pip install -r requirements.txt
`

2. **Run the Streamlit application:**
`ash
streamlit run app.py
`

---

## ☁️ Connecting Google Drive Model Weights

1. Open config.py.
2. Replace DRIVE_FILE_ID_POTATO, DRIVE_FILE_ID_TOMATO, and DRIVE_FILE_ID_APPLE with your Google Drive public file IDs.
3. Set USE_MOCK = False in config.py.
4. models/model_loader.py will automatically download and load the .h5/.pth model files into the application without altering the UI!
