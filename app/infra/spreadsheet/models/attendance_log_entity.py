from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from app.domain.models.attendance_log import AttendanceLog
from app.infra.spreadsheet.models.spreadsheet_entity import SpreadSheetEntity


@dataclass
class AttendanceLogEntity(SpreadSheetEntity):
    user_id: str
    bluetooth_mac_address: str
    in_at: int
    out_at: Optional[int]

    @classmethod
    def from_attendance_log(cls, attendance_log: AttendanceLog) -> AttendanceLogEntity:
        return AttendanceLogEntity(
            user_id=attendance_log.user_id,
            bluetooth_mac_address=attendance_log.bluetooth_mac_address,
            in_at=attendance_log.in_at,
            out_at=attendance_log.out_at
        )

    @classmethod
    def from_csv(cls, csv: list[str]) -> AttendanceLogEntity:
        return AttendanceLogEntity(
            user_id=csv[0],
            bluetooth_mac_address=csv[1],
            in_at=int(csv[2]),
            out_at=int(csv[3]) if len(csv) >= 4 and csv[3] != "" else None
        )

    def to_attendance_log(self):
        return AttendanceLog(
            user_id=self.user_id,
            bluetooth_mac_address=self.bluetooth_mac_address,
            in_at=self.in_at,
            out_at=self.out_at,
        )
