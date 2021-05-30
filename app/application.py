from flask import Flask

from app.views import (bluetooth, index, user, attendance)


def create_app() -> Flask:
    app = Flask(__name__)
    app.register_blueprint(attendance.route)
    app.register_blueprint(bluetooth.route)
    app.register_blueprint(index.route)
    app.register_blueprint(user.route)
    return app
