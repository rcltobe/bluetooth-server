from typing import List, Optional

from app.domain.models.bluetooth import BluetoothDevice
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
            devices.append(user.toBluetoothDevice())
        return devices

    async def find_by_user_id(self, user_id: str) -> Optional[BluetoothDevice]:
        row = await self.spreadsheet_util.get_row_number_of(user_id, 1)
        if row == -1:
            return None

        values = await self.spreadsheet_util.get_row(row)
        device = SpreadSheetUserEntity.from_csv(values)
        if device is None:
            return None

        return device.toBluetoothDevice()
