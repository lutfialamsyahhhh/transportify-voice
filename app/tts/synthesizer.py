import asyncio
import os
import subprocess
import tempfile
from contextlib import contextmanager
from pathlib import Path
from uuid import uuid4

from gtts import gTTS


SUPPORTED_SPEEDS = {"slow", "normal", "fast"}
SUPPORTED_VOICES = {"female", "male"}

VOICE_CONFIG = {
    "female": {
        "engine": "edge-tts",
        "voice_id": "id-ID-GadisNeural",
        "label": "Indonesian Female",
        "sapi_voice": "Microsoft Zira Desktop",
    },
    "male": {
        "engine": "edge-tts",
        "voice_id": "id-ID-ArdiNeural",
        "label": "Indonesian Male",
        "sapi_voice": "Microsoft David Desktop",
    },
}

SPEED_CONFIG = {
    "slow": {"edge_rate": "-35%", "sapi_rate": -5, "factor": 0.65, "label": "Slow"},
    "normal": {"edge_rate": "+0%", "sapi_rate": 0, "factor": 1.0, "label": "Normal"},
    "fast": {"edge_rate": "+80%", "sapi_rate": 8, "factor": 1.8, "label": "Fast"},
}


class TTSGenerationError(RuntimeError):
    pass


def generate_speech(text, speed="normal", voice="female", output_dir=None):
    speed = speed if speed in SUPPORTED_SPEEDS else "normal"
    voice = voice if voice in SUPPORTED_VOICES else "female"

    clean_text = (text or "").strip()
    if not clean_text:
        raise ValueError("Text input is required for speech generation.")

    output_dir = Path(output_dir or "app/static/generated/audio")
    output_dir.mkdir(parents=True, exist_ok=True)

    file_id = uuid4().hex
    warning = None
    engine = _default_engine()
    extension = ".wav" if engine == "windows-sapi" else ".mp3"
    output_path = output_dir / f"tts_{file_id}{extension}"

    try:
        if engine == "windows-sapi":
            _generate_windows_sapi(clean_text, output_path, voice, speed)
        else:
            _generate_edge_tts(clean_text, output_path, voice, speed)
    except Exception as exc:
        _safe_unlink(output_path)
        try:
            if engine == "windows-sapi":
                engine = "edge-tts"
                output_path = output_dir / f"tts_{file_id}.mp3"
                _generate_edge_tts(clean_text, output_path, voice, speed)
                warning = "Windows SAPI failed, so Edge Indonesian neural TTS was used."
            else:
                engine = "windows-sapi"
                output_path = output_dir / f"tts_{file_id}.wav"
                _generate_windows_sapi(clean_text, output_path, voice, speed)
                warning = (
                    "Edge Indonesian neural TTS was unavailable, so Windows local voice was used. "
                    "Male/female and speed are active, but pronunciation follows installed Windows voices."
                )
        except Exception as sapi_exc:
            _safe_unlink(output_path)
            if os.getenv("TTS_ALLOW_GTTS_FALLBACK", "0") != "1":
                raise TTSGenerationError(
                    "TTS could not generate audio. Windows SAPI and Edge TTS are unavailable."
                ) from sapi_exc

            output_path = output_dir / f"tts_{file_id}.mp3"
            warning = (
                "Edge TTS and Windows SAPI failed, so gTTS fallback was used. "
                "Gender voice selection and strong speed control are unavailable in fallback mode."
            )
            engine = "gtts-fallback"
            _generate_gtts_fallback(clean_text, output_path)

    duration_seconds = _read_audio_duration(output_path)
    speed_config = SPEED_CONFIG[speed]
    voice_config = VOICE_CONFIG[voice]
    effective_voice = voice_config["voice_id"] if engine == "edge-tts" else voice_config["sapi_voice"]
    effective_rate = speed_config["edge_rate"] if engine == "edge-tts" else str(speed_config["sapi_rate"])

    return {
        "text": clean_text,
        "speed": speed,
        "speed_factor": speed_config["factor"],
        "speed_rate": effective_rate,
        "playback_rate": 1.0,
        "voice": voice,
        "voice_id": effective_voice,
        "voice_label": voice_config["label"],
        "voice_note": f"{voice_config['label']} requested; generated with {effective_voice}.",
        "engine": engine,
        "audio_url": f"/static/generated/audio/{output_path.name}",
        "download_url": f"/static/generated/audio/{output_path.name}",
        "file_name": output_path.name,
        "original_duration_seconds": duration_seconds,
        "duration_seconds": duration_seconds,
        "warning": warning,
    }


def _generate_edge_tts(text, output_path, voice, speed):
    try:
        import edge_tts
    except ImportError as exc:
        raise TTSGenerationError(
            "edge-tts is not installed. Run: pip install -r requirements.txt"
        ) from exc

    voice_id = VOICE_CONFIG[voice]["voice_id"]
    rate = SPEED_CONFIG[speed]["edge_rate"]

    async def synthesize():
        communicate = edge_tts.Communicate(text=text, voice=voice_id, rate=rate)
        await communicate.save(str(output_path))

    with _tts_proxy_environment():
        asyncio.run(synthesize())


def _default_engine():
    configured = os.getenv("TTS_ENGINE", "").strip().lower()
    if configured in {"edge", "edge-tts"}:
        return "edge-tts"
    if configured in {"sapi", "windows-sapi"}:
        return "windows-sapi"
    return "edge-tts"


def _generate_windows_sapi(text, output_path, voice, speed):
    if os.name != "nt":
        raise TTSGenerationError("Windows SAPI fallback is only available on Windows.")

    script = r"""
param(
    [string]$TextPath,
    [string]$OutputPath,
    [string]$VoiceName,
    [int]$Rate
)
Add-Type -AssemblyName System.Speech
$text = Get-Content -LiteralPath $TextPath -Raw -Encoding UTF8
$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer
$selected = $synth.GetInstalledVoices() |
    Where-Object { $_.VoiceInfo.Name -eq $VoiceName } |
    Select-Object -First 1
if ($null -eq $selected) {
    $gender = if ($VoiceName -match 'David|Male') { 'Male' } else { 'Female' }
    $selected = $synth.GetInstalledVoices() |
        Where-Object { $_.VoiceInfo.Gender.ToString() -eq $gender } |
        Select-Object -First 1
}
if ($null -ne $selected) {
    $synth.SelectVoice($selected.VoiceInfo.Name)
}
$synth.Rate = $Rate
$synth.SetOutputToWaveFile($OutputPath)
$synth.Speak($text)
$synth.Dispose()
"""
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8") as text_file:
        text_file.write(text)
        text_path = text_file.name
    with tempfile.NamedTemporaryFile("w", suffix=".ps1", delete=False, encoding="utf-8") as script_file:
        script_file.write(script)
        script_path = script_file.name

    try:
        completed = subprocess.run(
            [
                "powershell",
                "-NoProfile",
                "-ExecutionPolicy",
                "Bypass",
                "-File",
                script_path,
                "-TextPath",
                text_path,
                "-OutputPath",
                str(output_path),
                "-VoiceName",
                VOICE_CONFIG[voice]["sapi_voice"],
                "-Rate",
                str(SPEED_CONFIG[speed]["sapi_rate"]),
            ],
            capture_output=True,
            text=True,
            timeout=60,
            check=False,
        )
        if completed.returncode != 0 or not output_path.exists() or output_path.stat().st_size == 0:
            raise TTSGenerationError(completed.stderr or "Windows SAPI did not create audio.")
    finally:
        Path(text_path).unlink(missing_ok=True)
        Path(script_path).unlink(missing_ok=True)


def _generate_gtts_fallback(text, output_path):
    try:
        tts = gTTS(text=text, lang="id", slow=False)
        with _tts_proxy_environment():
            tts.save(str(output_path))
    except Exception as exc:
        raise TTSGenerationError(
            "TTS could not generate audio. Check your internet connection or proxy settings."
        ) from exc


def _read_audio_duration(output_path):
    try:
        from pydub import AudioSegment

        audio = AudioSegment.from_file(output_path)
        return round(len(audio) / 1000, 3)
    except Exception:
        return None


def _safe_unlink(path):
    try:
        Path(path).unlink(missing_ok=True)
    except PermissionError:
        pass


@contextmanager
def _tts_proxy_environment():
    """Avoid broken local proxy env vars while keeping opt-in proxy support."""
    if os.getenv("TTS_USE_SYSTEM_PROXY", "0") == "1":
        yield
        return

    proxy_keys = [
        "HTTP_PROXY",
        "HTTPS_PROXY",
        "ALL_PROXY",
        "http_proxy",
        "https_proxy",
        "all_proxy",
    ]
    previous_values = {key: os.environ.get(key) for key in proxy_keys}

    try:
        for key in proxy_keys:
            os.environ.pop(key, None)
        yield
    finally:
        for key, value in previous_values.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value
