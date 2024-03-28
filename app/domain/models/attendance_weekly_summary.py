from __future__ import annotations
from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import List

from app.domain.models.attendance_log import AttendanceLog
from app.domain.models.attendance_summary import AttendanceSummary


@dataclass
class AttendanceWeeklySummary:
    summaries: List[AttendanceSummary]

    def to_json(self):
        return {
            "summaries": [
                summary.to_json() for summary in self.summaries
            ]
        }

    def count_attendance_time_over(self, hour: int) -> int:
        """
        出席時間が指定された時間を超えている日数を取得
        """
        count = 0
        for summary in self.summaries:
            if summary.get_attendance_time_in_sec() >= hour * 60 * 60:
                count += 1
        return count

    def is_attended_at(self, weekday: int, hour: int) -> bool:
        """
        指定した曜日、時刻に出席しているかどうかを返す
        """
        for summary in self.summaries:
            for attendance in summary.attendances:
                attendance_weekday = attendance.get_in_at_datetime().weekday()
                if attendance_weekday != weekday:
                    continue
                
                attendance_hour = attendance.get_in_at_datetime().hour
                if attendance_hour <= hour:
                    return True
        return False

    @staticmethod
    def generate_weekly_summary(
            attendance_logs: List[AttendanceLog],
            user_id: str,
            start_date: datetime,
    ) -> AttendanceWeeklySummary:
        WEEKDAY_SUNDAY = 6

        summaries = []
        for i in range(0, WEEKDAY_SUNDAY - start_date.weekday() + 1):
            day = start_date + timedelta(days=i)

            summary: AttendanceSummary = AttendanceSummary.generate_summary(
                attendance_logs=attendance_logs,
                day=day,
                user_id=user_id,
            )
            if len(summary.attendances) == 0:
                continue
        
            summaries.append(summary)

        return AttendanceWeeklySummary(
            summaries=summaries,
        )
