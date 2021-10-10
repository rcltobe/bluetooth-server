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
    logger = logging.getLogger(__name__)

    async def _scan_devices():
        logger.info("START SCAN")
        while True:
            start = time.time()
            service = DeviceService()
            await service.scan_devices(None)
            end = time.time()

            # 1回のサイクルに最低10秒かかるようにし、
            # 不必要な繰り返しをしないようにする
            if end - start < 10:
                duration = end - start
                time.sleep(10 - duration)

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
