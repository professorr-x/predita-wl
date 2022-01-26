from colorama import init
from colorama import Fore
from datetime import datetime
from accounts import DiscordAccount
import time
import ctypes
from discord import Discord


def RecycledChat(token, channel_id, server_id, delay, delete_message_delay):
    disc = Discord()
    channel_name = disc.get_channel_name(token, channel_id)
    name = disc.get_server_name(token, server_id)
    title = "Predita WL - Chat - {} {}".format(channel_name, name)
    ctypes.windll.kernel32.SetConsoleTitleW(title)
    da = DiscordAccount()
    if token:
        da.set_token(token)
        while True:
            message = disc.get_message(token, channel_id)
            sent_message = da.send_message(channel_id, message)
            if sent_message != False:
                print(
                    Fore.GREEN
                    + "[{}] Successfully Sent Message:  {}".format(
                        str(datetime.now()), sent_message
                    )
                )
                channel_id = sent_message["channel_id"]
                message_id = sent_message["id"]
                print(
                    Fore.CYAN
                    + "[{}] Delay for {}s before deleting".format(
                        str(datetime.now()), delete_message_delay
                    )
                )
                time.sleep(delete_message_delay)
                deleted_msg = da.delete_message(channel_id, message_id)

                if deleted_msg:
                    print(
                        Fore.GREEN
                        + "[{}] Successfully Deleted Message".format(
                            str(datetime.now())
                        )
                    )
                else:
                    print(
                        Fore.RED
                        + "[{}] Unable To Delete Message".format(str(datetime.now()))
                    )
                print(
                    Fore.CYAN
                    + "[{}] Delay for {}s, before next message".format(
                        str(datetime.now()), delay
                    )
                )
                time.sleep(delay)
    else:
        print(Fore.RED + "[{}] No Token Provided".format(str(datetime.now())))


def ServerChat(token, message_list, channel_id, server_id, delay, delete_message_delay):
    disc = Discord()
    channel_name = disc.get_channel_name(token, channel_id)
    name = disc.get_server_name(token, server_id)
    title = "Predita WL - Chat - {} {}".format(channel_name, name)
    ctypes.windll.kernel32.SetConsoleTitleW(title)
    da = DiscordAccount()
    if token:
        da.set_token(token)
        while True:
            for message in message_list:
                sent_message = da.send_message(channel_id, message)
                if sent_message != False:
                    print(
                        Fore.GREEN
                        + "[{}] Successfully Sent Message:  {}".format(
                            str(datetime.now()), sent_message
                        )
                    )
                    channel_id = sent_message["channel_id"]
                    message_id = sent_message["id"]
                    print(
                        Fore.CYAN
                        + "[{}] Delay for {}s before deleting".format(
                            str(datetime.now()), delete_message_delay
                        )
                    )
                    time.sleep(delete_message_delay)
                    deleted_msg = da.delete_message(channel_id, message_id)

                    if deleted_msg:
                        print(
                            Fore.GREEN
                            + "[{}] Successfully Deleted Message".format(
                                str(datetime.now())
                            )
                        )
                    else:
                        print(
                            Fore.RED
                            + "[{}] Unable To Delete Message".format(
                                str(datetime.now())
                            )
                        )
                    print(
                        Fore.CYAN
                        + "[{}] Delay for {}s, before next message".format(
                            str(datetime.now()), delay
                        )
                    )
                    time.sleep(delay)
    else:
        print(Fore.RED + "[{}] No Token Provided".format(str(datetime.now())))
