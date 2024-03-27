from __future__ import annotations

import time
from dataclasses import dataclass
from typing import List, Optional

from app.domain.models.user import User


@dataclass
class AttendanceLog:
    user_id: str
    user_name: str
    bluetooth_mac_address: str
    created_at: int
    is_attending: bool 

    def to_json(self):
        return {
            "user_id": self.user_id,
            "user_name": self.user_name,
            "bluetooth_address": self.bluetooth_mac_address,
            "is_attending": self.is_attending,
            "created_at": self.created_at,
        }

    def to_csv(self):
        return [self.user_id, self.user_name, self.bluetooth_mac_address, self.created_at, self.is_attending]

    @staticmethod
    def from_user(user: User, created_at: int, is_attending: bool) -> AttendanceLog:
        return AttendanceLog(
            user_id=user.user_id,
            user_name=user.user_name,
            bluetooth_mac_address=user.address,
            is_attending=is_attending,
            created_at=created_at,
        )

    @staticmethod
    def create_attendance_log(
        prev_attendance_logs: Optional[List[AttendanceLog]],
        is_found: bool,
        user: User,
        now: Optional[int]
    ) -> Optional[AttendanceLog]:
        if now is None:
            now = int(time.time()) 
            
        if prev_attendance_logs is None:
            prev_attendance_logs = []

        prev_attendance_logs_of_user = [
            log for log in prev_attendance_logs 
            if log.user_id == user.user_id
        ]
        # sorted by created_at
        prev_attendance_logs_of_user.sort(key=lambda log: log.created_at, reverse=True)

        prev_attendance_log = None
        if len(prev_attendance_logs_of_user) > 0:
            prev_attendance_log = prev_attendance_logs_of_user[0]

        # まだ出席していない
        if prev_attendance_log is None and not is_found:
            return None
        
        # 前回の出席状態と同じ
        if prev_attendance_log is not None and prev_attendance_log.is_attending == is_found:
            return None

        attendance_log = AttendanceLog(
            user_id=user.user_id,
            user_name=user.user_name,
            bluetooth_mac_address=user.address,
            is_attending=is_found,
            created_at=now,
        )

        return attendance_log