import os

from app.infra.discord.discord_client import DiscordClient
from app.infra.spreadsheet.attendance_log_repository import SpreadSheetAttendanceLogRepository
from app.infra.spreadsheet.user_repository import SpreadSheetUserRepository


class AttendanceLogInDay:
    _attendance_log_repository = SpreadSheetAttendanceLogRepository()
    _user_repository = SpreadSheetUserRepository()
    _self_cache_uid_to_name = {}

    """
    1日の出席ログをスキャン
    """

    def run(self):
        # 出席を確認

        # TODO: 既に通知した人に関してはログを取らない

        # Discordに通知
        discord_client = DiscordClient(os.environ.get("DISCORD_ATTENDANCE_LOG_WEBHOOK"))
        discord_client.send_message("Hello from python!")

    async def _fetch_user_name_by_user_id(self, user_id: str) -> str:
        if user_id not in self._self_cache_uid_to_name:
            users = await self._user_repository.find_all()
            for user in users:
                self._self_cache_uid_to_name[user.user_id]

        return self._self_cache_uid_to_name[user_id]
