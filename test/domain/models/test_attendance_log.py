import time
import datetime
import unittest
from dataclasses import dataclass
from typing import List, Optional

from app.domain.models.attendance_log import AttendanceLog
from app.domain.models.user import User


class TestAttendanceLog(unittest.TestCase):
    def test_create_attendance_log(self):
        test_user = User(
            address="00:00:00:00",
            user_name="test", 
            user_id="test"
        )

        cases = [
            CreateAttendanceLogTestCase(
                case="出席",
                user=test_user,
                is_found=True,
                now=_timestamp_from_datetime(datetime.datetime(2024, 3, 1, 12, 0, 0)),
                prev_attendance_logs=None,
                expect=AttendanceLog.from_user(
                    user=test_user,
                    created_at=_timestamp_from_datetime(datetime.datetime(2024, 3, 1, 12, 0, 0)),
                    room="O501",
                    is_attending=True,
                )
            ),
            CreateAttendanceLogTestCase(
                case="退出",
                user=test_user,
                is_found=False,
                now=_timestamp_from_datetime(datetime.datetime(2024, 3, 1, 15, 0, 0)),
                prev_attendance_logs=[
                    AttendanceLog.from_user(
                        user=test_user,
                        is_attending=True,
                        room="O501",
                        created_at=_timestamp_from_datetime(datetime.datetime(2024, 3, 1, 12, 0, 0)),
                    ),
                ],
                expect=AttendanceLog.from_user(
                    user=test_user,
                    is_attending=False,
                    room="O501",
                    created_at=_timestamp_from_datetime(datetime.datetime(2024, 3, 1, 15, 0, 0)),
                )
            ),
            CreateAttendanceLogTestCase(
                case="退出後に入室",
                user=test_user,
                is_found=True,
                now=datetime.datetime(2024, 3, 1, 17, 0, 0),
                prev_attendance_logs=[
                    AttendanceLog.from_user(
                        user=test_user, 
                        created_at=_timestamp_from_datetime(datetime.datetime(2024, 3, 1, 12, 0, 0)), 
                        room="O501",
                        is_attending=True,
                    ),
                    AttendanceLog.from_user(
                        user=test_user, 
                        created_at=_timestamp_from_datetime(datetime.datetime(2024, 3, 1, 15, 0, 0)),
                        room="O501",
                        is_attending=False,
                    ),
                    AttendanceLog.from_user(
                        user=test_user, 
                        created_at=_timestamp_from_datetime(datetime.datetime(2024, 3, 1, 16, 0, 0)),
                        room="O501",
                        is_attending=False,
                    ),
                ],
                expect=AttendanceLog.from_user(
                    user=test_user, 
                    created_at=_timestamp_from_datetime(datetime.datetime(2024, 3, 1, 17, 0, 0)),
                    room="O501",
                    is_attending=True,
                )
            ),
            CreateAttendanceLogTestCase(
                case="未出席",
                user=test_user,
                is_found=False,
                now=_timestamp_from_datetime(datetime.datetime(2024, 3, 1, 12, 0, 0)),
                prev_attendance_logs=None,
                expect=None,
            ),
        ]

        for case in cases:
            actual = AttendanceLog.create_attendance_log(
                prev_attendance_logs=case.prev_attendance_logs,
                user=case.user,
                is_found=case.is_found,
                room="O501",
                now=case.now,
            )

            self.assertEqual(case.expect is not None, actual is not None)
            if actual is None:
                continue

            self.assertEqual(
                case.expect.user_id, 
                actual.user_id,
                case.case
            )
            self.assertEqual(
                case.expect.user_name,
                actual.user_name, 
                case.case
            )
            self.assertEqual(
                case.expect.is_attending,
                actual.is_attending, 
                case.case
            )
            self.assertEqual(
                _timestamp_from_datetime(case.expect.created_at),
                _timestamp_from_datetime(actual.created_at), 
                case.case
            )

def _timestamp_from_datetime(dt: datetime.datetime) -> int:
    if type(dt) is int:
        return dt
    return int(time.mktime(dt.timetuple()))
@dataclass
class CreateAttendanceLogTestCase:
    case: str
    user: User
    is_found: bool
    now: int 
    prev_attendance_logs: Optional[List[AttendanceLog]]
    expect: Optional[AttendanceLog]