from typing import List

from app.domain.models.device import BluetoothDevice
from app.domain.repository.device_repository import AbstractDeviceRepository
from app.infra.spreadsheet.spreadsheet_user_entity import SpreadSheetUserEntity
from app.infra.spreadsheet.spreadsheet_util import SpreadSheetUtil


class SpreadSheetDeviceRepository(AbstractDeviceRepository):
    spreadsheet_util = SpreadSheetUtil(4, "users")

    async def find_all(self) -> List[BluetoothDevice]:
        rows = await self.spreadsheet_util.get_values()
        devices = []
        for values in rows:
            user = SpreadSheetUserEntity.from_csv(values)
            if user is None:
                continue
            devices.append(user.to_bluetooth_device())
        return devices
