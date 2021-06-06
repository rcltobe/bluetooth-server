from __future__ import annotations

from typing import List, Optional


class BluetoothDevice:
    def __init__(self, address: str, user_id: str):
        """
        :param address: Bluetooth端末のMACアドレス
        :param user_id: この端末を結びつけるユーザーのID
        """
        self.address: str = address
        self.user_id: str = user_id

    def to_json(self):
        return {
            "address": self.address,
            "userId": self.user_id,
        }

    def to_csv(self) -> List[str]:
        return [self.address, self.user_id]

    @classmethod
    def from_csv(cls, csv: List[str]) -> Optional[BluetoothDevice]:
        if len(csv) < 2:
            return None

        return BluetoothDevice(
            address=csv[0],
            user_id=csv[1]
        )