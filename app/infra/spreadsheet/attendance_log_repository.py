from app.domain.models.attendance_log import AttendanceLog
from app.domain.util.datetime import datetime_now
from app.infra.spreadsheet.models.attendance_log_entity import AttendanceLogEntity
from app.infra.spreadsheet.spreadsheet_util import SpreadSheetUtil
from typing import List

class SpreadSheetAttendanceLogRepository:
    """
    SpreadSheetのフォーマット
    (AttendanceID, MACアドレス, 入室時刻, 退出時刻(nullable))
    """
    spreadsheet_util_today = SpreadSheetUtil(4, "attendance")
    spreadsheet_util_archive = SpreadSheetUtil(4, "attendance_archive")

    async def fetch_logs_of_today(self) -> List[AttendanceLog]:
        rows = await self.spreadsheet_util_today.get_values()

        now = datetime_now()
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = now.replace(hour=23, minute=59, second=59, microsecond=0)
        logs_of_today = [
            row for row in rows
            if int(today_start.timestamp()) <= int(row[2]) <= int(today_end.timestamp())
        ]

        return [AttendanceLogEntity.from_csv(log).to_attendance_log() for log in logs_of_today]

    async def update_logs_today(self, attendance_logs: List[AttendanceLog]):
        # reset all values
        await self.spreadsheet_util_today.delete_rows(0, 1000000)

        # set values
        await self.spreadsheet_util_today.append_all_values([
            log.to_csv() for log in attendance_logs
        ])

    # 本日分のログをアーカイブする
    async def archive_logs(self):
        log_of_today = await self.fetch_logs_of_today()
        await self.spreadsheet_util_archive.append_all_values([log.to_csv() for log in log_of_today])
        await self.spreadsheet_util_today.delete_rows(0, 100000)
