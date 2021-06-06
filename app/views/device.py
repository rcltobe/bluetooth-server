from flask import Blueprint, request, Response, jsonify

from app.domain.service.device import DeviceService

route = Blueprint("devices", __name__, url_prefix="/devices")


@route.get("/")
async def get_devices():
    service = DeviceService()
    return jsonify([device.to_json() for device in await service.get_devices()])


@route.post("/create")
async def add_device():
    """
    リクエスト例
    {
        "userId": "test",
        "address": "00:00:00:00:00:00"
    }
    """
    request_json = request.json
    if "userId" not in request_json or "address" not in request_json:
        return Response(status=400)

    service = DeviceService()
    await service.add_device(
        user_id=request_json["userId"],
        address=request_json["address"]
    )

    return Response(status=200)


@route.delete("/delete")
async def delete_device():
    """
    リクエスト例
    {
        "address": "00:00:00:00:00:00"
    }
    """
    request_json = request.json
    if "address" not in request_json:
        return Response(status=400)

    service = DeviceService()
    await service.delete_device(
        address=request_json["address"]
    )


@route.get('/scan')
async def scans_bluetooth():
    service = DeviceService()
    return jsonify([
        result.to_json()
        for result in await service.get_scan_results()
    ])
