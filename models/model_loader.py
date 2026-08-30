import os
import urllib.request
from pathlib import Path
from config import MODELS_DIR, PLANTS, USE_MOCK

def download_file_from_google_drive(file_id: str, destination_path: Path):
    "
    Downloads model weights from a public Google Drive File ID.
    "
    URL = fhttps://drive.google.com/uc?export=download&id={file_id}
    try:
        print(f[ModelLoader] Downloading weights from Google Drive ID: {file_id} to {destination_path}...)
        urllib.request.urlretrieve(URL, str(destination_path))
        print(f[ModelLoader] Download complete: {destination_path})
        return True
    except Exception as e:
        print(f[ModelLoader] Failed to download from Google Drive: {e})
        return False

def get_model_path(plant_id: str) -> Path:
    plant_config = PLANTS.get(plant_id.lower())
    if not plant_config:
        return None
    model_filename = plant_config.get(model_file, f{plant_id}_model.h5)
    return MODELS_DIR / model_filename

def ensure_model_available(plant_id: str):
    "
    Ensures model weight file is downloaded locally from Google Drive if configured.
    "
    if USE_MOCK:
        return False
        
    model_path = get_model_path(plant_id)
    if model_path and model_path.exists():
        return True
        
    plant_config = PLANTS.get(plant_id.lower(), {})
    file_id = plant_config.get(drive_file_id)
    
    if file_id and file_id != DRIVE_FILE_ID_POTATO and not file_id.startswith(DRIVE_FILE_ID):
        return download_file_from_google_drive(file_id, model_path)
        
    return False

def load_plant_model(plant_id: str):
    "
    Loads model into memory (Keras/TensorFlow/PyTorch/ONNX).
    If weights not found or USE_MOCK is True, returns None to trigger mock engine.
    "
    if USE_MOCK:
        return None

    model_path = get_model_path(plant_id)
    if not model_path or not model_path.exists():
        # Try downloading
        if not ensure_model_available(plant_id):
            return None

    try:
        # Example TensorFlow / Keras loader (lazy import)
        import tensorflow as tf
        model = tf.keras.models.load_model(str(model_path))
        print(f[ModelLoader] Loaded live {plant_id} model successfully.)
        return model
    except ImportError:
        print([ModelLoader] TensorFlow not installed. Using mock engine.)
        return None
    except Exception as e:
        print(f[ModelLoader] Error loading {plant_id} model: {e}. Falling back to mock engine.)
        return None
