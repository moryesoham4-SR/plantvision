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

# Supabase Cloud Database Config
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://ypytalpbuzzutxrspmje.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InlweXRhbHBidXp6dXR4cnNwbWplIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODgwOTkyNTAsImV4cCI6MjEwMzY3NTI1MH0.PLKOAJmwz_x0ZmMANUi6Ser811WSP7b4bUNQy_2NWOA")

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
        "drive_file_id": "1uPPXXC90noUpibecudBMiw9RPht9wpCP",
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
        "drive_file_id": "1uPPXXC90noUpibecudBMiw9RPht9wpCP",
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

