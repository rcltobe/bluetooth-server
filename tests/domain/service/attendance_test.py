import unittest

from app.domain.models.bluetooth import BluetoothDevice, DeviceState
from app.domain.models.user import User
from app.domain.service.attendance import AttendanceService
from app.infra.in_memory.device_repository import InMemoryDeviceRepository
from app.infra.in_memory.device_state_repository import InMemoryDeviceStateRepository, DeviceStateEntity
from app.infra.in_memory.user_repository import InMemoryUserRepository


class TestAttendanceService(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.user_repository = InMemoryUserRepository()
        self.device_repository = InMemoryDeviceRepository()
        self.state_repository = InMemoryDeviceStateRepository()
        self.service = AttendanceService(
            user_repository=self.user_repository,
            device_repository=self.device_repository,
            device_state_repository=self.state_repository
        )

    async def test_get_attendance(self):
        """
        出席データを取得
        DeviceStateRepositoryに、端末の状態(FOUND, NOT-FOUND)が記録されているので
        その対応付が正しく行われるかをテストする。
        """
        user = User(name="test", grade=None)
        await self.user_repository.save(user)
        device = BluetoothDevice(address="abc", user_id=user.id)
        await self.device_repository.save(device)

        found_state = DeviceStateEntity(address=device.address, state=DeviceState.FOUND)
        not_found_state = DeviceStateEntity(address=device.address, state=DeviceState.NOT_FOUND)
        await self.state_repository.save(found_state)
        await self.state_repository.save(not_found_state)

        attendances = await self.service.get_attendance(user)
        self.assertTrue(len(attendances) > 0)

        attendance = attendances[0]
        print(attendance.__dict__)

        self.assertEqual(attendance.name, user.name)
        self.assertTrue(attendance.enter_at, found_state.created_at)
        self.assertTrue(attendance.left_at, not_found_state.created_at)

    async def test_get_attendances(self):
        user = User(name="test", grade=None)
        await self.user_repository.save(user)
        device = BluetoothDevice(address="abc", user_id=user.id)
        await self.device_repository.save(device)

        for i in range(10):
            found_state = DeviceStateEntity(address=device.address, state=DeviceState.FOUND)
            not_found_state = DeviceStateEntity(address=device.address, state=DeviceState.NOT_FOUND)
            await self.state_repository.save(found_state)
            await self.state_repository.save(not_found_state)

            attendances = await self.service.get_attendance(user)
            self.assertTrue(len(attendances) > 0)

            attendance = attendances[i]
            print(attendance.__dict__)

            self.assertEqual(attendance.name, user.name)
            self.assertTrue(attendance.enter_at, found_state.created_at)
            self.assertTrue(attendance.left_at, not_found_state.created_at)
