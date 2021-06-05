import csv
import os
from typing import List

from app.domain.models.body_temperature import BodyTemperature
from app.domain.repository.body_temperature_repository import AbstractBodyTemperatureRepository
from app.infra.csv.csv_util import save_row


class CsvBodyTemperatureRepository(AbstractBodyTemperatureRepository):
    _FILE_PATH = f"{os.curdir}/data/body_temperature.csv"

    async def find_all(self) -> List[BodyTemperature]:
        if not os.path.exists(self._FILE_PATH):
            return []

        with open(self._FILE_PATH, 'r') as file:
            reader = csv.reader(file)
            rows = [row for row in reader]

        return [
            result
            for result in [BodyTemperature.from_csv(row) for row in rows]
            if result is not None
        ]

    async def save(self, data: BodyTemperature):
        data_csv = data.to_csv()
        if data_csv is None:
            return
        save_row(self._FILE_PATH, data_csv)
