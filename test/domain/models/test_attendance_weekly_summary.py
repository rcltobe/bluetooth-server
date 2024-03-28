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
                "start_day": datetime(2024, 4, 1),  # 月曜日
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
                                    in_at=datetime(
                                        2024, 4, 1, 12, 0, 0).timestamp(),
                                    out_at=datetime(
                                        2024, 4, 1, 15, 0, 0).timestamp(),
                                    room="O502"
                                ),
                            ]
                        ),
                        AttendanceSummary(
                            user_id="test",
                            day=datetime(2024, 4, 7),
                            attendances=[
                                Attendance(
                                    in_at=datetime(
                                        2024, 4, 7, 10, 0, 0).timestamp(),
                                    out_at=datetime(
                                        2024, 4, 7, 12, 0, 0).timestamp(),
                                    room="O502"
                                ),
                            ]
                        )
                    ]
                )
            },
            {
                "name": "一度も出席をしていない",
                "user_id": "test",
                "start_day": datetime(2024, 4, 1),  # 月曜日
                "attending_logs": [],
                "expected": AttendanceWeeklySummary(
                    summaries=[]
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

    def test_to_csv(self):
        cases = [
            {
                "name": "1日も出席していない",
                "start_date": datetime(2024, 4, 1),
                "duration": 7,
                "weekly_summary": AttendanceWeeklySummary(
                    summaries=[]
                ),
                "expected": [0, 0, 0, 0, 0, 0, 0, None, None]
            },
            {
                "name": "1週間の出席時間をCSVに変換",
                "start_date": datetime(2024, 4, 1),
                "duration": 7,
                "weekly_summary": AttendanceWeeklySummary(
                    summaries=[
                        AttendanceSummary(
                            day=datetime(2024, 4, 1),
                            user_id="test",
                            attendances=[
                                Attendance(
                                    in_at=datetime(2024, 4, 1, 12, 0, 0).timestamp(),
                                    out_at=datetime(2024, 4, 1, 15, 0, 0).timestamp(),
                                    room="O502"
                                ),
                            ],
                        ),
                        AttendanceSummary(
                            day=datetime(2024, 4, 7),
                            user_id="test",
                            attendances=[
                                Attendance(
                                    in_at=datetime(2024, 4, 7, 10, 0, 0).timestamp(),
                                    out_at=datetime(2024, 4, 7, 12, 0, 0).timestamp(),
                                    room="O502"
                                ),
                            ],
                        )
                    ],
                ),
                "expected": [10800, 0, 0, 0, 0, 0, 7200, None, None],
            },
            {
                "name": "火曜日の出席時間をCSVに変換",
                "start_date": datetime(2024, 4, 1),
                "duration": 7,
                "weekly_summary": AttendanceWeeklySummary(
                    summaries=[
                        AttendanceSummary(
                            day=datetime(2024, 4, 2),
                            user_id="test",
                            attendances=[
                                Attendance(
                                    in_at=datetime(2024, 4, 1, 12, 0, 0).timestamp(),
                                    out_at=datetime(2024, 4, 1, 15, 0, 0).timestamp(),
                                    room="O502"
                                ),
                            ],
                        ),
                    ],
                ),
                "expected": [0, 3 * 60 * 60, 0, 0, 0, 0, 0, 12, 0],
            }
        ]

        for case in cases:
            with self.subTest(case["name"]):
                actual = case["weekly_summary"].to_csv(
                    start_date=case["start_date"],
                    duration=case["duration"]
                )
                self.assertEqual(
                    actual,
                    case["expected"]
                )