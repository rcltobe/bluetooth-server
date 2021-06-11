import datetime
import time
from typing import List, Optional

from app.domain.models.bluetooth import BluetoothDevice
from app.domain.repository.device_repository import AbstractDeviceRepository
from app.domain.repository.device_state_repository import AbstractDeviceStateRepository, DeviceStateEntity
from app.infra.bluetooth import scan_device
from app.infra.repository import RepositoryContainer


class ScanResultEntity:
    def __init__(self, user_id: str, address: str, found: bool):
        self.user_id = user_id
        self.address = address
        self.found = found

    def to_json(self):
        return {
            "user_id": self.user_id,
            "address": self.address,
            "found": self.found
        }


class DeviceService:
    def __init__(self,
                 device_repository: AbstractDeviceRepository = RepositoryContainer.device_repository,
                 state_repository: AbstractDeviceStateRepository = RepositoryContainer.device_state_repository,
                 ):
        self.device_repository = device_repository
        self.state_repository = state_repository

    INTERVAL_SCAN = 10 * 60  # 端末を発見してから次に検索するまでの間隔
    INTERVAL_UPDATE = 10 * 60  # 状態が変化していないときに、更新する間隔

    async def get_devices(self) -> List[BluetoothDevice]:
        return await self.device_repository.find_all()

    async def add_device(self, user_id: str, address: str):
        device = BluetoothDevice(address=address, user_id=user_id)
        await self.device_repository.save(device)

    async def delete_device(self, address: str):
        await self.device_repository.delete(address)

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

        for address in addresses:
            state = await self.state_repository.find_last(address)
            if state is not None \
                    and state.created_at >= time.time() - self.INTERVAL_SCAN \
                    and state.found:
                # 10分以内に発見されていたら、スキャンせずに、前の結果を使う
                continue

            result = scan_device(address=address)
            await self.update_state(address=address, found=result.found)
            print("{0:%Y-%m-%d %H:%M:%S}".format(datetime.datetime.now()), "[scan_devices]", result.to_json())

    async def get_scan_results(self) -> List[ScanResultEntity]:
        devices = await self.device_repository.find_all()

        results: List[ScanResultEntity] = []
        for device in devices:
            address = device.address
            last_state = await self.state_repository.find_last(address)
            if last_state is None:
                results.append(ScanResultEntity(address=address, found=False, user_id=device.user_id))
                continue

            # 10分以内に端末を発見していれば、スキャンしない
            in_10m = last_state.created_at >= time.time() - self.INTERVAL_SCAN
            entity = ScanResultEntity(
                address=address,
                user_id=device.user_id,
                found=last_state.found and in_10m,
            )
            results.append(entity)

        return results

    async def update_state(self, address: str, found: bool):
        entity = await self.state_repository.find_last(address)

        # 前回と状態が変化していなければ、更新しない
        if entity is not None \
                and entity.found == found \
                and entity.created_at >= time.time() - self.INTERVAL_UPDATE:
            return

        new_entity = DeviceStateEntity(address=address, found=found)
        await self.state_repository.save(new_entity)
