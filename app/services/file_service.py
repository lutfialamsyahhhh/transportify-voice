from pathlib import Path
from uuid import uuid4

from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename


ALLOWED_AUDIO_EXTENSIONS = {".wav", ".wave", ".webm", ".mp3", ".m4a", ".ogg"}


def save_uploaded_audio(file: FileStorage, upload_dir: Path) -> Path:
    original_name = secure_filename(file.filename or "recording.wav")
    extension = Path(original_name).suffix.lower()

    if extension not in ALLOWED_AUDIO_EXTENSIONS:
        raise ValueError("Unsupported audio format. Please upload a WAV audio file.")

    upload_dir.mkdir(parents=True, exist_ok=True)
    filename = f"{uuid4().hex}{extension or '.wav'}"
    destination = upload_dir / filename
    file.save(destination)

    if destination.stat().st_size == 0:
        destination.unlink(missing_ok=True)
        raise ValueError("Uploaded audio file is empty.")

    return destination
