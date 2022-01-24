from colorama import Fore
from colorama import init
from datetime import datetime
import proxy_processor
from accounts import DiscordAccount
import time
from discord import Discord


def write_to_file(verfication, name, token):
    if verfication == 'verified':
        filename = 'verified_{}.txt'.format(name)
        with open(filename, 'a') as f:
            f.write(token + '\n')
    elif verfication == 'unverified':
        filename = 'unverified_{}.txt'.format(name)
        with open(filename, 'a') as f:
            f.write(token + '\n')



def JoinServer(
    token,
    user_accounts,
    invite_code,
    server_id,
    channel_id,
    verification_code,
    join_server_delay,
    proxy_pool,
):
    disc = Discord()
    name = disc.get_server_name(token, server_id)
    verified_accounts = 0
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
                    verified_accounts += 1
                    print(
                        Fore.GREEN
                        + "[{}] Successfully Verified | Verified = {}".format(
                            str(datetime.now()), verified_accounts
                        )
                    )
                    write_to_file('verified', name, token)
                    break
                else:
                    print(
                        Fore.RED
                        + "[{}] Unable To Verifiy, Incomplete Process".format(
                            str(datetime.now())
                        )
                    )
                    write_to_file('unverified', name, token)
                    tries += 1
        else:
            print(
                Fore.RED + "[{}] Unable To Join Server".format(str(datetime.now())))
            write_to_file('unverified', name, token)
        print(
            Fore.CYAN
            + "[{}] Chilling For {}s".format(str(datetime.now()), join_server_delay)
        )
        time.sleep(join_server_delay)


def JoinServerReact(token, user_accounts, server_invite_id, server_id, channel_id, message_id, react_btn, delay, proxy_pool):
    disc = Discord()
    name = disc.get_server_name(token, server_id)
    verified_accounts = 0
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
                verified_accounts += 1
                print(
                    Fore.GREEN + "[{}] Successfully Verified On Server | Verified = {}".format(
                        str(datetime.now()), verified_accounts
                    )
                )
                write_to_file('verified', name, token)
            else:
                print(
                    Fore.RED
                    + "[{}] Unable To Verify On Server".format(str(datetime.now()))
                )
                write_to_file('unverified', name, token)
        else:
            print(
                Fore.RED +
                "[{}] Unable To Join Server".format(str(datetime.now()))
            )
            write_to_file('unverified', name, token)
        time.sleep(delay)


def JoinServerReactConfirmation(token, user_accounts, server_id, server_invite_id, channel_id, message_id, react_btn, delay, proxy_pool):
    disc = Discord()
    name = disc.get_server_name(token, server_id)
    verified_accounts = 0
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
                    verified_accounts += 1
                    print(
                        Fore.GREEN + "[{}] Successfully Verified On Server | Verified = {}".format(
                            str(datetime.now()), verified_accounts
                        )
                    )
                    write_to_file('verified', name, token)
                else:
                    print(
                        Fore.RED
                        + "[{}] Unable To Verify On Server".format(str(datetime.now()))
                    )
                    write_to_file('unverified', name, token)
            else:
                print(
                    Fore.RED
                    + "[{}] Unable To Accept T&C".format(str(datetime.now()))
                )
                write_to_file('unverified', name, token)
        else:
            print(
                Fore.RED +
                "[{}] Unable To Join Server".format(str(datetime.now()))
            )
            write_to_file('unverified', name, token)
        time.sleep(delay)
