import csv
import os
from typing import List, Optional

from app.domain.models.user import User
from app.domain.repository.user_repository import AbstractUserRepository
from app.infra.csv.csv_util import delete_row, update_row


class CsvUserRepository(AbstractUserRepository):
    INDEX_ID = 0
    _FILE_PATH = f"{os.curdir}/data/users.csv"

    async def find_all(self) -> List[User]:
        if not os.path.exists(self._FILE_PATH):
            return []

        with open(self._FILE_PATH) as file:
            reader = csv.reader(file)
            rows = [row for row in reader]
        return [
            user
            for user in [User.from_csv(row) for row in rows]
            if user is not None
        ]

    async def find(self, user_id: str) -> Optional[User]:
        users = await self.find_all()
        users = [user for user in users if user.id == user_id]

        if len(users) == 0:
            return None

        return users[0]

    async def save(self, user: User):
        mode = 'a' if os.path.exists(self._FILE_PATH) else 'w'
        with open(self._FILE_PATH, mode) as file:
            writer = csv.writer(file)
            writer.writerow(user.to_csv())

    async def delete(self, user_id: str):
        delete_row(
            file_name=self._FILE_PATH,
            check=lambda row: row[self.INDEX_ID] == user_id,
        )

    async def update_name(self, user_id: str, name: str):
        def _update_name(row: List[str]) -> List[str]:
            user = User.from_csv(row)
            user.name = name
            return user.to_csv()

        update_row(
            file_name=self._FILE_PATH,
            check=lambda row: row[self.INDEX_ID] == user_id,
            on_update=_update_name,
        )

    async def update_grade(self, user_id: str, grade: str):
        def _update_grade(row: List[str]) -> List[str]:
            user = User.from_csv(row)
            user.grade = grade
            return user.to_csv()

        update_row(
            file_name=self._FILE_PATH,
            check=lambda row: row[self.INDEX_ID] == user_id,
            on_update=_update_grade,
        )

    async def delete_grade(self, user_id: str):
        if not os.path.exists(self._FILE_PATH):
            return

        def _delete_grade(row: List[str]) -> List[str]:
            user = User.from_csv(row)
            user.grade = None
            return user.to_csv()

        update_row(
            file_name=self._FILE_PATH,
            check=lambda row: row[self.INDEX_ID] == user_id,
            on_update=_delete_grade
        )
