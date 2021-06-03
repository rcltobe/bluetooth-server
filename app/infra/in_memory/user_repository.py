from typing import List, Optional

from app.domain.models.user import User
from app.domain.repository.user_repository import AbstractUserRepository


class InMemoryUserRepository(AbstractUserRepository):
    _users: List[User] = []

    async def find_all(self) -> List[User]:
        return InMemoryUserRepository._users

    async def find(self, user_id: str) -> Optional[User]:
        user = [user for user in InMemoryUserRepository._users if user.id == user_id]
        if len(user) == 0:
            return None
        return user[0]

    async def save(self, user: User):
        InMemoryUserRepository._users.append(user)

    async def delete(self, user_id: str):
        InMemoryUserRepository._users = [
            user for user in InMemoryUserRepository._users
            if user.id != user_id
        ]

    async def update_name(self, user_id: str, name: str):
        user = await self.find(user_id)
        if user is None:
            return
        await self.delete(user_id)
        user.name = name
        await self.save(user)

    async def update_grade(self, user_id: str, grade: str):
        user = await self.find(user_id)
        if user is None:
            return
        await self.delete(user_id)
        user.grade = grade
        await self.save(user)

    async def delete_grade(self, user_id: str):
        user = await self.find(user_id)
        if user is None:
            return
        await self.delete(user_id)
        user.grade = None
        await self.save(user)
