import asyncio
from datetime import datetime
import logging
import os
import time

from app.application.attendance_summary import AttendanceSummaryTask
from app.domain.util.datetime import datetime_today
import dotenv

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
    
    logging.info("Started Discord Attendance Summary")
    task = AttendanceSummaryTask(
        discord_webhook_url=os.environ.get("DISCORD_ATTENDANCE_LOG_SUMMARY_WEBHOOK")
    )

    today = datetime_today()
    yesterday = today - datetime.timedelta(days=1)
    await task.run(date_to_generate_summary=yesterday)

    logging.info("Finished Discord Attendance Summary")

if __name__ == '__main__':
    asyncio.run(main())