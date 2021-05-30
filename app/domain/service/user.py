from typing import List, Optional

from app.domain.models.bluetooth import BluetoothDevice
from app.domain.models.user import User
from app.domain.repository.device_repository import AbstractDeviceRepository
from app.domain.repository.user_repository import AbstractUserRepository
from app.infra.in_memory.device_repository import InMemoryDeviceRepository
from app.infra.in_memory.user_repository import InMemoryUserRepository


class UserData:
    def __init__(self, user: User, devices: List[str]):
        self.id = user.id
        self.name = user.name
        self.grade = user.grade
        self.devices = devices

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "grade": self.grade,
            "devices": self.devices
        }


class UserService:
    def __init__(self,
                 user_repository: AbstractUserRepository = InMemoryUserRepository(),
                 device_repository: AbstractDeviceRepository = InMemoryDeviceRepository()):
        self.user_repository: AbstractUserRepository = user_repository
        self.device_repository: AbstractDeviceRepository = device_repository

    async def get_users(self) -> List[UserData]:
        users = await self.user_repository.find_all()
        data: List[UserData] = []
        for user in users:
            devices = await self.device_repository.find_by_user_id(user.id)
            data.append(UserData(
                user=user,
                devices=[device.address for device in devices]
            ))
        return data

    async def add_user(self, name: str, grade: Optional[str], devices: List[str]) -> User:
        user = User(name=name, grade=grade)
        # ユーザーを保存
        await self.user_repository.save(user)

        # ユーザーのBluetooth機器を保存
        for address in devices:
            device = BluetoothDevice(address=address, user_id=user.id)
            await self.device_repository.save(device)

        return User(name=name, grade=grade)

    async def delete_user(self, user_id: str):
        await self.user_repository.find(user_id)
        await self.device_repository.delete_all_by_user_id(user_id=user_id)

    async def get_devices(self, user_id: str) -> List[BluetoothDevice]:
        return await self.device_repository.find_by_user_id(user_id)

    async def add_device(self, user_id: str, address: str) -> Optional[BluetoothDevice]:
        user = await self.user_repository.find(user_id)
        if user is None:
            return None

        device = BluetoothDevice(address=address, user_id=user_id)
        await self.device_repository.save(device)
        return device
