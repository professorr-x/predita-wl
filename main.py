import json
import os, sys
from colorama import init
from colorama import Fore
from chat import ServerChat



init(autoreset=True)

filename = os.path.join(os.path.dirname(sys.executable), 'config.json')


with open(filename, "r") as f:
    config = json.load(f)

if __name__ == "__main__":
    if config["license_key"] == "DEVELOPMENT":
        option = input(Fore.CYAN + "1) Chat In Servers \n ")
        if option == "1":
            ServerChat(config['main_account_token'],config['message_list'], config['chat']['channel_id'], config['chat']['message_delay'])


