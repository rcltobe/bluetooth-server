from app.domain.repository.body_temperature_repository import AbstractBodyTemperatureRepository
from app.domain.repository.device_repository import AbstractDeviceRepository
from app.domain.repository.device_state_repository import AbstractDeviceStateRepository
from app.domain.repository.user_repository import AbstractUserRepository
from app.infra.csv.body_temperature_repository import CsvBodyTemperatureRepository
from app.infra.csv.device_repository import CsvDeviceRepository
from app.infra.csv.state_repository import CsvDeviceStateRepository
from app.infra.csv.user_repository import CsvUserRepository


class RepositoryContainer:
    user_repository: AbstractUserRepository = CsvUserRepository()
    device_repository: AbstractDeviceRepository = CsvDeviceRepository()
    device_state_repository: AbstractDeviceStateRepository = CsvDeviceStateRepository()
    body_temperature_repository: AbstractBodyTemperatureRepository = CsvBodyTemperatureRepository()
