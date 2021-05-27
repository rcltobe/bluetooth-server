from typing import List

from app.domain.models.user import User
from app.domain.repository.user_repository import AbstractUserRepository


class InMemoryUserRepository(AbstractUserRepository):
    _users: List[User] = []

    async def find_all(self) -> List[User]:
        return InMemoryUserRepository._users

    async def save(self, user: User):
        InMemoryUserRepository._users.append(user)
