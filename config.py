import os
from pathlib import Path

# Base Paths
BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / users.db
UPLOAD_DIR = BASE_DIR / uploads
STATIC_DIR = BASE_DIR / static
SAMPLES_DIR = STATIC_DIR / samples
MODELS_DIR = BASE_DIR / models / saved

# Ensure directories exist
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
MODELS_DIR.mkdir(parents=True, exist_ok=True)
SAMPLES_DIR.mkdir(parents=True, exist_ok=True)

# Application Config
APP_NAME = PlantVision AI
APP_TAGLINE = Computer Vision-Powered Plant Disease Detection System
APP_ICON = 🌿

# ML Input Configuration
IMAGE_SIZE = (224, 224)
INPUT_SHAPE = (1, 224, 224, 3)

# Default Mode (Set to False when live model weights from Drive are available)
USE_MOCK = True

# Supported Plants
PLANTS = {
    potato: {
        id: potato,
        name: Potato,
        scientific_name: Solanum tuberosum,
        icon: 🥔,
        model_file: potato_model.h5,
        drive_file_id: DRIVE_FILE_ID_POTATO,  # Replace with actual Google Drive File ID
        classes: [Early Blight, Late Blight, Healthy]
    },
    tomato: {
        id: tomato,
        name: Tomato,
        scientific_name: Solanum lycopersicum,
        icon: 🍅,
        model_file: tomato_model.h5,
        drive_file_id: DRIVE_FILE_ID_TOMATO,  # Replace with actual Google Drive File ID
        classes: [Early Blight, Late Blight, Septoria Leaf Spot, Healthy]
    },
    apple: {
        id: apple,
        name: Apple,
        scientific_name: Malus domestica,
        icon: 🍎,
        model_file: apple_model.h5,
        drive_file_id: DRIVE_FILE_ID_APPLE,   # Replace with actual Google Drive File ID
        classes: [Apple Scab, Black Rot, Cedar Apple Rust, Healthy]
    }
}

# Severity Styling Mapping
SEVERITY_COLORS = {
    None: {badge: 🟢 Healthy, color: #10B981, bg: #ECFDF5, border: #6EE7B7},
    Moderate: {badge: 🟡 Moderate Risk, color: #F59E0B, bg: #FFFBEB, border: #FCD34D},
    Severe: {badge: 🔴 High / Critical Risk, color: #EF4444, bg: #FEF2F2, border: #FCA5A5}
}
