import csv
import os
from typing import List

from app.domain.models.bluetooth import BluetoothDevice
from app.domain.repository.device_repository import AbstractDeviceRepository
from app.infra.csv.csv_util import delete_row


class CsvDeviceRepository(AbstractDeviceRepository):
    INDEX_ADDRESS = 0
    _FILE_PATH = f"{os.curdir}/data/devices.csv"

    async def find_all(self) -> List[BluetoothDevice]:
        if not os.path.exists(self._FILE_PATH):
            return []

        with open(self._FILE_PATH) as file:
            reader = csv.reader(file)
            rows = [row for row in reader]

        return [
            result
            for result in [BluetoothDevice.from_csv(row) for row in rows]
            if result is not None
        ]

    async def find_by_user_id(self, user_id: str) -> List[BluetoothDevice]:
        return [user for user in await self.find_all() if user.user_id == user_id]

    async def save(self, device: BluetoothDevice):
        mode = 'a' if os.path.exists(self._FILE_PATH) else 'w'
        with open(self._FILE_PATH, mode) as file:
            writer = csv.writer(file)
            writer.writerow(device.to_csv())

    async def delete(self, address: str):
        if not os.path.exists(self._FILE_PATH):
            return

        def check(csv: List[str]) -> bool:
            return csv[self.INDEX_ADDRESS] == address

        delete_row(self._FILE_PATH, check)

    async def delete_all_by_user_id(self, user_id: str):
        def _check(row: List[str]) -> bool:
            device = BluetoothDevice.from_csv(row)
            if device is None:
                return False
            return device.user_id == user_id

        delete_row(
            file_name=self._FILE_PATH,
            check=_check
        )
