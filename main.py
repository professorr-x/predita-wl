import json
import os, sys
import colorama
from colorama import init
from colorama import Fore
from chat import ServerChat

colorama.init()
init(autoreset=True)

filename = os.path.join(os.path.dirname(sys.executable), 'config.json')


with open(filename, "r") as f:
    config = json.load(f)

if __name__ == "__main__":
    if config["license_key"] == "DEVELOPMENT":
        option = input(Fore.CYAN + "    1. Silent Chat In Servers \n ")
        if option == "1":
            token = config['main_account_token']
            message_list = config['message_list']
            channel_id = config['chat']['channel_id']
            message_delay = config['chat']['message_delay']
            ServerChat(token,message_list, channel_id, message_delay)


