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
    
    def to_csv(self, start_date: datetime, duration: int):
        """
        CSV形式に変換する
        """
        csv = []

        # 曜日ごとの出席時間を追加
        for i in range(0, duration):
            day = start_date + timedelta(days=i)
            summary_of_day = next(
                (summary for summary in self.summaries if summary.day == day),
                None
            )
            if summary_of_day is None:
                csv.append(0)
                continue
                
            csv.append(summary_of_day.get_attendance_time_in_sec())

        # 火曜日の出席時間を追加
        summary_of_tuesday = next(
            (summary for summary in self.summaries if summary.day.weekday() == 1),
            None
        )
        if summary_of_tuesday is None or len(summary_of_tuesday.attendances) == 0:
            csv.extend([None, None])
        else:
            csv.extend([
                summary_of_tuesday.attendances[0].get_in_at_datetime().hour,
                summary_of_tuesday.attendances[0].get_in_at_datetime().minute,
            ])
    
        return csv

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
    def csv_header():
        return [
            "月",
            "火",
            "水",
            "木",
            "金",
            "土",
            "日",
            "火曜日の登校時間（時）",
            "火曜日の登校時間（分）",
        ]

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
