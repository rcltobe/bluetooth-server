import asyncio
import os

import dotenv

from app.domain.models.device_state import DeviceState
from app.infra.spreadsheet.device_state_repository import SpreadSheetDeviceStateRepository


async def main():
    rep = SpreadSheetDeviceStateRepository()
    states = await rep.find_all()
    address = "40:B0:76:89:98:B4"
    prev = DeviceState.get_last_device_states(address, states)
    print(prev.__dict__)
    new = DeviceState(address, True)
    print(new.should_update_state(prev))
    # rep = SpreadSheetDeviceStateRepository()
    # await rep.delete_before(1634099585)


if __name__ == '__main__':
    dotenv.load_dotenv(verbose=True)
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    dotenv.load_dotenv(dotenv_path)
    asyncio.run(main())
