from __future__ import annotations

from typing import List, Optional

from app.domain.models.device import BluetoothDevice
from app.infra.spreadsheet.models.spreadsheet_entity import SpreadSheetEntity


class UserEntity(SpreadSheetEntity):
    """
    SpreadSheetのセルの形式
    (id, 名前, 学年, 端末のMACアドレス)
    """

    def __init__(self, user_id: str, mac_address):
        self.user_id = user_id
        self.mac_address = mac_address

    @classmethod
    def from_csv(cls, csv: List[str]) -> Optional[UserEntity]:
        if not cls.validate(attr_size=4, values=csv, require_filled=False):
            return None

        if len(csv[0]) == 0 or len(csv[3]) == 0:
            return None

        return UserEntity(
            user_id=csv[0],
            mac_address=csv[3]
        )

    def to_bluetooth_device(self) -> BluetoothDevice:
        return BluetoothDevice(
            user_id=self.user_id,
            address=self.mac_address
        )
