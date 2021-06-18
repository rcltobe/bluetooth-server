from app.domain.repository.device_repository import AbstractDeviceRepository
from app.domain.repository.device_state_repository import AbstractDeviceStateRepository
from app.infra.csv.device_repository import CsvDeviceRepository
from app.infra.csv.device_state_repository import CsvDeviceStateRepository


class RepositoryContainer:
    device_repository: AbstractDeviceRepository = CsvDeviceRepository()
    device_state_repository: AbstractDeviceStateRepository = CsvDeviceStateRepository()
