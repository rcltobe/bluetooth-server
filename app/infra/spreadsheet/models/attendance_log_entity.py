from __future__ import annotations

from dataclasses import dataclass
from typing import List
from typing import Optional

from app.domain.models.attendance_log import AttendanceLog
from app.infra.spreadsheet.models.spreadsheet_entity import SpreadSheetEntity


@dataclass
class AttendanceLogEntity(SpreadSheetEntity):
    user_id: str
    user_name: str
    bluetooth_mac_address: str
    in_at: int
    out_at: Optional[int]

    @classmethod
    def from_attendance_log(cls, attendance_log: AttendanceLog) -> AttendanceLogEntity:
        return AttendanceLogEntity(
            user_id=attendance_log.user_id,
            bluetooth_mac_address=attendance_log.bluetooth_mac_address,
            in_at=attendance_log.created_at,
            out_at=attendance_log.out_at
        )

    @classmethod
    def from_csv(cls, csv: List[str]) -> AttendanceLogEntity:
        return AttendanceLogEntity(
            user_id=csv[0],
            user_name=csv[1],
            bluetooth_mac_address=csv[2],
            in_at=int(csv[3]),
            out_at=int(csv[4]) if len(csv) >= 5 and csv[4] != "" else None
        )

    def to_attendance_log(self):
        return AttendanceLog(
            user_id=self.user_id,
            user_name=self.user_name,
            bluetooth_mac_address=self.bluetooth_mac_address,
            created_at=self.in_at,
            out_at=self.out_at,
        )
