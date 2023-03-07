import asyncio
import logging
import os

import dotenv

from app.application.notify_discord import AttendanceLogInDay


async def main():
    # ロガーの初期化
    logging.basicConfig(format='%(asctime)s[%(levelname)s]: %(message)s', level=logging.INFO)

    # .envファイルを読み込み
    dotenv.load_dotenv(verbose=True)
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    dotenv.load_dotenv(dotenv_path)

    task = AttendanceLogInDay()
    await task.run()

if __name__ == '__main__':
    asyncio.run(main())
