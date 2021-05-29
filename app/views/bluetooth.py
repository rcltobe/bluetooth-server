from flask import Blueprint, request
from app.domain.service.bluetooth import BluetoothService

route = Blueprint("bluetooth", __name__)


@route.get('/bluetooth/scan')
async def scans_bluetooth():
    service = BluetoothService()
    return {
        "results": await service.scan_devices(None)
    }


@route.post('/bluetooth/scan')
async def scan_bluetooth():
    """
    Bluetooth端末のMACアドレスから、そのデバイスが近くにいるかどうかを調べる。
    リクエスト例:
    {
        "devices": [
            "XX:XX:XX:XX:XX:XX",
            "OO:OO:OO:OO:OO:OO"
        ]

    }
    レスポンス例
    {
        "results": [
            {
                "address": "XX:XX:XX:XX:XX:XX",
                "found": true
            },
            {
                "address": "OO:OO:OO:OO:OO:OO",
                "found": false
            }
        ]
    }
    """

    addresses = request.json["devices"]
    service = BluetoothService()
    results = await service.scan_devices(addresses)
    return {"results": results}
