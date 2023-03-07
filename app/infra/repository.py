from app.domain.repository.user_repository import AbstractUserRepository
from app.domain.repository.device_state_repository import AbstractDeviceStateRepository
from app.infra.spreadsheet.user_repository import SpreadSheetUserRepository
from app.infra.spreadsheet.device_state_repository import SpreadSheetDeviceStateRepository


class RepositoryContainer:
    device_repository: AbstractUserRepository = SpreadSheetUserRepository()
    device_state_repository: AbstractDeviceStateRepository = SpreadSheetDeviceStateRepository()
