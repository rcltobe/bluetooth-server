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
            service = BluetoothService()
            await service.scan_devices(None)
            time.sleep(10)

    asyncio.run(_scan_devices())


if __name__ == '__main__':
    t = threading.Thread(target=scan_devices)
    t.start()
    app = create_app()
    app.run()
