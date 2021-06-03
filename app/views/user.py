from flask import Blueprint, request, Response, jsonify

from app.domain.service.user import UserService

route = Blueprint("users", __name__, url_prefix="/users")


@route.get("/")
async def get_users():
    service = UserService()
    users = [user.to_json() for user in await service.get_users()]
    return jsonify(users)


@route.get("/<id>")
async def get_user(id=None):
    if id is None:
        return Response(status=400)

    service = UserService()
    user = await service.get_user(id)
    if user is None:
        return Response(status=400)

    return user.to_json()


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


@route.post('/edit/<id>')
async def edit(id=None):
    """
    リクエスト例:
    {
        "name": "new-name",
        "devices": [],
        "grade": "M1"
    }
    """
    if id is None:
        return Response(status=400)

    service = UserService()

    request_json = request.json
    if "name" in request_json:
        await service.update_name(id, request_json["name"])

    if "grade" in request_json:
        await service.update_grade(id, request_json["grade"])

    if "devices" in request_json:
        await service.update_devices(id, request_json["devices"])

    return Response(status=200)


@route.delete('/delete/{id}')
async def delete(id=None):
    if id is None:
        return Response(status=400)

    service = UserService()
    await service.delete_user(id)

    return Response(status=200)


@route.get('/<id>/device')
async def get_devices(id=None):
    if id is None:
        return Response(status=400)

    service = UserService()
    return jsonify([device.to_json() for device in await service.get_devices(id)])
