from pathlib import Path
from uuid import uuid4

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np


def generate_visualizations(signal, sample_rate, mfcc, output_dir):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    waveform_path = output_dir / f"waveform_{uuid4().hex}.png"
    mfcc_path = output_dir / f"mfcc_{uuid4().hex}.png"

    _save_waveform(signal, sample_rate, waveform_path)
    _save_mfcc_heatmap(mfcc, mfcc_path)

    return {
        "waveform_url": _static_generated_url(waveform_path),
        "mfcc_url": _static_generated_url(mfcc_path),
    }


def _save_waveform(signal, sample_rate, output_path):
    time_axis = np.arange(len(signal)) / float(sample_rate)
    plt.figure(figsize=(9, 3), dpi=120)
    plt.plot(time_axis, signal, color="#22d3ee", linewidth=1)
    plt.fill_between(time_axis, signal, 0, color="#0891b2", alpha=0.22)
    plt.title("Waveform Preview", color="#e5faff")
    plt.xlabel("Time (s)", color="#9ca3af")
    plt.ylabel("Amplitude", color="#9ca3af")
    _style_plot()
    plt.tight_layout()
    plt.savefig(output_path, transparent=True)
    plt.close()


def _save_mfcc_heatmap(mfcc, output_path):
    plt.figure(figsize=(9, 3), dpi=120)
    plt.imshow(mfcc, aspect="auto", origin="lower", cmap="magma")
    plt.colorbar(label="MFCC")
    plt.title("MFCC Heatmap", color="#e5faff")
    plt.xlabel("Frame", color="#9ca3af")
    plt.ylabel("Coefficient", color="#9ca3af")
    _style_plot()
    plt.tight_layout()
    plt.savefig(output_path, transparent=True)
    plt.close()


def _style_plot():
    ax = plt.gca()
    ax.set_facecolor("#071018")
    ax.tick_params(colors="#9ca3af")
    for spine in ax.spines.values():
        spine.set_color("#164e63")
    plt.gcf().patch.set_alpha(0)


def _static_generated_url(path):
    path = Path(path)
    return f"/static/generated/visualizations/{path.name}"
