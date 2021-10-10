from typing import Optional

from app.domain.repository.device_state_repository import AbstractDeviceStateRepository, DeviceStateEntity
from app.infra.spreadsheet.spreadsheet_util import SpreadSheetUtil


class SpreadSheetDeviceStateRepository(AbstractDeviceStateRepository):
    """
    SpreadSheetのフォーマット
    ID, MACアドレス, 端末を発見できたか（1or0）, 検索日時（Unix時間）
    """
    spreadsheet_util = SpreadSheetUtil(4, "attendance")

    async def find_last(self, address: str) -> Optional[DeviceStateEntity]:
        cells = await self.spreadsheet_util.find_all(address, 2)
        if len(cells) == 0:
            return None

        # 最後のデータの行番号を取得
        row_numbers = [cell.row for cell in cells]
        last_row_number = max(row_numbers)

        values = await self.spreadsheet_util.get_row(last_row_number)
        entity = DeviceStateEntity.from_csv(values)
        return entity

    async def save(self, state: DeviceStateEntity):
        await self.spreadsheet_util.append_values(state.to_csv())
