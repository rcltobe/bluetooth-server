import logging
from typing import List, Optional

from app.domain.models.attendance_log import AttendanceLog
from app.domain.models.user import User
from app.domain.repository.user_repository import AbstractUserRepository
from app.infra.bluetooth.scanner import scan_device
from app.infra.repository import RepositoryContainer
from app.infra.spreadsheet.attendance_log_repository import SpreadSheetAttendanceLogRepository


class DeviceService:
    """
    端末のスキャン処理と、スキャン結果の保存を行う
    SpreadSheetに過度なアクセスをしないように実装されている。
    """

    def __init__(self,
                 user_repository: AbstractUserRepository = RepositoryContainer.device_repository,
                 ):
        self.attendance_log_repository = SpreadSheetAttendanceLogRepository()
        self.user_repository = user_repository
        self.logger = logging.getLogger(__name__)

    INTERVAL_UPDATE = 10 * 60  # 状態が変化していないときに、更新する間隔

    async def scan_devices(self, room: str):
        """
        Bluetooth端末を検索

        @param room 部屋名

        【注意】
        この処理を同時に呼ぶと、正しい結果を得ることができない
        """
        # 登録されたすべての端末のMACアドレスを取得
        users = await self.user_repository.find_all()
        addresses = [device.address for device in users]

        self.logger.info(f"SCAN FOR {addresses}")

        # 本日分のAttendance Logを取得する
        attendance_logs_today = await self.attendance_log_repository.fetch_logs_of_today()

        # 端末をBluetoothでスキャンする
        attendance_logs = []
        attendance_logs.append(attendance_logs_today)

        for user in users:
            try:
                attendance_log = await self._scan_device(user=user, prev_attendance_log=attendance_logs_today, room=room)
                if attendance_log is None:
                    continue
                attendance_logs.append(attendance_log)
            except Exception as e:
                logging.error(e, stack_info=True)

        # attendance logを更新する
        await self.attendance_log_repository.update_logs_today(attendance_logs)

    async def _scan_device(
            self,
            user: User,
            prev_attendance_logs: Optional[List[AttendanceLog]],
            room: str
    ) -> Optional[AttendanceLog]:
        """
        付近に端末がいるかどうか、スキャンする
        @:param prev_state 前回のスキャン結果
        @:return スキャン結果（10分以内に発見されている場合はNoneを返す）
        """
        # スキャン
        result = scan_device(address=user.address)

        attendance_log = AttendanceLog.create_attendance_log(
            prev_attendance_logs=prev_attendance_logs,
            user=user,
            is_found=result.found,
            room=room,
        )
        if attendance_log is not None:
            if result.found:
                self.logger.info(f"DEVICE SCANNED -> FOUND {user.user_name}:{user.address}")
            else:
                self.logger.info(f"DEVICE SCANNED -> NOT FOUND {user.user_name}:{user.address}")
        else:
            self.logger.info(f"DEVICE SCANNED -> NOT NOT LOGGED {user.user_name}:{user.address}")

        return attendance_log
