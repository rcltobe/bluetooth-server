from typing import List

from app.domain.models.bluetooth import BluetoothDevice
from app.domain.repository.device_repository import AbstractDeviceRepository


class InMemoryDeviceRepository(AbstractDeviceRepository):
    _devices: List[BluetoothDevice] = []

    async def find_all(self) -> List[BluetoothDevice]:
        return InMemoryDeviceRepository._devices

    async def find_by_user_id(self, user_id: str) -> List[BluetoothDevice]:
        return list(
            filter(
                lambda device: device.user_id == user_id,
                InMemoryDeviceRepository._devices
            )
        )

    async def save(self, device: BluetoothDevice):
        InMemoryDeviceRepository._devices.append(device)
