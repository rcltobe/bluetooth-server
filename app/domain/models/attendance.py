from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Attendance:
    in_at: int
    out_at: Optional[int]
    room: str

    def to_json(self):
        return {
            "in_at": self.in_at,
            "out_at": self.out_at,
            "room": self.room,
        }

    def is_attending(self):
        return self.out_at is None 
    
    def get_attendance_time_in_sec(self):
        if self.out_at is None:
            return 0
        return self.out_at - self.in_at 
    
    def get_in_at_datetime(self):
        return datetime.fromtimestamp(self.in_at)