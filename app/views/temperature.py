from flask import Blueprint, request, Response, jsonify

from app.domain.service.temperature import BodyTemperatureService

route = Blueprint("temperature", __name__, url_prefix="/temperature")


@route.get('/')
async def get_body_temperature_data():
    service = BodyTemperatureService()
    return jsonify([
        data.to_json()
        for data in await service.find_all()
    ])


@route.post('/create')
async def save_temperature():
    """
    リクエスト例
    {
        user_id: "test_user",
        temperature: 36.5
    }
    """
    request_json = request.json
    if "user_id" not in request_json or "temperature" not in request_json:
        return Response(status=400)

    user_id = request_json["user_id"]
    try:
        temperature = float(request_json["temperature"])
    except ValueError:
        return Response(status=400)

    service = BodyTemperatureService()
    await service.save(temperature, user_id)

    return Response(status=200)
