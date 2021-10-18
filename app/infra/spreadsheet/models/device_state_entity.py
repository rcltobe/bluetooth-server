from __future__ import annotations

from typing import Optional, List

from app.domain.models.device_state import DeviceState
from app.infra.spreadsheet.models.spreadsheet_entity import SpreadSheetEntity


class DeviceStateEntity(SpreadSheetEntity):
    """
    端末の検索履歴
    @:param address 端末のMACアドレス
    @:param found 端末が付近にあった場合はTrue
    """

    def __init__(self, id: str, address: str, found: bool, created_at: float):
        self.id = id
        self.created_at: float = created_at
        self.address: str = address
        self.found = found

    @classmethod
    def from_device_state(cls, state: DeviceState) -> DeviceStateEntity:
        return DeviceStateEntity(id=state.id, address=state.address, found=state.found, created_at=state.created_at)

    @classmethod
    def from_csv(cls, csv: List[str]) -> Optional[DeviceStateEntity]:
        if not cls.validate(attr_size=4, values=csv):
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

    def to_csv(self) -> List[str]:
        return [self.id, self.address, 1 if self.found else 0, int(self.created_at)]

    def to_device_state(self) -> DeviceState:
        return DeviceState(id=self.id, address=self.address, found=self.found, created_at=self.created_at)
