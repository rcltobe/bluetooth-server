from flask import Blueprint, request
from concurrent import futures
from app.infra.bluetooth import scan_device

route = Blueprint("bluetooth", __name__)


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
    future_list = []
    with futures.ThreadPoolExecutor() as executor:
        for address in addresses:
            future = executor.submit(scan_device, address)
            future_list.append(future)

    results = []
    for future in future_list:
        result = future.result()
        results.append({
            "address": result.address,
            "found": result.found,
        })

    return {"results": results}
