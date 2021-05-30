from __future__ import annotations

import uuid
from enum import Enum
from typing import Optional


class Grade(Enum):
    B4 = "B4"
    M1 = "M1"
    M2 = "M2"
    GRAD = "Grad"
    Prof = "Prof"

    @classmethod
    def value_of(cls, target_value: Optional[str]) -> Optional[Grade]:
        if target_value is None:
            return None

        for e in Grade:
            if e.value == target_value:
                return e
        return None


class User:
    def __init__(self, name: str, grade: Optional[Grade], id: str = str(uuid.uuid4())):
        self.id = id
        self.name: str = name
        self.grade: Optional[Grade] = grade

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "grade": self.grade
        }
