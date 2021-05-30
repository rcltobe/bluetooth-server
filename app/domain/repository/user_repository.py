from abc import abstractmethod
from typing import List, Optional

from app.domain.models.user import User


class AbstractUserRepository:
    @abstractmethod
    async def find_all(self) -> List[User]:
        pass

    @abstractmethod
    async def find(self, id: str) -> Optional[User]:
        pass

    @abstractmethod
    async def save(self, user: User):
        pass

    @abstractmethod
    async def delete(self, id: str):
        pass
