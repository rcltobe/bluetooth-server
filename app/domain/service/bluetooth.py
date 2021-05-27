import asyncio

from app.domain.models.bluetooth import DeviceState, BluetoothDevice
from app.domain.repository.device_repository import AbstractDeviceRepository
from app.domain.repository.device_state_repository import AbstractDeviceStateRepository, DeviceStateEntity
from app.infra.bluetooth import scan_device


class BluetoothService:
    def __init__(self, device_repository: AbstractDeviceRepository, state_repository: AbstractDeviceStateRepository):
        self.device_repository = device_repository
        self.state_repository = state_repository

    async def add_device(self, device: BluetoothDevice):
        """
        ユーザーに紐付ける端末を追加
        """
        await self.device_repository.save(device)

    async def scan(self):
        """
        登録されているBluetooth端末を検索
        """
        devices = await self.device_repository.find_all()
        addresses = [device.address for device in devices]
        scan_results = [scan_device(address) for address in addresses]

        tasks = []
        for result in scan_results:
            state = DeviceState.FOUND if result.found else DeviceState.NOT_FOUND
            entity = DeviceStateEntity(result.address, state)
            tasks.append(self.state_repository.save(entity))

        await asyncio.gather(*[tasks])
