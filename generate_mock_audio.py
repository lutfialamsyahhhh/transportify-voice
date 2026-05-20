import argparse
from pathlib import Path

import numpy as np
from scipy.io import wavfile

from app.asr.constants import DEFAULT_SAMPLE_RATE, TRANSPORT_WORDS
from app.config import Config


BASE_FREQUENCIES = {
    "mobil": 220,
    "motor": 260,
    "bus": 300,
    "kereta": 340,
    "kapal": 380,
    "pesawat": 420,
    "sepeda": 460,
    "halte": 500,
    "terminal": 540,
    "bandara": 580,
}


def generate_mock_audio(output_dir=Config.GENERATED_DIR / "mock_audio", duration=1.4):
    """Generate synthetic WAV clips for UI/API smoke tests, not model training."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    sample_count = int(DEFAULT_SAMPLE_RATE * duration)
    time_axis = np.linspace(0, duration, sample_count, endpoint=False)
    generated_files = []

    for index, word in enumerate(TRANSPORT_WORDS):
        frequency = BASE_FREQUENCIES[word]
        envelope = np.linspace(0.2, 1.0, sample_count)
        tone = 0.22 * np.sin(2 * np.pi * frequency * time_axis)
        harmonic = 0.06 * np.sin(2 * np.pi * (frequency * 1.5) * time_axis)
        pulse = 0.03 * np.sin(2 * np.pi * (3 + index) * time_axis)
        signal = (tone + harmonic + pulse) * envelope
        pcm = np.clip(signal * 32767, -32768, 32767).astype(np.int16)

        path = output_dir / f"{word}_mock.wav"
        wavfile.write(path, DEFAULT_SAMPLE_RATE, pcm)
        generated_files.append(path)

    return generated_files


def parse_args():
    parser = argparse.ArgumentParser(description="Generate synthetic mock WAV files.")
    parser.add_argument(
        "--output",
        default=str(Config.GENERATED_DIR / "mock_audio"),
        help="Output directory for generated mock WAV files",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    files = generate_mock_audio(args.output)
    print(f"Generated {len(files)} mock WAV files in {args.output}")
