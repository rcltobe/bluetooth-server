from datetime import datetime
import json
import unittest

from app.domain.models.attendance import Attendance
from app.domain.models.attendance_log import AttendanceLog
from app.domain.models.attendance_summary import AttendanceSummary
from app.domain.models.attendance_weekly_summary import AttendanceWeeklySummary


class TestAttendanceWeeklySummary(unittest.TestCase):
    def test_generate_weekly_summary(self):
        cases = [
            {
                "name": "1週間の出席サマリーを作成",
                "user_id": "test",
                "start_day": datetime(2024, 4, 1), # 月曜日
                "attending_logs": [
                    AttendanceLog(
                        user_id="test",
                        user_name="test",
                        bluetooth_mac_address="00:00:00:00",
                        is_attending=True,
                        room="O502",
                        created_at=datetime(2024, 4, 1, 12, 0, 0).timestamp(),
                    ),
                    AttendanceLog(
                        user_id="test",
                        user_name="test",
                        bluetooth_mac_address="00:00:00:00",
                        is_attending=False,
                        room="O502",
                        created_at=datetime(2024, 4, 1, 15, 0, 0).timestamp(),
                    ),
                    AttendanceLog(
                        user_id="test",
                        user_name="test",
                        bluetooth_mac_address="00:00:00:00",
                        is_attending=True,
                        room="O502",
                        created_at=datetime(2024, 4, 7, 10, 0, 0).timestamp(),
                    ),
                    AttendanceLog(
                        user_id="test",
                        user_name="test",
                        bluetooth_mac_address="00:00:00:00",
                        is_attending=False,
                        room="O502",
                        created_at=datetime(2024, 4, 7, 12, 0, 0).timestamp(),
                    ),
                ],
                "expected": AttendanceWeeklySummary(
                    summaries=[
                        AttendanceSummary(
                            user_id="test",
                            day=datetime(2024, 4, 1),
                            attendances=[
                                Attendance(
                                    in_at=datetime(2024, 4, 1, 12, 0, 0).timestamp(),
                                    out_at=datetime(2024, 4, 1, 15, 0, 0).timestamp(),
                                    room="O502"
                                ),
                            ]
                        ),
                        AttendanceSummary(
                            user_id="test",
                            day=datetime(2024, 4, 7),
                            attendances=[
                                Attendance(
                                    in_at=datetime(2024, 4, 7, 10, 0, 0).timestamp(),
                                    out_at=datetime(2024, 4, 7, 12, 0, 0).timestamp(),
                                    room="O502"
                                ),
                            ]
                        )
                    ]
                )
            }
        ]

        for case in cases:
            with self.subTest(case["name"]):
                actual = AttendanceWeeklySummary.generate_weekly_summary(
                    attendance_logs=case["attending_logs"],
                    user_id=case["user_id"],
                    start_date=case["start_day"],
                )
                self.assertEqual(
                    actual.to_json(), 
                    case["expected"].to_json()
                )