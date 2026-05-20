def ensure_runtime_directories(app):
    directories = [
        app.config["GENERATED_DIR"],
        app.config["GENERATED_AUDIO_DIR"],
        app.config["GENERATED_VISUALIZATION_DIR"],
        app.config["UPLOAD_DIR"],
        app.config["MODEL_DIR"],
    ]
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
