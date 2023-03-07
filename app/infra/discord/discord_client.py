from dataclasses import dataclass

import requests


@dataclass
class DiscordClient:
    webhook_url: str

    def send_message(self, message: str):
        requests.post(self.webhook_url, data={
            "content": message
        })
