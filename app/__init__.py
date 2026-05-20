from flask import Flask, jsonify, render_template

from app.config import Config
from app.routes import register_blueprints
from app.utils.logging import configure_logging
from app.utils.storage import ensure_runtime_directories


def create_app(config_class=Config):
    """Application factory for Transportify Voice."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Allows overrides such as TRANSPORTIFY_SECRET_KEY=...
    if hasattr(app.config, "from_prefixed_env"):
        app.config.from_prefixed_env(prefix="TRANSPORTIFY")

    ensure_runtime_directories(app)
    configure_logging(app)
    register_blueprints(app)
    register_error_handlers(app)

    app.logger.info("Transportify Voice application initialized")
    return app


def register_error_handlers(app):
    @app.errorhandler(404)
    def not_found(error):
        if _wants_json():
            return jsonify({"success": False, "error": "Resource not found"}), 404
        return render_template("404.html"), 404

    @app.errorhandler(413)
    def payload_too_large(error):
        return jsonify(
            {
                "success": False,
                "error": "Audio file is too large. Maximum upload size is 12 MB.",
            }
        ), 413

    @app.errorhandler(Exception)
    def handle_unexpected_error(error):
        app.logger.exception("Unhandled application error: %s", error)
        if _wants_json():
            return jsonify({"success": False, "error": "Internal server error"}), 500
        return render_template("500.html"), 500


def _wants_json():
    from flask import request

    return request.path.startswith("/api/") or request.accept_mimetypes.best == "application/json"
