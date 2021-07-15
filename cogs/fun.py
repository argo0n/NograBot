# |------------------------------------------------------------------------------------|
# |                                                                                    |
# |                                                                                    |
# |                               Fun Cog for Nogra Bot                                |
# |                               Written by Argon#0002                                |
# |                               Commands in this cog:                                |
# |   say, pogpong, bon, blacklisttypefor, secretping, yeet, unoreverse, dumbfight     |
# |                                                                                    |
# |                                                                                    |
# |------------------------------------------------------------------------------------
from discord.ext import commands
from discord.utils import find
import discord
import datetime
from datetime import datetime as dt
from datetime import date
import time
import math
import random
import asyncio
from discord.ext.buttons import Paginator
import postbin
import traceback
from cogs.nograhelpers import *
import os
import requests
import json


def gettraceback(error):
    etype = type(error)
    trace = error.__traceback__
    lines = traceback.format_exception(etype, error, trace)
    return ''.join(lines)


start_time = time.time()

TENOR_API_KEY = os.environ['TENORkey']

class Fun(commands.Cog):

    def __init__(self, client, emoji="🎮"):
        self.client = client
        self.description = "🎮 Fun commands!"
        self.emoji =emoji

    @commands.Cog.listener()
    async def on_ready(self):
        print("Cogs \"Fun\" has loaded")

    async def cog_command_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.ChannelNotFound):
            await ctx.send(error)
            return
        if isinstance(error, commands.MissingPermissions):
            if "--sudo permbypass" in ctx.message.content and ctx.author.id == 650647680837484556:
                await ctx.send("Reinvoking command with check bypass. Errors, if any, will show up in the console")
                await ctx.reinvoke()
                return
            await ctx.send(error)
            return
        if isinstance(error, commands.CommandOnCooldown):
            if "--sudo cdbypass" in ctx.message.content and ctx.author.id == 650647680837484556:
                await ctx.send("Reinvoking command with cooldown bypass. Errors, if any, will show up in the console")
                await ctx.reinvoke()
                return
            cooldown = error.retry_after
            await ctx.send(
                f"Please wait for another **{secondstotiming(cooldown)}** seconds before executing this command!")
            return
        if isinstance(error, commands.MemberNotFound):
            await ctx.send(f"{error}\n It has to be a mention or user ID.")
            return
        if isinstance(error, commands.CommandInvokeError):
            error = error.original
        if isinstance(error, ValueError):
            await ctx.send(
                "I expected a number somwhere in your command, but I got something else instead. Check if the numbers I require are just integers.")
            return
        if isinstance(error, discord.errors.Forbidden):
            if "Missing Permissions" in str(error):
                await ctx.send("I do not have the permissions to perform the required actions in this command. ")
            elif "Missing Access" in str(error):
                await ctx.send("I do not have the permissions to access something (probably a channel).")
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

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id == 800184970298785802:
            return

    @commands.command(name="say", brief="Says whatever user wants Nogra to say",
                      description="Says whatever user wants Nogra to say")
    async def say(self, ctx, *, arg=None):
        if ctx.author.id == 560251854399733760:
            return
        if arg is None:
            await ctx.send("Give me something to say <:ff_hmph:818436762333610014>")
        else:
            await ctx.send(arg)
            print(
                f"{ctx.author.name}#{ctx.author.discriminator} ({ctx.author.mention}) just used the say command to say {arg} in {ctx.channel.mention}")

    @commands.command(name="pogpong", brief="real ping !! 1 ms!!", description="Creates a fake ping duration.")
    async def pogpong(self, ctx, pong=None):
        if pong is None:
            await ctx.send("Pong! ∞ ms  🏓")
            return
        await ctx.send(f'Pong! {pong}ms  🏓')

    @commands.command(name="bon", brief="Fake ban", description="Makes a fake ban message")
    async def bon(self, ctx, member: discord.Member = None, *, reason=None):
        duration = ["30 years, 7 months, and 10 days", "11 years, 3 months, and 9 days", "4 years, 1 month, and 5 days",
                    "8 months and 3 days", "6 months and 1 day", "3 months and 27 days",
                    "22 days, 14 hours and 3 minutes.", "4 days, 2 hours and 58 minutes.", "21 hours and 17 minutes.",
                    "9 minutes and 4 seconds."]
        if member is None:
            await ctx.send("You didn't provide a member, It has to be a mention or user ID.")
            return
        if reason is None:
            await ctx.send(
                f"**{member.name}#{member.discriminator}** has been banned by {ctx.author.mention} for **{random.choice(duration)}**.")
        else:
            await ctx.send(
                f"**{member.name}#{member.discriminator}** has been banned by {ctx.author.mention} for **{random.choice(duration)}**. Reason: {reason}")

    @commands.command(name="spamping", brief="spam pings people", description="Spam pings people", aliases=["sp"], hidden = True)
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def spamping(self, ctx, member: discord.Member = None, times=None, *, message=None):
        await ctx.send("This command is deprecated from build **2.5.0** onwards. For more information, check out the changelog.\nNogra will no longer respond to this command after the next update.")
        return

    @commands.command(name="blacklist", brief="blacklists user",
                      description="Sends user a fake dm just like Dank Memer when one is blacklisted")
    @commands.cooldown(1, 1800, commands.BucketType.user)
    async def blacklist(self, ctx, member: discord.Member = None):
        if member is None:
            await ctx.send("You didn't provide a member lol")
            ctx.command.reset_cooldown(ctx)
            return
        await ctx.send("For what reason?")
        try:
            msg = await self.client.wait_for("message",
                                             check=lambda m: m.channel == ctx.channel and m.author == ctx.author,
                                             timeout=20.0)
        except asyncio.TimeoutError:
            await ctx.send("Could not detect a message for the span of 2 minutes. Try again please.")
            ctx.command.reset_cooldown(ctx)
            return
        await ctx.send("For how many days?")
        try:
            secondmsg = await self.client.wait_for("message",
                                                   check=lambda m: m.channel == ctx.channel and m.author == ctx.author,
                                                   timeout=30.0)
        except asyncio.TimeoutError:
            await ctx.send("Could not detect a message for the span of 2 minutes. Try again please.")
            ctx.command.reset_cooldown(ctx)
            return
        messagetousers = f"You have been temporarily blacklisted for {secondmsg.content} days by a Bot Moderator for {msg.content}\nIf you believe this is in error or would like to provide context, you can appeal at https://dankmemer.lol/appeals"
        await member.send(messagetousers)
        await ctx.message.add_reaction("<a:Tick:796984073603383296>")
        await ctx.send(f"user blacklisted for {secondmsg.content} days")

    @commands.command(name="typefor", brief="types",
                      description="Types for however you want, but must be below 1000 seconds")
    async def typefor(self, ctx, number=None):
        if number is None:
            await ctx.send("Aight I typed for 0 seconds")
            return
        number = int(number)
        if number < 1000:
            async with ctx.typing():
                await asyncio.sleep(number)
            return
        if ctx.author.id == 650647680837484556:
            await ctx.send(
                "You're Argon so you have elevated privileges for using this command <:nogradoghah:803901434919125033>",
                delete_after=5)
            async with ctx.typing():
                await asyncio.sleep(number)
            return
        await ctx.send("Nice try, you're not Argon, don't try to break me.", delete_after=5)

    @commands.command(name="secretping", brief="Pings user secretly",
                      description="Have Nogra help you ping someone, you just need that person's ID.")
    async def secretping(self, ctx, userid=None, *, message=None):
        if userid is None:
            await ctx.send(
                r"Imagine trying to ask me to ping someone but not giving me the ID of that person. ¯\_(ツ)_/¯")
            return
        userid = int(userid)
        if message is None:
            await ctx.message.delete()
            await ctx.send(f"<@{userid}>")
        else:
            await ctx.message.delete()
            await ctx.send(f"<@{userid}> {message}")

    @commands.command()
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def dumbfight(self, ctx, member: discord.Member = None):
        if member is None:
            await ctx.send("You need to tell me who you want to dumbfight.")
        else:
            duration = random.randint(1, 120)
            decidingmoment = ["yes", "no"]
            doesauthorwin = random.choice(decidingmoment)
            channel = ctx.channel
            if doesauthorwin == "yes":
                overwrite = discord.PermissionOverwrite()
                overwrite.send_messages = False
                await channel.set_permissions(member, overwrite=overwrite)
                embed = discord.Embed(colour=0x00FF00)
                embed.add_field(name="**get rekt noob**",
                                value=f"{ctx.author.mention} won against {member.mention} and {member.mention}has been muted for {duration} seconds. <a:RobloxDancee:830440782657486890>",
                                inline=True)
                embed.set_footer(text=f"Exercise more tbh {member.name}")
                await ctx.send(embed=embed)
                await asyncio.sleep(duration)
                overwrite.send_messages = True
                await channel.set_permissions(member, overwrite=overwrite)

            else:
                overwrite = discord.PermissionOverwrite()
                overwrite.send_messages = False
                await channel.set_permissions(ctx.author, overwrite=overwrite)
                embed = discord.Embed(colour=0xFF0000)
                embed.add_field(name="**get rekt noob**",
                                value=f"{ctx.author.mention} lost against {member.mention} and {ctx.author.mention} has been muted for {duration} seconds. <:fitethefuck:831879631119450112>",
                                inline=True)
                embed.set_footer(text=f"Exercise more tbh {ctx.author.name}")
                await ctx.send(embed=embed)
                await asyncio.sleep(duration)
                overwrite.send_messages = True
                await channel.set_permissions(ctx.author, overwrite=overwrite)

    @commands.command(name="hug", brief="hug someone or ship two people with a hug!")
    async def hug(self, ctx, target1: discord.Member = None, target2: discord.Member = None):
        if target1 is None:
            await ctx.send("You need to tell me who you want to hug <:sadsit:826716508750086195>")
        else:
            hug1, hug2 = (ctx.author, target1) if target2 is None else (target1, target2)
            hugembed = discord.Embed(title="", color=0x8B95C9)
            hugembed.add_field(name="owo how cute",
                               value=f"{hug1.mention} hugs {hug2.mention}, owo how cute <:nyaFlowers:832598466474803221>")
            response = requests.get("https://some-random-api.ml/animu/hug")
            json_data = json.loads(response.text)
            huggif = json_data["link"]
            
            hugembed.set_image(url=str(huggif))
            await ctx.send(f"{hug1.mention} {hug2.mention}", embed=hugembed)
            
    @commands.command(name="slap", brief="slap someone with or even without any reason!")
    async def slap(self, ctx, slapTarget: discord.Member = None):
        if slapTarget is None:
            await ctx.send("Congratulations you just slapped yourself <:dv_tfWhatteaOwO:837880380941533214>")
        else:
            author = ctx.author
            slapembed = discord.Embed(title="", color=0xd41919)
            slapembed.add_field(name="What a slap!", value=f"{slapTarget} just got a hard slap from {author}!")
            search_term = "slap"
            r = requests.get(f"https://g.tenor.com/v1/search?q={search_term}&key={TENOR_API_KEY}&limit=30")
            if r.status_code == 200:
                json_data = json.loads(r.text)
                slapgif = json_data["results"][random.randint(0, 29)]["media"][0]["gif"]["url"]
                slapembed.set_image(url=str(slapgif))
                slapembed.set_footer(text="GIFs taken from tenor")
                await ctx.send(f"{slapTarget}", embed=slapembed)
            else:
                print("There's something happened on the tenor API")
                await ctx.send("Some error occured, please dm Argon#0002 or Maple 🍁#2204. \n `ERROR CODE: ERR_API_TNR_SLP`")
            
    @commands.command(name="kiss", brief="kiss someone :)")
    async def kiss(self, ctx, kissTarget: discord.Member = None):
        if kissTarget is None:
            await ctx.send("You need to mention someone to kiss <:sad:753682653462396979>")
        else:
            author = ctx.author
            kissembed = discord.Embed(title="", color=0xf7a8a1)
            kissembed.add_field(name="How cute :3", value=f"{kissTarget}, you got a kiss from {author} :)")
            search_term = "kiss"
            r = requests.get(f"https://g.tenor.com/v1/search?q={search_term}&key={TENOR_API_KEY}&limit=30")
            if r.status_code == 200:
                json_data = json.loads(r.text)
                kissgif = json_data["results"][random.randint(0, 29)]["media"][0]["gif"]["url"]
                kissembed.set_image(url=str(kissgif))
                kissembed.set_footer(name="GIFs taken from tenor")
                await ctx.send(f"{kissTarget}", embed=kissembed)
            else:
                print("There's something happened on the tenor API")
                await ctx.send("Some error occured, please dm Argon#0002 or Maple 🍁#2204. \n `ERROR CODE: ERR_API_TNR_KSS`")

def setup(client):
    client.add_cog(Fun(client))
