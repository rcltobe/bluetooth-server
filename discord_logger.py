import asyncio
import logging
import os
import time

import dotenv

from app.application.notify_discord import AttendanceLogInDay

# 5分ごと通知
INTERVAL_NOTIFY = 5 * 60


async def main():
    # ロガーの初期化
    logging.basicConfig(
        filename="discord_logger.log",
        format='%(asctime)s[%(levelname)s]: %(message)s',
        level=logging.INFO
    )

    # .envファイルを読み込み
    dotenv.load_dotenv(verbose=True)
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    dotenv.load_dotenv(dotenv_path)

    task = AttendanceLogInDay()

    while True:
        start = time.time()
        try:
            logging.info("NOTIFY")
            await task.run()
        except Exception as e:
            logging.error(e, stack_info=True)

        # 1回のサイクルに必ず一定時間かけることで、
        # 不必要な繰り返しをしないようにする
        end = time.time()
        if end - start < INTERVAL_NOTIFY:
            duration = end - start
            time.sleep(INTERVAL_NOTIFY - duration)


if __name__ == '__main__':
    asyncio.run(main())
