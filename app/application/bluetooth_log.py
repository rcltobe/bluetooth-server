import logging
import time
from typing import Optional

from app.domain.service.device import DeviceService
from app.domain.util.datetime import datetime_now, is_same_day
from app.infra.spreadsheet.attendance_log_repository import SpreadSheetAttendanceLogRepository


class BluetoothLogTask:
    """
    一定時間ごと、付近の端末をスキャンし、その結果を保存する。
    """

    # スキャン処理を行う間隔
    INTERVAL_SCAN = 60

    SECONDS_HOUR = 60 * 60
    SECONDS_DAY = 24 * 60 * 60

    # 1日分のスキャン結果を残す
    SAVE_RESULT_SPAN = 1 * SECONDS_DAY

    def __init__(self):
        self.last_archived_at: Optional[datetime] = None
        self.attendance_log_repository = SpreadSheetAttendanceLogRepository()
        self.service = DeviceService()

    async def run(self):
        while True:
            await self._scan_devices(self.INTERVAL_SCAN)

            if not await self._did_archived_today():
                await self.attendance_log_repository.archive_logs()
                self.last_archived_at = datetime_now()

    async def _scan_devices(self, interval: int):
        logging.info("START SCAN")
        start = time.time()

        try:
            await self.service.scan_devices()
        except Exception as e:
            logging.error(e)

        logging.info("END SCAN")
        end = time.time()

        # 1回のサイクルに必ず一定時間かけることで、
        # 不必要な繰り返しをしないようにする
        if end - start < interval:
            duration = end - start
            time.sleep(interval - duration)

    async def _did_archived_today(self):
        if self.last_archived_at is None:
            return False

        now = datetime_now()
        is_archived_today = is_same_day(now, self.last_archived_at)
        return is_archived_today
