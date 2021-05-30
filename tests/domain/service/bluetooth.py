import unittest

from app.domain.models.bluetooth import BluetoothDevice, DeviceState
from app.domain.service.bluetooth import BluetoothService
from app.infra.in_memory.device_repository import InMemoryDeviceRepository
from app.infra.in_memory.device_state_repository import InMemoryDeviceStateRepository


class TestAttendanceService(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.device_repository = InMemoryDeviceRepository()
        self.state_repository = InMemoryDeviceStateRepository()
        self.service = BluetoothService(
            device_repository=self.device_repository,
            state_repository=self.state_repository
        )

    async def test_update_state(self):
        device = BluetoothDevice(address="abc", user_id="test")
        await self.device_repository.save(device)

        await self.service.update_state(device.address, DeviceState.FOUND)
        states = await self.state_repository.find_all()
        self.assertEqual(len(states), 1)

        # DeviceStateが変更されていなければ、何もしない
        await self.service.update_state(device.address, DeviceState.FOUND)
        states = await self.state_repository.find_all()
        self.assertEqual(len(states), 1)

        await self.service.update_state(device.address, DeviceState.NOT_FOUND)
        states = await self.state_repository.find_all()
        self.assertEqual(len(states), 2)
