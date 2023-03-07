from __future__ import annotations

from typing import List, Optional

from app.domain.models.user import User
from app.infra.spreadsheet.models.spreadsheet_entity import SpreadSheetEntity


class UserEntity(SpreadSheetEntity):
    """
    SpreadSheetのセルの形式
    (id, 名前, 学年, 端末のMACアドレス)
    """

    def __init__(self, user_id: str, user_name: str, mac_address: str):
        self.user_id = user_id
        self.user_name = user_name
        self.mac_address = mac_address

    @classmethod
    def from_csv(cls, csv: List[str]) -> Optional[UserEntity]:
        if not cls.validate(attr_size=4, values=csv, require_filled=False):
            return None

        if len(csv[0]) == 0 or len(csv[3]) == 0:
            return None

        return UserEntity(
            user_id=csv[0],
            user_name=csv[1],
            mac_address=csv[3]
        )

    def to_bluetooth_device(self) -> User:
        return User(
            user_id=self.user_id,
            user_name=self.user_name,
            address=self.mac_address
        )
