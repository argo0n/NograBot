from discord.ext import commands
import discord, datetime, time
import pytz
from pytz import timezone
import asyncio


timeformat = "%Y-%m-%d %H:%M:%S"
durationformat = "%-dd %-Hh %-Mm %-Ss"
def timetosgtime(x):
    utctime = x
    sgttime = utctime.astimezone(timezone("Asia/Singapore"))
    return sgttime.strftime(timeformat)

start_time = time.time()
utcbootime = datetime.datetime.now(timezone("UTC"))

class DankMemerHelp(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Cog \"Moderation\" loaded")
        channel = self.client.get_channel(830352644027449354)
        await channel.send("Nogra has just rebooted, any existing reminders have been wiped.")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id == 800184970298785802:
            return
        if "pls lottery" in message.content or "Pls lottery" in message.content:
            await message.channel.send("Will remind you in 1 hour")
            await asyncio.sleep(3600)
            await message.channel.send(f"{message.author.mention} Time to buy a lottery again <a:takethismoney:806096182594109471>")

        if message.channel.id == 821640987003977778 and "roblox.com" not in message.content:
            await message.delete()
            await message.channel.send(
                f"{message.author.mention} this channel is for posting ROBLOX games only! :c\nIf you want to talk about the game, do it in <#818436261891014660> or <#821033003823923212>",
                delete_after=3.0)

        if ("were caught HAHAHA") in message.content:
            await message.channel.send("Wait for 10 seconds <a:uwushyyy:807637815226531932>")
            tmanmfail = await message.channel.send("□□□□□□□□□□")
            await asyncio.sleep(3)
            await tmanmfail.edit(content="■■■□□□□□□□")
            await asyncio.sleep(3)
            await tmanmfail.edit(content="■■■■■■□□□□")
            await asyncio.sleep(4)
            await tmanmfail.edit(content="■■■■■■■■■■")
            for m in message.guild.members:
                if m.mention in message.content:
                    await message.channel.send(f"{m.mention} rob now!")
            else:
                await message.channel.send("No proper mention was found.")

        if ("BASICALLY EVERYTHING") in message.content:
            if message.author == 270904126974590976:
                await message.channel.send("nice i'm proud of you <:nogracuteblush:806168390003064883>")

        if ("a TINY portion") in message.content or ("a small portion") in message.content or (
        "fairly decent chunk") in message.content:
            await message.channel.send("Wait for 2 minutes <a:uwushyyy:807637815226531932>")
            tmanmport = await message.channel.send("□□□□□□□□□□□□")
            await asyncio.sleep(10)
            await tmanmport.edit(content="■□□□□□□□□□□□")
            await asyncio.sleep(10)
            await tmanmport.edit(content="■■□□□□□□□□□□")
            await asyncio.sleep(10)
            await tmanmport.edit(content="■■■□□□□□□□□□")
            await asyncio.sleep(10)
            await tmanmport.edit(content="■■■■□□□□□□□□")
            await asyncio.sleep(10)
            await tmanmport.edit(content="■■■■■□□□□□□□")
            await asyncio.sleep(10)
            await tmanmport.edit(content="■■■■■■□□□□□□")
            await asyncio.sleep(10)
            await tmanmport.edit(content="■■■■■■■□□□□□")
            await asyncio.sleep(10)
            await tmanmport.edit(content="■■■■■■■■□□□□")
            await asyncio.sleep(10)
            await tmanmport.edit(content="■■■■■■■■■□□□")
            await asyncio.sleep(10)
            await tmanmport.edit(content="■■■■■■■■■■□□")
            await asyncio.sleep(10)
            await tmanmport.edit(content="■■■■■■■■■■■□")
            await asyncio.sleep(10)
            await tmanmport.edit(content="■■■■■■■■■■■■")
            for m in message.guild.members:
                if m.mention in message.content:
                    await message.channel.send(f"{m.mention} rob now!")
            else:
                await message.channel.send("No proper mention was found.")

        if message.content.startswith("Nice I'm proud of you"):
            if message.author.id == 805251248488054794:
                await message.channel.send("<:nogracuteblush:806168390003064883> ty")
def setup(client):
    client.add_cog(DankMemerHelp(client))
