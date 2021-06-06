from flask import Flask

from app.views import (device, index, user, temperature)


def create_app() -> Flask:
    app = Flask(__name__)
    app.register_blueprint(device.route)
    app.register_blueprint(index.route)
    app.register_blueprint(temperature.route)
    app.register_blueprint(user.route)
    return app
