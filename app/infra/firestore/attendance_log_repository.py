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
            logs.append(AttendanceLog(
                user_id=data['user_id'],
                user_name=data['user_name'],
                bluetooth_mac_address=data['address'],
                is_attending=data['is_attending'],
                room=data['room'],
                created_at=data['created_at'].timestamp()
            ))
        
        return logs

    async def add_attendance_logs(self, attendance_logs: List[AttendanceLog]):
        for log in attendance_logs:
            self.db.collection('attendance').add({
                'user_id': log.user_id,
                'user_name': log.user_name,
                'address': log.bluetooth_mac_address,
                'is_attending': log.is_attending,
                'room': log.room,
                'created_at': datetime.fromtimestamp(log.created_at),
            })