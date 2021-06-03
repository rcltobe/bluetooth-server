from __future__ import annotations

import uuid
from enum import Enum
from typing import Optional, List


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
    def __init__(self, name: str, grade: Optional[Grade], user_id: Optional[str] = None):
        self.id = user_id if user_id is not None else str(uuid.uuid4())
        self.name: str = name
        self.grade: Optional[Grade] = grade

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "grade": self.grade
        }

    def to_csv(self) -> List[str]:
        return [self.id, self.name, self.grade]

    @classmethod
    def from_csv(cls, csv: List[str]) -> User:
        grade = Grade.value_of(csv[2]) if len(csv) > 2 else None
        return User(
            user_id=csv[0],
            name=csv[1],
            grade=grade
        )
