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
    """
    端末のスキャン処理と、スキャン結果の保存を行う
    SpreadSheetに過度なアクセスをしないように実装されている。
    """

    def __init__(self,
                 device_repository: AbstractDeviceRepository = RepositoryContainer.device_repository,
                 state_repository: AbstractDeviceStateRepository = RepositoryContainer.device_state_repository,
                 ):
        self.device_repository = device_repository
        self.state_repository = state_repository
        self.logger = logging.getLogger(__name__)

    INTERVAL_SCAN = 10 * 60  # 端末を発見してから次に検索するまでの間隔
    INTERVAL_UPDATE = 10 * 60  # 状態が変化していないときに、更新する間隔

    async def delete_results_before(self, time_in_mills):
        await self.state_repository.delete_before(time_in_mills)

    async def scan_devices(self, addresses: Optional[List[str]] = None):
        """
        Bluetooth端末を検索

        【注意】
        この処理を同時に呼ぶと、正しい結果を得ることができない

        :param addresses: 検索する端末のMACアドレス, Noneの場合は、登録された端末を検索する
        """
        # 登録されたすべての端末のMACアドレスを取得
        if addresses is None:
            devices = await self.device_repository.find_all()
            addresses = [device.address for device in devices]

        self.logger.info(f"SCAN FOR {addresses}")

        # 端末をBluetoothでスキャンする
        all_states = await self.state_repository.find_all()
        scan_results = []
        for address in addresses:
            last_state = self._get_last_device_states(address, all_states)
            result = await self._scan_device(address, last_state)
            if result is not None:
                scan_results.append(result)

        # 保存が必要な結果のみを抽出
        results_for_updates = []
        for result in scan_results:
            prev_state = self._get_last_device_states(result.address, all_states)
            if self._should_update_state(prev_state, result):
                results_for_updates.append(result)

        # スキャン結果を保存
        await self.state_repository.save_all(results_for_updates)

    async def _scan_device(self, address: str, prev_state: DeviceStateEntity) -> Optional[DeviceStateEntity]:
        """
        付近に端末がいるかどうか、スキャンする
        @:param prev_state 前回のスキャン結果
        @:return スキャン結果（前回のスキャンと結果が変わらない場合はNoneを返す）
        """
        # 10分以内に発見されていたら、スキャンせずに、前の結果を使う
        if prev_state is not None \
                and prev_state.created_at >= time.time() - self.INTERVAL_SCAN \
                and prev_state.found:
            self.logger.info(f"SCAN(USE CACHE) {prev_state.to_json()}")
            return None

        # スキャン
        result = scan_device(address=address)
        prev_state = DeviceStateEntity(address=address, found=result.found)
        self.logger.info(f"DEVICE SCANNED {prev_state.to_json()}")
        return prev_state

    def _should_update_state(self, prev_result: DeviceStateEntity, new_result: DeviceStateEntity) -> bool:
        """
        検索結果を更新すべきかどうかを判定する
        """
        # 初回のデータの場合は更新する。
        if prev_result is None:
            return True

        # 前回と状態が変化していれば更新する
        if prev_result.found != new_result.found:
            return True

        return False

    def _get_last_device_states(
            self, address: str,
            states: List[DeviceStateEntity]
    ) -> Optional[DeviceStateEntity]:
        """
        端末のすべての検索結果から、最新の検索結果を取得する
        Google Spread Sheetへのアクセス回数を減らすために、このメソッドを使用する
        """
        # 端末に対応する検索結果
        device_states = list(filter(lambda s: s.address == address, states))

        if len(device_states) == 0:
            return None

        # 検索結果を、日付が新しい順にソート
        return max(states, key=lambda s: s.created_at)
