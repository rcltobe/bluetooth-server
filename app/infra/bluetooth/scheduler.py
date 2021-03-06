import asyncio
import logging
import time

from app.domain.service.device import DeviceService


class BluetoothScanScheduler:
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

    def run_sync(self):
        asyncio.run(self.run())

    async def run(self):
        next_delete = time.time() + self.SECONDS_HOUR
        while True:
            await self._scan_devices(self.INTERVAL_SCAN)

            # 1時間ごとに、SAVE_RESULT_SPANで指定した期間の出席データを削除する
            now = time.time()
            if now < next_delete:
                await self.service.delete_results_before(time.time() - self.SAVE_RESULT_SPAN)
                next_delete += self.SECONDS_HOUR

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
