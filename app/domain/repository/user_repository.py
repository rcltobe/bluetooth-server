from abc import abstractmethod
from typing import List

from app.domain.models.user import User


class AbstractUserRepository:
    @abstractmethod
    async def find_all(self) -> List[User]:
        """
        すべての端末を取得する
        """
        pass
