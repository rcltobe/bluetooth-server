import asyncio
import datetime
import time
from concurrent.futures import ThreadPoolExecutor
from typing import List, Optional

from app.domain.models.bluetooth import DeviceState, BluetoothDevice
from app.domain.repository.device_repository import AbstractDeviceRepository
from app.domain.repository.device_state_repository import AbstractDeviceStateRepository, DeviceStateEntity
from app.infra.bluetooth import scan_device, ScanDeviceResult
from app.infra.repository import RepositoryContainer


class BluetoothService:
    def __init__(self,
                 device_repository: AbstractDeviceRepository = RepositoryContainer.device_repository,
                 state_repository: AbstractDeviceStateRepository = RepositoryContainer.device_state_repository,
                 ):
        self.device_repository = device_repository
        self.state_repository = state_repository

    async def add_device(self, device: BluetoothDevice):
        """
        ユーザーに紐付ける端末を追加
        """
        await self.device_repository.save(device)

    async def scan_devices(self, addresses: Optional[List[str]] = None):
        """
        Bluetooth端末を検索
        注意! この処理を同時に呼ぶと、正しい結果を得ることができないので、
        同時に呼び出してしまう可能性があるときは get_scan_results でキャッシュした情報を得る
        :param addresses: 検索する端末のMACアドレス, Noneの場合は、登録された端末を検索する
        """
        if addresses is None:
            devices = await self.device_repository.find_all()
            addresses = [device.address for device in devices]

        loop = asyncio.get_running_loop()
        executor = ThreadPoolExecutor()

        for address in addresses:
            state = await self.state_repository.find_last(address)
            if state is not None \
                    and state.created_at >= time.time() - 10 * 60 \
                    and state.state.value == DeviceState.FOUND.value:
                # 10分以内に発見されていたら、スキャンせずに、前の結果を使う
                continue

            result = await asyncio.ensure_future(loop.run_in_executor(executor, scan_device, address))
            state = DeviceState.FOUND if result.found else DeviceState.NOT_FOUND
            await self.update_state(address=address, state=state)
            print("{0:%Y-%m-%d %H:%M:%S}".format(datetime.datetime.now()), "[scan_devices]", result.to_json())

    async def get_scan_results(self, addresses: Optional[List[str]] = None) -> List[ScanDeviceResult]:
        if addresses is None:
            devices = await self.device_repository.find_all()
            addresses = [device.address for device in devices]

        results = []
        for address in addresses:
            last_state = await self.state_repository.find_last(address)
            if last_state is None:
                results.append(ScanDeviceResult(address=address, found=False))
                continue
            found = last_state.state.value == DeviceState.FOUND.value
            in_10m = last_state.created_at >= time.time() - 10 * 60
            results.append(ScanDeviceResult(address=address, found=found and in_10m))

        return results

    async def update_state(self, address: str, state: DeviceState):
        entity = await self.state_repository.find_last(address)

        # 前回と状態が変化していなければ、更新しない
        if entity is not None and entity.state.value == state.value:
            return

        new_entity = DeviceStateEntity(address=address, state=state)
        await self.state_repository.save(new_entity)
