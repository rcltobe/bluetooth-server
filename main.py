import asyncio
import threading
import time

from app.application import create_app
from app.domain.service.bluetooth import BluetoothService


def scan_devices():
    """
    10秒ごとにBluetooth端末の検索を行う
    """

    async def _scan_devices():
        while True:
            start = time.time()
            service = BluetoothService()
            await service.scan_devices(None)
            end = time.time()

            # 1回のサイクルに最低10秒かかるようにし、
            # 不必要な繰り返しをしないようにする
            if end - start < 10:
                duration = end - start
                time.sleep(10 - duration)

    asyncio.run(_scan_devices())


if __name__ == '__main__':
    t = threading.Thread(target=scan_devices)
    t.start()
    app = create_app()
    app.run(host="0.0.0.0")
