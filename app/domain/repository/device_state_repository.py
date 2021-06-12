from __future__ import annotations

import time
import uuid
from abc import abstractmethod
from typing import List, Optional

from app.domain.models.util import DateRange


class DeviceStateEntity:
    def __init__(self, address: str, found: bool, id: Optional[str] = None, created_at: Optional[float] = None):
        self.id = str(uuid.uuid4()) if id is None else id
        self.created_at: float = time.time() if created_at is None else created_at
        self.address: str = address
        self.found = found

    def in_range(self, range: Optional[DateRange]) -> bool:
        """
        このデータが指定された日時の範囲内にあるかを判定する。
        :return 日時の範囲内の場合 True を返す。 また、rangeがNoneの場合もTrueを返す
        """
        if range is None:
            return True

        return range.start <= self.created_at <= range.end

    def to_json(self):
        return {
            "id": self.id,
            "address": self.address,
            "found": self.found,
            "createdAt": int(self.created_at),
        }

    def to_csv(self) -> List[str]:
        return [self.id, self.address, 1 if self.found else 0, int(self.created_at)]

    @classmethod
    def from_csv(cls, csv: List[str]) -> Optional[DeviceStateEntity]:
        if len(csv) < 4:
            return None

        try:
            found = True if int(csv[2]) == 1 else False
        except ValueError:
            found = False

        return DeviceStateEntity(
            id=csv[0],
            address=csv[1],
            found=found,
            created_at=float(csv[3])
        )

    def before(self, states: List[DeviceStateEntity]) -> Optional[DeviceStateEntity]:
        """
        時系列順に並べたときの、同じ端末の前のDeviceStateEntityを取得
        """
        before = [state for state
                  in states
                  if state.address == self.address
                  and state.created_at < self.created_at
                  ]

        if len(before) == 0:
            return None
        before = sorted(before, key=lambda state: state.created_at)
        return before[0]

    def next(self, states: List[DeviceStateEntity]) -> Optional[DeviceStateEntity]:
        """
        時系列順に並べたときの、同じ端末の次のDeviceStateEntityを取得
        """
        after = [state for state
                 in states
                 if state.address == self.address
                 and state.created_at > self.created_at
                 ]
        if len(after) == 0:
            return None

        after = sorted(after, key=lambda state: state.created_at, reverse=True)

        return after[0]


class AbstractDeviceStateRepository:
    @abstractmethod
    async def find_all(self, date_range: Optional[DateRange] = None) -> List[DeviceStateEntity]:
        pass

    @abstractmethod
    async def find_last(self, address: str) -> Optional[DeviceStateEntity]:
        """
        更新日が最新の DeviceStateEntity を取得
        """
        pass

    @abstractmethod
    async def find_all_by_address(self, address: str) -> List[DeviceStateEntity]:
        pass

    @abstractmethod
    async def save(self, state: DeviceStateEntity):
        pass

    @abstractmethod
    async def delete(self, state_id: str):
        pass
