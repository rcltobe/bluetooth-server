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
                "day": datetime.datetime(2024, 3, 1),
                "expected": [
                    AttendanceSummary(
                        user_id="test",
                        attendances=[]
                    )
                ]
            },
            {
                "name": "入出済み 未退出",
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
                "day": datetime.datetime(2024, 3, 1),
                "expected": [
                    AttendanceSummary(
                        user_id="test",
                        attendances=[
                            Attendance(
                                in_at=datetime.datetime(2024, 3, 1, 12, 0, 0).timestamp(),
                                out_at=None,
                                room="O502"
                            )
                        ],
                    )
                ]
            },
            {
                "name": "退出済み",
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
                "day": datetime.datetime(2024, 3, 1),
                "expected": [
                    AttendanceSummary(
                        user_id="test",
                        attendances=[
                            Attendance(
                                in_at=datetime.datetime(2024, 3, 1, 12, 0, 0).timestamp(),
                                out_at=datetime.datetime(2024, 3, 1, 12, 30, 0).timestamp(),
                                room="O502"
                            )
                        ],
                    )
                ]
            },
            {
                "name": "複数の入退室",
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
                "day": datetime.datetime(2024, 3, 1),
                "expected": [
                    AttendanceSummary(
                        user_id="test",
                        attendances=[
                            Attendance(
                                in_at=datetime.datetime(2024, 3, 1, 12, 0, 0).timestamp(),
                                out_at=datetime.datetime(2024, 3, 1, 12, 30, 0).timestamp(),
                                room="O502"
                            ),
                            Attendance(
                                in_at=datetime.datetime(2024, 3, 1, 13, 0, 0).timestamp(),
                                out_at=datetime.datetime(2024, 3, 1, 13, 30, 0).timestamp(),
                                room="O502"
                            )
                        ],
                    )
                ],
            },
            {
                "name": "O502 と N501 で入退室",
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
                "day": datetime.datetime(2024, 3, 1),
                "expected": [
                    AttendanceSummary(
                        user_id="test",
                        attendances=[
                            Attendance(
                                in_at=datetime.datetime(2024, 3, 1, 12, 0, 0).timestamp(),
                                out_at=datetime.datetime(2024, 3, 1, 12, 30, 0).timestamp(),
                                room="O502"
                            ),
                            Attendance(
                                in_at=datetime.datetime(2024, 3, 1, 13, 0, 0).timestamp(),
                                out_at=datetime.datetime(2024, 3, 1, 13, 30, 0).timestamp(),
                                room="N501"
                            )
                        ],
                    )
                ],
            },
        ]

        for case in cases:
            with self.subTest(name=case["name"]):
                actual = AttendanceSummary.generate_summary(
                    attendance_logs=case["attendance_logs"],
                    day=case["day"]
                )
                self.assertEqual(
                    [summary.to_json() for summary in actual],
                    [summary.to_json() for summary in case["expected"]]
                )