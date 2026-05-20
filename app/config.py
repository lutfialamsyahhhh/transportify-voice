import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "transportify-dev-secret")
    DEBUG = os.getenv("FLASK_DEBUG", "0") == "1"
    TESTING = False

    MAX_CONTENT_LENGTH = int(os.getenv("MAX_CONTENT_LENGTH", 12 * 1024 * 1024))

    APP_DIR = BASE_DIR / "app"
    STATIC_DIR = APP_DIR / "static"
    GENERATED_DIR = STATIC_DIR / "generated"
    GENERATED_AUDIO_DIR = GENERATED_DIR / "audio"
    GENERATED_VISUALIZATION_DIR = GENERATED_DIR / "visualizations"
    UPLOAD_DIR = GENERATED_DIR / "uploads"

    DATASET_DIR = BASE_DIR / "dataset"
    MODEL_DIR = BASE_DIR / "app" / "models"
    ASR_MODEL_PATH = MODEL_DIR / "asr_model.joblib"

    SAMPLE_RATE = int(os.getenv("SAMPLE_RATE", 16000))
    AUDIO_DURATION_SECONDS = float(os.getenv("AUDIO_DURATION_SECONDS", 2.0))
    HISTORY_LIMIT = int(os.getenv("HISTORY_LIMIT", 30))

    TRANSPORT_WORDS = [
        "mobil",
        "motor",
        "bus",
        "kereta",
        "kapal",
        "pesawat",
        "sepeda",
        "halte",
        "terminal",
        "bandara",
    ]


class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
