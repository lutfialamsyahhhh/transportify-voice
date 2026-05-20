from app.routes.asr_api import asr_api as asr_api_blueprint
from app.routes.integration_api import integration_api as integration_api_blueprint
from app.routes.pages import pages as pages_blueprint
from app.routes.tts_api import tts_api as tts_api_blueprint


def register_blueprints(app):
    app.register_blueprint(pages_blueprint)
    app.register_blueprint(asr_api_blueprint)
    app.register_blueprint(tts_api_blueprint)
    app.register_blueprint(integration_api_blueprint)
