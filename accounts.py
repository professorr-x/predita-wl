import requests
import json
import time
from colorama import Fore
from colorama import init
from datetime import datetime
import proxy_processor


class DiscordAccount:
    client = requests.Session()
    token = ""

    def set_token(self, token):
        self.token = token

    def join_server(self, invite_code, proxy):
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
                invite_code, invite_code
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

            url = "https://discord.com/api/v9/guilds/{}/requests/@me".format(
                server_id)

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

            response = requests.request(
                "PUT", url, headers=headers, data=data, proxies=proxies)

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
            "https://discord.com/api/v9/channels/{}/messages".format(
                channel_id),
            headers=headers,
            proxies=proxies,
            data=payload,
        )

        if res.status_code == 201 or 204 or 200:
            return True
        else:
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
                "https://discord.com/api/v9/channels/{}/messages".format(
                    channel_id),
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
        while True:
            res = self.client.delete(
                "https://discord.com/api/v9/channels/{}/messages/{}".format(
                    channel_id, message_id
                ),
                headers=headers,
            )

            if res.status_code == 204:
                return True
            elif res.status_code == 429:
                data = res.json()
                retry = data['retry_after']
                time.sleep(round(retry))
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
                "https://discord.com/api/v9/guilds/{}/requests/@me".format(
                    message_id),
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

    def check_token(self, proxy):
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
        try:
            res = self.client.get(
                'https://discord.com/api/v9/users/@me', headers=headers, proxies=proxies)
        except Exception as e:
            print(e)

        if res.status_code == 401 or 200:
            return res.status_code
        else:
            return False

    def account_checker(self, user_accounts, proxy_pool):
        for token in user_accounts:
            try:
                token = token.split(":")[2]
            except:
                pass

            print(Fore.CYAN +
                  "[{}] Getting Proxies...".format(str(datetime.now())))
            proxy = proxy_processor.GetProxy(proxy_pool)
            print(Fore.CYAN +
                  "[{}] Using Proxy {}".format(str(datetime.now()), proxy))

            self.set_token(token)
            account_status = self.check_token(proxy)

            if account_status == 401:
                print(
                    Fore.YELLOW + "[{}] Writing Banned Token {}".format(str(datetime.now()), token))
                with open('banned_accounts.txt', 'a') as f:
                    f.write(token + '\n')
            elif account_status == 200:
                print(
                    Fore.GREEN + "[{}] Writing Verified Token {}".format(str(datetime.now()), token))
                with open('verified_accounts.txt', 'a') as f:
                    f.write(token + '\n')
            else:
                print(
                    Fore.RED + "[{}] Unable To Check Token {}".format(str(datetime.now()), token))
        input(Fore.CYAN + "[{}] Process Complete".format(str(datetime.now())))
