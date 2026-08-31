import os
from pathlib import Path

# Base Paths
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "models"
UPLOAD_DIR = BASE_DIR / "uploads"
STATIC_DIR = BASE_DIR / "static"
SAMPLES_DIR = BASE_DIR / "sample_leaves"

# Ensure directories exist
for directory in [DATA_DIR, MODELS_DIR, UPLOAD_DIR, STATIC_DIR, SAMPLES_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Database Config
DATABASE_PATH = BASE_DIR / "plantvision.db"

# Image Preprocessing Settings
IMAGE_TARGET_SIZE = (224, 224)
IMAGE_CHANNELS = 3

# Inference Switch
USE_MOCK = os.getenv("USE_MOCK", "True").lower() in ("true", "1", "yes")

# Plant and Model Registry
PLANTS = {
    "potato": {
        "name": "Potato",
        "scientific_name": "Solanum tuberosum",
        "icon": "🥔",
        "status": "Active",
        "model_file": "potato_model.keras",
        "drive_file_id": "18_aAbCdefGhiJklMnoPqrStUvWxYz012",
        "classes": [
            "Early Blight",
            "Late Blight",
            "Healthy"
        ]
    },
    "tomato": {
        "name": "Tomato",
        "scientific_name": "Solanum lycopersicum",
        "icon": "🍅",
        "status": "Active",
        "model_file": "tomato_model.keras",
        "drive_file_id": "19_bCdEfGhiJklMnoPqrStUvWxYz345",
        "classes": [
            "Early Blight",
            "Late Blight",
            "Septoria Leaf Spot",
            "Healthy"
        ]
    },
    "apple": {
        "name": "Apple",
        "scientific_name": "Malus domestica",
        "icon": "🍎",
        "status": "Active",
        "model_file": "apple_model.keras",
        "drive_file_id": "20_cDeFgHiJklMnoPqrStUvWxYz678",
        "classes": [
            "Apple Scab",
            "Black Rot",
            "Cedar Apple Rust",
            "Healthy"
        ]
    }
}

