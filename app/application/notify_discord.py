import os

from app.domain.util.datetime import datetime_today, is_same_day
from app.infra.discord.discord_client import DiscordClient
from app.infra.spreadsheet.attendance_log_repository import SpreadSheetAttendanceLogRepository
from app.infra.spreadsheet.user_repository import SpreadSheetUserRepository


class AttendanceLogInDay:
    _attendance_log_repository = SpreadSheetAttendanceLogRepository()
    _user_repository = SpreadSheetUserRepository()
    _cache_bluetooth_address_to_name = {}
    _notified_logs = {}

    discord_client = DiscordClient(os.environ.get("DISCORD_ATTENDANCE_LOG_WEBHOOK"))

    """
    1日の出席ログをスキャン
    """

    async def run(self):
        # 出席を確認
        attendance_logs_today = await self._attendance_log_repository.fetch_logs_of_today()
        for attendance_log in attendance_logs_today:
            user_name = await self._fetch_user_name_by_bluetooth_address(attendance_log.bluetooth_mac_address)

            # 既に通知した人に関してはログを取らない
            did_notified = user_name in self._notified_logs
            did_notified_today = did_notified and is_same_day(self._notified_logs[user_name], datetime_today())
            if did_notified_today:
                continue

            # Discordに通知
            self.discord_client.send_message(f"{user_name}の出席を確認しました")
            self._notified_logs[user_name] = datetime_today()

    async def _fetch_user_name_by_bluetooth_address(self, bluetooth_mac: str) -> str:
        if bluetooth_mac not in self._cache_bluetooth_address_to_name:
            users = await self._user_repository.find_all()
            for user in users:
                self._cache_bluetooth_address_to_name[user.address] = user.user_name

        return self._cache_bluetooth_address_to_name[bluetooth_mac]
