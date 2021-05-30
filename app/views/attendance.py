from flask import Blueprint

from app.domain.service.attendance import AttendanceService

route = Blueprint("attendance", __name__, url_prefix="/attendance")


@route.get("/")
async def get_attendance():
    service = AttendanceService()
    return {"results": [attendance.to_json() for attendance in await service.get_attendances()]}
