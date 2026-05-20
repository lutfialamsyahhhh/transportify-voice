# Dataset Recording Guide

Create one folder per Indonesian transportation word. Each folder should contain 20 WAV recordings.

Required audio format:

- `.wav`
- mono
- 16 kHz
- 1-2 seconds

Target words included in this starter:

- mobil
- motor
- bus
- kereta
- kapal
- pesawat
- sepeda
- halte
- terminal
- bandara

Example:

```text
dataset/
├── mobil/
│   ├── mobil_1.wav
│   ├── mobil_2.wav
│   └── mobil_20.wav
└── motor/
    ├── motor_1.wav
    └── motor_20.wav
```

TODO: add real recorded dataset files before running `python train_model.py`.
