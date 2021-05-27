from flask import Blueprint, request, Response, jsonify

from app.domain.service.user import UserService
from app.infra.json import to_json

route = Blueprint("user", __name__)


@route.post("/user/create")
async def add():
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

    return jsonify({
        "user": to_json(new_user)
    })


@route.get("/user")
async def get_users():
    service = UserService()
    users = await service.get_users()
    return jsonify({
        "users": [to_json(user) for user in users]
    })
