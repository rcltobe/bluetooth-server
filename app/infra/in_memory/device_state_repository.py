from app.domain.repository.device_state_repository import AbstractDeviceStateRepository, DeviceStateEntity


class InMemoryDeviceStateRepository(AbstractDeviceStateRepository):
    _states: [DeviceStateEntity] = []

    async def find_all(self) -> [DeviceStateEntity]:
        return InMemoryDeviceStateRepository._states

    async def save(self, state: DeviceStateEntity):
        InMemoryDeviceStateRepository._states.append(state)
