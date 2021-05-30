from typing import List, Optional

from app.domain.models.user import User
from app.domain.repository.user_repository import AbstractUserRepository


class InMemoryUserRepository(AbstractUserRepository):
    _users: List[User] = []

    async def find_all(self) -> List[User]:
        return InMemoryUserRepository._users

    async def find(self, id: str) -> Optional[User]:
        user = [user for user in InMemoryUserRepository._users if user.id == id]
        if len(user) == 0:
            return None
        return user[0]

    async def save(self, user: User):
        InMemoryUserRepository._users.append(user)

    async def delete(self, id: str):
        InMemoryUserRepository._users = [
            user for user in InMemoryUserRepository._users
            if user.id != id
        ]
