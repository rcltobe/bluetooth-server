import csv
import os
from typing import List, Optional

from app.domain.repository.device_state_repository import AbstractDeviceStateRepository, DeviceStateEntity


class CsvDeviceStateRepository(AbstractDeviceStateRepository):
    _FILE_PATH = f"{os.curdir}/data/device_states.csv"

    async def find_all(self) -> List[DeviceStateEntity]:
        if not os.path.exists(self._FILE_PATH):
            return []

        with open(self._FILE_PATH) as file:
            reader = csv.reader(file)
            rows = [row for row in reader]
        return [DeviceStateEntity.from_csv(row) for row in rows]

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
        with open(self._FILE_PATH, 'a') as file:
            writer = csv.writer(file)
            writer.writerow(state.to_csv())
