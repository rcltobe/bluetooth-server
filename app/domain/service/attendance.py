from typing import List

from app.domain.models.attendance import Attendance
from app.domain.models.bluetooth import DeviceState
from app.domain.models.user import User
from app.domain.repository.device_repository import AbstractDeviceRepository
from app.domain.repository.device_state_repository import AbstractDeviceStateRepository
from app.domain.repository.user_repository import AbstractUserRepository
from app.infra.in_memory.device_repository import InMemoryDeviceRepository
from app.infra.in_memory.device_state_repository import InMemoryDeviceStateRepository
from app.infra.in_memory.user_repository import InMemoryUserRepository


class AttendanceService:
    def __init__(self,
                 user_repository: AbstractUserRepository = InMemoryUserRepository(),
                 device_repository: AbstractDeviceRepository = InMemoryDeviceRepository(),
                 device_state_repository: AbstractDeviceStateRepository = InMemoryDeviceStateRepository()):
        self.user_repository = user_repository
        self.device_repository = device_repository
        self.device_state_repository = device_state_repository

    async def get_attendance(self, user: User) -> List[Attendance]:
        # ユーザーの端末を取得
        devices = await self.device_repository.find_by_user_id(user.id)

        # ユーザーの端末の入退室履歴
        states_all = [await self.device_state_repository.find_all_by_address(device.address) for device in devices]
        states = [state for states in states_all for state in states]

        # 入室と退室の対応付を行う
        attendances = []
        states_found = [state for state in states if state.state == DeviceState.FOUND]
        for state_found in states_found:
            state_next_not_found = state_found.next(states)
            left_at = state_next_not_found.created_at if (state_next_not_found is not None) else None
            attendances.append(Attendance(
                name=user.name,
                enter_at=state_found.created_at,
                left_at=left_at
            ))

        return attendances

    async def get_attendances(self) -> List[Attendance]:
        users = await self.user_repository.find_all()
        attendances_all = [await self.get_attendance(user) for user in users]
        attendances = [attendance for attendances in attendances_all for attendance in attendances]
        return attendances
