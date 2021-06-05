from __future__ import annotations

import time
import uuid
from typing import Optional, List


class BodyTemperature:
    def __init__(self,
                 temperature: float,
                 user_id: str,
                 data_id: Optional[str] = None,
                 created_at: Optional[int] = None
                 ):
        self.id = str(uuid.uuid4()) if data_id is None else data_id
        self.temperature = temperature
        self.user_id = user_id
        self.created_at = int(time.time()) if created_at is None else created_at

    def to_json(self):
        return {
            "id": self.id,
            "temperature": self.temperature,
            "user_id": self.user_id,
            "created_at": self.created_at,
        }

    def to_csv(self) -> List[str]:
        return [self.id, self.temperature, self.user_id, self.created_at]

    @classmethod
    def from_csv(cls, csv: List[str]) -> Optional[BodyTemperature]:
        if len(csv) < 4:
            return None
        try:
            temperature = float(csv[1])
            created_at = int(csv[3])
        except ValueError:
            return None

        return BodyTemperature(
            data_id=csv[0],
            temperature=temperature,
            user_id=csv[2],
            created_at=created_at
        )
