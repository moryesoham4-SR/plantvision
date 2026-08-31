import os
from pathlib import Path
import config

_LOADED_MODELS = {}

def download_from_google_drive(file_id: str, destination: Path) -> bool:
    if destination.exists():
        return True
    try:
        import gdown
        url = f"https://drive.google.com/uc?id={file_id}"
        gdown.download(url, str(destination), quiet=False)
        return destination.exists()
    except Exception as e:
        print(f"Failed to download model from Google Drive: {e}")
        return False

def get_or_load_model(plant_key: str):
    if plant_key in _LOADED_MODELS:
        return _LOADED_MODELS[plant_key]

    plant_info = config.PLANTS.get(plant_key)
    if not plant_info:
        return None

    model_path = config.MODELS_DIR / plant_info["model_file"]

    if not model_path.exists():
        drive_id = plant_info.get("drive_file_id")
        if drive_id:
            download_from_google_drive(drive_id, model_path)

    if model_path.exists():
        try:
            import tensorflow as tf
            model = tf.keras.models.load_model(str(model_path))
            _LOADED_MODELS[plant_key] = model
            return model
        except Exception as e:
            print(f"Error loading model {plant_key}: {e}")
            return None

    return None

