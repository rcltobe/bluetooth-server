import os
from typing import List

from app.domain.models.attendance_log import AttendanceLog
from app.domain.util.datetime import datetime_now
from app.infra.spreadsheet.spreadsheet_util import SpreadSheetUtil


def _is_empty_row(row: List[str]):
    for value in row:
        if len(value) != 0:
            return False
    return True


class SpreadSheetAttendanceLogRepository:
    """
    SpreadSheetのフォーマット
    (AttendanceID, Name, MACアドレス, 入室時刻, 退出時刻(nullable))
    """
    def __init__(self) -> None:
        self.spreadsheet_util_today = SpreadSheetUtil(4, book_name=os.environ.get("SPREADSHEET_BOOK_ATTENDANCE"))
        self.spreadsheet_util_archive = SpreadSheetUtil(4, book_name=os.environ.get("SPREADSHEET_BOOK_ATTENDANCE_ARCHIVE"))

    async def fetch_logs_of_today(self) -> List[AttendanceLog]:
        rows = await self.spreadsheet_util_today.get_values()

        # 空の行は取得しない
        rows = [row for row in rows if not _is_empty_row(row)]
        
        logs = [AttendanceLog.from_csv(log) for log in rows]        
        todays_logs = [log for log in logs if log.is_todays_log()]

        return todays_logs 
    
    async def update_logs_today(self, attendance_logs: List[AttendanceLog]):
        # reset all values
        await self.spreadsheet_util_today.clear_worksheet()

        # set values
        await self.spreadsheet_util_today.set_values(1, [
            log.to_csv() for log in attendance_logs
        ])

    # 本日分のログをアーカイブする
    async def archive_logs(self):
        logs_of_today = await self.fetch_logs_of_today()
        await self.spreadsheet_util_archive.append_all_values([log.to_csv() for log in logs_of_today])

        await self.spreadsheet_util_today.clear_worksheet()
