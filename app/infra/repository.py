from app.domain.repository.device_repository import AbstractDeviceRepository
from app.domain.repository.device_state_repository import AbstractDeviceStateRepository
from app.infra.spreadsheet.device_repository import SpreadSheetDeviceRepository
from app.infra.spreadsheet.device_state_repository import SpreadSheetDeviceStateRepository


class RepositoryContainer:
    device_repository: AbstractDeviceRepository = SpreadSheetDeviceRepository()
    device_state_repository: AbstractDeviceStateRepository = SpreadSheetDeviceStateRepository()
