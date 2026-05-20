from flask import current_app

from app.asr.features import extract_feature_vector
from app.asr.model import ASRModelManager
from app.asr.visualization import generate_visualizations


def predict_audio(audio_path):
    sample_rate = current_app.config["SAMPLE_RATE"]
    duration_seconds = current_app.config["AUDIO_DURATION_SECONDS"]

    feature_vector, mfcc, signal, sr = extract_feature_vector(
        audio_path,
        sample_rate=sample_rate,
        duration_seconds=duration_seconds,
    )

    model_manager = ASRModelManager(
        model_path=current_app.config["ASR_MODEL_PATH"],
        labels=current_app.config["TRANSPORT_WORDS"],
    )
    prediction = model_manager.predict(feature_vector)
    visualizations = generate_visualizations(
        signal=signal,
        sample_rate=sr,
        mfcc=mfcc,
        output_dir=current_app.config["GENERATED_VISUALIZATION_DIR"],
    )

    return {
        **prediction,
        **visualizations,
        "sample_rate": sr,
        "duration_seconds": duration_seconds,
        "recognized_scope": current_app.config["TRANSPORT_WORDS"],
    }
