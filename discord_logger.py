import logging
import os

import dotenv

from app.infra.discord.discord_client import DiscordClient


def main():
    # ロガーの初期化
    logging.basicConfig(format='%(asctime)s[%(levelname)s]: %(message)s', level=logging.INFO)

    # .envファイルを読み込み
    dotenv.load_dotenv(verbose=True)
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    dotenv.load_dotenv(dotenv_path)

    discord_client = DiscordClient(os.environ.get("DISCORD_ATTENDANCE_LOG_WEBHOOK"))
    discord_client.send_message("Hello from python!")


if __name__ == '__main__':
    main()
