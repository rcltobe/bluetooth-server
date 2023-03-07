import asyncio
import logging
import os

import dotenv

from app.application.bluetooth_log import BluetoothLogTask


async def main():
    # ロガーの初期化
    logging.basicConfig(
        filename="bluetooth.log",
        format='%(asctime)s[%(levelname)s]: %(message)s',
        level=logging.INFO
    )

    # .envファイルを読み込み
    dotenv.load_dotenv(verbose=True)
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    dotenv.load_dotenv(dotenv_path)

    # 端末のスキャンを開始
    task = BluetoothLogTask()
    await task.run()


if __name__ == '__main__':
    asyncio.run(main())
