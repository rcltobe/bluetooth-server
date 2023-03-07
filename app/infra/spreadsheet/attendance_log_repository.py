from datetime import datetime, timedelta, timezone

from app.domain.models.attendance_log import AttendanceLog
from app.infra.spreadsheet.spreadsheet_util import SpreadSheetUtil


class SpreadSheetAttendanceLogRepository:
    """
    SpreadSheetのフォーマット
    (ID, MACアドレス, 入室時刻, 退出時刻(nullable))
    """
    spreadsheet_util = SpreadSheetUtil(4, "attendance")

    async def fetch_logs_of_today(self) -> list[AttendanceLog]:
        rows = await self.spreadsheet_util.get_values()

        t_delta = timedelta(hours=9)
        JST = timezone(t_delta, 'JST')
        now = datetime.now(JST)
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = now.replace(hour=23, minute=59, second=59, microsecond=0)
        logs_of_today = [
            row for row in rows
            if int(today_start.timestamp()) <= int(row[2]) < int(today_end.timestamp())
        ]

        return [AttendanceLog(
            user_id=log[0],
            bluetooth_mac_address=log[1],
            in_at=int(log[2]),
            out_at=int(log[3]) if log[3] != "" else None
        ) for log in logs_of_today]
