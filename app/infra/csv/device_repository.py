import csv
import os
from typing import List

from app.domain.models.bluetooth import BluetoothDevice
from app.domain.repository.device_repository import AbstractDeviceRepository


class CsvDeviceRepository(AbstractDeviceRepository):
    _FILE_PATH = f"{os.curdir}/data/devices.csv"

    async def find_all(self) -> List[BluetoothDevice]:
        if not os.path.exists(self._FILE_PATH):
            return []

        with open(self._FILE_PATH) as file:
            reader = csv.reader(file)
            rows = [row for row in reader]
        return [BluetoothDevice.from_csv(row) for row in rows]

    async def find_by_user_id(self, user_id: str) -> List[BluetoothDevice]:
        return [user for user in await self.find_all() if user.user_id == user_id]

    async def save(self, device: BluetoothDevice):
        with open(self._FILE_PATH, 'a') as file:
            writer = csv.writer(file)
            writer.writerow(device.to_csv())

    async def delete_all_by_user_id(self, user_id: str):
        with open(self._FILE_PATH, 'r') as inp, open(self._FILE_PATH, 'w') as out:
            writer = csv.writer(out)
            reader = csv.reader(inp)
            for row in reader:
                device = BluetoothDevice.from_csv(row)
                if device.user_id != user_id:
                    writer.writerow(row)
