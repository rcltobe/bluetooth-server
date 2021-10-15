import bluetooth


class ScanDeviceResult:
    """
    端末の検索結果
    """

    def __init__(self, address: str, found: bool):
        self.address = address
        self.found = found

    def to_json(self):
        return {
            "address": self.address,
            "found": self.found
        }


def scan_device(address: str) -> ScanDeviceResult:
    """
    注意! この処理を、並行、並列処理で呼び出すと正しいスキャン結果を得ることができません。
    :param address に対応した端末を検索する
    """
    if not bluetooth.is_valid_address(address):
        return ScanDeviceResult(address=address, found=False)

    device_name = bluetooth.lookup_name(address, timeout=5)  # 最低5秒で検索できることが多い
    return ScanDeviceResult(address=address, found=device_name is not None)
