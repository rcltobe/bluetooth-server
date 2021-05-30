import asyncio
from concurrent.futures import ProcessPoolExecutor

import bluetooth


class ScanDeviceResult:
    def __init__(self, address: str, found: bool):
        self.address = address
        self.found = found


async def scan_device(address: str) -> ScanDeviceResult:
    loop = asyncio.get_running_loop()
    executor = ProcessPoolExecutor()
    result = await asyncio.ensure_future(loop.run_in_executor(executor, bluetooth.lookup_name, address))
    executor.shutdown(wait=True)
    device_name = result
    return ScanDeviceResult(address=address, found=device_name is not None)
