import time
import datetime
import unittest
from dataclasses import dataclass
from typing import List, Optional

from app.domain.models.attendance import Attendance
from app.domain.models.attendance_log import AttendanceLog
from app.domain.models.attendance_summary import AttendanceSummary


class TestAttendanceSummary(unittest.TestCase):
    def test_generate_attendance_summary(self):
        cases = [
            {
                "name": "未入室（退出データあり）",
                "user_id": "test",
                "day": datetime.datetime(2024, 3, 1),
                "attendance_logs": [
                    AttendanceLog(
                        user_id="test",
                        user_name="test",
                        bluetooth_mac_address="00:00:00:00",
                        is_attending=False,
                        room="O502",
                        created_at=datetime.datetime(
                            2024, 3, 1, 12, 0, 0).timestamp(),
                    )
                ],
                "expected": AttendanceSummary(
                    user_id="test",
                    attendances=[],
                    day=datetime.datetime(2024, 3, 1)
                )
            },
            {
                "name": "入出済み 未退出",
                "user_id": "test",
                "day": datetime.datetime(2024, 3, 1),
                "attendance_logs": [
                    AttendanceLog(
                        user_id="test",
                        user_name="test",
                        bluetooth_mac_address="00:00:00:00",
                        is_attending=True,
                        room="O502",
                        created_at=datetime.datetime(
                            2024, 3, 1, 12, 0, 0).timestamp(),
                    )
                ],
                "expected": AttendanceSummary(
                    user_id="test",
                    day=datetime.datetime(2024, 3, 1),
                    attendances=[
                            Attendance(
                                in_at=datetime.datetime(
                                    2024, 3, 1, 12, 0, 0).timestamp(),
                                out_at=None,
                                room="O502"
                            )
                    ],
                )
            },
            {
                "name": "退出済み",
                "user_id": "test",
                "day": datetime.datetime(2024, 3, 1),
                "attendance_logs": [
                    AttendanceLog(
                        user_id="test",
                        user_name="test",
                        bluetooth_mac_address="00:00:00:00",
                        is_attending=True,
                        room="O502",
                        created_at=datetime.datetime(
                            2024, 3, 1, 12, 0, 0).timestamp(),
                    ),
                    AttendanceLog(
                        user_id="test",
                        user_name="test",
                        bluetooth_mac_address="00:00:00:00",
                        is_attending=False,
                        room="O502",
                        created_at=datetime.datetime(
                            2024, 3, 1, 12, 30, 0).timestamp(),
                    )
                ],
                "expected": AttendanceSummary(
                    user_id="test",
                    day=datetime.datetime(2024, 3, 1),
                    attendances=[
                            Attendance(
                                in_at=datetime.datetime(
                                    2024, 3, 1, 12, 0, 0).timestamp(),
                                out_at=datetime.datetime(
                                    2024, 3, 1, 12, 30, 0).timestamp(),
                                room="O502"
                            )
                    ],
                )
            },
            {
                "name": "複数の入退室",
                "user_id": "test",
                "day": datetime.datetime(2024, 3, 1),
                "attendance_logs": [
                    AttendanceLog(
                        user_id="test",
                        user_name="test",
                        bluetooth_mac_address="00:00:00:00",
                        is_attending=True,
                        room="O502",
                        created_at=datetime.datetime(
                            2024, 3, 1, 12, 0, 0).timestamp(),
                    ),
                    AttendanceLog(
                        user_id="test",
                        user_name="test",
                        bluetooth_mac_address="00:00:00:00",
                        is_attending=False,
                        room="O502",
                        created_at=datetime.datetime(
                            2024, 3, 1, 12, 30, 0).timestamp(),
                    ),
                    AttendanceLog(
                        user_id="test",
                        user_name="test",
                        bluetooth_mac_address="00:00:00:00",
                        is_attending=True,
                        room="O502",
                        created_at=datetime.datetime(
                            2024, 3, 1, 13, 0, 0).timestamp(),
                    ),
                    AttendanceLog(
                        user_id="test",
                        user_name="test",
                        bluetooth_mac_address="00:00:00:00",
                        is_attending=False,
                        room="O502",
                        created_at=datetime.datetime(
                            2024, 3, 1, 13, 30, 0).timestamp(),
                    )
                ],
                "expected": AttendanceSummary(
                    user_id="test",
                    day=datetime.datetime(2024, 3, 1),
                    attendances=[
                            Attendance(
                                in_at=datetime.datetime(
                                    2024, 3, 1, 12, 0, 0).timestamp(),
                                out_at=datetime.datetime(
                                    2024, 3, 1, 12, 30, 0).timestamp(),
                                room="O502"
                            ),
                        Attendance(
                                in_at=datetime.datetime(
                                    2024, 3, 1, 13, 0, 0).timestamp(),
                                out_at=datetime.datetime(
                                    2024, 3, 1, 13, 30, 0).timestamp(),
                                room="O502"
                            )
                    ],
                )
            },
            {
                "name": "O502 と N501 で入退室",
                "user_id": "test",
                "day": datetime.datetime(2024, 3, 1),
                "attendance_logs": [
                    AttendanceLog(
                        user_id="test",
                        user_name="test",
                        bluetooth_mac_address="00:00:00:00",
                        is_attending=True,
                        room="O502",
                        created_at=datetime.datetime(
                            2024, 3, 1, 12, 0, 0).timestamp(),
                    ),
                    AttendanceLog(
                        user_id="test",
                        user_name="test",
                        bluetooth_mac_address="00:00:00:00",
                        is_attending=False,
                        room="O502",
                        created_at=datetime.datetime(
                            2024, 3, 1, 12, 30, 0).timestamp(),
                    ),
                    AttendanceLog(
                        user_id="test",
                        user_name="test",
                        bluetooth_mac_address="00:00:00:00",
                        is_attending=True,
                        room="N501",
                        created_at=datetime.datetime(
                            2024, 3, 1, 13, 0, 0).timestamp(),
                    ),
                    AttendanceLog(
                        user_id="test",
                        user_name="test",
                        bluetooth_mac_address="00:00:00:00",
                        is_attending=False,
                        room="N501",
                        created_at=datetime.datetime(
                            2024, 3, 1, 13, 30, 0).timestamp(),
                    )
                ],
                "expected": AttendanceSummary(
                        user_id="test",
                        day=datetime.datetime(2024, 3, 1),
                        attendances=[
                            Attendance(
                                in_at=datetime.datetime(
                                    2024, 3, 1, 12, 0, 0).timestamp(),
                                out_at=datetime.datetime(
                                    2024, 3, 1, 12, 30, 0).timestamp(),
                                room="O502"
                            ),
                            Attendance(
                                in_at=datetime.datetime(
                                    2024, 3, 1, 13, 0, 0).timestamp(),
                                out_at=datetime.datetime(
                                    2024, 3, 1, 13, 30, 0).timestamp(),
                                room="N501"
                            )
                        ],
                    )
            },
        ]

        for case in cases:
            with self.subTest(name=case["name"]):
                actual = AttendanceSummary.generate_summary(
                    attendance_logs=case["attendance_logs"],
                    day=case["day"],
                    user_id=case["user_id"],
                )
                self.assertEqual(
                    actual.to_json(),
                    case["expected"].to_json()
                )
