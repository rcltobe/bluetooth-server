from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Optional


@dataclass
class AttendanceLog:
    user_id: str
    bluetooth_mac_address: str
    in_at: int
    out_at: Optional[int]

    def update_log(self, is_attending: bool):
        has_out_log = self.out_at is not None
        # 退出した後に再度入室したら、退出の記録を削除する
        if is_attending and has_out_log:
            self.out_at = None
        # 退出した（退出時間が更新されないように、退出記録がなかった場合だけ行う）
        elif not is_attending and not has_out_log:
            self.out_at = int(time.time())

    def to_json(self):
        return {
            "user_id": self.user_id,
            "bluetooth_address": self.bluetooth_mac_address,
            "in": self.in_at,
            "out": self.out_at
        }

    def to_csv(self):
        return [self.user_id, self.bluetooth_mac_address, self.in_at, self.out_at]
