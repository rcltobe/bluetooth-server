import bluetooth


class ScanDeviceResult:
    def __init__(self, address: str, found: bool):
        self.address = address
        self.found = found


def scan_device(address: str) -> ScanDeviceResult:
    device_name = bluetooth.lookup_name(address)
    return ScanDeviceResult(address=address, found=device_name is not None)
