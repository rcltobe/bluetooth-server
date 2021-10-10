import logging
import time
from typing import List, Optional

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

    async def scan_devices(self, addresses: Optional[List[str]] = None):
        """
        Bluetooth端末を検索

        【注意】
        この処理を同時に呼ぶと、正しい結果を得ることができない

        :param addresses: 検索する端末のMACアドレス, Noneの場合は、登録された端末を検索する
        """
        logger = logging.getLogger(__name__)

        # 登録されたすべての端末のMACアドレスを取得
        if addresses is None:
            devices = await self.device_repository.find_all()
            addresses = [device.address for device in devices]

        logger.info(f"SCAN FOR {addresses}")

        # 端末をBluetoothでスキャンする
        for address in addresses:
            # 10分以内に発見されていたら、スキャンせずに、前の結果を使う
            state = await self.state_repository.find_last(address)
            if state is not None \
                    and state.created_at >= time.time() - self.INTERVAL_SCAN \
                    and state.found:
                continue

            # スキャン
            result = scan_device(address=address)
            await self.update_state(address=address, found=result.found)
            logger.info(f"DEVICE SCANNED {result.to_json()}")

    async def update_state(self, address: str, found: bool):
        prev_entity = await self.state_repository.find_last(address)
        new_entity = DeviceStateEntity(address=address, found=found)
        # 初回のデータ、または、端末を発見した場合は更新する。
        if prev_entity is None or found:
            await self.state_repository.save(new_entity)
            return

        # 前回と状態が変化していれば更新する
        if prev_entity.found != found:
            await self.state_repository.save(new_entity)
            return
