from flask import Blueprint, current_app, request

from app.tts.synthesizer import TTSGenerationError, generate_speech
from app.utils.responses import api_error, api_success


tts_api = Blueprint("tts_api", __name__, url_prefix="/api/tts")


@tts_api.post("/generate")
def generate():
    payload = request.get_json(silent=True) or {}
    text = (payload.get("text") or "").strip()
    speed = (payload.get("speed") or "normal").strip().lower()
    voice = (payload.get("voice") or "female").strip().lower()

    if not text:
        return api_error("Text input is required for speech generation.", 400)

    try:
        result = generate_speech(
            text=text,
            speed=speed,
            voice=voice,
            output_dir=current_app.config["GENERATED_AUDIO_DIR"],
        )
        return api_success(result, message="TTS audio generated")
    except ValueError as exc:
        return api_error(str(exc), 400)
    except TTSGenerationError as exc:
        current_app.logger.warning("TTS generation failed: %s", exc)
        return api_error(str(exc), 503)
    except Exception as exc:
        current_app.logger.exception("Unexpected TTS failure: %s", exc)
        return api_error("Unable to generate speech at this time.", 500)
