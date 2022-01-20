import json
import os, sys
import colorama
from colorama import init
from colorama import Fore
from chat import ServerChat
from join_server import JoinServer
from itertools import cycle
from manual_mode import ManualMode
import psycopg2
from psycopg2 import Error

try:
    # Connect to an existing database
    connection = psycopg2.connect(user="predate_key_checker",
                                  password="ZB)~6vnuT8N[",
                                  host="78.141.225.199",
                                  port="5432",
                                  database="predita")

    # Create a cursor to perform database operations
    cursor = connection.cursor()

    cursor.execute("SELECT * from keys;")
    # Fetch result
    record = cursor.fetchone()
    development_key=record[1]

except (Exception, Error) as error:
    print("Error during key check")
finally:
    if (connection):
        cursor.close()
        connection.close()



colorama.init()
init(autoreset=True)

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


proxies = GetProxies()
proxy_pool = cycle(proxies)


if __name__ == "__main__":
    if config["license_key"] == development_key:
        option = input(
            Fore.CYAN
            + "1. Silent Chat In Servers \n2. Join Server & Verify w/ Code \n3. Manual Mode \n"
        )
        if option == "1":
            token = config["main_account_token"]
            message_list = config["message_list"]
            channel_id = config["chat"]["channel_id"]
            message_delay = config["chat"]["message_delay"]
            ServerChat(token, message_list, channel_id, message_delay)
        elif option == "2":
            user_accounts = read_accounts(accounts_filename)
            invite_code = config["join_server_with_code"]["server_invite_code"]
            server_id = config["join_server_with_code"]["server_id"]
            channel_id = config["join_server_with_code"]["verification_channel_id"]
            verification_code = config["join_server_with_code"][
                "server_verification_code"
            ]
            join_server_delay = config["join_server_with_code"]["join_server_delay"]
            JoinServer(
                user_accounts,
                invite_code,
                server_id,
                channel_id,
                verification_code,
                join_server_delay,
                proxy_pool,
            )
        elif option == "3":
            user_accounts = read_accounts(manual_accounts_filename)
            ManualMode(user_accounts, proxy_pool)
    else:
        print("INVALID KEY")
