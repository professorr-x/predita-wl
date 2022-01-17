import requests
import json
import time


class DiscordAccount:
    client = requests.Session()
    token = ""

    def set_token(self, token):
        self.token = token

    def send_message(self, channel_id, message):
        payload = json.dumps(
            {
                "content": message,
                "nonce": "",
                "tts": False,
            }
        )

        headers = {
            "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
            "X-Debug-Options": "bugReporterEnabled",
            "sec-ch-ua-mobile": "?0",
            "Authorization": self.token,
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
            "X-Discord-Locale": "en-US",
            "sec-ch-ua-platform": '"macOS"',
            "Accept": "*/*",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
        }
        try:
            res = self.client.post(
                "https://discord.com/api/v9/channels/{}/messages".format(channel_id),
                headers=headers,
                data=payload,
            )

            if res.status_code == 200:
                return res.json()
            else:
                return False
        except Exception as e:
            print(e)
            return False

    def delete_message(self, channel_id, message_id):
        headers = {
            "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
            "X-Debug-Options": "bugReporterEnabled",
            "sec-ch-ua-mobile": "?0",
            "Authorization": self.token,
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
            "X-Discord-Locale": "en-US",
            "sec-ch-ua-platform": '"macOS"',
            "Accept": "*/*",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
        }

        res = self.client.delete(
            "https://discord.com/api/v9/channels/{}/messages/{}".format(
                channel_id, message_id
            ),
            headers=headers,
        )

        if res.status_code == 204:
            return True
        else:
            res = self.client.delete(
                "https://discord.com/api/v9/channels/{}/messages/{}".format(
                    channel_id, message_id
                ),
                headers=headers,
            )
            if res.status_code == 204:
                return True
            else:
                return False
