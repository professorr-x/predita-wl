import json
import os, sys
import colorama
from colorama import init
from colorama import Fore
from chat import ServerChat
from join_server import JoinServer

colorama.init()
init(autoreset=True)

filename = os.path.join(os.path.dirname(sys.executable), 'config.json')


with open(filename, "r") as f:
    config = json.load(f)

def read_accounts():
    accounts = []
    with open("accounts.txt", "r") as f:
        for line in f:
            line = line.replace("\n", "")
            accounts.append(line)
    return accounts


if __name__ == "__main__":
    if config["license_key"] == "DEVELOPMENT":
        option = input(Fore.CYAN + "    1. Silent Chat In Servers \n 2. Join Server & Verify w/ Code \n")
        if option == "1":
            token = config['main_account_token']
            message_list = config['message_list']
            channel_id = config['chat']['channel_id']
            message_delay = config['chat']['message_delay']
            ServerChat(token,message_list, channel_id, message_delay)
        elif option == "2":
            user_accounts = read_accounts()
            invite_code = config['join_server_with_code']['server_invite_code']
            server_id = config['join_server_with_code']['server_id']
            channel_id = config['join_server_with_code']['verification_channel_id']
            verification_code = config['join_server_with_code']['server_verification_code']
            join_server_delay = config['join_server_with_code']['join_server_delay']
            
            JoinServer(user_accounts, invite_code, server_id, channel_id, verification_code, join_server_delay)



