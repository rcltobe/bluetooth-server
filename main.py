import asyncio
import logging
import os
import threading
import time

import dotenv

from app.application import create_app
from app.domain.service.device import DeviceService


def scan_devices():
    """
    10秒ごとにBluetooth端末の検索を行う
    """
    # スキャン処理を行う間隔
    interval_scan = 60

    # 2日分のスキャン結果を残す
    mills_day = 24 * 60 * 60 * 1000
    save_result_span = 2 * mills_day

    async def _scan_devices():
        logging.info("START SCAN")

        counter = 0
        while True:
            start = time.time()
            service = DeviceService()
            try:
                await service.scan_devices(None)
            except Exception as e:
                logging.error(e)

            end = time.time()

            # 1回のサイクルに最低60秒かかるようにし、
            # 不必要な繰り返しをしないようにする
            if end - start < interval_scan:
                duration = end - start
                time.sleep(interval_scan - duration)

            # 1時間ごとに、今から2日前の出席データを削除する
            if counter == 60:
                await service.delete_results_before(time.time() - save_result_span)
                counter = 0

            counter += 1

    asyncio.run(_scan_devices())


if __name__ == '__main__':
    # ロガーの初期化
    logging.basicConfig(format='%(asctime)s[%(levelname)s]: %(message)s', level=logging.INFO)

    # .envファイルを読み込み
    dotenv.load_dotenv(verbose=True)
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    dotenv.load_dotenv(dotenv_path)

    # 端末のスキャンを開始
    t = threading.Thread(target=scan_devices)
    t.start()

    # サーバーを起動
    app = create_app()
    app.run(host="0.0.0.0")
