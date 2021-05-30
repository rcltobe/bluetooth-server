import asyncio
from typing import List, Optional

from app.domain.models.bluetooth import DeviceState, BluetoothDevice
from app.domain.repository.device_repository import AbstractDeviceRepository
from app.domain.repository.device_state_repository import AbstractDeviceStateRepository, DeviceStateEntity
from app.infra.bluetooth import scan_device
from app.infra.in_memory.device_repository import InMemoryDeviceRepository
from app.infra.in_memory.device_state_repository import InMemoryDeviceStateRepository


class BluetoothService:
    def __init__(self,
                 device_repository: AbstractDeviceRepository = InMemoryDeviceRepository(),
                 state_repository: AbstractDeviceStateRepository = InMemoryDeviceStateRepository(),
                 ):
        self.device_repository = device_repository
        self.state_repository = state_repository

    async def add_device(self, device: BluetoothDevice):
        """
        ユーザーに紐付ける端末を追加
        """
        await self.device_repository.save(device)

    async def _scan_device(self, address: str):
        """
        Bluetooth端末を検索
        :param address: 検索する端末のMACアドレス
        """
        result = await scan_device(address)
        state = DeviceState.FOUND if result.found else DeviceState.NOT_FOUND
        await self.update_state(address=address, state=state)
        return result.to_json()

    async def scan_devices(self, addresses: Optional[List[str]]):
        if addresses is None:
            devices = await self.device_repository.find_all()
            addresses = [device.address for device in devices]

        tasks = []
        for address in addresses:
            tasks.append(asyncio.ensure_future(self._scan_device(address)))

        return await asyncio.gather(*tasks)

    async def update_state(self, address: str, state: DeviceState):
        entity = await self.state_repository.find_last(address)

        # 前回と状態が変化していなければ、更新しない
        if entity is not None and entity.state.value == state.value:
            return

        new_entity = DeviceStateEntity(address=address, state=state)
        await self.state_repository.save(new_entity)
