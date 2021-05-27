from enum import Enum


class BluetoothDevice:
    def __init__(self, address: str, user_id: str):
        """
        :param address: Bluetooth端末のMACアドレス
        :param user_id: この端末を結びつけるユーザーのID
        """
        self.address: str = address
        self.user_id: str = user_id


class DeviceState(Enum):
    NOT_FOUND = 0
    FOUND = 1
