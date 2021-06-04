from flask import Blueprint, jsonify

from app.domain.service.bluetooth import BluetoothService

route = Blueprint("bluetooth", __name__, url_prefix="/bluetooth")


@route.get('/scan')
async def scans_bluetooth():
    service = BluetoothService()
    return jsonify([
        result.to_json()
        for result in await service.get_scan_results()
    ])
