from flask import Blueprint

from app.infra.repository import RepositoryContainer

route = Blueprint("index", __name__)


@route.get('/')
def index():
    return "Hello World"


@route.get('/debug')
async def debug():
    return {
        "devices": [device.to_json() for device in await RepositoryContainer.device_repository.find_all()],
        "states": [state.to_json() for state in await RepositoryContainer.device_state_repository.find_all()],
    }
