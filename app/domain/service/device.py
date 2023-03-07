import logging
import time
from typing import Optional

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

    async def scan_devices(self):
        """
        Bluetooth端末を検索

        【注意】
        この処理を同時に呼ぶと、正しい結果を得ることができない
        """
        # 登録されたすべての端末のMACアドレスを取得
        users = await self.user_repository.find_all()
        addresses = [device.address for device in users]

        self.logger.info(f"SCAN FOR {addresses}")

        # 本日分のAttendance Logを取得する
        attendance_logs_today = await self.attendance_log_repository.fetch_logs_of_today()
        bluetooth_address_to_log = {log.bluetooth_mac_address: log for log in attendance_logs_today}

        # 端末をBluetoothでスキャンする
        attendance_logs = []
        for user in users:
            prev_log: Optional[AttendanceLog] = bluetooth_address_to_log.get(user.address)
            try:
                attendance_log = self._scan_device(user=user, prev_attendance_log=prev_log)
                attendance_logs.append(attendance_log)
            except Exception as e:
                logging.error(e)
                if prev_log is None:
                    continue
                attendance_logs.append(prev_log)

        # attendance logを更新する
        await self.attendance_log_repository.update_logs_today(attendance_logs)

    async def _scan_device(
            self,
            user: User,
            prev_attendance_log: Optional[AttendanceLog]
    ) -> AttendanceLog:
        """
        付近に端末がいるかどうか、スキャンする
        @:param prev_state 前回のスキャン結果
        @:return スキャン結果（10分以内に発見されている場合はNoneを返す）
        """
        # スキャン
        result = scan_device(address=user.address)

        if prev_attendance_log is None:
            attendance_log = AttendanceLog(
                user_id=user.user_id,
                bluetooth_mac_address=user.address,
                in_at=int(time.time()),
                out_at=None,
            )
        else:
            prev_attendance_log.update_log(result.found)
            attendance_log = prev_attendance_log

        self.logger.info(f"DEVICE SCANNED {attendance_log.to_json()}")
        return attendance_log
