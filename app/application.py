from flask import Flask

from app.views import (index)


def create_app() -> Flask:
    """
    サービスが動いているかの確認用にFlaskサーバーを立てる。
    """
    app = Flask(__name__)
    app.register_blueprint(index.route)
    return app
