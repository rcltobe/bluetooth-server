from typing import List
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from app.domain.models.attendance_log import AttendanceLog


class FirestoreAttendanceLogRepository:
    def __init__(self) -> None:
        cred = credentials.Certificate('./credentials.json')
        self.app = firebase_admin.initialize_app(cred)
        self.db = firestore.client()

    async def fetch_logs_of_today(self) -> List[AttendanceLog]:
        pass

    async def add_attendance_logs(self, attendance_logs: List[AttendanceLog]):
        pass