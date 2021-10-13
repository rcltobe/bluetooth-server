from typing import List

from app.domain.repository.device_state_repository import AbstractDeviceStateRepository, DeviceStateEntity
from app.infra.spreadsheet.spreadsheet_util import SpreadSheetUtil


class SpreadSheetDeviceStateRepository(AbstractDeviceStateRepository):
    """
    SpreadSheetのフォーマット
    ID, MACアドレス, 端末を発見できたか（1or0）, 検索日時（Unix時間）
    """
    spreadsheet_util = SpreadSheetUtil(4, "attendance")

    async def find_all(self) -> List[DeviceStateEntity]:
        cells = await self.spreadsheet_util.get_values()
        if len(cells) == 0:
            return []
        states = [DeviceStateEntity.from_csv(row) for row in cells]
        return [state for state in states if state is not None]

    async def save_all(self, states: List[DeviceStateEntity]):
        values = [state.to_csv() for state in states]
        await self.spreadsheet_util.append_all_values(values)

    async def delete_before(self, time_in_mills: int):
        states = await self.find_all()

        row_for_delete = 1
        for state in states:
            if int(state.created_at) > time_in_mills:
                break
            row_for_delete += 1

        await self.spreadsheet_util.delete_rows(1, row_for_delete)
