from typing import List, Optional

from app.domain.models.bluetooth import BluetoothDevice
from app.domain.models.user import User
from app.domain.repository.device_repository import AbstractDeviceRepository
from app.domain.repository.user_repository import AbstractUserRepository
from app.infra.repository import RepositoryContainer


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
            "grade": self.grade.value if self.grade is not None else None,
            "devices": self.devices
        }


class UserService:
    def __init__(self,
                 user_repository: AbstractUserRepository = RepositoryContainer.user_repository,
                 device_repository: AbstractDeviceRepository = RepositoryContainer.device_repository):
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

    async def get_user(self, user_id: str) -> Optional[UserData]:
        user = await self.user_repository.find(user_id)
        if user is None:
            return None
        devices = await self.device_repository.find_by_user_id(user.id)
        return UserData(
            user=user,
            devices=[device.address for device in devices],
        )

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

    async def update_name(self, user_id: str, name: str):
        await self.user_repository.update_name(user_id, name)

    async def update_grade(self, user_id: str, grade: Optional[str]):
        if grade is None:
            await self.user_repository.delete_grade(user_id)
        else:
            await self.user_repository.update_grade(user_id, grade)

    async def get_devices(self, user_id: str) -> List[BluetoothDevice]:
        return await self.device_repository.find_by_user_id(user_id)

    async def update_devices(self, user_id: str, addresses: List[str]):
        devices = await self.device_repository.find_by_user_id(user_id)
        device_addresses = [device.address for device in devices]

        added = set(addresses) - set(device_addresses)
        deleted = set(device_addresses) - set(addresses)

        for address in added:
            device = BluetoothDevice(address=address, user_id=user_id)
            await self.device_repository.save(device)

        for address in deleted:
            await self.device_repository.delete(address)
