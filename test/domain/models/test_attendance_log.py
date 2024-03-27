import time
import unittest
from dataclasses import dataclass
from typing import Optional

from app.domain.models.attendance_log import AttendanceLog
from app.domain.models.user import User


class TestAttendanceLog(unittest.TestCase):
    def test_update_attendance_log(self):
        test_user = User(address="00:00:00:00", user_name="test", user_id="test")
        in_at = int(time.time())
        out_at = int(time.time()) + 1000
        cases = [
            UpdateAttendanceLogTestCase(
                case="退出",
                is_found=False,
                base=AttendanceLog.from_user(user=test_user, in_at=in_at, out_at=None),
                expect=AttendanceLog.from_user(user=test_user, in_at=in_at, out_at=out_at)
            ),
            UpdateAttendanceLogTestCase(
                case="退出後に入室",
                is_found=True,
                base=AttendanceLog.from_user(user=test_user, in_at=in_at, out_at=out_at),
                expect=AttendanceLog.from_user(user=test_user, in_at=in_at, out_at=None)
            ),
        ]

        for case in cases:
            case.base.update_log(is_attending=case.is_found, now=out_at)
            self.assertEqual(case.base.created_at, case.expect.created_at)
            self.assertEqual(case.base.out_at, case.expect.out_at)

    def test_create_attendance_log(self):
        test_user = User(address="00:00:00:00", user_name="test", user_id="test")
        now = int(time.time())
        in_at = int(time.time())
        out_at = int(time.time()) + 1000
        cases = [
            CreateAttendanceLogTestCase(
                case="出席",
                user=test_user,
                is_found=True,
                prev_attendance_log=None,
                expect=AttendanceLog.from_user(user=test_user, in_at=now, out_at=None)
            ),
            CreateAttendanceLogTestCase(
                case="退出",
                user=test_user,
                is_found=False,
                prev_attendance_log=AttendanceLog.from_user(user=test_user, in_at=in_at, out_at=None),
                expect=AttendanceLog.from_user(user=test_user, in_at=in_at, out_at=now)
            ),
            CreateAttendanceLogTestCase(
                case="退出後に入室",
                user=test_user,
                is_found=True,
                prev_attendance_log=AttendanceLog.from_user(user=test_user, in_at=in_at, out_at=out_at),
                expect=AttendanceLog.from_user(user=test_user, in_at=in_at, out_at=None)
            ),
            CreateAttendanceLogTestCase(
                case="未出席",
                user=test_user,
                is_found=False,
                prev_attendance_log=None,
                expect=None
            ),
        ]

        for case in cases:
            result = AttendanceLog.create_attendance_log(
                prev_attendance_log=case.prev_attendance_log,
                user=case.user,
                is_found=case.is_found,
                now=now
            )

            self.assertEqual(case.expect is not None, result is not None)
            if result is None:
                continue

            self.assertEqual(case.expect.user_id, result.user_id, case.case)
            self.assertEqual(case.expect.user_name, result.user_name, case.case)
            self.assertEqual(case.expect.created_at, result.created_at, case.case)
            self.assertEqual(case.expect.out_at, result.out_at, case.case)


@dataclass
class UpdateAttendanceLogTestCase:
    case: str
    base: AttendanceLog
    is_found: bool
    expect: AttendanceLog


@dataclass
class CreateAttendanceLogTestCase:
    case: str
    prev_attendance_log: Optional[AttendanceLog]
    user: User
    is_found: bool
    expect: Optional[AttendanceLog]
