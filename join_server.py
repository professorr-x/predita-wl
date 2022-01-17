from colorama import Fore
from colorama import init
from datetime import datetime
import proxy_processor
from accounts import DiscordAccount
import time


def JoinServer(user_accounts, invite_code, server_id, channel_id, verification_code, join_server_delay):
    for token in user_accounts:
        print(Fore.CYAN + "[{}] Getting Proxies...".format(str(datetime.now())))
        proxy = proxy_processor.GetProxy()
        print(Fore.CYAN + "[{}] Using Proxy {}".format(str(datetime.now()), proxy))
        da = DiscordAccount()
        da.set_token(token)
        print(
            Fore.CYAN
            + "[{}] Joining Server With Invite Code {}".format(
                str(datetime.now()), invite_code
            )
        )
        joined = da.join_server(invite_code, proxy)
        if joined:
            print(
                Fore.GREEN
                + "[{}] Successfully Joined Server".format(str(datetime.now()))
            )
            member_verified = da.post_member_verification(server_id, proxy)
            code_verification = da.code_verification(
                channel_id , verification_code, proxy
            )
            if code_verification:
                print(
                    Fore.GREEN
                    + "[{}] Successfully Verified, Process Complete".format(str(datetime.now()))
                )
            else:
                print(
                    Fore.RED + "[{}] Unable To Verifiy, Incomplete Process".format(str(datetime.now()))
                )
        else:
            print(Fore.RED + "[{}] Unable To Join Server".format(str(datetime.now())))

        time.sleep(join_server_delay)
    else:
        print(Fore.RED + "[{}] Unable To Login".format(str(datetime.now())))
