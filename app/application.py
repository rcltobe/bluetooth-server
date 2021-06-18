from flask import Flask

from app.views import (device, index)


def create_app() -> Flask:
    app = Flask(__name__)
    app.register_blueprint(device.route)
    app.register_blueprint(index.route)
    return app
