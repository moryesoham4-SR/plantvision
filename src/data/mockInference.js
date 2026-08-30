import { DISEASE_DATABASE } from ./diseaseData;

export function simulateInference(plantId, imageHint = ") {
 const plantKey = plantId.toLowerCase();
 const available = DISEASE_DATABASE[plantKey] || DISEASE_DATABASE[tomato];
 const diseaseKeys = Object.keys(available);

 let selectedDisease = null;
 const lowerHint = (imageHint || ).toLowerCase();

 if (lowerHint.includes(early_blight) || lowerHint.includes(early blight)) {
 selectedDisease = diseaseKeys.includes(Early Blight) ? Early Blight : diseaseKeys[0];
 } else if (lowerHint.includes(late_blight) || lowerHint.includes(late blight)) {
 selectedDisease = diseaseKeys.includes(Late Blight) ? Late Blight : diseaseKeys[0];
 } else if (lowerHint.includes(healthy)) {
 selectedDisease = Healthy;
 } else if (lowerHint.includes(scab)) {
 selectedDisease = diseaseKeys.includes(Apple Scab) ? Apple Scab : diseaseKeys[0];
 } else if (lowerHint.includes(black_rot) || lowerHint.includes(black rot)) {
 selectedDisease = diseaseKeys.includes(Black Rot) ? Black Rot : diseaseKeys[0];
 } else if (lowerHint.includes(rust)) {
 selectedDisease = diseaseKeys.includes(Cedar Apple Rust) ? Cedar Apple Rust : diseaseKeys[0];
 } else if (lowerHint.includes(septoria)) {
 selectedDisease = diseaseKeys.includes(Septoria Leaf Spot) ? Septoria Leaf Spot : diseaseKeys[0];
 } else {
 // Default random choice
 selectedDisease = diseaseKeys[Math.floor(Math.random() * diseaseKeys.length)];
 }

 // Realistic confidence (92.4% - 98.6%)
 const confidence = Number((0.92 + Math.random() * 0.065).toFixed(4));
 const remaining = Number((1.0 - confidence).toFixed(4));

 const otherDiseases = diseaseKeys.filter(d => d !== selectedDisease);
 const probabilities = { [selectedDisease]: confidence };

 if (otherDiseases.length > 0) {
 const rawShares = otherDiseases.map(() => Math.random());
 const sumShares = rawShares.reduce((a, b) => a + b, 0);
 otherDiseases.forEach((d, idx) => {
 probabilities[d] = Number(((rawShares[idx] / sumShares) * remaining).toFixed(4));
 });
 }

 const diseaseInfo = available[selectedDisease];

 return {
 plantId: plantKey,
 predictedDisease: selectedDisease,
 pathogen: diseaseInfo.pathogen,
 confidence: confidence,
 confidencePercent: ${(confidence * 100).toFixed(1)}%,
 isHealthy: diseaseInfo.isHealthy,
 severity: diseaseInfo.severity,
 description: diseaseInfo.description,
 causes: diseaseInfo.causes,
 symptoms: diseaseInfo.symptoms,
 remedies: diseaseInfo.remedies,
 probabilities: probabilities,
 inferenceTimeMs: Math.floor(35 + Math.random() * 25),
 isMock: true
 };
}
