from flask import Blueprint, current_app, request

from app.asr.pipeline import predict_audio
from app.services.file_service import save_uploaded_audio
from app.services.history_service import prediction_history
from app.utils.responses import api_error, api_success


asr_api = Blueprint("asr_api", __name__, url_prefix="/api/asr")


@asr_api.post("/predict")
def predict():
    audio = request.files.get("audio")
    if audio is None or not audio.filename:
        return api_error("Please provide a WAV audio file in the 'audio' field.", 400)

    try:
        audio_path = save_uploaded_audio(audio, current_app.config["UPLOAD_DIR"])
        result = predict_audio(audio_path)
        history_item = prediction_history.add(
            label=result["label"],
            confidence=result["confidence"],
            demo=result["demo"],
            source_filename=audio.filename,
        )
        result["history_item"] = history_item
        return api_success(result, message="ASR prediction completed")
    except ValueError as exc:
        current_app.logger.warning("ASR validation failed: %s", exc)
        return api_error(str(exc), 400)
    except Exception as exc:
        current_app.logger.exception("ASR prediction failed: %s", exc)
        return api_error("Failed to process audio. Please use a mono WAV recording.", 500)


@asr_api.get("/history")
def history():
    return api_success({"items": prediction_history.list_recent()})
