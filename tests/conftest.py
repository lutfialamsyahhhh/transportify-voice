import pytest

from app import create_app
from app.config import TestingConfig


@pytest.fixture()
def app(tmp_path):
    class TestConfig(TestingConfig):
        GENERATED_DIR = tmp_path / "generated"
        GENERATED_AUDIO_DIR = GENERATED_DIR / "audio"
        GENERATED_VISUALIZATION_DIR = GENERATED_DIR / "visualizations"
        UPLOAD_DIR = GENERATED_DIR / "uploads"
        MODEL_DIR = tmp_path / "models"
        ASR_MODEL_PATH = MODEL_DIR / "missing_model.joblib"
        DATASET_DIR = tmp_path / "dataset"

    return create_app(TestConfig)


@pytest.fixture()
def client(app):
    return app.test_client()
