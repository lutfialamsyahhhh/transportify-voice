import logging
from logging.handlers import RotatingFileHandler


def configure_logging(app):
    level = logging.DEBUG if app.config.get("DEBUG") else logging.INFO
    app.logger.setLevel(level)

    if app.testing:
        return

    log_dir = app.config["GENERATED_DIR"] / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / "transportify.log"

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )
    handler = RotatingFileHandler(log_file, maxBytes=1_000_000, backupCount=3)
    handler.setFormatter(formatter)
    handler.setLevel(level)

    if not any(isinstance(existing, RotatingFileHandler) for existing in app.logger.handlers):
        app.logger.addHandler(handler)
