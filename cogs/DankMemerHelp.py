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
import postbin, traceback
import random

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

    @commands.Cog.listener()
    async def on_ready(self):
        print("Cog \"DankMemerHelp\" loaded")
        channel = self.client.get_channel(830352644027449354)
        await channel.send("Rebooted, reminders erased.")

    @commands.Cog.listener()
    async def on_message(self, message):
        def embedcheck(message):
            for e in message.embeds:
                return "You bought a lottery ticket" in e.title and message.author.id == 270904126974590976
        if message.author.id == 800184970298785802:
            return
        if message.content.startswith("pls lottery") or message.content.startswith("Pls lottery") and message.author.id not in [270904126974590976, 341994639395520526]:
            try:
                msg = await self.client.wait_for("message", check=embedcheck, timeout = 7.0)
            except asyncio.TimeoutError:
                await message.channel.send("I could not detect a message that was from Dank Memer.", delete_after = 5.0)
                return
            else:
                emojis = ["<a:Tick:796984073603383296>", "⏲️"]
                for emo in emojis:
                    await message.add_reaction(emo)
                if message.author.id == 395020663116529674:
                    await message.add_reaction("<:mention:838255192952274974>")
                    await asyncio.sleep(3600)
                    await message.channel.send(
                    f"{message.author.mention} Time to buy a lottery again <a:takethismoney:806096182594109471>")
                    with open('questresources/lotterytimes.txt', 'r', encoding='utf8') as f:
                        content = f.read()
                        content = int(content)
                        if content < 8:
                            content += 1
                            content = str(content)
                            with open('questresources/lotterytimes.txt', 'w', encoding='utf8') as f:
                                f.write(content)
                            channel = self.client.get_channel(842615048371568650)
                            await channel.send(f"bern has done lottery {content} times")
                            return
                        else:
                            with open('questresources/hasdonelottery.txt', 'r', encoding='utf8') as f:
                                content = f.read()
                                if content == "1":
                                    return
                                else:
                                    with open('questresources/hasdonelottery.txt', 'w', encoding='utf8') as f:
                                        f.write("1")
                                    await message.channel.send(
                                        "You completed a task! <a:Tick:796984073603383296>\n`lottery go brr`")
                                    channel = self.client.get_channel(842615048371568650)
                                    await channel.send(f"bern has completed lottery task")
                                return
                    return
                try:
                    await message.author.send("I will remind you in your DMs after an hour!", delete_after = 10.0)
                    await message.add_reaction("<:dms:838255193266716742>")
                    await asyncio.sleep(3600)
                    messagelink = discord.Embed(color=0x00FFFF)
                    messagelink.set_author(name=self.client.user.name, icon_url=str(self.client.user.avatar_url))
                    messagelink.add_field(name="\u200b", value=f"[Jump to message](https://discord.com/channels/{message.guild.id}/{message.channel.id}/{message.id})",
                                      inline=False)
                    await message.author.send(f"{message.author.mention} You were reminded in **{message.channel.mention}**: Time to buy a lottery again <a:takethismoney:806096182594109471>", embed=messagelink)

                except discord.errors.Forbidden:
                    await message.add_reaction("<:mention:838255192952274974>")
                    await asyncio.sleep(3600)
                    await message.channel.send(
                        f"{message.author.mention} Time to buy a lottery again <a:takethismoney:806096182594109471>")
                    return
        if ("Mate") in message.content and message.author.id == 270904126974590976:
            await message.channel.send("Just wait for the lottery to be done tbh")
            return
        if ("Alright") in message.content and message.author.id == 270904126974590976:
            await message.channel.send("make up your mind LMAOOO")
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
            else:
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
            else:
                await message.channel.send("No proper mention was found.")

        if (
            message.content.startswith("Nice I'm proud of you")
            and message.author.id == 805251248488054794
        ):
            await message.channel.send("<:nograblushsuit:831001647005564970> ty")

        if message.content.startswith("pIs rob") or message.content.startswith("PIs rob"):
            if message.author.id == 395020663116529674:
                with open('questresources/robtimes.txt', 'r', encoding='utf8') as f:
                    content = f.read()
                    content = int(content)
                    if content < 3:
                        content += 1
                        content = str(content)
                        channel = self.client.get_channel(842615048371568650)
                        await channel.send(f"bern has done fake rob {content} times.")
                        with open('questresources/robtimes.txt', 'w', encoding='utf8') as f:
                            f.write(content)
                            pass
                    else:
                        with open('questresources/hasdonerob.txt', 'r', encoding='utf8') as f:
                            content = f.read()
                            if content == "1":
                                pass
                            else:
                                with open('questresources/hasdonerob.txt', 'w', encoding='utf8') as f:
                                    f.write("1")
                                await message.channel.send("You completed a task! <a:Tick:796984073603383296>\n`lottery go brr`")
                                channel = self.client.get_channel(842615048371568650)
                                await channel.send("bern has finished fakerob task")
                                pass
            list = ["30,620,956","2,912,053","21,706,777","12,879,693","98,088,176","77,629,360","13,020,603","49,996,631","4,885,187","467,511","22,375,088","37,523,359","68,228,030","62,615,734","48,622,895","92,330,896","18,646,281","63,114,372","13,510,918","36,952,204"]
            number = random.choice(list)
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

    @commands.command(name="manualremind", brief="Manually ping for lottery", description="Manually sets pings for lottery whenever bot reboots")
    async def manualremind(self, ctx, memberid, duration):
        memberid = int(memberid)
        duration = int(duration)
        durationinminutes = duration*60
        member = ctx.guild.get_member(memberid)
        await asyncio.sleep(durationinminutes)
        if memberid in [392127809939570688, 650647680837484556]:
            await member.send(f"{member.mention} You were reminded in **{ctx.guild.name}**: Time to buy a lottery again <a:takethismoney:806096182594109471>")
            print(f"I've sent a lottery message to {member.name}#{member.discriminator}")
        else:
            await ctx.send(f"{member.mention} Time to buy a lottery again <a:takethismoney:806096182594109471>")
    @manualremind.error
    async def manualremind_error(self, ctx, error):
        errorembed = discord.Embed(title=f"Oops!",
                                     description="This command just received an error. It has been sent to Argon and it will be fixed soon.",
                                     color=0x00ff00)
        errorembed.add_field(name="Error", value=f"```{error}```", inline=False)
        errorembed.set_thumbnail(url="https://www.freeiconspng.com/thumbs/error-icon/orange-error-icon-0.png")
        errorembed.set_footer(text="Thank you for bearing with me during this beta period!")
        await ctx.send(embed=errorembed)
        print(error)
def setup(client):
    client.add_cog(DankMemerHelp(client))
