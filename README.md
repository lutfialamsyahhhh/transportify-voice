# 🎤 Transportify Voice

> Production-style Flask web application untuk Indonesian transportation vocabulary speech recognition dengan ASR manual (MFCC + SVM) dan TTS terintegrasi.

Transportify Voice adalah aplikasi web untuk pengenalan suara transportasi Indonesia yang menggabungkan **manual ASR pipeline** (tanpa Whisper atau cloud API) dengan **text-to-speech generation** menggunakan Edge TTS.

**Kata-kata target:** `mobil`, `motor`, `bus`, `kereta`, `kapal`, `pesawat`, `sepeda`, `halte`, `terminal`, `bandara` (10 kelas).

---

## ✨ Fitur Utama

### 🎨 **Frontend & UI**

- Dark AI dashboard dengan Bootstrap 5
- Responsive design dengan custom CSS
- Browser microphone recording (real-time)
- WAV file upload dengan preview
- Waveform visualization
- MFCC heatmap display
- Confidence score dan probability list
- Prediction history (30 terakhir)
- Audio player dengan player controls
- Loading animations dan alert notifications

### 🤖 **ASR Pipeline (Speech Recognition)**

- Manual MFCC feature extraction (librosa)
- SVM classification (scikit-learn)
- Audio preprocessing:
  - Audio loading dan mono resampling ke 16 kHz
  - Auto trim/pad ke durasi target (2 detik)
  - Feature normalization
  - Label encoding
- Model persistence dengan joblib
- Demo fallback saat model belum ada (dapat langsung dijalankan)

### 🗣️ **TTS (Text-to-Speech)**

- Indonesian TTS via Edge TTS
- Voice options: `id-ID-ArdiNeural` (pria) & `id-ID-GadisNeural` (wanita)
- Speed control: `slow`, `normal`, `fast`
- ASR-to-TTS integration: misal "Anda mengatakan kereta"
- Fallback graceful saat internet offline

### 🔌 **Teknologi**

- Backend: Flask 3.0.3
- Audio processing: librosa 0.10.2, scipy
- ML: scikit-learn (SVM), numpy
- Visualization: matplotlib
- Web framework: Werkzeug 3.0.3
- Testing: pytest 8.2.2

---

## 📁 Struktur Project

```
transportify-voice/
├── app/                                    # Main Flask application
│   ├── __init__.py                        # App factory & error handlers
│   ├── config.py                          # Configuration (Config, TestingConfig)
│   │
│   ├── asr/                               # Speech Recognition Pipeline
│   │   ├── __init__.py
│   │   ├── audio.py                       # Audio loading & preprocessing
│   │   ├── features.py                    # MFCC extraction & normalization
│   │   ├── model.py                       # SVM model management & prediction
│   │   ├── constants.py                   # ASR constants & defaults
│   │   ├── pipeline.py                    # End-to-end prediction workflow
│   │   └── visualization.py               # Waveform & heatmap generation
│   │
│   ├── tts/                               # Text-to-Speech
│   │   ├── __init__.py
│   │   └── synthesizer.py                 # Edge TTS integration
│   │
│   ├── routes/                            # API Endpoints & Pages
│   │   ├── __init__.py                    # Blueprint registration
│   │   ├── pages.py                       # HTML page routes (GET /)
│   │   ├── asr_api.py                     # ASR API (POST /api/asr/*)
│   │   ├── tts_api.py                     # TTS API (POST /api/tts/*)
│   │   └── integration_api.py             # Integrated ASR+TTS API
│   │
│   ├── services/                          # Business Logic
│   │   ├── __init__.py
│   │   ├── file_service.py                # File upload & management
│   │   └── history_service.py             # Prediction history storage
│   │
│   ├── utils/                             # Utility Functions
│   │   ├── __init__.py
│   │   ├── logging.py                     # Logging configuration
│   │   ├── responses.py                   # Standard API response wrapper
│   │   └── storage.py                     # Directory & file utilities
│   │
│   ├── models/                            # Trained Models (Git LFS)
│   │   ├── asr_model.joblib              # Trained SVM model
│   │   └── features.joblib               # Extracted MFCC features
│   │
│   ├── static/                            # Frontend Assets
│   │   ├── css/
│   │   │   └── styles.css                # Custom dark theme styling
│   │   ├── js/
│   │   │   ├── main.js                   # Main app initialization
│   │   │   ├── asr.js                    # ASR UI & microphone handling
│   │   │   └── tts.js                    # TTS UI & audio control
│   │   ├── img/                          # Logo & assets
│   │   └── generated/                    # Runtime outputs (ignored in git)
│   │       ├── audio/                    # Generated TTS audio
│   │       ├── uploads/                  # User uploaded files
│   │       ├── visualizations/           # Waveform & heatmap images
│   │       ├── mock_audio/               # Demo audio samples
│   │       └── logs/                     # Application logs
│   │
│   └── templates/                         # HTML Templates
│       ├── base.html                     # Base template (navbar, footer)
│       ├── home.html                     # Home page
│       ├── asr.html                      # ASR interface
│       ├── tts.html                      # TTS interface
│       ├── about.html                    # About page
│       ├── 404.html                      # 404 error page
│       └── 500.html                      # 500 error page
│
├── dataset/                               # Training Dataset (Not in Git LFS)
│   ├── README.md                         # Dataset guidelines
│   ├── mobil/                            # Transport word folders
│   ├── motor/
│   ├── bus/
│   ├── kereta/
│   ├── kapal/
│   ├── pesawat/
│   ├── sepeda/
│   ├── halte/
│   ├── terminal/
│   └── bandara/
│
├── tests/                                 # Unit & Integration Tests
│   ├── conftest.py                       # Pytest fixtures & setup
│   ├── test_app.py                       # App initialization tests
│   ├── test_asr.py                       # ASR pipeline tests
│   └── __pycache__/
│
├── notebooks/                             # Jupyter Notebooks
│   └── README.md                         # Notebook guidelines
│
├── Root Scripts                           # Data Preparation & Training
│   ├── preprocess.py                     # Dataset validation & checking
│   ├── extract_features.py               # MFCC feature extraction
│   ├── train_model.py                    # SVM model training
│   ├── predict.py                        # Single-file prediction
│   ├── generate_mock_audio.py            # Demo audio generation
│   ├── test_gtts.py                      # gTTS testing script
│   └── run.py                            # Flask application entry point
│
├── pytest.ini                             # Pytest configuration
├── requirements.txt                       # Python dependencies
└── README.md                              # This file
```

### 📝 File-File Penting

| File                                       | Fungsi                            |
| ------------------------------------------ | --------------------------------- |
| [run.py](run.py)                           | Entry point Flask app (port 5000) |
| [app/config.py](app/config.py)             | Environment & configuration       |
| [preprocess.py](preprocess.py)             | Validasi dataset WAV              |
| [extract_features.py](extract_features.py) | Extract MFCC features → joblib    |
| [train_model.py](train_model.py)           | Train SVM model → joblib          |
| [predict.py](predict.py)                   | Predict single WAV file           |
| [app/asr/pipeline.py](app/asr/pipeline.py) | ASR prediction workflow           |
| [requirements.txt](requirements.txt)       | Python dependencies               |
| [pytest.ini](pytest.ini)                   | Pytest configuration              |

---

## 🔄 Workflow Pipeline

```
┌─────────────────────────────────────────────────────────┐
│ 1. DATASET PREPARATION                                  │
├─────────────────────────────────────────────────────────┤
│ Collect WAV files → dataset/[kata]/[kata]_N.wav        │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│ 2. DATA VALIDATION                                      │
├─────────────────────────────────────────────────────────┤
│ python preprocess.py                                    │
│ ✓ Check format (WAV, mono, 16kHz)                      │
│ ✓ Check duration (1-2s)                                │
│ ✓ Generate summary stats                               │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│ 3. FEATURE EXTRACTION (MFCC)                            │
├─────────────────────────────────────────────────────────┤
│ python extract_features.py --output app/models/...    │
│ → app/models/features.joblib                           │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│ 4. MODEL TRAINING (SVM)                                 │
├─────────────────────────────────────────────────────────┤
│ python train_model.py                                   │
│ → app/models/asr_model.joblib                          │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│ 5. RUN FLASK APPLICATION                                │
├─────────────────────────────────────────────────────────┤
│ python run.py                                           │
│ → http://127.0.0.1:5000 ✓                              │
└─────────────────────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│ 6. REAL-TIME INFERENCE                                  │
├─────────────────────────────────────────────────────────┤
│ User upload/record WAV                                  │
│ → Audio preprocessing (16kHz, 2s, mono)                │
│ → MFCC extraction & normalization                      │
│ → SVM prediction (confidence + probabilities)          │
│ → Optional: TTS response generation                    │
└─────────────────────────────────────────────────────────┘
```

---

## 📦 Dependencies

### Core Libraries

| Package          | Version      | Fungsi                |
| ---------------- | ------------ | --------------------- |
| **Flask**        | 3.0.3        | Web framework         |
| **Werkzeug**     | 3.0.3        | WSGI utilities        |
| **librosa**      | 0.10.2.post1 | Audio analysis & MFCC |
| **numpy**        | 1.26.4       | Numerical computation |
| **scipy**        | 1.13.1       | Scientific computing  |
| **scikit-learn** | 1.5.1        | SVM classifier        |
| **matplotlib**   | 3.8.4        | Visualization         |
| **joblib**       | 1.4.2        | Model serialization   |

### Audio & TTS

| Package         | Version | Fungsi                           |
| --------------- | ------- | -------------------------------- |
| **pydub**       | 0.25.1  | Audio format conversion          |
| **sounddevice** | 0.4.7   | Audio device access              |
| **gTTS**        | 2.5.2   | Google Text-to-Speech (fallback) |
| **edge-tts**    | 7.2.8   | Microsoft Edge TTS               |

### Development

| Package    | Version | Fungsi            |
| ---------- | ------- | ----------------- |
| **pytest** | 8.2.2   | Testing framework |

---

## 🚀 Installation & Setup

### 1️⃣ Prerequisites

- Python 3.8+ (recommended 3.10+)
- pip & virtualenv
- FFmpeg (untuk pydub audio conversion)
- Microphone (untuk recording)

### 2️⃣ Clone Repository

```bash
git clone https://github.com/yourusername/transportify-voice.git
cd transportify-voice
```

### 3️⃣ Virtual Environment

**Windows (PowerShell):**

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

**macOS/Linux:**

```bash
python -m venv venv
source venv/bin/activate
```

### 4️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 5️⃣ Run Application

```bash
python run.py
```

**Aplikasi siap di:** `http://127.0.0.1:5000`

> ⚠️ **Demo Mode:** Aplikasi dapat langsung dijalankan meski model belum dilatih. Akan menggunakan demo fallback untuk testing.

---

## 📊 Dataset Preparation

### Struktur Dataset

```
dataset/
├── mobil/
│   ├── mobil_1.wav
│   ├── mobil_2.wav
│   └── ... (min 20 files)
├── motor/
├── bus/
├── kereta/
├── kapal/
├── pesawat/
├── sepeda/
├── halte/
├── terminal/
└── bandara/
```

### Spesifikasi Recording

| Kriteria         | Nilai                  |
| ---------------- | ---------------------- |
| Format           | WAV                    |
| Channels         | Mono (1 channel)       |
| Sample Rate      | 16 kHz                 |
| Duration         | 1-2 detik per file     |
| Bit Depth        | 16-bit                 |
| Files per kata   | Min 20, ideal 30-50    |
| Total files      | Min 200, ideal 300-500 |
| Background noise | Konsisten antar kelas  |

### Best Practices

- 📝 Bersihkan background noise (quiet room)
- 🎤 Gunakan microphone berkualitas
- 🗣️ Ucapkan dengan jelas dan natural
- 📈 Variasi intonasi dan kecepatan
- ⏱️ Jangan terlalu cepat atau lambat
- ✅ Review file yang corrupt/noise

---

## 🔧 Model Training

### Step 1: Validasi Dataset

```bash
python preprocess.py
```

**Output:**

- ✓ Dataset summary (total files, duration)
- ✓ Class distribution
- ✓ Format validation (WAV, 16kHz, mono)
- ✓ Duration check (1-2s)

### Step 2: Extract MFCC Features

```bash
python extract_features.py --output app/models/features.joblib
```

**Output:**

- `app/models/features.joblib` (feature vectors)
- Feature shape & statistics
- Normalization parameters

**Options:**

```bash
python extract_features.py \
    --dataset dataset/ \
    --output app/models/features.joblib \
    --sample-rate 16000 \
    --n-mfcc 13
```

### Step 3: Train SVM Model

```bash
python train_model.py
```

**Output:**

- `app/models/asr_model.joblib` (trained SVM)
- Training metrics (accuracy, precision, recall, F1)
- Cross-validation scores
- Training time

**Options:**

```bash
python train_model.py \
    --features app/models/features.joblib \
    --output app/models/asr_model.joblib \
    --kernel rbf \
    --C 100
```

### Step 4: Test Prediction

```bash
python predict.py dataset/mobil/mobil_1.wav
```

**Output:**

```
Predicted: mobil
Confidence: 0.95
Probabilities: {'mobil': 0.95, 'motor': 0.04, ...}
```

---

## 🌐 API Endpoints

### ASR (Speech Recognition)

#### `POST /api/asr/predict`

Upload WAV file untuk prediksi

- **Content-Type:** `multipart/form-data`
- **Parameter:** `audio` (file WAV)

**Response:**

```json
{
  "success": true,
  "prediction": "kereta",
  "confidence": 0.97,
  "probabilities": {
    "kereta": 0.97,
    "motor": 0.02,
    "mobil": 0.01
  },
  "is_demo": false,
  "waveform_url": "/static/generated/visualizations/waveform_12345.png",
  "mfcc_url": "/static/generated/visualizations/mfcc_12345.png",
  "message": "Prediction successful"
}
```

#### `GET /api/asr/history`

Ambil history prediksi terakhir

- **Query params:** `limit=30` (default)

**Response:**

```json
{
  "success": true,
  "history": [
    {
      "timestamp": "2024-05-20T10:30:45",
      "prediction": "kereta",
      "confidence": 0.97
    }
  ],
  "count": 30
}
```

### TTS (Text-to-Speech)

#### `POST /api/tts/generate`

Generate speech dari text

**Request:**

```json
{
  "text": "Halo, ini adalah contoh text-to-speech",
  "voice": "id-ID-ArdiNeural",
  "speed": "normal"
}
```

**Options:**

- `voice`: `id-ID-ArdiNeural` (pria) atau `id-ID-GadisNeural` (wanita)
- `speed`: `slow`, `normal`, `fast`

**Response:**

```json
{
  "success": true,
  "audio_url": "/static/generated/audio/tts_12345.mp3",
  "message": "TTS generated successfully"
}
```

### Integration

#### `POST /api/asr-tts/process`

ASR + TTS pipeline terintegrasi

- **Content-Type:** `multipart/form-data`
- **Parameters:**
  - `audio` (file WAV)
  - `voice` (optional, default: `id-ID-ArdiNeural`)
  - `speed` (optional, default: `normal`)

**Response:**

```json
{
  "success": true,
  "asr_prediction": "kereta",
  "asr_confidence": 0.97,
  "tts_text": "Anda mengatakan kereta",
  "tts_audio_url": "/static/generated/audio/response_12345.mp3",
  "waveform_url": "/static/generated/visualizations/waveform_12345.png"
}
```

### Page Routes

| URL      | Method | Description   |
| -------- | ------ | ------------- |
| `/`      | GET    | Home page     |
| `/asr`   | GET    | ASR interface |
| `/tts`   | GET    | TTS interface |
| `/about` | GET    | About page    |

---

## 🧪 Testing

### Run All Tests

```bash
pytest
```

### Run Specific Test File

```bash
pytest tests/test_asr.py
pytest tests/test_app.py
```

### Run with Verbose Output

```bash
pytest -v
```

### Run with Coverage

```bash
pytest --cov=app --cov-report=html
```

### Test Files

| File                                   | Scope                              |
| -------------------------------------- | ---------------------------------- |
| [tests/conftest.py](tests/conftest.py) | Fixtures & setup untuk semua tests |
| [tests/test_app.py](tests/test_app.py) | App factory & initialization       |
| [tests/test_asr.py](tests/test_asr.py) | ASR pipeline & model               |

---

## ⚙️ Configuration

File: [app/config.py](app/config.py)

### Environment Variables

```bash
# Flask
SECRET_KEY=your-secret-key
FLASK_DEBUG=0                    # 0=production, 1=debug
FLASK_RUN_HOST=127.0.0.1
FLASK_RUN_PORT=5000

# ASR
SAMPLE_RATE=16000               # Hz
AUDIO_DURATION_SECONDS=2.0      # Detik
MAX_CONTENT_LENGTH=12582912     # 12 MB (bytes)

# App
HISTORY_LIMIT=30                # Prediksi yang disimpan
```

### Config Classes

**Development:**

```python
DEBUG = True
TESTING = False
```

**Testing:**

```python
TESTING = True
WTF_CSRF_ENABLED = False
```

**Production:**

```python
DEBUG = False
SECRET_KEY = "use-strong-key"
```

---

## 📱 Frontend Usage

### Home Page

- Overview aplikasi
- Link ke ASR dan TTS

### ASR Page

1. **Record with Microphone:**
   - Click "🎤 Start Recording"
   - Speak transportation word (1-2s)
   - Click "Stop Recording"
   - Result akan muncul dengan confidence score

2. **Upload WAV File:**
   - Click "Upload Audio File"
   - Select .wav file
   - Result dengan visualizations (waveform + MFCC heatmap)

3. **View Results:**
   - Prediction label
   - Confidence score (%)
   - Probability distribution
   - Waveform visualization
   - MFCC heatmap
   - History list

### TTS Page

1. **Generate Speech:**
   - Enter text (Indonesia)
   - Select voice (pria/wanita)
   - Select speed (slow/normal/fast)
   - Click "Generate"
   - Audio player akan muncul

2. **Play Audio:**
   - HTML5 audio player
   - Download option tersedia

---

## 🔍 Troubleshooting

### ❌ Port 5000 sudah digunakan

```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# macOS/Linux
lsof -i :5000
kill -9 <PID>
```

Atau ubah port:

```bash
FLASK_RUN_PORT=5001 python run.py
```

### ❌ FFmpeg tidak ditemukan

```bash
# Windows
choco install ffmpeg

# macOS
brew install ffmpeg

# Linux (Ubuntu)
sudo apt-get install ffmpeg
```

### ❌ Microphone tidak terdeteksi

- Pastikan browser permission enabled
- Test microphone di: `chrome://settings/content/microphone`
- Restart browser

### ❌ TTS error (gTTS/Edge TTS)

- Check internet connection
- Edge TTS memerlukan internet untuk voice synthesis
- Fallback ke demo audio tersedia

### ❌ Model file not found

- Jalankan training script: `python train_model.py`
- Atau gunakan demo mode (fallback automatic)

### ❌ Dataset error

```bash
# Validasi dataset
python preprocess.py

# Check file format
file dataset/mobil/mobil_1.wav

# Convert ke WAV 16kHz mono (jika perlu)
ffmpeg -i input.mp3 -acodec pcm_s16le -ar 16000 output.wav
```

---

## 📚 Model Architecture

### Feature Extraction (MFCC)

```
WAV Audio (16kHz, mono)
    ↓
Mel-Frequency Cepstral Coefficients (MFCC)
    ├─ n_mfcc = 13
    ├─ n_fft = 2048
    ├─ hop_length = 512
    └─ Normalization (StandardScaler)
    ↓
Feature Vector (13,)
```

### Classification (SVM)

```
Feature Vector (13,)
    ↓
Support Vector Machine (SVM)
    ├─ Kernel: RBF (Radial Basis Function)
    ├─ C: 100 (regularization)
    └─ probability=True
    ↓
Prediction (label) + Confidence (probability)
```

---

## 🎓 Project Guidelines

### Adding New Transport Words

1. Create folder: `dataset/[word]/`
2. Collect 20+ recordings
3. Run: `python preprocess.py`
4. Re-train: `python train_model.py`
5. Update: [app/config.py](app/config.py) `TRANSPORT_WORDS`

### Training Notes

- Minimum 20 files per class
- Recommended 30-50 files per class
- Re-train whenever dataset changes
- Model retraining: ~5-10 menit
- Model size: ~1-2 MB

### Demo Fallback

- Automatically used jika model belum ada
- Untuk testing & development
- Tidak boleh digunakan untuk production

---

## 📜 License

[Insert your license here]

---

## 🤝 Contributing

Kontribusi welcome! Silakan:

1. Fork repository
2. Create feature branch: `git checkout -b feature/nama-fitur`
3. Commit changes: `git commit -m "Add: deskripsi"`
4. Push to branch: `git push origin feature/nama-fitur`
5. Open Pull Request

---

## 📧 Support

Untuk bantuan atau pertanyaan:

- 📝 Open GitHub Issue
- 📧 Email: [your-email@example.com]
- 💬 Discord: [link]

---

## 🙏 Acknowledgments

- [librosa](https://librosa.org/) - Audio analysis
- [scikit-learn](https://scikit-learn.org/) - Machine Learning
- [Flask](https://flask.palletsprojects.com/) - Web framework
- [Bootstrap 5](https://getbootstrap.com/) - Frontend framework
- [Edge TTS](https://github.com/rany2/edge-tts) - Text-to-Speech

---

**Last Updated:** May 2024
**Project Status:** Active Development 🚀
