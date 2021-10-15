from __future__ import annotations

import time
import uuid
from typing import Optional, List


class DeviceState:
    """
    端末の検索履歴
    @:param address 端末のMACアドレス
    @:param found 端末が付近にあった場合はTrue
    """

    def __init__(self, address: str, found: bool, id: Optional[str] = None, created_at: Optional[float] = None):
        self.id = str(uuid.uuid4()) if id is None else id
        self.created_at: float = time.time() if created_at is None else created_at
        self.address: str = address
        self.found = found

    @classmethod
    def from_csv(cls, csv: List[str]) -> Optional[DeviceState]:
        if len(csv) < 4:
            return None

        try:
            found = True if int(csv[2]) == 1 else False
        except ValueError:
            found = False

        return DeviceState(
            id=csv[0],
            address=csv[1],
            found=found,
            created_at=float(csv[3])
        )

    @classmethod
    def get_last_device_states(cls, address, states: List[DeviceState]) -> Optional[DeviceState]:
        """
       端末のすべての検索結果から、最新の検索結果を取得する
       """
        # 端末に対応する検索結果
        device_states = list(filter(lambda s: s.address == address, states))
        if len(device_states) == 0:
            return None

        # 日時が最新の検索結果を取得
        return max(device_states, key=lambda s: s.created_at)

    def to_json(self):
        return {
            "id": self.id,
            "address": self.address,
            "found": self.found,
            "createdAt": int(self.created_at),
        }

    def to_csv(self) -> List[str]:
        return [self.id, self.address, 1 if self.found else 0, int(self.created_at)]

    def should_update_state(self, prev_result: DeviceState) -> bool:
        """
        検索結果を更新すべきかどうかを判定する
        """
        assert self.address == prev_result.address

        # 初回のデータの場合は更新する。
        if prev_result is None:
            return True

        # 前回と状態が変化していれば更新する
        if prev_result.found != self.found:
            return True

        return False
