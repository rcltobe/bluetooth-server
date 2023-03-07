from __future__ import annotations

import time
from typing import Optional, List


class DeviceState:
    """
    端末の検索履歴
    @:param address 端末のMACアドレス
    @:param found 端末が付近にあった場合はTrue
    """

    def __init__(self, address: str, found: bool, created_at: Optional[float] = None):
        self.created_at: float = time.time() if created_at is None else created_at
        self.address: str = address
        self.found = found

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
            "address": self.address,
            "found": self.found,
            "createdAt": int(self.created_at),
        }

    def should_update_state(self, prev_result: Optional[DeviceState]) -> bool:
        """
        検索結果を更新すべきかどうかを判定する
        """
        if prev_result is None:
            # 初回のデータの場合は更新する。
            return True
        else:
            assert self.address == prev_result.address

        # 前回と状態が変化していれば更新する
        if prev_result.found != self.found:
            return True

        return False
