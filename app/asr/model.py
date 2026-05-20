from pathlib import Path

import joblib
import numpy as np

from app.asr.constants import TRANSPORT_WORDS


class ASRModelManager:
    def __init__(self, model_path, labels=None):
        self.model_path = Path(model_path)
        self.labels = labels or TRANSPORT_WORDS
        self.artifact = None
        self._load()

    @property
    def is_trained(self):
        return self.artifact is not None

    def _load(self):
        if self.model_path.exists():
            self.artifact = joblib.load(self.model_path)

    def predict(self, feature_vector):
        if not self.is_trained:
            return self._demo_predict(feature_vector)

        scaler = self.artifact["scaler"]
        model = self.artifact["model"]
        encoder = self.artifact["label_encoder"]

        features = np.asarray(feature_vector, dtype=np.float32).reshape(1, -1)
        scaled = scaler.transform(features)
        probabilities = model.predict_proba(scaled)[0]
        best_index = int(np.argmax(probabilities))
        label = encoder.inverse_transform([best_index])[0]

        probability_map = {
            label_name: round(float(probability), 4)
            for label_name, probability in zip(encoder.classes_, probabilities)
        }

        return {
            "label": label,
            "confidence": round(float(probabilities[best_index]), 4),
            "probabilities": probability_map,
            "demo": False,
            "model_status": "trained",
        }

    def _demo_predict(self, feature_vector):
        values = np.asarray(feature_vector, dtype=np.float32)
        energy_signature = int(abs(float(np.sum(values))) * 1000)
        index = energy_signature % len(self.labels)
        confidence = 0.72 + ((energy_signature % 18) / 100)
        label = self.labels[index]

        remainder = max(0.0, 1.0 - confidence)
        other_probability = remainder / max(1, len(self.labels) - 1)
        probabilities = {
            word: round(other_probability, 4)
            for word in self.labels
        }
        probabilities[label] = round(confidence, 4)

        return {
            "label": label,
            "confidence": round(confidence, 4),
            "probabilities": probabilities,
            "demo": True,
            "model_status": "demo_fallback",
        }
