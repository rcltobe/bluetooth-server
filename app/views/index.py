from flask import Blueprint

from app.infra.in_memory.device_repository import InMemoryDeviceRepository
from app.infra.in_memory.device_state_repository import InMemoryDeviceStateRepository
from app.infra.in_memory.user_repository import InMemoryUserRepository

route = Blueprint("index", __name__)


@route.get('/')
def index():
    return "Hello World"


@route.get('/debug')
async def debug():
    return {
        "states": [state.to_json() for state in await InMemoryDeviceStateRepository().find_all()],
        "users": [user.to_json() for user in await InMemoryUserRepository().find_all()],
        "devices": [device.to_json() for device in await InMemoryDeviceRepository().find_all()],
    }
