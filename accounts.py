import requests
import json
import random
from twocap_solver import solve_captcha
import time


class DiscordAccount:
    client = requests.Session()
    token = ""

    def set_token(self, token):
        self.token = token

    def login(self, email, password):
        """
        login to user account

        params:

        email: str
        password: str

        """
        payload = json.dumps(
            {
                "login": email,
                "password": password,
                "undelete": False,
                "captcha_key": None,
                "login_source": None,
                "gift_code_sku_id": None,
            }
        )

        headers = {
            "Host": "discord.com",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
            "Accept": "*/*",
            "Accept-Language": "en-US",
            "Accept-Encoding": "gzip, deflate, br",
            "Content-Type": "application/json",
            "Origin": "https://discord.com",
            "Connection": "keep-alive",
            "Referer": "https://discord.com/channels/@me",
            "sec-ch-ua": '" Not;A Brand";v="99", "Firefox";v="91", "Chromium";v="96"',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "sec-ch-ua-mobile": "?0",
            "TE": "trailers",
        }

        while True:
            res = self.client.post(
                "https://discord.com/api/v9/auth/login", headers=headers, data=payload
            )
            if res.status_code == 200:
                self.token = res.json()["token"]
                return True
            elif res.status_code == 400:
                data = json.loads(res.text)
                if data["captcha_key"]:
                    captcha = solve_captcha()
                    if captcha:
                        payload = json.loads(payload)
                        payload["captcha_key"] = captcha["code"]
                        payload = json.dumps(payload)
                print("Retrying")
            else:
                return False

    def join_server(self, server_uid, proxy):
        """
        join discord server

        params

        server_uid: str - found on the end of the discord invite link

        """
        headers = {
            "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
            "X-Debug-Options": "bugReporterEnabled",
            "sec-ch-ua-mobile": "?0",
            "Authorization": self.token,
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
            "X-Discord-Locale": "en-US",
            "sec-ch-ua-platform": '"macOS"',
            "Accept": "*/*",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
        }

        proxies = {"http": proxy, "https": proxy}
        res = self.client.get(
            "https://discord.com/api/v9/invites/{}?inputValue=https%3A%2F%2Fdiscord.gg%2F{}&with_counts=true&with_expiration=true".format(
                server_uid, server_uid
            ),
            headers=headers,
            proxies=proxies,
        )

        code = res.json()["code"]

        res = self.client.post(
            "https://discord.com/api/v9/invites/" + str(code),
            headers=headers,
            data={},
            proxies=proxies,
        )

        if res.status_code == 200:
            return True
        else:
            return False

    def react_to_verify(self, channel_id, message_id, emoji_id):
        """
        React to verify yourself on a server

        params

        channel_id: str
        message_id: str
        emoji_id: str - found by inspect the emoji

        """
        headers = {
            "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
            "X-Debug-Options": "bugReporterEnabled",
            "sec-ch-ua-mobile": "?0",
            "Authorization": self.token,
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
            "X-Discord-Locale": "en-US",
            "sec-ch-ua-platform": '"macOS"',
            "Accept": "*/*",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
        }

        res = self.client.put(
            "https://discord.com/api/v9/channels/{}/messages/{}/reactions/{}/%40me".format(
                channel_id, message_id, emoji_id
            ),
            headers=headers,
            data={},
        )

        if res.status_code == 204:
            return True
        else:
            res = self.client.put(
                "https://discord.com/api/v9/guilds/{}/requests/@me".format(message_id),
                headers=headers,
                data={},
            )
            res = self.client.put(
                "https://discord.com/api/v9/channels/{}/messages/{}/reactions/{}/%40me".format(
                    channel_id, message_id, emoji_id
                ),
                headers=headers,
                data={},
            )
            return False

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
            time.sleep(60)
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

    def select_option_verification(self):
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

        res = self.client.get(
            "https://discord.com/api/v9/channels/920610008784318545/messages?limit=50",
            headers=headers,
        )

    def post_member_verification(self, server_id, proxy):
        proxies = {"http": proxy, "https": proxy}

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
        res = self.client.get(
            "https://discord.com/api/v9/guilds/{}/member-verification?with_guild=false&invite_code=monsterapeclub".format(
                server_id
            ),
            headers=headers,
            proxies=proxies,
        )

        if res.status_code == 200:
            data = json.dumps(res.json())

            url = "https://discord.com/api/v9/guilds/929363884790390784/requests/@me"

            headers = {
              'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
              'X-Debug-Options': 'bugReporterEnabled',
              'sec-ch-ua-mobile': '?0',
              'Authorization': self.token,
              'Content-Type': 'application/json',
              'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
              'X-Discord-Locale': 'en-US',
              'sec-ch-ua-platform': '"macOS"',
              'Accept': '*/*'
            }

            response = requests.request("PUT", url, headers=headers, data=data, proxies=proxies)

            if response.status_code == 201 or 204 or 200:
                return True
            else:
                return False
        else:
            return False

    def code_verification(self, channel_id, code, proxy):
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

        proxies = {"http": proxy, "https": proxy}

        payload = json.dumps({"content": code, "nonce": "", "tts": False})

        res = self.client.post(
            "https://discord.com/api/v9/channels/{}/messages".format(channel_id),
            headers=headers,
            proxies=proxies,
            data=payload,
        )

        if res.status_code == 201 or 204 or 200:
            return True
        else:
            return False
