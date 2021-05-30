import csv
import os
from typing import List, Optional

from app.domain.models.user import User
from app.domain.repository.user_repository import AbstractUserRepository


class CsvUserRepository(AbstractUserRepository):
    INDEX_ID = 0
    INDEX_NAME = 1
    INDEX_GRADE = 2
    _FILE_PATH = f"{os.curdir}/data/users.csv"

    async def find_all(self) -> List[User]:
        if not os.path.exists(self._FILE_PATH):
            return []

        with open(self._FILE_PATH) as file:
            reader = csv.reader(file)
            rows = [row for row in reader]
        return [User.from_csv(row) for row in rows]

    async def find(self, id: str) -> Optional[User]:
        users = await self.find_all()
        users = [user for user in users if user.id == id]

        if len(users) == 0:
            return None

        return users[0]

    async def save(self, user: User):
        with open(self._FILE_PATH, 'a') as file:
            writer = csv.writer(file)
            writer.writerow(user.to_csv())

    async def delete(self, id: str):
        if not os.path.exists(self._FILE_PATH):
            return

        with open(self._FILE_PATH, 'r') as inp, open(self._FILE_PATH, 'w') as out:
            writer = csv.writer(out)
            reader = csv.reader(inp)
            for row in reader:
                if row[self.INDEX_ID] != id:
                    writer.writerow(row)
