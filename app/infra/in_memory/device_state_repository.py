from typing import List, Optional

from app.domain.models.util import DateRange
from app.domain.repository.device_state_repository import AbstractDeviceStateRepository, DeviceStateEntity


class InMemoryDeviceStateRepository(AbstractDeviceStateRepository):
    _states: List[DeviceStateEntity] = []

    async def find_all(self, date_range: Optional[DateRange] = None) -> List[DeviceStateEntity]:
        return [
            state
            for state in InMemoryDeviceStateRepository._states
            if state.in_range(date_range)
        ]

    async def find_all_by_address(self, address: str) -> List[DeviceStateEntity]:
        return [device for device
                in InMemoryDeviceStateRepository._states
                if device.address == address
                ]

    async def find_last(self, address: str) -> Optional[DeviceStateEntity]:
        if len(InMemoryDeviceStateRepository._states) == 0:
            return None

        states = [
            state for state in InMemoryDeviceStateRepository._states
            if state.address == address
        ]

        if len(states) == 0:
            return None

        states = sorted(states, key=lambda state: state.created_at, reverse=True)
        return states[0]

    async def save(self, state: DeviceStateEntity):
        InMemoryDeviceStateRepository._states.append(state)

    async def delete(self, state_id: str):
        self._states = [
            state
            for state in self._states
            if state.id != state_id
        ]
