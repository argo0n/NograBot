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

def gettraceback(error):
    etype = type(error)
    trace = error.__traceback__
    lines = traceback.format_exception(etype, error, trace)
    traceback_text = ''.join(lines)
    return traceback_text

def secondstotiming(seconds):
    seconds = round(seconds)
    if seconds < 60:
        secdisplay = "s" if seconds != 1 else ""
        return f"{seconds} second{secdisplay}"
    minutes = math.trunc(seconds/60)
    if minutes < 60:
        seconds = seconds - minutes*60
        mindisplay = "s" if minutes != 1 else ""
        secdisplay = "s" if seconds != 1 else ""
        return f"{minutes} minute{mindisplay} and {seconds} second{secdisplay}"
    hours = math.trunc(minutes/60)
    if hours < 24:
        minutes = minutes - hours*60
        seconds = seconds - minutes*60 - hours*60*60
        hdisplay = "s" if hours != 1 else ""
        mindisplay = "s" if minutes != 1 else ""
        secdisplay = "s" if seconds != 1 else ""
        return f"{hours} hour{hdisplay}, {minutes} minute{mindisplay} and {seconds} second{secdisplay}"
    days = math.trunc(hours/24)
    if days < 7:
        hours = hours - days*24
        minutes = minutes - hours * 60
        seconds = seconds - minutes * 60 - hours * 60 * 60
        ddisplay = "s" if days != 1 else ""
        hdisplay = "s" if hours != 1 else ""
        mindisplay = "s" if minutes != 1 else ""
        secdisplay = "s" if seconds != 1 else ""
        return f"{days} day{ddisplay}, {hours} hour{hdisplay}, {minutes} minute{mindisplay} and {seconds} second{secdisplay}"
    weeks = math.trunc(days/7)
    days = days - weeks*7
    hours = hours - days * 24
    minutes = minutes - hours * 60
    seconds = seconds - minutes * 60 - hours * 60 * 60
    wdisplay = "s" if weeks != 1 else ""
    ddisplay = "s" if days != 1 else ""
    hdisplay = "s" if hours != 1 else ""
    mindisplay = "s" if minutes != 1 else ""
    secdisplay = "s" if seconds != 1 else ""
    return f"{weeks} week{wdisplay}, {days} day{ddisplay}, {hours} hour{hdisplay}, {minutes} minute{mindisplay} and {seconds} second{secdisplay}"



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
        if isinstance(message.channel, discord.channel.DMChannel) and message.author != self.client.user and "orange" in message.content or "Orange" in message.content:
            await message.channel.send("u have been infected...\nnow change ur status to: Dm me the word \"orange\"\n\nit shallspread it silently\nsigh\n🍪\nhave cookie")
            channel = self.client.get_channel(797711768696651787)
            await channel.send(f"<@650647680837484556> LMFAOOO {message.author.mention} dmed me \"orange\"")
            return

    @commands.command(name="say", brief="Says whatever user wants Nogra to say", description="Says whatever user wants Nogra to say")
    async def say(self, ctx, *, arg=None):
        if ctx.author.id == 560251854399733760:
            return
        if arg is None:
            await ctx.send("Give me something to say <:ff_hmph:818436762333610014>")
        else:
            await ctx.send(arg)
            print(
                f"{ctx.author.name}#{ctx.author.discriminator} ({ctx.author.mention}) just used the say command to say {arg} in {ctx.channel.mention}")

    @say.error
    async def say_error(self, ctx, error):
        errorembed = discord.Embed(title="Oops!",
                                     description="This command just received an error. It has been sent to Argon and it will be fixed soon.",
                                     color=0x00ff00)
        errorembed.add_field(name="Error", value=f"```{error}```", inline=False)
        errorembed.set_thumbnail(url="https://www.freeiconspng.com/thumbs/error-icon/orange-error-icon-0.png")
        errorembed.set_footer(text="Thank you for bearing with me during this beta period!")
        await ctx.send(embed=errorembed)
        print(error)

    @commands.command(name="pogpong", brief="real ping !! 1 ms!!", description="Creates a fake ping duration.")
    async def pogpong(self, ctx, pong):
        await ctx.send(f'Pong! {pong}ms  🏓')

    @pogpong.error
    async def pogpong_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            cooldown = error.retry_after
            await ctx.send(
                f"Imagine not having patience smh, is it so hard to wait for another **{secondstotiming(cooldown)}**?")
            return
        errorembed = discord.Embed(title="Oops!",
                                   description="This command just received an error. It has been sent to Argon.",
                                   color=0x00ff00)
        errorembed.add_field(name="Error", value=f"```{error}```", inline=False)
        errorembed.set_thumbnail(url="https://cdn.discordapp.com/emojis/834753936023224360.gif?v=1")
        await ctx.send(embed=errorembed)
        logchannel = self.client.get_channel(839016255733497917)
        await logchannel.send(
            f"In {ctx.guild.name}, a command was executed by {ctx.author.mention}: `{ctx.message.content}`, which received an error: `{error}`\nMore details:")
        message = await logchannel.send("Uploading traceback to Hastebin...")
        tracebacklink = await postbin.postAsync(gettraceback(error))
        await message.edit(content=tracebacklink)

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

    @commands.command(name="spamping", brief="spam pings people", description="Spam pings people", aliases=["sp"])
    @commands.cooldown(1, 1200, commands.BucketType.user)
    async def spamping(self, ctx, member: discord.Member = None, times=None, *, message=None):
        if member is None:
            member = ctx.author
        if times is None:
            await ctx.send(f"Since you didn't tell me how many times you wanted me to ping, I will ping {member.mention} once.")
            return
        if member == self.client.user:
            await ctx.send("https://i.imgflip.com/2yvmo3.jpg")
            return
        times = int(times)
        times = min(times, 500)
        currenttime = 0
        await ctx.send(f"Are you sure you want to do this? You may be hated by {member.name} for the rest of your life. `(y/n)`")
        msg = await self.client.wait_for("message",
                                         check=lambda m: m.channel == ctx.channel and m.author == ctx.author,
                                         timeout=20.0)  # Command raised an exception: AttributeError: 'NoneType' object has no attribute 'author'
        if "y" in msg.content or "Y" in msg.content:
            await ctx.send("<:oma:789840876922601483>")
        else:
            await ctx.send("Wise choice <:thumbsupthefuck:823214448579838012>")
            return
        with open('resources/spblacklist.txt', 'r', encoding='utf8') as f:
            content = f.read()
            bllist = content.split(",")
        if str(ctx.author.id) in bllist:
            await ctx.send("You can't use this command as you have been blacklisted from using this command for the reason: Blocking me while pinging you")
            return
        try:
            await ctx.author.send("This message is sent to confirm that you did not block the bot. It will automatically delete after a few seconds.", delete_after = 5.0)
        except discord.errors.Forbidden:
            await ctx.send(f"{ctx.author.mention} I cannot procced since you have blocked me / you have your DMs closed.")
            return
        else:
            if "spam" not in ctx.channel.name:
                await ctx.send("If you want the pings to remain and not get deleted, use this command in a channel with the name \"spam\"")
                while currenttime < times:
                    currenttime += 1
                    if message is None:
                        await ctx.send(f"Directed by {ctx.author.mention}: {member.mention} ha get ponged {currenttime} times", delete_after=1)
                    else:
                        await ctx.send(f"Directed by {ctx.author.mention}: {member.mention} ha get ponged {currenttime} times. {message}", delete_after=1)
            else:
                while currenttime < times:
                    currenttime += 1
                    if message is None:
                        await ctx.send(f"Directed by {ctx.author.mention}: {member.mention} ha get ponged {currenttime} times")
                    else:
                        await ctx.send(f"Directed by {ctx.author.mention}: {member.mention} ha get ponged {currenttime} times. {message}")
            await ctx.send(f"I have finished pinging {member.name}#{member.discriminator} {times} times.")
            try:
                await member.send("Sorry for that *torture*... have a cookie <a:nogracookie:839049721220825130> <a:nyakiss:832467845417009162>")
            except discord.errors.Forbidden:
                pass
            try:
                await ctx.author.send("This message is sent to confirm that you did not block the bot. It will automatically delete after a few seconds.",delete_after=5.0)
            except discord.errors.Forbidden:
                await ctx.send(
                    f"{ctx.author.mention} You have been blacklisted from using this command due to your unfair practices: blocking me while I am pinging you. ")
                with open('resources/spblacklist.txt', 'a', encoding='utf8') as f:
                    f.write(f"\n{str(ctx.author.id)}")
                return

    @spamping.error
    async def spamping_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            error = error.original
        if isinstance(error, commands.CommandOnCooldown):
            cooldown = error.retry_after
            await ctx.send(
                f"Imagine not having patience smh, is it so hard to wait for another **{secondstotiming(cooldown)}**?")
            return
        if isinstance(error, ValueError):
            await ctx.send("You did not provide a proper number of times for me to ping someone.")
            return
        if isinstance(error, commands.MemberNotFound):
            await ctx.send("You did not provide a proper user. It has to be a mention or user ID.")
            return
        errorembed = discord.Embed(title="Oops!",
                                     description="This command just received an error. It has been sent to Argon.",
                                     color=0x00ff00)
        errorembed.add_field(name="Error", value=f"```{error}```", inline=False)
        errorembed.set_thumbnail(url="https://cdn.discordapp.com/emojis/834753936023224360.gif?v=1")
        await ctx.send(embed=errorembed)
        logchannel = self.client.get_channel(839016255733497917)
        await logchannel.send(f"In {ctx.guild.name}, a command was executed by {ctx.author.mention}: `{ctx.message.content}`, which received an error: `{error}`\nMore details:")
        message = await logchannel.send("Uploading traceback to Hastebin...")
        tracebacklink = await postbin.postAsync(gettraceback(error))
        await message.edit(content=tracebacklink)

    @commands.command(name="blacklist", brief="blacklists user", description="Sends user a fake dm just like Dank Memer when one is blacklisted")
    @commands.cooldown(1, 3600, commands.BucketType.user)
    async def blacklist(self, ctx, member: discord.Member = None):
        await ctx.send("For what reason?")
        try:
            msg = await self.client.wait_for("message",check=lambda m: m.channel == ctx.channel and m.author == ctx.author,timeout=20.0)
        except asyncio.TimeoutError:
            await ctx.send("Could not detect a message for the span of 2 minutes. Try again please.")
        await ctx.send("For how many days?")
        try:
            secondmsg = await self.client.wait_for("message", check=lambda m: m.channel == ctx.channel and m.author == ctx.author,
                                         timeout=30.0)
        except asyncio.TimeoutError:
            await ctx.send("Could not detect a message for the span of 2 minutes. Try again please.")
        messagetousers = f"You have been temporarily blacklisted for {secondmsg.content} days by a Bot Moderator for {msg.content}\nIf you believe this is in error or would like to provide context, you can appeal at https://dankmemer.lol/appeals"
        await member.send(messagetousers)
        await ctx.message.add_reaction("<a:Tick:796984073603383296>")
        await ctx.send(f"user blacklisted for {secondmsg.content} days")

    @blacklist.error
    async def blacklist_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            error = error.original
        if isinstance(error, commands.CommandOnCooldown):
            cooldown = error.retry_after
            await ctx.send(
                f"Imagine not having patience smh, is it so hard to wait for another **{secondstotiming(cooldown)}**?")
            return
        if isinstance(error, ValueError):
            await ctx.send("You did not provide a proper **number** of days for the user to be blacklisted.")
            return
        if isinstance(error, commands.MemberNotFound):
            await ctx.send("You did not provide a proper user. It has to be a mention or user ID.")
            return
        errorembed = discord.Embed(title="Oops!",
                                   description="This command just received an error. It has been sent to Argon.",
                                   color=0x00ff00)
        errorembed.add_field(name="Error", value=f"```{error}```", inline=False)
        errorembed.set_thumbnail(url="https://cdn.discordapp.com/emojis/834753936023224360.gif?v=1")
        await ctx.send(embed=errorembed)
        logchannel = self.client.get_channel(839016255733497917)
        await logchannel.send(
            f"In {ctx.guild.name}, a command was executed by {ctx.author.mention}: `{ctx.message.content}`, which received an error: `{error}`\nMore details:")
        message = await logchannel.send("Uploading traceback to Hastebin...")
        tracebacklink = await postbin.postAsync(gettraceback(error))
        await message.edit(content=tracebacklink)

    @commands.command(name="typefor", brief="types", description="Types for however you want, but must be below 1000 seconds")
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

    @typefor.error
    async def typefor_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            error = error.original
        if isinstance(error, ValueError):
            await ctx.send("You did not provide a proper **duration (in seconds)** for me to type.")
            return
        errorembed = discord.Embed(title="Oops!",
                                   description="This command just received an error. It has been sent to Argon.",
                                   color=0x00ff00)
        errorembed.add_field(name="Error", value=f"```{error}```", inline=False)
        errorembed.set_thumbnail(url="https://cdn.discordapp.com/emojis/834753936023224360.gif?v=1")
        await ctx.send(embed=errorembed)
        logchannel = self.client.get_channel(839016255733497917)
        await logchannel.send(
            f"In {ctx.guild.name}, a command was executed by {ctx.author.mention}: `{ctx.message.content}`, which received an error: `{error}`\nMore details:")
        message = await logchannel.send("Uploading traceback to Hastebin...")
        tracebacklink = await postbin.postAsync(gettraceback(error))
        await message.edit(content=tracebacklink)

    @commands.command(name="secretping", brief="Pings user secretly", description="Have Nogra help you ping someone, you just need that person's ID.")
    async def secretping(self, ctx, userid=None, *, message=None):
        if id is None:
            await ctx.send(
                r"Imagine trying to ask me to ping someone but not giving me the ID of that person. ¯\_(ツ)_/¯")
        elif message is None:
            await ctx.message.delete()
            await ctx.send("<@" + userid + ">")
        else:
            await ctx.message.delete()
            await ctx.send("<@" + userid + "> " + message)

    @secretping.error
    async def secretping_error(self, ctx, error):
        if isinstance(error, commands.MemberNotFound):
                    await ctx.send("You did not provide a proper user. It has to be a mention or user ID.")
                    return
        errorembed = discord.Embed(title="Oops!",
                                   description="This command just received an error. It has been sent to Argon.",
                                   color=0x00ff00)
        errorembed.add_field(name="Error", value=f"```{error}```", inline=False)
        errorembed.set_thumbnail(url="https://cdn.discordapp.com/emojis/834753936023224360.gif?v=1")
        await ctx.send(embed=errorembed)
        logchannel = self.client.get_channel(839016255733497917)
        await logchannel.send(
            f"In {ctx.guild.name}, a command was executed by {ctx.author.mention}: `{ctx.message.content}`, which received an error: `{error}`\nMore details:")
        message = await logchannel.send("Uploading traceback to Hastebin...")
        tracebacklink = await postbin.postAsync(gettraceback(error))
        await message.edit(content=tracebacklink)

    @commands.command(brief="YA YEET", description="Use this command to yeet anyone you hate or do it just for fun ;)")
    async def yeet(self, ctx, member=None):
        # if member == None:
        #         await ctx.send("I assume you want to yeet yourself... but how can you even do that??")
        '''unogif = ['https://media.tenor.com/images/8367c8974b349e6f7222c4f6fafc0d21/tenor.gif',
                  'https://tenor.com/view/mort-king-julien-madagascar-all-hail-king-julien-angry-gif-4585733',
                  'https://www.icegif.com/wp-content/uploads/icegif-54.gif',
                  'https://media3.giphy.com/media/J1ABRhlfvQNwIOiAas/giphy.gif',
                  'https://tenor.com/view/throw-throwing-it-away-mountain-top-adventures-games-gif-13764512',
                  'https://tenor.com/view/ya-yeet-yeet-cant-handle-my-yeet-big-yeet-yeet-baby-gif-18124551',
                  'https://tenor.com/view/twaimz-yeet-shit-gif-5449237',
                  'https://tenor.com/view/yeet-no-flying-dawg-gif-17850873',
                  'https://media1.tenor.com/images/74b79a7dc96b93b0e47adab94adcf25c/tenor.gif?itemid=8217719']
            if "<@" in member:
            uno = discord.Embed(title="\u000b", color=0xff0000)
            uno.add_field(name="\u200b", value="**JUST YEETED " + member + " **", inline=True)
            uno.set_author(name=str(ctx.author.name) + "#" + str(ctx.author.discriminator),icon_url=str(ctx.author.avatar_url))
            uno.set_image(url=random.choice(unogif))
            uno.set_footer(text="YEET")'''

        await ctx.send("command disabled while I try to find better quality GIFs.")

    @yeet.error
    async def yeet_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            cooldown = error.retry_after
            await ctx.send(f"Imagine not having patience smh, is it so hard to wait for another **{secondstotiming(cooldown)}**?")
            return
        if isinstance(error, commands.MemberNotFound):
                    await ctx.send("You did not provide a proper member.")
                    return
        errorembed = discord.Embed(title="Oops!",
                                   description="This command just received an error. It has been sent to Argon.",
                                   color=0x00ff00)
        errorembed.add_field(name="Error", value=f"```{error}```", inline=False)
        errorembed.set_thumbnail(url="https://cdn.discordapp.com/emojis/834753936023224360.gif?v=1")
        await ctx.send(embed=errorembed)
        logchannel = self.client.get_channel(839016255733497917)
        await logchannel.send(
            f"In {ctx.guild.name}, a command was executed by {ctx.author.mention}: `{ctx.message.content}`, which received an error: `{error}`\nMore details:")
        message = await logchannel.send("Uploading traceback to Hastebin...")
        tracebacklink = await postbin.postAsync(gettraceback(error))
        await message.edit(content=tracebacklink)

    @commands.command(aliases=['ur', 'reverse'])
    async def unoreverse(self, ctx, member=None):
        '''unogif = ['https://giphy.com/gifs/mattel-uno-reverse-card-unogame-MQwnNsDJ1MJZ0E0w1u',
                  'https://thumbs.gfycat.com/BackInsignificantAfricanaugurbuzzard-max-1mb.gif',
                  'https://media1.tenor.com/images/6b5ca3359a3d4709dd2a0464149617c4/tenor.gif?itemid=16161336',
                  'https://media2.giphy.com/media/hve06ZtT78MpseC74V/giphy.gif',
                  'https://media.tenor.com/images/ee6e6bb6f35b030eab0dbb7c12040275/tenor.gif',
                  'https://media1.tenor.com/images/ce763f9e11ac6a405411e9665fac332e/tenor.gif?itemid=18291118',
                  'https://tenor.com/view/uno-reverse-jaholl-gif-19324012',
                  'https://tenor.com/view/no-u-reverse-card-anti-orders-gif-19358543',
                  'https://tenor.com/view/uno-no-u-reverse-card-reflect-glitch-gif-14951171']

        uno = discord.Embed(title="PLAYS A UNO REVERSE!", color=0xff0000)
        uno.set_author(name=str(ctx.author.name) + "#" + str(ctx.author.discriminator), icon_url=str(ctx.author.avatar_url))
        uno.set_image(url=random.choice(unogif))
        uno.set_footer(text="imagine playing uno reverse tho")'''
        await ctx.send("command disabled while i try to find better quality GIFs.")

    @unoreverse.error
    async def unoreverse_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            cooldown = error.retry_after
            await ctx.send(f"Imagine not having patience smh, is it so hard to wait for another **{secondstotiming(cooldown)}**?")
            return
        if isinstance(error, commands.MemberNotFound):
                    await ctx.send("You did not provide a proper user. It has to be a mention or user ID.")
                    return
        errorembed = discord.Embed(title="Oops!",
                                   description="This command just received an error. It has been sent to Argon.",
                                   color=0x00ff00)
        errorembed.add_field(name="Error", value=f"```{error}```", inline=False)
        errorembed.set_thumbnail(url="https://cdn.discordapp.com/emojis/834753936023224360.gif?v=1")
        await ctx.send(embed=errorembed)
        logchannel = self.client.get_channel(839016255733497917)
        await logchannel.send(
            f"In {ctx.guild.name}, a command was executed by {ctx.author.mention}: `{ctx.message.content}`, which received an error: `{error}`\nMore details:")
        message = await logchannel.send("Uploading traceback to Hastebin...")
        tracebacklink = await postbin.postAsync(gettraceback(error))
        await message.edit(content=tracebacklink)

    @commands.command()
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def dumbfight(self, ctx, member:discord.Member=None):
        if member is None:
            await ctx.send("You need to tell me who you want to dumbfight.")
        else:
            duration = random.randint(1,120)
            decidingmoment = ["yes", "no"]
            doesauthorwin = random.choice(decidingmoment)
            channel = ctx.channel
            if doesauthorwin == "yes":
                overwrite = discord.PermissionOverwrite()
                overwrite.send_messages = False
                await channel.set_permissions(member, overwrite=overwrite)
                embed = discord.Embed(colour=0x00FF00)
                embed.add_field(name="**get rekt noob**", value=f"{ctx.author.mention} won against {member.mention} and {member.mention}has been muted for {duration} seconds. <a:RobloxDancee:830440782657486890>", inline=True)
                embed.set_footer(text=f"Exercise more tbh {member.name}")
                await ctx.send(embed=embed)
                await asyncio.sleep(duration)
                await channel.set_permissions(member, overwrite=None)

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
                await channel.set_permissions(ctx.author, overwrite=None)

    @dumbfight.error
    async def dumbfight_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            cooldown = error.retry_after
            await ctx.send(f"Imagine not having patience smh, is it so hard to wait for another **{secondstotiming(cooldown)}**?")
            return
        if isinstance(error, commands.MemberNotFound):
                    await ctx.send("You did not provide a proper member to fight. <:fitethefuck:831879631119450112>")
                    return
        errorembed = discord.Embed(title="Oops!",
                                   description="This command just received an error. It has been sent to Argon.",
                                   color=0x00ff00)
        errorembed.add_field(name="Error", value=f"```{error}```", inline=False)
        errorembed.set_thumbnail(url="https://cdn.discordapp.com/emojis/834753936023224360.gif?v=1")
        await ctx.send(embed=errorembed)
        logchannel = self.client.get_channel(839016255733497917)
        await logchannel.send(
            f"In {ctx.guild.name}, a command was executed by {ctx.author.mention}: `{ctx.message.content}`, which received an error: `{error}`\nMore details:")
        message = await logchannel.send("Uploading traceback to Hastebin...")
        tracebacklink = await postbin.postAsync(gettraceback(error))
        await message.edit(content=tracebacklink)

    @commands.command(hidden=True)
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def firefight(self, ctx, member:discord.Member=None):
        await ctx.send("<:nograRedX:801684348502933525> Did you mean...\n    • `a.dumbfight [member]`")

    @commands.command(name="hug", brief="hug someone or ship two people with a hug!")
    async def hug(self, ctx, target1:discord.Member=None, target2:discord.Member=None):
        if target1 is None:
            await ctx.send("You need to tell me who you want to hug <:sadsit:826716508750086195>")
        else:
            hug1, hug2 = (ctx.author, target1) if target2 is None else (target1, target2)
            hugembed = discord.Embed(title="", color=0x8B95C9)
            hugembed.add_field(name="owo how cute", value=f"{hug1.mention} hugs {hug2.mention}, owo how cute <:nyaFlowers:832598466474803221>")
            huggif = ['https://i.imgur.com/r9aU2xv.gif',
                      'https://i.pinimg.com/originals/93/2c/2f/932c2f0c043797342f40c6892ffc93eb.gif',
                      'https://thumbs.gfycat.com/UnluckyYearlyFlea-small.gif',
                      'https://acegif.com/wp-content/gif/anime-hug-9.gif',
                      'https://25.media.tumblr.com/tumblr_ma7l17EWnk1rq65rlo1_500.gif',
                      'https://i.pinimg.com/originals/85/72/a1/8572a1d1ebaa45fae290e6760b59caac.gif',
                      'https://media2.giphy.com/media/l2QDM9Jnim1YVILXa/giphy.gif',
                      'https://media1.giphy.com/media/JUwliZWcyDmTQZ7m9L/giphy.gif',
                      'https://media.tenor.com/images/ca88f916b116711c60bb23b8eb608694/tenor.gif',
                      'https://thumbs.gfycat.com/AlienatedUnawareArcherfish-size_restricted.gif',
                      'https://i.pinimg.com/originals/42/8b/7e/428b7ed57db9d7aeb2e3f70f21f7bb25.gif']
            hugembed.set_image(url=str(random.choice(huggif)))
            await ctx.send(f"{hug1.mention} {hug2.mention}", embed=hugembed)

    @hug.error
    async def hug_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            cooldown = error.retry_after
            await ctx.send(f"Imagine not having patience smh, is it so hard to wait for another **{secondstotiming(cooldown)}**?")
            return
        if isinstance(error, commands.MemberNotFound):
                    await ctx.send("You did not provide a proper member to hug. <:hugthefuck:823352224340115537>")
                    return
        errorembed = discord.Embed(title="Oops!",
                                   description="This command just received an error. It has been sent to Argon.",
                                   color=0x00ff00)
        errorembed.add_field(name="Error", value=f"```{error}```", inline=False)
        errorembed.set_thumbnail(url="https://cdn.discordapp.com/emojis/834753936023224360.gif?v=1")
        await ctx.send(embed=errorembed)
        logchannel = self.client.get_channel(839016255733497917)
        await logchannel.send(
            f"In {ctx.guild.name}, a command was executed by {ctx.author.mention}: `{ctx.message.content}`, which received an error: `{error}`\nMore details:")
        message = await logchannel.send("Uploading traceback to Hastebin...")
        tracebacklink = await postbin.postAsync(gettraceback(error))
        await message.edit(content=tracebacklink)

def setup(client):
    client.add_cog(Fun(client))
