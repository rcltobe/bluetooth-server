from __future__ import annotations

from typing import List, Optional

from app.domain.models.device import BluetoothDevice


class SpreadSheetUserEntity:
    def __init__(self, user_id: str, mac_address):
        self.user_id = user_id
        self.mac_address = mac_address

    @classmethod
    def from_csv(cls, csv: List[str]) -> Optional[SpreadSheetUserEntity]:
        if len(csv) < 4:
            return None

        return SpreadSheetUserEntity(
            user_id=csv[0],
            mac_address=csv[3]
        )

    def to_bluetooth_device(self) -> BluetoothDevice:
        return BluetoothDevice(
            user_id=self.user_id,
            address=self.mac_address
        )
