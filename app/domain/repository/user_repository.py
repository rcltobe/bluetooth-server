from abc import abstractmethod
from typing import List, Optional

from app.domain.models.user import User


class AbstractUserRepository:
    @abstractmethod
    async def find_all(self) -> List[User]:
        pass

    @abstractmethod
    async def find(self, user_id: str) -> Optional[User]:
        pass

    @abstractmethod
    async def save(self, user: User):
        pass

    @abstractmethod
    async def delete(self, user_id: str):
        pass

    @abstractmethod
    async def update_name(self, user_id: str, name: str):
        pass

    @abstractmethod
    async def update_grade(self, user_id: str, grade: str):
        pass

    @abstractmethod
    async def delete_grade(self, user_id: str):
        pass
