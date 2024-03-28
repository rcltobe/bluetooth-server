from __future__ import annotations
from typing import List, Optional
from datetime import datetime
from dataclasses import dataclass
from app.domain.models.attendance import Attendance
from app.domain.models.attendance_log import AttendanceLog
from app.domain.util.datetime import is_same_day

@dataclass
class AttendanceSummary:
    user_id: str
    attendances: List[Attendance]
    day: datetime

    def merge(self, other: AttendanceSummary) -> AttendanceSummary:
        """
        ２つの部屋のデータをマージする
        """
        attendances_self = self.attendances
        attendances_other = other.attendances
        attendances = attendances_self + attendances_other
        attendances = sorted(attendances, key=lambda attendance: attendance.in_at)
        return AttendanceSummary(
            user_id=self.user_id,
            attendances=attendances,
            day=self.day,
        )
     
    def to_json(self):
        return {
            "user_id": self.user_id,
            "attendances": [attendance.to_json() for attendance in self.attendances],
            "day": self.day.timestamp(),
        }

    # 出席時間を取得
    def get_attendance_time_in_sec(self) -> int:
        return sum([attendance.get_attendance_time_in_sec() for attendance in self.attendances])
    
    @staticmethod
    def generate_summary(
        attendance_logs: List[AttendanceLog], 
        day: datetime,
        user_id: str,
    ) -> List[AttendanceSummary]:
        """
        指定された日のユーザーの出席の集計を行う
        """
        rooms = ["O502", "N501"]
        summaries = []
        for room in rooms:
            summary = AttendanceSummary._generate_summary_of_room(
                attendance_logs=attendance_logs,
                user_id=user_id,
                day=day,
                room=room,
            )
            summaries.append(summary)
        
        return summaries[0].merge(summaries[1])
    
    @staticmethod
    def _generate_summary_of_room(
        attendance_logs: List[AttendanceLog],
        user_id: str,
        room: str,
        day: datetime,
    ) -> AttendanceSummary:
        attendance_logs_of_user = [
            log for log in attendance_logs 
            if log.user_id == user_id and log.room == room and is_same_day(day, datetime.fromtimestamp(log.created_at))
        ]
        attendance_logs_sorted = sorted(
            attendance_logs_of_user, 
            key=lambda log: log.created_at
        )

        attendances: List[Attendance] = []
        for attendance_log in attendance_logs_sorted:
            # 最初の入室ログを見つける
            if len(attendances) == 0:
                if not attendance_log.is_attending:
                    continue
                
                attendances.append(Attendance(
                    in_at=attendance_log.created_at,
                    out_at=None,
                    room=attendance_log.room
                ))
                continue

            # 前の状態と同じであれば記録しない
            prev_attendance: Attendance = attendances[-1]
            if prev_attendance.is_attending() == attendance_log.is_attending:
                continue

            if prev_attendance.is_attending():
                attendances[-1].out_at = attendance_log.created_at
            else:
                attendances.append(Attendance(
                    in_at=attendance_log.created_at,
                    out_at=None,
                    room=attendance_log.room
                ))
        
        return AttendanceSummary(
            user_id=user_id,
            attendances=attendances,
            day=datetime(day.year, day.month, day.day)
        )