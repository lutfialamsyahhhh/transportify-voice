import argparse
from pathlib import Path

from app.asr.constants import DEFAULT_AUDIO_DURATION_SECONDS, DEFAULT_SAMPLE_RATE, TRANSPORT_WORDS
from app.asr.features import extract_feature_vector
from app.asr.model import ASRModelManager
from app.config import Config


def predict_file(audio_path, model_path=Config.ASR_MODEL_PATH):
    feature_vector, _, _, _ = extract_feature_vector(
        audio_path=audio_path,
        sample_rate=DEFAULT_SAMPLE_RATE,
        duration_seconds=DEFAULT_AUDIO_DURATION_SECONDS,
    )
    manager = ASRModelManager(model_path=model_path, labels=TRANSPORT_WORDS)
    return manager.predict(feature_vector)


def parse_args():
    parser = argparse.ArgumentParser(description="Predict one transportation word from a WAV file.")
    parser.add_argument("audio", help="Path to WAV audio file")
    parser.add_argument("--model", default=str(Config.ASR_MODEL_PATH), help="Model artifact path")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    result = predict_file(Path(args.audio), model_path=args.model)
    print(f"Prediction: {result['label']}")
    print(f"Confidence: {result['confidence']:.4f}")
    print(f"Model status: {result['model_status']}")
