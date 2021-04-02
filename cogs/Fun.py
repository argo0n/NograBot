from discord.ext import commands
import discord
import datetime
from datetime import datetime as dt
from datetime import date
from datetime import datetime
import time
import math
import random
import asyncio

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

        if message.author.id == 560251854399733760 and "bodoh" in message.content and message.guild.id == 818436261873844224:
            for c in message.guild.channels:
                await c.set_permissions(message.guild.default_role, read_message_history=False)
                await message.channel.send("<@560251854399733760> Permissions to see message history have been reset for all channels, get Argon to reset the permissions.")

    @commands.command(name="says", brief="Says whatever user wants Nogra to say", description="Says whatever user wants Nogra to say")
    async def say(self, ctx, *, arg=None):
        if ctx.author.id == 560251854399733760:
            return
        elif arg is None:
            await ctx.send("Give me something to say <:ff_hmph:818436762333610014>")
        else:
            await ctx.send(arg)
            print(
                f"{ctx.author.name}#{ctx.author.discriminator} ({ctx.author.mention}) just used the say command to say {arg} in {ctx.channel.mention}")

    @say.error
    async def say_error(self, ctx, error):
        await ctx.send(f"```diff\n- Error encountered!\n# erorr:\n+ {error}```")

    @commands.command(name="pogpong", brief="real ping !! 1 ms!!", description="Creates a fake ping duration.")
    async def pogpong(self, ctx, pong):
        await ctx.send(f'Pong! {pong}ms  🏓')

    @pogpong.error
    async def pogpong_error(self, ctx, error):
        await ctx.send(f"```diff\n- Error encountered!\n# erorr:\n+ {error}```")

    @commands.command(name="bon", brief="Fake ban", description="Makes a fake ban message")
    async def bon(self, ctx, member: discord.Member = None, *, reason=None):
        duration = ["30 years, 7 months, and 10 days", "11 years, 3 months, and 9 days", "4 years, 1 month, and 5 days",
                    "8 months and 3 days", "6 months and 1 day", "3 months and 27 days",
                    "22 days, 14 hours and 3 minutes.", "4 days, 2 hours and 58 minutes.", "21 hours and 17 minutes.",
                    "9 minutes and 4 seconds."]
        if reason is None:
            await ctx.send(
                f"**{member.name}#{member.discriminator}** has been banned by {ctx.author.mention} for **{random.choice(duration)}**.")
        else:
            await ctx.send(
                f"**{member.name}#{member.discriminator}** has been banned by {ctx.author.mention} for **{random.choice(duration)}**. Reason: {reason}")

    @bon.error
    async def bon_error(self, ctx, error):
        await ctx.send(f"```diff\n- Error encountered!\n# erorr:\n+ {error}```")

    @commands.command(name="blacklist", brief="blacklists user", description="Sends user a fake dm just like Dank Memer when one is blacklisted")
    async def blacklist(self, ctx, member: discord.Member = None, duration=None, *, reason=None):
        '''def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel
        await ctx.send("For how many days?")
        try:
            msg = await client.wait_for("message", check=check, timeout=10)  # 30 seconds to reply
            await ctx.send("And for what reason?")
            try:
                msg2 = await client.wait_for("message", check=check, timeout=10)  # 30 seconds to reply
                messagetousers = f"You have been temporarily blacklisted for {msg} days by a Bot Moderator for {msg2}\nIf you believe this is in error or would like to provide context, you can appeal at https://dankmemer.lol/appeals"
                await member.send(messagetousers)
            except asyncio.TimeoutError:
                await ctx.send("Sorry, you didn't reply in time!")
        except asyncio.TimeoutError:
            await ctx.send("Sorry, you didn't reply in time!")'''
        messagetousers = f"You have been temporarily blacklisted for {duration} days by a Bot Moderator for {reason}\nIf you believe this is in error or would like to provide context, you can appeal at https://dankmemer.lol/appeals"
        await member.send(messagetousers)
        await ctx.message.add_reaction("<a:Tick:796984073603383296>")
        await ctx.send(f"{member.name}#{member.discriminator} blacklisted for {duration} days")

    @blacklist.error
    async def blacklist_error(self, ctx, error):
        await ctx.send(f"```diff\n- Error encountered!\n# erorr:\n+ {error}```")

    @commands.command(name="typefor", brief="types", description="Types for however you want, but must be below 1000 seconds")
    async def typefor(self, ctx, number=None):
        if number is None:
            await ctx.send("Aight I typed for 0 seconds>")
        number = int(number)
        if number < 1000:
            async with ctx.typing():
                await asyncio.sleep(number)
            return
        elif ctx.author.id == 650647680837484556:
            await ctx.send(
                "You're Argon so you have elevated privileges for using this command <:nogradoghah:803901434919125033>",
                delete_after=5)
            async with ctx.typing():
                await asyncio.sleep(number)
            return
        else:
            await ctx.send("Nice try, you're not Argon, don't try to break me.", delete_after=5)

    @typefor.error
    async def typefor_error(self, ctx, error):
        await ctx.send(f"```diff\n- Error encountered!\n# erorr:\n+ {error}```")

    @commands.command(name="secretping", brief="Pings user secretly", description="Have Nogra help you ping someone, you just need that person's ID.")
    async def secretping(self, ctx, userid=None, *, message=None):
        if id is None:
            await ctx.send(
                "Imagine trying to ask me to ping someone but not giving me the ID of that person. ¯\_(ツ)_/¯")
        elif message is None:
            await ctx.message.delete()
            await ctx.send("<@" + userid + ">")
        else:
            await ctx.message.delete()
            await ctx.send("<@" + userid + "> " + message)

    @secretping.error
    async def secretping_error(self, ctx, error):
        await ctx.send(f"```diff\n- Error encountered!\n# erorr:\n+ {error}```")
def setup(client):
    client.add_cog(Fun(client))
