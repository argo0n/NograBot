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
from discord.ext import commands, tasks
import discord
import datetime
import time
import pytz
from pytz import timezone
import asyncio
import postbin
import traceback
import random
import json
import math


def secondstotiming(seconds):
    seconds = round(seconds)
    if seconds < 60:
        secdisplay = "s" if seconds != 1 else ""
        return f"{seconds} second{secdisplay}"
    minutes = math.trunc(seconds / 60)
    if minutes < 60:
        seconds = seconds - minutes * 60
        mindisplay = "s" if minutes != 1 else ""
        secdisplay = "s" if seconds != 1 else ""
        return f"{minutes} minute{mindisplay} and {seconds} second{secdisplay}"
    hours = math.trunc(minutes / 60)
    if hours < 24:
        minutes = minutes - hours * 60
        seconds = seconds - minutes * 60 - hours * 60 * 60
        hdisplay = "s" if hours != 1 else ""
        mindisplay = "s" if minutes != 1 else ""
        secdisplay = "s" if seconds != 1 else ""
        return f"{hours} hour{hdisplay}, {minutes} minute{mindisplay} and {seconds} second{secdisplay}"
    days = math.trunc(hours / 24)
    if days < 7:
        hours = hours - days * 24
        minutes = minutes - hours * 60
        seconds = seconds - minutes * 60 - hours * 60 * 60
        ddisplay = "s" if days != 1 else ""
        hdisplay = "s" if hours != 1 else ""
        mindisplay = "s" if minutes != 1 else ""
        secdisplay = "s" if seconds != 1 else ""
        return f"{days} day{ddisplay}, {hours} hour{hdisplay}, {minutes} minute{mindisplay} and {seconds} second{secdisplay}"
    weeks = math.trunc(days / 7)
    days = days - weeks * 7
    hours = hours - days * 24
    minutes = minutes - hours * 60
    seconds = seconds - minutes * 60 - hours * 60 * 60
    wdisplay = "s" if weeks != 1 else ""
    ddisplay = "s" if days != 1 else ""
    hdisplay = "s" if hours != 1 else ""
    mindisplay = "s" if minutes != 1 else ""
    secdisplay = "s" if seconds != 1 else ""
    return f"{weeks} week{wdisplay}, {days} day{ddisplay}, {hours} hour{hdisplay}, {minutes} minute{mindisplay} and {seconds} second{secdisplay}"


def gettraceback(error):
    etype = type(error)
    trace = error.__traceback__
    lines = traceback.format_exception(etype, error, trace)
    traceback_text = ''.join(lines)
    return traceback_text


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
        self.myLoop.start()

    @tasks.loop(seconds=5.0)
    async def myLoop(self):
        channel = self.client.get_channel(832294688345292801)
        await channel.send("hi")
        with open('nograresources/lottery.json', 'r', encoding='utf8') as f:
            lottery = json.load(f)
            for userid in lottery:
                if lottery[userid]["time"] > round(time.time()):
                    user = self.client.get_user(int(userid))
                    try:
                        channelid = lottery[userid]["channel"]
                        guildid = lottery[userid]["guild"]
                        messageid = lottery[userid]["message"]
                        user = self.client.get_user(int(userid))
                        channel = self.client.get_channel(channelid)
                        messagelink = discord.Embed(
                            description=f"[Jump to message](https://discord.com/channels/{guildid}/{channelid}/{messageid})",
                            color=0x00FFFF)
                        messagelink.set_author(name=self.client.user.name, icon_url=str(self.client.user.avatar_url))
                        await user.send(
                            f"{user.mention} You were reminded in **{channel.mention}**: Time to buy a lottery again <a:takethismoney:806096182594109471>",
                            embed=messagelink)
                    except discord.errors.Forbidden:
                        await channel.send(
                            f"{user.mention} time to enter the lottery again <a:takethismoney:806096182594109471>")
                    del lottery[userid]
                    with open('nograresources/lottery.json', 'w', encoding='utf8') as f:
                        json.dump(lottery, f, sort_keys=True, indent=4, ensure_ascii=False)

    @commands.Cog.listener()
    async def on_ready(self):
        print("Cog \"DankMemerHelp\" loaded")

    @commands.Cog.listener()
    async def on_message(self, message):
        def embedcheck(message):
            for e in message.embeds:
                return "You bought a lottery ticket" in e.title and message.author.id == 270904126974590976

        if message.author.id == 800184970298785802:
            return
        if message.content.startswith("pls lottery") or message.content.startswith(
                "pls lotto") or message.content.startswith("Pls lottery") or message.content.startswith(
                "Pls lotto") and message.author.id not in [270904126974590976, 341994639395520526]:
            try:
                msg = await self.client.wait_for("message",
                                                 check=lambda message: message.author.id == 270904126974590976,
                                                 timeout=5.0)
            except asyncio.TimeoutError:
                await message.channel.send("I could not detect a message that was from Dank Memer.", delete_after=5.0)
                return
            else:
                if msg.content == "You need at least ⏣ 5,000 for that, didn't you do the math? Go back to middle school bro":
                    await message.channel.send("||<:nograpoor:854565088831471636>|| ||just joking||", delete_after=5.0)
                    return
                if msg.content == "Mate you already entered this lottery, wait for the next one":
                    await message.channel.send("Just wait for the lottery to be done tbh")
                    return
                for embed in msg.embeds:
                    if "Too spicy" in embed.title:
                        await message.channel.send("<:thefuckcatears:837535368831041539>")
                        return
            try:
                msg2 = await self.client.wait_for("message",
                                                  check=lambda message: message.author.id == 270904126974590976,
                                                  timeout=5.0)
            except asyncio.TimeoutError:
                await message.channel.send("I could not detect a message that was from Dank Memer.", delete_after=5.0)
                return
            else:
                if msg2.content == "Alright whatever just come hit me up when you wanna win the lottery":
                    await message.channel.send("<:omagun:807125530897809448>")
                    return
                for e in msg2.embeds:
                    if "You bought a lottery ticket" in e.title and msg2.author.id == 270904126974590976:
                        pass
                    else:
                        return
                emojis = ["<a:Tick:796984073603383296>", "⏲️"]
                for emo in emojis:
                    await message.add_reaction(emo)
                with open('nograresources/lottery.json', 'r', encoding='utf8') as f:
                    remindtime = round(time.time())
                    while remindtime % 3600 != 0:
                        remindtime += 1
                    lottery = json.load(f)
                    lottery[f"{message.author.id}"]["time"] = remindtime
                    lottery[f"{message.author.id}"]["channel"] = message.channel.id
                    lottery[f"{message.author.id}"]["guild"] = message.guild.id
                    lottery[f"{message.author.id}"]["message"] = message.id
                    with open('nograresources/lottery.json', 'w', encoding='utf8') as f:
                        json.dump(lottery, f, sort_keys=True, indent=4, ensure_ascii=False)
                        await message.channel.send(
                            f"I will remind you in {secondstotiming(remindtime - round(time.time()))} to participate in the lottery again!")

                try:
                    await message.add_reaction("<:dms:838255193266716742>")
                    await asyncio.sleep(3600)
                    messagelink = discord.Embed(
                        description=f"[Jump to message](https://discord.com/channels/{message.guild.id}/{message.channel.id}/{message.id})",
                        color=0x00FFFF)
                    messagelink.set_author(name=self.client.user.name, icon_url=str(self.client.user.avatar_url))
                    await message.author.send(
                        f"{message.author.mention} You were reminded in **{message.channel.mention}**: Time to buy a lottery again <a:takethismoney:806096182594109471>",
                        embed=messagelink)
                except discord.errors.Forbidden:
                    await message.add_reaction("<:mention:838255192952274974>")
                    await asyncio.sleep(3600)
                    await message.channel.send(
                        f"{message.author.mention} Time to buy a lottery again <a:takethismoney:806096182594109471>")
                    return


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
                    return
            await message.channel.send("No proper mention was found.")

        if ("BASICALLY EVERYTHING") in message.content and message.author.id == 270904126974590976:
            await message.channel.send("nice i'm proud of you <:nograblushsuit:831001647005564970>")

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
                    return
            await message.channel.send("No proper mention was found.")

        if (
            message.content.startswith("Nice I'm proud of you")
            and message.author.id == 805251248488054794
        ):
            await message.channel.send("<:nograblushsuit:831001647005564970> ty")

        if message.content.startswith("pIs rob") or message.content.startswith("PIs rob"):
            moneylist = ["30,620,956","2,912,053","21,706,777","12,879,693","98,088,176","77,629,360","13,020,603","49,996,631","4,885,187","467,511","22,375,088","37,523,359","68,228,030","62,615,734","48,622,895","92,330,896","18,646,281","63,114,372","13,510,918","36,952,204"]
            number = random.choice(moneylist)
            await message.channel.send(f"{message.author.mention} You stole BASICALLY EVERYTHING LMFAO 🤑\nYour payout was **⏣ {number}**. ")
            for m in message.guild.members:
                if str(m.id) in message.content:
                    targetmember = m
            embed = discord.Embed(title="You have been stolen from!",
                                  description=f"**{message.author.name}#{message.author.discriminator}** ({message.author.mention}) has stolen **⏣ {number}** from you in **{message.guild.name}**!",
                                  colour=0xFF0000)
            try:
                await targetmember.send(embed=embed)
            except discord.errors.Forbidden:
                await message.channel.send("that guy blocked me or closed his dms, what a loser")

    @commands.command(name="stoptask", brief="Manually ping for lottery",
                      description="Manually sets pings for lottery whenever bot reboots", hidden=True)
    async def stoptask(self, ctx):
        emojis = ["<a:Tick:796984073603383296>", "⏲️"]
        for emo in emojis:
            await ctx.message.add_reaction(emo)

    @stoptask.error
    async def stoptask_error(self, ctx, error):
        errorembed = discord.Embed(title="Oops!",
                                   description="Error.",
                                   color=0x00ff00)
        errorembed.add_field(name="Error", value=f"```{error}```", inline=False)
        errorembed.set_thumbnail(url="https://www.freeiconspng.com/thumbs/error-icon/orange-error-icon-0.png")
        await ctx.send(embed=errorembed)


def setup(client):
    client.add_cog(DankMemerHelp(client))
