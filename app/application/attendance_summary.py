from datetime import datetime, timedelta
import os
from typing import List

from app.domain.models.attendance_summary import AttendanceSummary
from app.domain.models.attendance_weekly_summary import AttendanceWeeklySummary
from app.infra.discord.discord_client import DiscordClient
from app.infra.firestore.attendance_log_repository import FirestoreAttendanceLogRepository
from app.infra.spreadsheet.user_repository import SpreadSheetUserRepository

class AttendanceSummaryTask:
    def __init__(self, discord_webhook_url: str):
        self.attendance_log_repository = FirestoreAttendanceLogRepository()
        self.user_repository = SpreadSheetUserRepository() 
        self.discord_client = DiscordClient(webhook_url=discord_webhook_url)

    async def run(
        self, 
        date_start_generate_summary: datetime,
    ):
        """
        指定した日の出席サマリーを作成し、Discordに通知する
        
        メッセージ例:
        # 2021-01-01 ~ 2021-01-07 の出席サマリー
        ユーザー名： 出席回数, 火曜日10時前登校, 6時間以上出席回数
        user_name: 4, ○, 2
        user_name: 3, ×, 1 
        """
        date_start = date_start_generate_summary
        date_end = date_start_generate_summary + timedelta(days=7)

        users = await self.user_repository.find_all()
        attendance_logs = await self.attendance_log_repository.fetch_logs_of_day_between(
            day_start=date_start,
            day_end=date_end,
        )

        summaries: List[AttendanceWeeklySummary] = []
        for user in users:
            summary = AttendanceWeeklySummary.generate_weekly_summary(
                attendance_logs=attendance_logs,
                user_id=user.user_id,
                start_date=date_start_generate_summary,
            )
            summaries.append(summary)

        message = "```"
        message += f"# {date_start.strftime('%Y-%m-%d')} ~ {date_end.strftime('%Y-%m-%d')} の出席サマリー\n" 
        message += f"ユーザー名,{', '.join(AttendanceWeeklySummary.csv_header())}\n"
        for summary in summaries:
            message += f"{summary.user_name}, {', '.join(summary.to_csv())}\n"
        message += "```"

        self.discord_client.send_message(message=message)
