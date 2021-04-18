# |------------------------------------------------------------------------------------|
# |                                                                                    |
# |                                                                                    |
# |                            argonafk Cog for Nogra Bot                              |
# |                               Written by Argon#0002                                |
# |                               Commands in this cog:                                |
# |                                         NA                                         |
# |                                                                                    |
# |                                                                                    |
# |------------------------------------------------------------------------------------
from discord.utils import find
import random
import asyncio
import discord
import logging
from discord.ext import commands
import json
import os
import datetime, time
from datetime import datetime as dt
from datetime import date
import nacl
from pytz import timezone

start_time = time.time()
class argonafk(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Cogs \"Fun\" has loaded")

    @commands.Cog.listener()
    async def on_message(self, message):

        argon = message.guild.get_member(650647680837484556)
        if argon == None:
            return
        elif argon.mentioned_in(message) and message.author != self.client.user:
            date_time_obj = datetime.datetime.strptime('16/04/21 06:00:00', '%d/%m/%y %H:%M:%S')
            sinceafktime = date_time_obj.timestamp()
            formatofdatesinceafk = date_time_obj.strftime("%A, %d %B %Y, %H:%M:%S")
            timenow = datetime.datetime.now()
            nowtime = timenow.timestamp()
            difference = int(round(nowtime - sinceafktime))
            afksince = str(datetime.timedelta(seconds=difference))
            joinembed = discord.Embed(title="Argon is AFK", color=0x00ff00)
            joinembed.set_author(name=f"{argon.name}", icon_url=str(argon.avatar_url))
            joinembed.add_field(name=":(",
                                value="am in an exam rn <a:nyakiss:832467845417009162>\n- argon",
                                inline=True)
            joinembed.set_thumbnail(url="https://cdn.discordapp.com/emojis/679796247896391783.png?v=1")
            joinembed.set_footer(text=f"Argon has been AFK for {afksince}. Also this is not a afk command lmao")
            await message.channel.send(embed=joinembed)

        if message.author.id == 800184970298785802:
            return

def setup(client):
    client.add_cog(argonafk(client))
