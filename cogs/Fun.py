from discord.ext import commands
import discord
import datetime
from datetime import datetime as dt
from datetime import date
from datetime import datetime
import time
import math

start_time = time.time()
class Fun(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Cogs \"Fun\" has loaded")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id == 800184970298785802:
            return


def setup(client):
    client.add_cog(Fun(client))
