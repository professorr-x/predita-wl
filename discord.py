import requests
import time

class Discord:
    headers = {
        "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
        "X-Debug-Options": "bugReporterEnabled",
        "sec-ch-ua-mobile": "?0",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
        "X-Discord-Locale": "en-US",
        "sec-ch-ua-platform": '"macOS"',
        "Accept": "*/*",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
    }

    def get_server_name(self, token, server_id):
        url = "https://discord.com/api/v9/guilds/{}".format(server_id)
        self.headers["Authorization"] = token
        try:
            response = requests.get(url, headers=self.headers)
            res = response.json()
            name = res["name"]
        except Exception as e:
            print(e)
            name = server_id
        return name

    def get_channels(self, token, server_id):
        url = "https://discord.com/api/v9/guilds/{}/channels".format(server_id)
        self.headers["Authorization"] = token
        try:
            response = requests.get(url, headers=self.headers)
            res = response.json()
            if response.status_code == 200:
                return res
            elif response.status_code == 429:
                time.sleep(round(res['retry_after']))
            else:
                return None
        except Exception as e:
            print(e)
            return None

    def get_channel_name(self, token, channel_id):
        url = "https://discord.com/api/v9/channels/{}".format(channel_id)
        self.headers["Authorization"] = token
        try:
            response = requests.get(url, headers=self.headers)
            res = response.json()
            name = res["name"]
        except Exception as e:
            print(e)
            name = channel_id
        return name

    def get_messages(self, token, channel_id):
        url = "https://discord.com/api/v9/channels/{}/messages".format(channel_id)
        self.headers["Authorization"] = token
        try:
            response = requests.get(url, headers=self.headers)
            res = response.json()
            len(res)
            message = res[len(res) - 1]["content"]
            return message
        except Exception as e:
            print(e)
            return None

    def get_user(self, token, discord_id):
        url = "https://discord.com/api/v9/users/{}".format(discord_id)
        self.headers["Authorization"] = token

        try:
            response = requests.get(url, headers=self.headers)
            res = response.json()
            name = res["username"] + "#" + res["discriminator"]
            return name
        except Exception as e:
            print(e)
            return None

    def get_channel_messages(self, token, channel_id):
        url = "https://discord.com/api/v9/channels/{}/messages".format(channel_id)
        self.headers["Authorization"] = token
        try:
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                res = response.json()
                return res
            else:
                return None
        except Exception as e:
            print(e)
            return None

    def get_servers(self, token):
        url = "https://discord.com/api/v9/users/@me/guilds"
        self.headers["Authorization"] = token
        try:
            response = requests.get(url, headers=self.headers)
            res = response.json()
            if response.status_code == 200:
                return res
            elif response.status_code == 429:
                time.sleep(round(res['retry_after']))
            else:
                return None
        except Exception as e:
            print(e)
            return None
