import os
import sqlite3
from typing import List, Optional

from app.domain.models.util import DateRange
from app.domain.repository.device_state_repository import AbstractDeviceStateRepository, DeviceStateEntity


def create_database(func):
    async def _create_database(*args, **kwargs):
        if os.path.exists(SqliteDeviceStateRepository.DBPATH):
            return await func(*args, **kwargs)

        with sqlite3.connect(SqliteDeviceStateRepository.DBPATH) as conn:
            conn.execute(
                "CREATE TABLE IF NOT EXISTS "
                "device_states("
                "id VARCHAR(50) PRIMARY KEY, "
                "address CHARACTER(17), "
                "found INTEGER, "
                "created_at FLOAT"
                ");"
            )

        return await func(*args, **kwargs)

    return _create_database


class SqliteDeviceStateRepository(AbstractDeviceStateRepository):
    DBNAME = "device_states.sqlite3"
    DBPATH = f"data/{DBNAME}"

    @create_database
    async def find_all(self, date_range: Optional[DateRange] = None) -> List[DeviceStateEntity]:
        with sqlite3.connect(self.DBPATH) as conn:
            cursor = conn.cursor()
            # ?(プレースホルダー)で指定すると内部的にエスケープされる
            if date_range is None:
                cursor.execute("SELECT * FROM device_states")
            else:
                cursor.execute(
                    "SELECT * FROM device_states WHERE created_at > ? AND created_at < ?",
                    (date_range.start, date_range.end)
                )
        return [
            DeviceStateEntity.from_csv(state)
            for state in cursor.fetchall()
        ]

    @create_database
    async def find_last(self, address: str) -> Optional[DeviceStateEntity]:
        with sqlite3.connect(self.DBPATH) as conn:
            cursor = conn.cursor()
            # ?(プレースホルダー)で指定すると内部的にエスケープされる
            cursor.execute(
                "SELECT * FROM device_states WHERE address = ? ORDER BY created_at DESC;",
                (address,)
            )

        result = cursor.fetchone()
        if result is None or len(result) == 0:
            return None

        return DeviceStateEntity.from_csv(result)

    @create_database
    async def find_all_by_address(self, address: str) -> List[DeviceStateEntity]:
        with sqlite3.connect(self.DBPATH) as conn:
            cursor = conn.cursor()
            # ?(プレースホルダー)で指定すると内部的にエスケープされる
            cursor.execute(
                "SELECT * FROM device_states WHERE address = ?",
                (address,)
            )
        return [
            DeviceStateEntity.from_csv(state)
            for state in cursor.fetchall()
        ]

    @create_database
    async def save(self, state: DeviceStateEntity):
        with sqlite3.connect(self.DBPATH) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO device_states (id, address, found, created_at) VALUES (?, ?, ?, ?)",
                (state.id, state.address, state.found, int(state.created_at))
            )
            conn.commit()

    @create_database
    async def delete(self, state_id: str):
        with sqlite3.connect(self.DBPATH) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM device_states WHERE id = ?",
                (state_id,)
            )
            conn.commit()
