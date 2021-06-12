import csv
import os
from typing import List, Optional

from app.domain.models.util import DateRange
from app.domain.repository.device_state_repository import AbstractDeviceStateRepository, DeviceStateEntity
from app.infra.csv.csv_util import delete_row


class CsvDeviceStateRepository(AbstractDeviceStateRepository):
    _FILE_PATH = f"{os.curdir}/data/device_states.csv"

    async def find_all(self, date_range: Optional[DateRange] = None) -> List[DeviceStateEntity]:
        if not os.path.exists(self._FILE_PATH):
            return []

        with open(self._FILE_PATH) as file:
            reader = csv.reader(file)
            rows = [row for row in reader]

        return [
            state
            for state in [DeviceStateEntity.from_csv(row) for row in rows]
            if state is not None and state.in_range(date_range)
        ]

    async def find_last(self, address: str) -> Optional[DeviceStateEntity]:
        states = await self.find_all()
        if len(states) == 0:
            return None

        states = [
            state for state in states
            if state.address == address
        ]

        if len(states) == 0:
            return None

        states = sorted(states, key=lambda state: state.created_at, reverse=True)
        return states[0]

    async def find_all_by_address(self, address: str) -> List[DeviceStateEntity]:
        states = await self.find_all()
        return [state for state in states if state.address == address]

    async def save(self, state: DeviceStateEntity):
        mode = 'a' if os.path.exists(self._FILE_PATH) else 'w'
        with open(self._FILE_PATH, mode) as file:
            writer = csv.writer(file)
            writer.writerow(state.to_csv())

    async def delete(self, state_id: str):
        def check(csv: List[str]) -> bool:
            return csv[0] == state_id

        delete_row(self._FILE_PATH, check)
