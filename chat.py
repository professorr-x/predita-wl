from colorama import init
from colorama import Fore
from datetime import datetime
from accounts import DiscordAccount
import time


def ServerChat(token, message_list, channel_id, delay):
    da = DiscordAccount()
    if token:
        print(token)
        print(type(token))
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
                            + "[{}] Delay for {}".format(
                                str(datetime.now()), delay
                            )
                        )
                    time.sleep(delay)
    else:
        print(Fore.RED + "[{}] No Token Provided".format(str(datetime.now())))