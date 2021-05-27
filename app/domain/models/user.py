import uuid
from typing import Optional


class Grade:
    B4 = "B4"
    M1 = "M1"
    M2 = "M2"
    GRAD = "Grad"
    Prof = "Prof"


class User:
    def __init__(self, name: str, grade: Optional[Grade], id: str = str(uuid.uuid4())):
        self.id = id
        self.name: str = name
        self.grade: Optional[Grade] = grade
