import time
import numpy as np
from models.model_loader import load_plant_model
from data.mock_predictions import get_mock_prediction
from data.disease_library import DISEASE_KNOWLEDGE_BASE

APPLE_CLASSES = [Apple Scab, Black Rot, Cedar Apple Rust, Healthy]

def predict_apple(tensor_input: np.ndarray, original_filename: str = ") -> dict:
 "
 Inference handler for Apple Model.
 Input: Normalized NumPy array with shape (1, 224, 224, 3).
 Output: Standardized prediction dictionary.
 "
 model = load_plant_model(apple)
 
 if model is None:
 time.sleep(0.4)
 return get_mock_prediction(apple, original_filename)

 start_time = time.time()
 raw_predictions = model.predict(tensor_input)
 inference_time = (time.time() - start_time) * 1000

 predicted_idx = int(np.argmax(raw_predictions[0]))
 predicted_disease = APPLE_CLASSES[predicted_idx]
 confidence = float(raw_predictions[0][predicted_idx])

 probs = {cls_name: round(float(prob), 4) for cls_name, prob in zip(APPLE_CLASSES, raw_predictions[0])}
 disease_info = DISEASE_KNOWLEDGE_BASE[apple][predicted_disease]

 return {
 plant_id: apple,
 plant_name: Apple,
 scientific_name: Malus domestica,
 predicted_disease: predicted_disease,
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
 inference_time_ms: round(inference_time, 1),
 is_mock: False
 }
