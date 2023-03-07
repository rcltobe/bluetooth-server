import logging
import time

from app.domain.service.device import DeviceService


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
        self.service = DeviceService()

    async def run(self):
        while True:
            await self._scan_devices(self.INTERVAL_SCAN)

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