import bluetooth


class DeviceResult:
    def __init__(self, address: str, found: bool):
        self.address = address
        self.found = found


def scan(address: str) -> DeviceResult:
    device_name = bluetooth.lookup_name(address)
    return DeviceResult(address=address, found=device_name is not None)
