import logging
import os
from typing import Dict, List
from collections import defaultdict

from app.domain.models.attendance_log import AttendanceLog
from app.domain.util.datetime import datetime_now, datetime_today, is_same_day
from app.infra.discord.discord_client import DiscordClient
from app.infra.spreadsheet.attendance_log_repository import SpreadSheetAttendanceLogRepository
from app.infra.spreadsheet.user_repository import SpreadSheetUserRepository


class AttendanceLogInDay:
    _attendance_log_repository = SpreadSheetAttendanceLogRepository()
    _user_repository = SpreadSheetUserRepository()

    # 一日を通して、通知したかどうかだけを確認するためのデータ
    # このデータに入力された人は、すでに出席が確認されていて、その日は通知されない
    # user_name: { user_name: str, created_at: datetime }
    _notified_logs = {} 
    
    # 出席、退室のどちらの通知も行うためのデータ
    # 最後の出席データが記録される
    # user_name: { user_name: str, is_attended: bool, created_at: datetime }
    _attendance_logs = {}

    def __init__(self):
        self.discord_client = DiscordClient(webhook_url=os.environ.get("DISCORD_ATTENDANCE_LOG_WEBHOOK"))
        self.discord_client_detailed = DiscordClient(webhook_url=os.environ.get("DISCORD_ATTENDANCE_LOG_DETAILED_WEBHOOK"))

    """
    1日の出席ログをスキャン
    """

    async def run(self):
        self._remove_logs_before_today()

        # 出席ログを取得
        attendance_logs_today = await self._attendance_log_repository.fetch_logs_of_today()

        # ユーザーごとにログを分ける 
        attendance_logs_per_user = defaultdict(list)
        for attendance_log in attendance_logs_today:
            attendance_logs_per_user[attendance_log.user_name].append(attendance_log)

        # 通知
        await self.notify(attendance_logs_per_user)
        await self.notify_once(attendance_logs_per_user)


    # 一日に一度だけ通知を行う
    async def notify_once(self, attendance_logs_per_user: Dict[str, List[AttendanceLog]]):
        notify_target_users = []
        for user_name, attendance_log_of_user in attendance_logs_per_user.values():
            if len(attendance_log_of_user) == 0:
                continue
            
            # 最後のログを取得
            last_attendance_log = sorted(attendance_log_of_user, key=lambda log: log.created_at, reverse=True)[-1]
            user_name = last_attendance_log.user_name
            is_attended = last_attendance_log.is_attended

            # 出席が確認され、まだ通知していない人に関しては通知
            did_notified = user_name in self._notified_logs
            did_notified_today = did_notified and is_same_day(self._notified_logs[user_name], datetime_today())
            if not did_notified_today and is_attended:
                notify_target_users.append({
                    "user_name": user_name,
                    "is_attended": True, 
                })

        # discordに通知
        logging.info(f"notify {notify_target_users}")
        for notify_content in notify_target_users:
            user_name = notify_content["user_name"]
            is_attended = notify_content["is_attended"]

            self.discord_client.send_message(f"{user_name}の出席を確認しました")
            self._notified_logs[user_name] = {
                "user_name": user_name,
                "created_at": datetime_today()
            } 

    # 出席と退出のどちらも通知を行う
    async def notify(self, attendance_logs_per_user: Dict[str, List[AttendanceLog]]):
        notify_detail_target_users = []
        for user_name, attendance_log_of_user in attendance_logs_per_user.values():
            if len(attendance_log_of_user) == 0:
                continue
            
            # 最後のログを取得
            last_attendance_log = sorted(attendance_log_of_user, key=lambda log: log.created_at, reverse=True)[-1]
            user_name = last_attendance_log.user_name
            is_attended = last_attendance_log.is_attended

            # 過去のログと状態が変化している場合は詳細通知
            is_changed = self._notified_logs.get(user_name, {}).get("is_attended", False) != is_attended
            if is_changed:
                notify_detail_target_users.append({
                    "user_name": user_name,
                    "is_attended": is_attended
                })
        
        # discordに通知(詳細)
        logging.info(f"notify_detail {notify_detail_target_users}")
        for notify_content in notify_detail_target_users:
            user_name = notify_content["user_name"]
            is_attended = notify_content["is_attended"]

            self.discord_client_detailed.send_message(
                f"{user_name}の出席を確認しました"
                if is_attended
                else f"{user_name}の退室を確認しました"
            )
            self._attendance_logs[user_name] = {
                "user_name": user_name,
                "is_attended": is_attended,
                "created_at": datetime_now()
            }


    # 今日以前のログを削除
    def _remove_logs_before_today(self):
        for user_name, created_at in self._notified_logs.items():
            if not is_same_day(created_at, datetime_today()):
                del self._notified_logs[user_name]