from flask import Blueprint, request, Response, jsonify

from app.domain.models.util import DateRange
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


@route.post("/delete")
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


@route.get('/states')
async def get_all_device_states():
    service = DeviceService()
    states = await service.get_all_device_states()
    return jsonify([
        state.to_json()
        for state in states
    ])


@route.post('/states')
async def get_all_device_states_in_date_range():
    """
    リクエスト例
    {
        "start": 1622977822,
        "end": 1622977847
    }
    """
    request_json = request.json
    if "start" not in request_json or "end" not in request_json:
        return Response(status=400)

    try:
        start = int(request_json["start"])
        end = int(request_json["end"])
    except ValueError:
        return Response(status=400)

    service = DeviceService()
    states = await service.get_all_device_states(DateRange(start, end))

    return jsonify([
        state.to_json()
        for state in states
    ])


@route.post("/states/<address>")
async def get_device_states(address: str = None):
    if address is None:
        return Response(status=400)

    service = DeviceService()
    states = await service.get_device_states(address)

    return jsonify([
        state.to_json()
        for state in states
    ])
