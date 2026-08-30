import random
import time
from data.disease_library import DISEASE_KNOWLEDGE_BASE
from config import PLANTS

def get_mock_prediction(plant_id: str, image_name: str = ") -> dict:
 "
 Simulates CNN / Deep Learning inference for Potato, Tomato, and Apple models.
 Deterministic based on filename if sample name is provided, else intelligent mock.
 "
 plant_key = plant_id.lower()
 if plant_key not in DISEASE_KNOWLEDGE_BASE:
 plant_key = tomato

 available_diseases = list(DISEASE_KNOWLEDGE_BASE[plant_key].keys())
 
 # Check if filename hints at the disease (e.g., from sample picker)
 selected_disease = None
 lower_name = image_name.lower()
 
 if early_blight in lower_name or early blight in lower_name:
 selected_disease = Early Blight if Early Blight in available_diseases else available_diseases[0]
 elif late_blight in lower_name or late blight in lower_name:
 selected_disease = Late Blight if Late Blight in available_diseases else available_diseases[0]
 elif healthy in lower_name:
 selected_disease = Healthy
 elif scab in lower_name:
 selected_disease = Apple Scab if Apple Scab in available_diseases else available_diseases[0]
 elif black_rot in lower_name or black rot in lower_name:
 selected_disease = Black Rot if Black Rot in available_diseases else available_diseases[0]
 elif rust in lower_name or cedar in lower_name:
 selected_disease = Cedar Apple Rust if Cedar Apple Rust in available_diseases else available_diseases[0]
 elif septoria in lower_name:
 selected_disease = Septoria Leaf Spot if Septoria Leaf Spot in available_diseases else available_diseases[0]
 else:
 # Default weighted random selection (70% diseased, 30% healthy)
 weights = [0.35 if d != Healthy else 0.30 for d in available_diseases]
 selected_disease = random.choices(available_diseases, weights=weights, k=1)[0]

 # Generate confidence score (typically 91% to 98.8%)
 confidence = round(random.uniform(0.925, 0.988), 4)

 # Build probability distribution for all classes for chart visualization
 remaining_prob = 1.0 - confidence
 other_classes = [d for d in available_diseases if d != selected_disease]
 
 probs = {selected_disease: confidence}
 if other_classes:
 sub_probs = [random.random() for _ in other_classes]
 total_sub = sum(sub_probs)
 for cls_name, p in zip(other_classes, sub_probs):
 probs[cls_name] = round((p / total_sub) * remaining_prob, 4)

 # Retrieve rich knowledge details
 disease_info = DISEASE_KNOWLEDGE_BASE[plant_key][selected_disease]

 return {
 plant_id: plant_key,
 plant_name: PLANTS[plant_key][name],
 scientific_name: PLANTS[plant_key][scientific_name],
 predicted_disease: selected_disease,
 pathogen: disease_info[scientific_name],
 confidence: confidence,
 confidence_percent: f{confidence * 100:.1f}%,
 is_healthy: disease_info[is_healthy],
 severity: disease_info[severity],
 description: disease_info[description],
 causes: disease_info[causes],
 symptoms: disease_info[symptoms],
 remedies: {
 organic: disease_info[organic_remedies],
 chemical: disease_info[chemical_treatments],
 prevention: disease_info[prevention]
 },
 class_probabilities: probs,
 inference_time_ms: round(random.uniform(32, 68), 1),
 is_mock: True
 }
