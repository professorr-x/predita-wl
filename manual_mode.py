from manual_driver import ManualDriver
from datetime import datetime
from colorama import Fore
from colorama import init
import proxy_processor

def ManualMode(user_accounts, proxy_pool):
    for account in user_accounts:
        account = account.split(":")
        email = account[0]
        password = account[1]
        token = account[2]
        print(Fore.CYAN + "[{}] Getting Proxies...".format(str(datetime.now())))
        proxy = proxy_processor.GetProxy(proxy_pool)
        print(Fore.CYAN + "[{}] Using Proxy {}".format(str(datetime.now()), proxy))
        md = ManualDriver()
        md.drive(email, password, token, proxy)