import os
import re
import requests
from pathlib import Path
import config

_LOADED_MODELS = {}

def extract_file_id(drive_url_or_id: str) -> str:
    """Extracts the Google Drive file ID from a URL or raw ID."""
    if not drive_url_or_id:
        return ""
    drive_url_or_id = drive_url_or_id.strip()
    match = re.search(r'/file/d/([a-zA-Z0-9_-]+)', drive_url_or_id)
    if match:
        return match.group(1)
    match_id = re.search(r'id=([a-zA-Z0-9_-]+)', drive_url_or_id)
    if match_id:
        return match_id.group(1)
    return drive_url_or_id

def download_from_google_drive(file_id_or_url: str, destination: Path) -> bool:
    """Downloads large model files directly from Google Drive with chunk streaming."""
    file_id = extract_file_id(file_id_or_url)
    if not file_id:
        return False
    if destination.exists() and destination.stat().st_size > 1024:
        return True

    url = "https://docs.google.com/uc?export=download"
    session = requests.Session()
    try:
        response = session.get(url, params={'id': file_id}, stream=True, timeout=30)
        token = None
        for key, value in response.cookies.items():
            if key.startswith('download_warning'):
                token = value
                break

        if token:
            params = {'id': file_id, 'confirm': token}
            response = session.get(url, params=params, stream=True, timeout=30)

        destination.parent.mkdir(parents=True, exist_ok=True)
        with open(destination, "wb") as f:
            for chunk in response.iter_content(32768):
                if chunk:
                    f.write(chunk)

        return destination.exists() and destination.stat().st_size > 1024
    except Exception as e:
        print(f"Failed to stream model from Google Drive ({file_id}): {e}")
        return False

def get_or_load_model(plant_key: str):
    if plant_key in _LOADED_MODELS:
        return _LOADED_MODELS[plant_key]

    plant_info = config.PLANTS.get(plant_key)
    if not plant_info:
        return None

    model_path = config.MODELS_DIR / plant_info["model_file"]

    if not model_path.exists() or model_path.stat().st_size < 1024:
        drive_id = plant_info.get("drive_file_id")
        if drive_id:
            download_from_google_drive(drive_id, model_path)

    if model_path.exists() and model_path.stat().st_size > 1024:
        try:
            import tensorflow as tf
            model = tf.keras.models.load_model(str(model_path))
            _LOADED_MODELS[plant_key] = model
            return model
        except Exception as e:
            print(f"Error loading model {plant_key}: {e}")
            return None

    return None


