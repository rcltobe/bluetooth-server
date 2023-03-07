from typing import List

from app.domain.models.user import User
from app.domain.repository.user_repository import AbstractUserRepository
from app.infra.spreadsheet.models.user_entity import UserEntity
from app.infra.spreadsheet.spreadsheet_util import SpreadSheetUtil


class SpreadSheetUserRepository(AbstractUserRepository):
    spreadsheet_util = SpreadSheetUtil(4, "users")

    async def find_all(self) -> List[User]:
        rows = await self.spreadsheet_util.get_values()
        devices = []
        for values in rows:
            user = UserEntity.from_csv(values)
            if user is None:
                continue
            devices.append(user.to_bluetooth_device())
        return devices
