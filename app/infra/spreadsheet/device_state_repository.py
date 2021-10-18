from typing import List

from app.domain.models.device_state import DeviceState
from app.domain.repository.device_state_repository import AbstractDeviceStateRepository
from app.infra.spreadsheet.models.device_state_entity import DeviceStateEntity
from app.infra.spreadsheet.spreadsheet_util import SpreadSheetUtil


class SpreadSheetDeviceStateRepository(AbstractDeviceStateRepository):
    """
    SpreadSheetのフォーマット
    (ID, MACアドレス, 端末を発見できたか（1or0）, 検索日時（Unix時間）)
    """
    spreadsheet_util = SpreadSheetUtil(4, "attendance")

    async def find_all(self) -> List[DeviceState]:
        cells = await self.spreadsheet_util.get_values()
        if len(cells) == 0:
            return []
        entities = [DeviceStateEntity.from_csv(row) for row in cells]
        entities = [entity for entity in entities if entity is not None]
        return [entity.to_device_state() for entity in entities]

    async def save_all(self, states: List[DeviceState]):
        entities = [DeviceStateEntity.from_device_state(state) for state in states]
        values = [entity.to_csv() for entity in entities]
        await self.spreadsheet_util.append_all_values(values)

    async def delete_before(self, time_in_mills: int):
        states = await self.find_all()

        row_for_delete = [state for state in states if int(state.created_at) <= time_in_mills]
        if len(row_for_delete) == 0:
            # 削除するものが何もない場合は、何もしない
            return

        await self.spreadsheet_util.delete_rows(1, len(row_for_delete))
