# |------------------------------------------------------------------------------------|
# |                                                                                    |
# |                                                                                    |
# |                          DankMemerHelp Cog for Nogra Bot                           |
# |                               Written by Argon#0002                                |
# |                               Commands in this cog:                                |
# |                           pls lottery and rob reminders                            |
# |                                                                                    |
# |                                                                                    |
# |------------------------------------------------------------------------------------
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
            if message.author.id == 392127809939570688 or message.author.id == 650647680837484556:
                await message.channel.send("Will remind you in 1 hour via DMS")
                await asyncio.sleep(3600)
                await message.author.send(
                    f"{message.author.mention} Time to buy a lottery again <a:takethismoney:806096182594109471>")
                print(f"I've sent a lottery message to {message.author.name}#{message.author.discriminator}")
            else:
                await message.channel.send("Will remind you in 1 hour")
                await asyncio.sleep(3600)
                await message.channel.send(f"{message.author.mention} Time to buy a lottery again <a:takethismoney:806096182594109471> \n ||If you want to be DMed for these reminders instead, message Argon||")

        if message.channel.id == 821640987003977778 and "roblox.com" not in message.content:
            await message.delete()
            await message.channel.send(
                f"{message.author.mention} this channel is for posting ROBLOX games only! :c\nIf you want to talk about the game, do it in <#818436261891014660> or <#821033003823923212>",
                delete_after=3.0)

        if ("were caught **HAHAHA**") in message.content and message.author.id == 270904126974590976:
            await message.channel.send("Wait for 30 seconds <a:uwushyyy:807637815226531932>")
            tmanmfail = await message.channel.send("□□□□□□□□□□")
            await asyncio.sleep(3)
            await tmanmfail.edit(content="■□□□□□□□□□")
            await asyncio.sleep(3)
            await tmanmfail.edit(content="■■□□□□□□□□")
            await asyncio.sleep(3)
            await tmanmfail.edit(content="■■■□□□□□□□")
            await asyncio.sleep(3)
            await tmanmfail.edit(content="■■■■□□□□□□")
            await asyncio.sleep(3)
            await tmanmfail.edit(content="■■■■■□□□□□")
            await asyncio.sleep(3)
            await tmanmfail.edit(content="■■■■■■□□□□")
            await asyncio.sleep(3)
            await tmanmfail.edit(content="■■■■■■■□□□")
            await asyncio.sleep(3)
            await tmanmfail.edit(content="■■■■■■■■□□")
            await asyncio.sleep(3)
            await tmanmfail.edit(content="■■■■■■■■■□")
            await asyncio.sleep(3)
            await tmanmfail.edit(content="■■■■■■■■■■")
            for m in message.guild.members:
                if str(m.id) in message.content:
                    await message.channel.send(f"{m.mention} rob now!")
            else:
                await message.channel.send("No proper mention was found.")

        if ("BASICALLY EVERYTHING") in message.content and message.author.id == 270904126974590976:
            await message.channel.send("nice i'm proud of you <:nogracuteblush:806168390003064883>")

        if ("a TINY portion") in message.content or ("a small portion") in message.content or (
        "fairly decent chunk") in message.content and message.author.id == 270904126974590976:
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
                if str(m.id) in message.content:
                    await message.channel.send(f"{m.mention} rob now!")
            else:
                await message.channel.send("No proper mention was found.")

        if message.content.startswith("Nice I'm proud of you"):
            if message.author.id == 805251248488054794:
                await message.channel.send("<:nogracuteblush:806168390003064883> ty")

        @commands.command(name="manualremind", brief="Manually ping for lottery", description="Manually sets pings for lottery whenever bot reboots")
        async def manualremind(self, ctx, memberid, duration):
            durationinminutes = duration*60
            member = ctx.guild.get_member(memberid)
            await asyncio.sleep(durationinminutes)
            if ctx.author.id == 392127809939570688 or ctx.author.id == 650647680837484556:
                await member.send(f"{member.mention} Time to buy a lottery again <a:takethismoney:806096182594109471>")
                print(f"I've sent a lottery message to {member.name}#{member.discriminator}")
            else:
                await ctx.send(f"{member.mention} Time to buy a lottery again <a:takethismoney:806096182594109471>")





            try:
                await ctx.send(embed=embed)
            except discord.HTTPException:
                await ctx.send(
                    f"Invite {self.client.user.name} to your server with only necessary permissions here **(Recommended): https://discord.com/api/oauth2/authorize?client_id=800184970298785802&permissions=8&scope=bot\n")
def setup(client):
    client.add_cog(DankMemerHelp(client))
