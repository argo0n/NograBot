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
from cogs.nograhelpers import *
import sqlite3
from discord.ext.buttons import Paginator
import os

DB_PATH = "databases/"


def gettraceback(error):
    etype = type(error)
    trace = error.__traceback__
    lines = traceback.format_exception(etype, error, trace)
    return ''.join(lines)


timeformat = "%Y-%m-%d %H:%M:%S"
durationformat = "%-dd %-Hh %-Mm %-Ss"


def timetosgtime(x):
    utctime = x
    sgttime = utctime.astimezone(timezone("Asia/Singapore"))
    return sgttime.strftime(timeformat)


class Pag(Paginator):
    async def teardown(self):
        try:
            await self.page.clear_reactions()
        except discord.HTTPException:
            pass


start_time = time.time()
utcbootime = datetime.datetime.now(timezone("UTC"))


class DankMemerHelp(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.myLoop.start()
        self.description = "<:nogradank:863371598303068160> Dank Memer Utilities"

    @tasks.loop(seconds=2.0)
    async def myLoop(self):
        await self.client.wait_until_ready()
        timenow = round(time.time())
        lotterydb = sqlite3.connect('databases/lottery.sqlite')
        cursor = lotterydb.cursor()
        result = cursor.execute("SELECT * FROM main WHERE lotterytime < ?", (timenow,)).fetchall()
        if len(result) == 0:
            return
        for row in result:
            user = self.client.get_user(row[0])
            guildid = row[2]
            channelid = row[3]
            messageid = row[4]
            channel = self.client.get_channel(channelid)
            messagelink = discord.Embed(
                description=f"[Jump to message](https://discord.com/channels/{guildid}/{channelid}/{messageid})",
                color=0x00FFFF)
            messagelink.set_author(name=self.client.user.name, icon_url=str(self.client.user.avatar.url))
            with open("nograresources/lotterychoice.json", 'r', encoding="utf8") as f:
                choices = json.load(f)
                choice = choices[str(row[0])]
            if choice == "dm" or choices not in ["dm", "mention"]:
                try:
                    await user.send(
                        f"{user.mention} You were reminded in **{channel.mention}**: Time to buy a lottery again <a:takethismoney:806096182594109471>",
                        embed=messagelink)
                except discord.errors.Forbidden:
                    await channel.send(
                        f"{user.mention} You have your DMs closed, so I have to mention you instead.\nTime to enter the lottery again <a:takethismoney:806096182594109471>")
            elif choice == "mention":
                await channel.send(
                    f"{user.mention} Time to enter the lottery again <a:takethismoney:806096182594109471>")
        cursor.execute("DELETE FROM main WHERE lotterytime < ?", (timenow,))
        lotterydb.commit()
        cursor.close()
        lotterydb.close()

    @commands.Cog.listener()
    async def on_ready(self):
        print("Cog \"DankMemerHelp\" loaded")
        db = sqlite3.connect('databases/lottery.sqlite')
        cursor = db.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS main(member_id integer, lotterytime integer, guild_id integer, channel_id integer, message_id integer)")

    @commands.Cog.listener()
    async def on_message(self, message):  # sourcery skip: remove-pass-body
        if message.author == self.client.user:
            return
        if message.author.id == self.client.user.id:
            return
        if message.content.startswith("pls lottery") or message.content.startswith(
                "pls lotto") or message.content.startswith("Pls lottery") or message.content.startswith(
            "Pls lotto") and message.author.id not in [270904126974590976, 341994639395520526]:
            with open('nograresources/lotterychoice.json', 'r', encoding='utf8') as f:
                lotterychoice = json.load(f)
                if lotterychoice[str(message.author.id)] is None:
                    return
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
                remindtime = round(time.time())
                while remindtime % 3600 != 0:
                    remindtime += 1
                lottery = sqlite3.connect('databases/lottery.sqlite')
                cursor = lottery.cursor()
                sql = "INSERT INTO main(member_id ,lotterytime, guild_id, channel_id,message_id) VALUES(?,?,?,?,?)"
                val = (message.author.id, remindtime, message.guild.id, message.channel.id, message.id)
                cursor.execute(sql, val)
                lottery.commit()
                cursor.close()
                lottery.close()
                await message.channel.send(
                    f"I will remind you in {secondstotiming(remindtime - round(time.time()))} to participate in the lottery again!")

        if "were caught **HAHAHA**" in message.content and message.author.id == 270904126974590976:
            await message.channel.send("Wait for 30 seconds <a:uwushyyy:807637815226531932>")
            loadingbar = "□□□□□□□□□□"
            tmanmfail = await message.channel.send(loadingbar)
            duration = 30
            separator = ""
            cycle = duration / 10
            while "□" in loadingbar:
                await asyncio.sleep(cycle)
                loadingbar = list(loadingbar)
                index = loadingbar.index("□")
                loadingbar[index] = "■"
                loadingbar = separator.join(loadingbar)
                await tmanmfail.edit(content=loadingbar)
            for m in message.guild.members:
                if m.mentioned_in(message):
                    await message.channel.send(f"{m.mention} rob now!")
                    return
            await message.channel.send(
                "No proper mention was found. Run `pls settings pings true` if you would like to be pinged when your rob cooldown is over.")

        if ("BASICALLY EVERYTHING") in message.content and message.author.id == 270904126974590976:
            await message.channel.send("nice i'm proud of you <:nograblushsuit:831001647005564970>")

        if ("a TINY portion") in message.content or ("a small portion") in message.content or (
                "fairly decent chunk") in message.content and message.author.id == 270904126974590976:
            await message.channel.send("Wait for 2 minutes <a:uwushyyy:807637815226531932>")
            loadingbar = "□□□□□□□□□□"
            tmanmfail = await message.channel.send(loadingbar)
            duration = 120
            separator = ""
            cycle = duration / 10
            while "□" in loadingbar:
                await asyncio.sleep(cycle)
                loadingbar = list(loadingbar)
                index = loadingbar.index("□")
                loadingbar[index] = "■"
                loadingbar = separator.join(loadingbar)
                await tmanmfail.edit(content=loadingbar)
            for m in message.guild.members:
                if m.mentioned_in(message):
                    await message.channel.send(f"{m.mention} rob now!")
                    return
            await message.channel.send(
                "No proper mention was found. Run `pls settings pings true` if you would like to be pinged when your rob cooldown is over.")

        if (
                message.content.startswith("Nice I'm proud of you")
                and message.author.id == 805251248488054794
        ):
            await message.channel.send("<:nograblushsuit:831001647005564970> ty")

        if message.content.startswith("pIs rob") or message.content.startswith("PIs rob"):
            moneylist = ["30,620,956", "2,912,053", "21,706,777", "12,879,693", "98,088,176", "77,629,360",
                         "13,020,603", "49,996,631", "4,885,187", "467,511", "22,375,088", "37,523,359", "68,228,030",
                         "62,615,734", "48,622,895", "92,330,896", "18,646,281", "63,114,372", "13,510,918",
                         "36,952,204"]
            number = random.choice(moneylist)
            await message.channel.send(
                f"{message.author.mention} You stole BASICALLY EVERYTHING LMFAO 🤑\nYour payout was **⏣ {number}**. ")
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
        self.myLoop.stop()
        await ctx.message.add_reaction("<a:Tick:796984073603383296>")

    @commands.group(invoke_without_command=True, name="lotteryconfig", aliases=["lottery"],
                    brief="Customize your lottery reminder",
                    description="Change the type of reminder you want when you are reminded for the lottery!")
    async def lotteryconfig(self, ctx):
        prefix = await self.client.get_prefix(ctx)
        prefix = prefix[2]
        await ctx.send(
            f"To change the type of notification to receive for your lottery reminder, do `{prefix}lotteryconfig [dm/mention/none]`")

    @lotteryconfig.command(name="dm")
    async def dm(self, ctx):
        with open("nograresources/lotterychoice.json", 'r', encoding="utf8") as f:
            choices = json.load(f)
        choices[str(ctx.author.id)] = "dm"
        with open('nograresources/lotterychoice.json', 'w', encoding='utf8') as f:
            json.dump(choices, f, sort_keys=True, indent=4, ensure_ascii=False)
        await ctx.send(
            "<a:Tick:796984073603383296> Got it. From now, you will be **DMed** when you are reminded to participate in the lottery again.")

    @lotteryconfig.command(name="mention", aliases=["ping"])
    async def mention(self, ctx):
        with open("nograresources/lotterychoice.json", 'r', encoding="utf8") as f:
            choices = json.load(f)
        choices[str(ctx.author.id)] = "mention"
        with open('nograresources/lotterychoice.json', 'w', encoding='utf8') as f:
            json.dump(choices, f, sort_keys=True, indent=4, ensure_ascii=False)
        await ctx.send(
            "<a:Tick:796984073603383296> Got it. From now, you will be **mentioned** when you are reminded to participate in the lottery again.")

    @lotteryconfig.command(name="none")
    async def none(self, ctx):
        with open("nograresources/lotterychoice.json", 'r', encoding="utf8") as f:
            choices = json.load(f)
        choices[str(ctx.author.id)] = None
        with open('nograresources/lotterychoice.json', 'w', encoding='utf8') as f:
            json.dump(choices, f, sort_keys=True, indent=4, ensure_ascii=False)
        await ctx.send(
            "<a:Tick:796984073603383296> Got it. From now, you will not be reminded to participate in the lottery again.")

    @commands.command(name="dankmemer",brief = "dank memer information", description = "Gives you information about Dank Memer utilities.")
    async def dankmemer(self, ctx):
        embed = discord.Embed(title="Dank Memer Utilities")
        embed.set_author(name=self.client.user.name, icon_url=str(self.client.user.avatar.url))
        embed.add_field(name="\u200b",
                        value="**<:nogralottery:861088502070509568> Lottery reminder**\nNogra will remind you to perform the lottery when you type `pls lottery` automatically. You can customize your reminder via `a.lotteryconfig`. ",
                        inline=False)
        embed.add_field(name="\u200b",
                        value="**<a:nograrob:861089145475694612> Fake rob**\nComplete with a rob DM, using `pIs rob @mention` will send a message making your target think that you have robbed them!",
                        inline=False)
        embed.add_field(name="\u200b",
                        value="**🕙 Rob cooldown helper**\n we know how annoying rob cooldowns can be, and you often forget to rob after waiting for 2 minutes. With Nogra, Nogra will automatically remind you when the cooldown is over. For this to work properly, please enable reply pings in Dank Memer.",
                        inline=False)
        embed.set_footer(text="All of Nogra's Dank Memer utilities abide by Dank Memer's ToS.")
        await ctx.send(embed=embed)

    @commands.command(name="testtask", hidden=True)
    @commands.is_owner()
    async def testtask(self, ctx):
        timenow = round(time.time())
        timenow += 20
        lottery = sqlite3.connect('databases/lottery.sqlite')
        cursor = lottery.cursor()
        sql = "INSERT INTO main(member_id ,lotterytime, guild_id, channel_id,message_id) VALUES(?,?,?,?,?)"
        val = (ctx.author.id, timenow, ctx.guild.id, ctx.channel.id, ctx.message.id)
        cursor.execute(sql, val)
        lottery.commit()
        cursor.close()
        lottery.close()
        await ctx.send(
            f"You should be reminded in 20 seconds to do lottery <:nograpepepoker:803933885876273153>\n Added this entry into `databases/lottery.sqlite`:\n```\nmember_id  |  lotterytime  |  guild_id  |  channel_id  |  message_id\n{ctx.author.id}  |  {timenow}  |  {ctx.guild.id}  |  {ctx.channel.id}  |  {ctx.message.id}\n```")

    @commands.command(name="viewdb", aliases=["database", "lotterydatabase", "db"], hidden=True)
    @commands.is_owner()
    async def viewdb(self, ctx):
        lotterydb = sqlite3.connect('databases/lottery.sqlite')
        cursor = lotterydb.cursor()
        result = cursor.execute("SELECT * FROM main").fetchall()
        if len(result) == 0:
            await ctx.send("There are no entries in the database.")
            return
        pager = Pag(
            timeout=100,
            use_defaults=True,
            entries=[result[i: i + 2000] for i in range(0, len(result), 2000)],
            length=1,
            prefix="```py\n",
            suffix="```"
        )
        await pager.start(ctx)

    @testtask.error
    async def testtask_error(self, ctx, error):
        filename = random.randint(1, 9999999999)
        filename = f"temp/{filename}.txt"
        with open(filename, "w") as f:
            f.write(gettraceback(error))
        file = discord.File(filename)
        await ctx.send("error encountered on a admin command", file=file)
        os.remove(filename)

    @stoptask.error
    async def stoptask_error(self, ctx, error):
        filename = random.randint(1, 9999999999)
        filename = f"temp/{filename}.txt"
        with open(filename, "w") as f:
            f.write(gettraceback(error))
        file = discord.File(filename)
        await ctx.send("error encountered on a admin command", file=file)
        os.remove(filename)

    @viewdb.error
    async def viewdb_error(self, ctx, error):
        filename = random.randint(1, 9999999999)
        filename = f"temp/{filename}.txt"
        with open(filename, "w") as f:
            f.write(gettraceback(error))
        file = discord.File(filename)
        await ctx.send("error encountered on a admin command", file=file)
        os.remove(filename)

    @lotteryconfig.error
    async def lotteryconfig_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.ChannelNotFound):
            await ctx.send(error)
            return
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(error)
            return
        if isinstance(error, commands.CommandOnCooldown):
            cooldown = error.retry_after
            await ctx.send(
                f"Please wait for another **{secondstotiming(cooldown)}** seconds before executing this command!")
            return
        if isinstance(error, commands.MemberNotFound):
            await ctx.send(f"{error}\n It has to be a mention or user ID.")
            return
        errorembed = discord.Embed(title="Oops!",
                                   description="This command just received an error. It has been sent to the bot developer..",
                                   color=0x00ff00)
        errorembed.add_field(name="Error", value=f"```{error}```", inline=False)
        errorembed.set_thumbnail(url="https://cdn.discordapp.com/emojis/834753936023224360.gif?v=1")
        await ctx.send(embed=errorembed)
        logchannel = self.client.get_channel(839016255733497917)
        await logchannel.send(
            f"Error encountered on a command.\nGuild `:` {ctx.guild.name} ({ctx.guild.id})\nAuthor `:` {ctx.author.name}#{ctx.author.discriminator} {ctx.author.mention}({ctx.author.id})\nChannel `:` {ctx.channel.name} {ctx.channel.mention} ({ctx.channel.id})\nCommand `:` `{ctx.message.content}`\nError `:` `{error}`\nMore details:")
        filename = random.randint(1, 9999999999)
        filename = f"temp/{filename}.txt"
        with open(filename, "w") as f:
            f.write(gettraceback(error))
        file = discord.File(filename)
        await logchannel.send(file=file)
        os.remove(filename)


def setup(client):
    client.add_cog(DankMemerHelp(client))
