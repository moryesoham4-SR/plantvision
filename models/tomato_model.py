import numpy as np
from typing import Dict, Any
import config
from data.mock_predictions import get_mock_prediction
from data.disease_library import DISEASE_KNOWLEDGE_BASE

def predict_tomato(tensor_input: np.ndarray, image_hint: str = "") -> Dict[str, Any]:
    if config.USE_MOCK:
        return get_mock_prediction("tomato", image_hint)

    from models.model_loader import get_or_load_model
    model = get_or_load_model("tomato")

    if model is None:
        return get_mock_prediction("tomato", image_hint)

    predictions = model.predict(tensor_input)
    class_idx = int(np.argmax(predictions[0]))
    confidence = float(predictions[0][class_idx])

    classes = config.PLANTS["tomato"]["classes"]
    predicted_disease = classes[class_idx]
    disease_info = DISEASE_KNOWLEDGE_BASE["tomato"].get(predicted_disease, {})

    probabilities = {classes[i]: float(predictions[0][i]) for i in range(len(classes))}

    return {
        "plant_id": "tomato",
        "plant_name": config.PLANTS["tomato"]["name"],
        "scientific_name": config.PLANTS["tomato"]["scientific_name"],
        "predicted_disease": predicted_disease,
        "pathogen": disease_info.get("pathogen", "N/A"),
        "confidence": confidence,
        "confidence_percent": f"{confidence * 100:.1f}%",
        "is_healthy": disease_info.get("is_healthy", False),
        "severity": disease_info.get("severity", "Moderate"),
        "description": disease_info.get("description", ""),
        "causes": disease_info.get("causes", ""),
        "symptoms": disease_info.get("symptoms", []),
        "remedies": {
            "organic": disease_info.get("organic_remedies", []),
            "chemical": disease_info.get("chemical_treatments", []),
            "prevention": disease_info.get("prevention", [])
        },
        "class_probabilities": probabilities,
        "is_mock": False
    }

