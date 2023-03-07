from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Optional

from app.domain.models.user import User


@dataclass
class AttendanceLog:
    user_id: str
    user_name: str
    bluetooth_mac_address: str
    in_at: int
    out_at: Optional[int]

    def update_log(self, is_attending: bool, now=time.time()):
        has_out_log = self.out_at is not None
        # 退出した後に再度入室したら、退出の記録を削除する
        if is_attending and has_out_log:
            self.out_at = None
        # 退出した（退出時間が更新されないように、退出記録がなかった場合だけ行う）
        elif not is_attending and not has_out_log:
            self.out_at = int(now)

    def to_json(self):
        return {
            "user_id": self.user_id,
            "user_name": self.user_name,
            "bluetooth_address": self.bluetooth_mac_address,
            "in": self.in_at,
            "out": self.out_at
        }

    def to_csv(self):
        if self.out_at is not None:
            return [self.user_id, self.user_name, self.bluetooth_mac_address, self.in_at, self.out_at]
        else:
            return [self.user_id, self.user_name, self.bluetooth_mac_address, self.in_at]

    @staticmethod
    def from_user(user: User, in_at: int, out_at: Optional[int]) -> AttendanceLog:
        return AttendanceLog(
            user_id=user.user_id,
            user_name=user.user_name,
            bluetooth_mac_address=user.address,
            in_at=in_at,
            out_at=out_at
        )

    @staticmethod
    def create_attendance_log(
            prev_attendance_log: Optional[AttendanceLog],
            is_found: bool,
            user: User,
            now=time.time()
    ) -> Optional[AttendanceLog]:
        # まだ出席していない
        if prev_attendance_log is None and not is_found:
            return None

        if prev_attendance_log is None:
            attendance_log = AttendanceLog(
                user_id=user.user_id,
                user_name=user.user_name,
                bluetooth_mac_address=user.address,
                in_at=int(now),
                out_at=None,
            )
        else:
            prev_attendance_log.update_log(is_found, now=now)
            attendance_log = prev_attendance_log

        return attendance_log
