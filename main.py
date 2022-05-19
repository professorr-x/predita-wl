import json
import os
import sys
import colorama
from colorama import init
from colorama import Fore
from accounts import DiscordAccount
from chat import ServerChat, RecycledChat
from join_server import JoinServer, JoinServerReact, JoinServerReactConfirmation
from itertools import cycle
from manual_mode import ManualMode
from discord import Discord
import ctypes
import requests
from giveaways import giveaway_monitor

ctypes.windll.kernel32.SetConsoleTitleW("Preditah WL")
colorama.init()

config_filename = os.path.join(os.path.dirname(sys.executable), "config.json")
accounts_filename = os.path.join(os.path.dirname(sys.executable), "accounts.txt")
proxies_filename = os.path.join(os.path.dirname(sys.executable), "proxies.txt")
manual_accounts_filename = os.path.join(
    os.path.dirname(sys.executable), "manual_accounts.txt"
)

if sys.executable == "/Users/yas/Documents/preditah/preditah_bot/venv/bin/python":
    config_filename = "config.json"
    accounts_filename = "accounts.txt"
    proxies_filename = "proxies.txt"
    manual_accounts_filename = "manual_accounts.txt"

with open(config_filename, "r") as f:
    config = json.load(f)


def read_accounts(account_type):
    accounts = []
    with open(account_type, "r") as f:
        for line in f:
            line = line.replace("\n", "")
            accounts.append(line)
    return accounts


def GetProxies():
    with open(proxies_filename, "r") as temp_file:
        proxies = [line.rstrip("\n") for line in temp_file]
    return proxies


def key_check(key):
    url = "https://stage.api.solseeker.xyz/key"
    payload = {"key": key}
    headers = {"accept": "application/json"}
    try:
        res = requests.get(url, headers=headers, params=payload)
        data = res.json()
        try:
            if data["error"]:
                return None
        except:
            return data
    except Exception as e:
        print(e)
        return None


proxies = GetProxies()
proxy_pool = cycle(proxies)


if __name__ == "__main__":
    print(Fore.CYAN + "\nPREDITAH \n")
    token = config["main_account_token"]
    disc = Discord()
    # name = disc.get_user(token, user["discord_id"])
    print(Fore.CYAN + "Welcome")
    option = input(
        Fore.CYAN
        + "\n1. Silent Chat In Servers \n2. Join Server & Verify w/ Code \n3. Manual Mode \n4. Join Server By Reacting To Message \n5. Join Server By Confirming T&C And React To Message \n6. Check Tokens \n7. Recycled Chat In Servers \n8. Giveaways\n"
    )
    if option == "1":
        token = config["main_account_token"]
        message_list = config["message_list"]
        channel_id = config["chat"]["channel_id"]
        server_id = config["chat"]["server_id"]
        message_delay = config["chat"]["message_delay"]
        delete_message_delay = config["chat"]["delete_message_delay"]
        delete = config["chat"]["delete"]
        ServerChat(
            token,
            message_list,
            channel_id,
            server_id,
            message_delay,
            delete_message_delay,
            delete,
        )
    elif option == "2":
        token = config["main_account_token"]
        user_accounts = read_accounts(accounts_filename)
        invite_code = config["join_server_with_code"]["server_invite_code"]
        server_id = config["join_server_with_code"]["server_id"]
        channel_id = config["join_server_with_code"]["verification_channel_id"]
        verification_code = config["join_server_with_code"][
            "server_verification_code"
        ]
        join_server_delay = config["join_server_with_code"]["join_server_delay"]
        JoinServer(
            token,
            user_accounts,
            invite_code,
            server_id,
            channel_id,
            verification_code,
            join_server_delay,
            proxy_pool,
        )
    elif option == "3":
        ctypes.windll.kernel32.SetConsoleTitleW("Preditah WL - Manual Mode")
        user_accounts = read_accounts(manual_accounts_filename)
        ManualMode(user_accounts, proxy_pool)
    elif option == "4":
        token = config["main_account_token"]
        user_accounts = read_accounts(accounts_filename)
        server_invite_id = config["react_to_join_server"]["server_invite_code"]
        server_id = config["react_to_join_server"]["server_id"]
        channel_id = config["react_to_join_server"]["verification_channel_id"]
        message_id = config["react_to_join_server"]["verification_message_id"]
        react_btn = config["react_to_join_server"]["react_verification_btn_id"]
        delay = config["react_to_join_server"]["join_server_delay"]
        JoinServerReact(
            token,
            user_accounts,
            server_invite_id,
            server_id,
            channel_id,
            message_id,
            react_btn,
            delay,
            proxy_pool,
        )
    elif option == "5":
        token = config["main_account_token"]
        user_accounts = read_accounts(accounts_filename)
        server_invite_id = config["react_to_join_server"]["server_invite_code"]
        server_id = config["react_to_join_server"]["server_id"]
        channel_id = config["react_to_join_server"]["verification_channel_id"]
        message_id = config["react_to_join_server"]["verification_message_id"]
        react_btn = config["react_to_join_server"]["react_verification_btn_id"]
        delay = config["react_to_join_server"]["join_server_delay"]
        JoinServerReactConfirmation(
            token,
            user_accounts,
            server_id,
            server_invite_id,
            channel_id,
            message_id,
            react_btn,
            delay,
            proxy_pool,
        )
    elif option == "6":
        ctypes.windll.kernel32.SetConsoleTitleW("Preditah WL - Account Checker")
        user_accounts = read_accounts(accounts_filename)
        da = DiscordAccount()
        da.account_checker(user_accounts, proxy_pool)
    elif option == "7":
        token = config["main_account_token"]
        channel_id = config["chat"]["channel_id"]
        server_id = config["chat"]["server_id"]
        message_delay = config["chat"]["message_delay"]
        delete_message_delay = config["chat"]["delete_message_delay"]
        RecycledChat(
            token, channel_id, server_id, message_delay, delete_message_delay
        )
    elif option == "8":
        ctypes.windll.kernel32.SetConsoleTitleW("Preditah WL - Giveaways Monitor")
        token = config["main_account_token"]
        webhook_url = config["webhook_url"]
        giveaway_monitor(token, webhook_url)
