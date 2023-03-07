from app.domain.repository.user_repository import AbstractUserRepository
from app.infra.spreadsheet.user_repository import SpreadSheetUserRepository


class RepositoryContainer:
    device_repository: AbstractUserRepository = SpreadSheetUserRepository()