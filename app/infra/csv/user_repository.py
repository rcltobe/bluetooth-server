import csv
import os
from typing import List, Optional

from app.domain.models.user import User
from app.domain.repository.user_repository import AbstractUserRepository


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
        with open(self._FILE_PATH, 'a') as file:
            writer = csv.writer(file)
            writer.writerow(user.to_csv())

    async def delete(self, user_id: str):
        if not os.path.exists(self._FILE_PATH):
            return

        with open(self._FILE_PATH, 'r') as inp, open(self._FILE_PATH, 'w') as out:
            writer = csv.writer(out)
            reader = csv.reader(inp)
            for row in reader:
                if row[self.INDEX_ID] != user_id:
                    writer.writerow(row)

    async def update_name(self, user_id: str, name: str):
        if not os.path.exists(self._FILE_PATH):
            return

        with open(self._FILE_PATH, 'r') as inp, open(self._FILE_PATH, 'w') as out:
            writer = csv.writer(out)
            reader = csv.reader(inp)
            for row in reader:
                if row[self.INDEX_ID] == user_id:
                    user = User.from_csv(row)
                    user.name = name
                    writer.writerow(user.to_csv())
                else:
                    writer.writerow(row)

    async def update_grade(self, user_id: str, grade: str):
        if not os.path.exists(self._FILE_PATH):
            return

        with open(self._FILE_PATH, 'r') as inp, open(self._FILE_PATH, 'w') as out:
            writer = csv.writer(out)
            reader = csv.reader(inp)
            for row in reader:
                if row[self.INDEX_ID] == user_id:
                    user = User.from_csv(row)
                    user.grade = grade
                    writer.writerow(user.to_csv())
                else:
                    writer.writerow(row)

    async def delete_grade(self, user_id: str):
        if not os.path.exists(self._FILE_PATH):
            return

        with open(self._FILE_PATH, 'r') as inp, open(self._FILE_PATH, 'w') as out:
            writer = csv.writer(out)
            reader = csv.reader(inp)
            for row in reader:
                if row[self.INDEX_ID] == user_id:
                    user = User.from_csv(row)
                    user.grade = None
                    writer.writerow(user.to_csv())
                else:
                    writer.writerow(row)
