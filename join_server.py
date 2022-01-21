from colorama import Fore
from colorama import init
from datetime import datetime
import proxy_processor
from accounts import DiscordAccount
import time


def JoinServer(
    user_accounts,
    invite_code,
    server_id,
    channel_id,
    verification_code,
    join_server_delay,
    proxy_pool,
):
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
            tries = 0
            code_verification = da.code_verification(
                channel_id, verification_code, proxy
            )
            while tries < 3:
                if code_verification:
                    print(
                        Fore.GREEN
                        + "[{}] Successfully Verified, Process Complete".format(
                            str(datetime.now())
                        )
                    )
                    break
                else:
                    print(
                        Fore.RED
                        + "[{}] Unable To Verifiy, Incomplete Process".format(
                            str(datetime.now())
                        )
                    )
                    tries += 1
        else:
            print(
                Fore.RED + "[{}] Unable To Join Server".format(str(datetime.now())))
        print(
            Fore.CYAN
            + "[{}] Chilling For {}s".format(str(datetime.now()), join_server_delay)
        )
        time.sleep(join_server_delay)
    else:
        print(Fore.RED + "[{}] Unable To Login".format(str(datetime.now())))


def JoinServerReact(user_accounts, server_invite_id, channel_id, message_id, react_btn, delay, proxy_pool):
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
        da = DiscordAccount()
        da.set_token(token)
        joined = da.join_server(server_invite_id, proxy)
        if joined:
            verification = da.react_to_verify(
                channel_id, message_id, react_btn)
            if verification:
                print(
                    Fore.GREEN + "[{}] Successfully Verified On Server".format(
                        str(datetime.now())
                    )
                )
            else:
                print(
                    Fore.RED
                    + "[{}] Unable To Verify On Server".format(str(datetime.now()))
                )
        else:
            print(
                Fore.RED +
                "[{}] Unable To Join Server".format(str(datetime.now()))
            )
        time.sleep(delay)


def JoinServerReactConfirmation(user_accounts, server_id, server_invite_id, channel_id, message_id, react_btn, delay, proxy_pool):
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
        da = DiscordAccount()
        da.set_token(token)
        joined = da.join_server(server_invite_id, proxy)
        if joined:
            member_verified = da.post_member_verification(server_id, proxy)
            if member_verified:
                print(Fore.GREEN +
                      "[{}] Accepted T&C".format(str(datetime.now())))
                verification = da.react_to_verify(
                    channel_id, message_id, react_btn)
                if verification:
                    print(
                        Fore.GREEN + "[{}] Successfully Verified On Server".format(
                            str(datetime.now())
                        )
                    )
                else:
                    print(
                        Fore.RED
                        + "[{}] Unable To Verify On Server".format(str(datetime.now()))
                    )
            else:
                print(
                    Fore.RED
                    + "[{}] Unable To Accept T&C".format(str(datetime.now()))
                )
        else:
            print(
                Fore.RED +
                "[{}] Unable To Join Server".format(str(datetime.now()))
            )
        time.sleep(delay)
