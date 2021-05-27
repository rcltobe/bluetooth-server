from flask import Blueprint

route = Blueprint("index", __name__)


@route.get('/')
def index():
    return "Hello World"
