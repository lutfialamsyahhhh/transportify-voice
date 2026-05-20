from pathlib import Path

import librosa
import numpy as np


def load_audio(
    audio_path: Path,
    sample_rate: int = 16000,
    duration_seconds: float = 2.0,
):
    """Load audio as mono, resample, trim silence, and fix length."""
    if not Path(audio_path).exists():
        raise ValueError(f"Audio file not found: {audio_path}")

    signal, sr = librosa.load(audio_path, sr=sample_rate, mono=True)
    if signal.size == 0:
        raise ValueError("Audio file does not contain readable signal data.")

    signal, _ = librosa.effects.trim(signal, top_db=30)
    target_length = int(sample_rate * duration_seconds)

    if signal.size < target_length:
        signal = np.pad(signal, (0, target_length - signal.size), mode="constant")
    else:
        signal = signal[:target_length]

    return signal.astype(np.float32), sr
