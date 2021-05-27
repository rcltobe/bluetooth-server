from flask import Flask
from app.views import (bluetooth, index)


def create_app() -> Flask:
    app = Flask(__name__)
    app.register_blueprint(bluetooth.route)
    app.register_blueprint(index.route)
    return app
