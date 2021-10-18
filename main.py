import logging
import os
import threading

import dotenv

from app.application import create_app
from app.infra.bluetooth.scheduler import BluetoothScanScheduler


def main():
    # ロガーの初期化
    logging.basicConfig(format='%(asctime)s[%(levelname)s]: %(message)s', level=logging.INFO)

    # .envファイルを読み込み
    dotenv.load_dotenv(verbose=True)
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    dotenv.load_dotenv(dotenv_path)

    # 端末のスキャンを開始
    scheduler = BluetoothScanScheduler()
    t = threading.Thread(target=scheduler.run_sync)
    t.start()

    # サーバーを起動
    app = create_app()
    app.run(host="0.0.0.0")


if __name__ == '__main__':
    main()
