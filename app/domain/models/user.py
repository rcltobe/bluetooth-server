from __future__ import annotations

from dataclasses import dataclass


@dataclass
class User:
    """
    :param address: Bluetooth端末のMACアドレス
    :param user_id: この端末を結びつけるユーザーのID
    """
    address: str
    user_id: str
    user_name: str
