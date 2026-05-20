from flask import Blueprint, current_app, request

from app.tts.synthesizer import TTSGenerationError, generate_speech
from app.utils.responses import api_error, api_success


integration_api = Blueprint("integration_api", __name__, url_prefix="/api/integrations")


@integration_api.post("/asr-to-tts")
def asr_to_tts():
    payload = request.get_json(silent=True) or {}
    prediction = (payload.get("prediction") or "").strip().lower()
    speed = (payload.get("speed") or "normal").strip().lower()

    if not prediction:
        return api_error("Prediction text is required.", 400)

    response_text = f"Anda mengatakan {prediction}"

    try:
        result = generate_speech(
            text=response_text,
            speed=speed,
            voice="female",
            output_dir=current_app.config["GENERATED_AUDIO_DIR"],
        )
        result["response_text"] = response_text
        return api_success(result, message="ASR response voice generated")
    except TTSGenerationError as exc:
        current_app.logger.warning("ASR to TTS response failed: %s", exc)
        return api_error(str(exc), 503, details={"response_text": response_text})
    except Exception as exc:
        current_app.logger.exception("ASR to TTS integration failed: %s", exc)
        return api_error("Unable to generate voice response.", 500)
