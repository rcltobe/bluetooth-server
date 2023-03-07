from dataclasses import dataclass
from typing import Optional


@dataclass
class AttendanceLog:
    bluetooth_mac_address: str
    in_at: int
    out_at: Optional[int]
