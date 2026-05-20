import numpy as np

from app.asr.constants import DEFAULT_SAMPLE_RATE, N_MFCC, TRANSPORT_WORDS
from app.asr.features import extract_features_from_signal
from app.asr.model import ASRModelManager
from app.tts.synthesizer import SPEED_CONFIG, VOICE_CONFIG
from preprocess import scan_dataset_structure


def test_mfcc_feature_shape():
    duration = 2.0
    t = np.linspace(0, duration, int(DEFAULT_SAMPLE_RATE * duration), endpoint=False)
    signal = 0.25 * np.sin(2 * np.pi * 440 * t)
    features, mfcc = extract_features_from_signal(signal, sample_rate=DEFAULT_SAMPLE_RATE)

    assert features.shape == (N_MFCC * 3 * 4,)
    assert mfcc.shape[0] == N_MFCC


def test_demo_fallback_prediction(tmp_path):
    manager = ASRModelManager(tmp_path / "missing.joblib", labels=TRANSPORT_WORDS)
    result = manager.predict(np.zeros(N_MFCC * 3 * 4, dtype=np.float32))

    assert result["demo"] is True
    assert result["label"] in TRANSPORT_WORDS
    assert result["model_status"] == "demo_fallback"


def test_dataset_scan_empty_structure(tmp_path):
    for word in TRANSPORT_WORDS:
        (tmp_path / word).mkdir()

    summary = scan_dataset_structure(tmp_path, labels=TRANSPORT_WORDS)
    assert summary["actual_total"] == 0
    assert summary["expected_total"] == len(TRANSPORT_WORDS) * 20


def test_tts_voice_and_speed_profiles_are_real_edge_profiles():
    assert VOICE_CONFIG["male"]["voice_id"] == "id-ID-ArdiNeural"
    assert VOICE_CONFIG["male"]["sapi_voice"] == "Microsoft David Desktop"
    assert VOICE_CONFIG["female"]["voice_id"] == "id-ID-GadisNeural"
    assert SPEED_CONFIG["slow"]["edge_rate"] == "-35%"
    assert SPEED_CONFIG["normal"]["edge_rate"] == "+0%"
    assert SPEED_CONFIG["fast"]["edge_rate"] == "+80%"
    assert SPEED_CONFIG["fast"]["sapi_rate"] == 8
