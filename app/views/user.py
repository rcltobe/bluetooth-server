from flask import Blueprint, request, Response, jsonify

from app.domain.service.user import UserService

route = Blueprint("user", __name__, url_prefix="/user")


@route.get("/")
async def get_users():
    service = UserService()
    users = [user.to_json() for user in await service.get_users()]
    return jsonify(users)


@route.post("/create")
async def create():
    """
    リクエスト例:
    {
        "name": "山田太郎",
        "devices": [
            "XX:XX:XX:XX:XX:XX",
            "OO:OO:OO:OO:OO:OO"
        ],
        "grade": "M4"
    }

    """
    request_json = request.json
    if "name" not in request_json \
            or "devices" not in request_json:
        return Response(status=400)

    name = request_json["name"]
    devices = request_json["devices"]

    grade = request_json["grade"] if "grade" in request_json else ""

    service = UserService()
    new_user = await service.add_user(name=name, devices=devices, grade=grade)

    return new_user.to_json()


@route.delete('/delete')
async def delete():
    """
    リクエスト例:
    {
        "id": "eb5e3b86-3373-4beb-99af-eade43fa9829"
    }
    """
    request_json = request.json
    if "id" not in request_json:
        return Response(status=400)

    service = UserService()
    await service.delete_user(request_json["id"])

    return Response(status=200)


@route.get('/<id>/device')
async def get_devices(id=None):
    if id is None:
        return Response(status=400)

    service = UserService()
    return jsonify([device.to_json() for device in await service.get_devices(id)])


@route.post('/<id>/device/add')
async def add_device(id=None):
    """
    リクエスト例:
    {
        "device": "OO:OO:OO:OO:OO:OO"
    }
    """

    if id is None:
        return Response(status=400)

    request_json = request.json
    if id is None or "device" not in request_json:
        return Response(status=400)

    service = UserService()
    device = await service.add_device(user_id=id, address=request_json["device"])

    return {
        "result": device.to_json() if device is not None else "fail"
    }
