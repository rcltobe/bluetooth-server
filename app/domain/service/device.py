import logging
import time
from typing import Optional

from app.domain.models.device_state import DeviceState
from app.domain.repository.user_repository import AbstractUserRepository
from app.domain.repository.device_state_repository import AbstractDeviceStateRepository
from app.infra.bluetooth.scanner import scan_device
from app.infra.repository import RepositoryContainer


class DeviceService:
    """
    端末のスキャン処理と、スキャン結果の保存を行う
    SpreadSheetに過度なアクセスをしないように実装されている。
    """

    def __init__(self,
                 user_repository: AbstractUserRepository = RepositoryContainer.device_repository,
                 state_repository: AbstractDeviceStateRepository = RepositoryContainer.device_state_repository,
                 ):
        self.user_repository = user_repository
        self.state_repository = state_repository
        self.logger = logging.getLogger(__name__)

    INTERVAL_SCAN = 10 * 60  # 端末を発見してから次に検索するまでの間隔
    INTERVAL_UPDATE = 10 * 60  # 状態が変化していないときに、更新する間隔

    async def delete_results_before(self, time_in_mills):
        self.logger.info(f"delete result before {time_in_mills}")
        await self.state_repository.delete_before(time_in_mills)

    async def scan_devices(self):
        """
        Bluetooth端末を検索

        【注意】
        この処理を同時に呼ぶと、正しい結果を得ることができない
        """
        # 登録されたすべての端末のMACアドレスを取得
        devices = await self.user_repository.find_all()
        addresses = [device.address for device in devices]

        self.logger.info(f"SCAN FOR {addresses}")

        # 端末をBluetoothでスキャンする
        all_states = await self.state_repository.find_all()
        scan_results = []
        for address in addresses:
            last_state = DeviceState.get_last_device_states(address, all_states)
            result = await self._scan_device(address, last_state)
            if result is not None:
                scan_results.append(result)

        # 保存が必要な結果のみを抽出
        results_for_updates = []
        for result in scan_results:
            prev_state = DeviceState.get_last_device_states(result.address, all_states)
            if result.should_update_state(prev_state):
                p = f"{prev_state.found}" if prev_state else "NONE"
                self.logger.info(f"UPDATE {result.address}({p} -> {result.found})")
                results_for_updates.append(result)

        # スキャン結果を保存
        await self.state_repository.save_all(results_for_updates)

    async def _scan_device(self, address: str, prev_state: Optional[DeviceState]) -> Optional[DeviceState]:
        """
        付近に端末がいるかどうか、スキャンする
        @:param prev_state 前回のスキャン結果
        @:return スキャン結果（10分以内に発見されている場合はNoneを返す）
        """
        # 10分以内に発見されていたら、スキャンせずに、前の結果を使う
        if prev_state is not None \
                and prev_state.created_at >= time.time() - self.INTERVAL_SCAN \
                and prev_state.found:
            self.logger.info(f"SCAN(USE CACHE) {prev_state.to_json()}")
            return None

        # スキャン
        try:
            result = scan_device(address=address)
        except Exception as e:
            logging.error(e)
            return None

        prev_state = DeviceState(address=address, found=result.found)
        self.logger.info(f"DEVICE SCANNED {prev_state.to_json()}")
        return prev_state
