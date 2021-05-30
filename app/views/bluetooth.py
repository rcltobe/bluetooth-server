from flask import Blueprint

from app.domain.service.bluetooth import BluetoothService

route = Blueprint("bluetooth", __name__, url_prefix="/bluetooth")


@route.get('/scan')
async def scans_bluetooth():
    service = BluetoothService()
    return {
        "results": await service.scan_devices(None)
    }