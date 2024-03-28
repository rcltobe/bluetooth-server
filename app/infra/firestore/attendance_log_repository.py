from datetime import datetime
from typing import List
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from google.cloud.firestore_v1.base_query import FieldFilter

from app.domain.models.attendance_log import AttendanceLog


class FirestoreAttendanceLogRepository:
    def __init__(self) -> None:
        cred = credentials.Certificate('./credentials.json')
        self.app = firebase_admin.initialize_app(cred)
        self.db = firestore.client()

    async def fetch_logs_of_day(self, day: datetime) -> List[AttendanceLog]:
        day_start = datetime(day.year, day.month, day.day, 0, 0, 0)
        day_end = datetime(day.year, day.month, day.day, 23, 59, 59)
        query = self.db.collection('attendance')
        query = query.where(filter=FieldFilter('created_at', '>=', day_start))
        query = query.where(filter=FieldFilter('created_at', '<=', day_end))
        docs = query.stream()
        logs = []
        for doc in docs:
            data = doc.to_dict()
            logs.append(AttendanceLog.from_firestore_dict(data))
        return logs
    
    async def fetch_logs_of_day_between(self, day_start: datetime, day_end: datetime) -> List[AttendanceLog]:
        query = self.db.collection('attendance')
        query = query.where(filter=FieldFilter('created_at', '>=', datetime(day_start.year, day_start.month, day_start.day, 0, 0, 0)))
        query = query.where(filter=FieldFilter('created_at', '<=', datetime(day_end.year, day_end.month, day_end.day, 23, 59, 59)))
        docs = query.stream()
        logs = []
        for doc in docs:
            data = doc.to_dict()
            logs.append(AttendanceLog.from_firestore_dict(data))
        return logs

    async def add_attendance_logs(self, attendance_logs: List[AttendanceLog]):
        for log in attendance_logs:
            self.db.collection('attendance').add(log.to_firestore_dict())