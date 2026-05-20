def test_pages_render(client):
    for route in ["/", "/asr", "/tts", "/about"]:
        response = client.get(route)
        assert response.status_code == 200


def test_asr_validation_error(client):
    response = client.post("/api/asr/predict")
    assert response.status_code == 400
    assert response.get_json()["success"] is False


def test_tts_validation_error(client):
    response = client.post("/api/tts/generate", json={"text": ""})
    assert response.status_code == 400
    assert response.get_json()["success"] is False


def test_tts_generate_route_with_mock(client, monkeypatch):
    def fake_generate_speech(text, speed, voice, output_dir):
        return {
            "text": text,
            "speed": speed,
            "speed_factor": 1.0,
            "speed_rate": "+0%",
            "playback_rate": 1.0,
            "voice": voice,
            "voice_id": "id-ID-GadisNeural",
            "voice_label": "Indonesian Female",
            "engine": "edge-tts",
            "audio_url": "/static/generated/audio/test.mp3",
            "download_url": "/static/generated/audio/test.mp3",
            "file_name": "test.mp3",
            "original_duration_seconds": 1.0,
            "duration_seconds": 1.0,
            "warning": None,
            "voice_note": "mock",
        }

    monkeypatch.setattr("app.routes.tts_api.generate_speech", fake_generate_speech)
    response = client.post(
        "/api/tts/generate",
        json={"text": "Anda mengatakan bus", "speed": "normal", "voice": "female"},
    )
    payload = response.get_json()
    assert response.status_code == 200
    assert payload["success"] is True
    assert payload["data"]["file_name"] == "test.mp3"
