import random
from typing import Dict, Any
from data.disease_library import DISEASE_KNOWLEDGE_BASE
import config

def get_mock_prediction(plant_id: str, image_hint: str = "") -> Dict[str, Any]:
    plant_info = config.PLANTS.get(plant_id, config.PLANTS["tomato"])
    disease_classes = plant_info["classes"]
    plant_diseases = DISEASE_KNOWLEDGE_BASE.get(plant_id, {})

    # Determine condition from hint or sample
    hint_lower = image_hint.lower()
    selected_disease = None

    if "early_blight" in hint_lower or "early blight" in hint_lower:
        selected_disease = "Early Blight" if "Early Blight" in disease_classes else disease_classes[0]
    elif "late_blight" in hint_lower or "late blight" in hint_lower:
        selected_disease = "Late Blight" if "Late Blight" in disease_classes else disease_classes[0]
    elif "healthy" in hint_lower:
        selected_disease = "Healthy" if "Healthy" in disease_classes else disease_classes[-1]
    elif "scab" in hint_lower:
        selected_disease = "Apple Scab" if "Apple Scab" in disease_classes else disease_classes[0]
    elif "black_rot" in hint_lower or "black rot" in hint_lower:
        selected_disease = "Black Rot" if "Black Rot" in disease_classes else disease_classes[0]
    elif "rust" in hint_lower:
        selected_disease = "Cedar Apple Rust" if "Cedar Apple Rust" in disease_classes else disease_classes[0]
    elif "septoria" in hint_lower:
        selected_disease = "Septoria Leaf Spot" if "Septoria Leaf Spot" in disease_classes else disease_classes[0]
    else:
        selected_disease = random.choice(disease_classes)

    # Realistic Confidence score between 91.5% and 98.8%
    confidence = round(random.uniform(0.915, 0.988), 4)
    remaining = round(1.0 - confidence, 4)

    # Generate synthetic softmax distribution
    other_classes = [c for c in disease_classes if c != selected_disease]
    probabilities = {selected_disease: confidence}

    if other_classes:
        raw_weights = [random.random() for _ in other_classes]
        total_w = sum(raw_weights)
        for idx, cls_name in enumerate(other_classes):
            probabilities[cls_name] = round((raw_weights[idx] / total_w) * remaining, 4)

    disease_info = plant_diseases.get(selected_disease, {
        "scientific_name": "Unknown",
        "pathogen": "Unknown",
        "severity": "Moderate",
        "is_healthy": False,
        "description": "Plant pathology metadata unavailable.",
        "causes": "Environmental factors.",
        "symptoms": ["Leaf spotting and discoloration"],
        "organic_remedies": ["Apply standard organic bio-fungicide"],
        "chemical_treatments": ["Apply standard broad-spectrum fungicide"],
        "prevention": ["Maintain balanced crop nutrition"]
    })

    return {
        "plant_id": plant_id,
        "plant_name": plant_info["name"],
        "scientific_name": plant_info["scientific_name"],
        "predicted_disease": selected_disease,
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
        "inference_time_ms": random.randint(32, 58),
        "is_mock": True
    }

