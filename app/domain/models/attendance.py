from typing import Optional


class Attendance:
    def __init__(self, name: str, enter_at: float, left_at: Optional[float]):
        self.name = name
        self.enter_at = enter_at
        self.left_at = left_at

    def to_json(self):
        return {
            "name": self.name,
            "enterAt": int(self.enter_at),
            "leftAt": int(self.left_at) if self.left_at is not None else None,
        }
