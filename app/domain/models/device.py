from __future__ import annotations


class BluetoothDevice:
    def __init__(self, address: str, user_id: str):
        """
        :param address: Bluetooth端末のMACアドレス
        :param user_id: この端末を結びつけるユーザーのID
        """
        self.address: str = address
        self.user_id: str = user_id