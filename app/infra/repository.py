from app.domain.repository.device_repository import AbstractDeviceRepository
from app.domain.repository.device_state_repository import AbstractDeviceStateRepository
from app.domain.repository.user_repository import AbstractUserRepository
from app.infra.csv.device_repository import CsvDeviceRepository
from app.infra.csv.user_repository import CsvUserRepository
from app.infra.in_memory.device_state_repository import InMemoryDeviceStateRepository


class RepositoryContainer:
    user_repository: AbstractUserRepository = CsvUserRepository()
    device_repository: AbstractDeviceRepository = CsvDeviceRepository()
    device_state_repository: AbstractDeviceStateRepository = InMemoryDeviceStateRepository()
