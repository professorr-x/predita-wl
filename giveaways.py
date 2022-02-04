import os
import sys
from discord import Discord
import random
import time
from discord_webhook import DiscordWebhook, DiscordEmbed
from colorama import Fore
from colorama import init
from datetime import datetime
from db import create_connection, create_table, add_message_id, check_message_id

db_dir = os.path.join(os.path.dirname(sys.executable), "preditah.db")
if sys.executable == "/Users/yas/Documents/preditah/preditah_bot/venv/bin/python":
    db_dir = "preditah.db"
if os.path.exists(db_dir):
    conn = create_connection(db_dir)
else:
    conn = create_connection(db_dir)
    create_table(conn)


def giveaway_monitor(token, webhook_url):
    webhook = DiscordWebhook(url=webhook_url)
    disc = Discord()
    while True:
        print(Fore.CYAN + "[{}] Monitoring Giveaways".format(str(datetime.now())))
        time.sleep(random.randint(0, 5))
        servers = disc.get_servers(token)
        if servers != None:
            for server in servers:
                channels = disc.get_channels(token, server["id"])
                if channels != None:
                    for channel in channels:
                        if "giveaway" in channel["name"] and channel["position"] != 0:
                            messages = disc.get_channel_messages(token, channel["id"])
                            if messages != None and len(messages) > 0:
                                message_exists = check_message_id(
                                    conn,
                                    server["id"],
                                    channel["id"],
                                    messages[0]["id"],
                                )
                                if message_exists == False:
                                    message_added = add_message_id(
                                        conn,
                                        server["id"],
                                        channel["id"],
                                        messages[0]["id"],
                                    )
                                    if message_added:
                                        embed = DiscordEmbed(
                                            title="{} | {}".format(
                                                server["name"], channel["name"]
                                            )
                                        )
                                        embed.set_author(
                                            name="CLICK HERE TO OPEN MESSAGE",
                                            url="https://discord.com/channels/{}/{}/{}".format(
                                                server["id"],
                                                channel["id"],
                                                messages[0]["id"],
                                            ),
                                        )
                                        embed.add_embed_field(
                                            name="Message",
                                            value=messages[0]["content"],
                                            inline=False,
                                        )
                                        webhook.add_embed(embed)
                                        response = webhook.execute()
                                        webhook.embeds = []
