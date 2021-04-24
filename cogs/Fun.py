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

    @commands.command(name="say", brief="Says whatever user wants Nogra to say", description="Says whatever user wants Nogra to say")
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
        errorembed = discord.Embed(title=f"Oops!",
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
        errorembed = discord.Embed(title=f"Oops!",
                                     description="This command just received an error. It has been sent to Argon and it will be fixed soon.",
                                     color=0x00ff00)
        errorembed.add_field(name="Error", value=f"```{error}```", inline=False)
        errorembed.set_thumbnail(url="https://www.freeiconspng.com/thumbs/error-icon/orange-error-icon-0.png")
        errorembed.set_footer(text="Thank you for bearing with me during this beta period!")
        await ctx.send(embed=errorembed)
        print(error)

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

    @commands.command(name="spamping", brief="spam pings people", description="Spam pings people")
    async def spamping(self, ctx, member: discord.Member = None, times=None, *, message=None):
        currenttime = 0
        if times is None:
            await ctx.send(f"Since you didn't tell me how many times you wanted me to ping, I will ping {member.mention} once.")
        else:
            times = int(times)
            if times > 1000:
                times = 1000
            if "spam" not in ctx.channel.name:
                await ctx.send("If you want the pings to remain and not get deleted, use this command in a channel with the name \"spam\"")
                if message is None:
                    while currenttime < times:
                        currenttime += 1
                        await ctx.send(f"{member.mention} ha get ponged {currenttime} times", delete_after=1)
                    await ctx.send(f"I have finished pinging {member.name}#{member.discriminator} {times} times.")
                    return
                else:
                    while currenttime < times:
                        currenttime += 1
                        await ctx.send(f"{member.mention} ha get ponged {currenttime} times. {message}", delete_after=1)
                    await ctx.send(f"I have finished pinging {member.name}#{member.discriminator} {times} times.")
            else:
                if message is None:
                    while currenttime < times:
                        currenttime += 1
                        await ctx.send(f"{member.mention} ha get ponged {currenttime} times")
                    await ctx.send(f"I have finished pinging {member.name}#{member.discriminator} {times} times.")
                    return
                else:
                    while currenttime < times:
                        currenttime += 1
                        await ctx.send(f"{member.mention} ha get ponged {currenttime} times. {message}")
                    await ctx.send(f"I have finished pinging {member.name}#{member.discriminator} {times} times.")

    @spamping.error
    async def spamping_error(self, ctx, error):
        errorembed = discord.Embed(title=f"Oops!",
                                     description="This command just received an error. It has been sent to Argon and it will be fixed soon.",
                                     color=0x00ff00)
        errorembed.add_field(name="Error", value=f"```{error}```", inline=False)
        errorembed.set_thumbnail(url="https://www.freeiconspng.com/thumbs/error-icon/orange-error-icon-0.png")
        errorembed.set_footer(text="Thank you for bearing with me during this beta period!")
        await ctx.send(embed=errorembed)
        print(error)

    @commands.command(name="blacklist", brief="blacklists user", description="Sends user a fake dm just like Dank Memer when one is blacklisted")
    async def blacklist(self, ctx, member: discord.Member = None, duration=None, *, reason=None):
        messagetousers = f"You have been temporarily blacklisted for {duration} days by a Bot Moderator for {reason}\nIf you believe this is in error or would like to provide context, you can appeal at https://dankmemer.lol/appeals"
        await member.send(messagetousers)
        await ctx.message.add_reaction("<a:Tick:796984073603383296>")
        await ctx.send(f"{member.name}#{member.discriminator} blacklisted for {duration} days")

    @blacklist.error
    async def blacklist_error(self, ctx, error):
        errorembed = discord.Embed(title=f"Oops!",
                                     description="This command just received an error. It has been sent to Argon and it will be fixed soon.",
                                     color=0x00ff00)
        errorembed.add_field(name="Error", value=f"```{error}```", inline=False)
        errorembed.set_thumbnail(url="https://www.freeiconspng.com/thumbs/error-icon/orange-error-icon-0.png")
        errorembed.set_footer(text="Thank you for bearing with me during this beta period!")
        await ctx.send(embed=errorembed)
        print(error)

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
        errorembed = discord.Embed(title=f"Oops!",
                                     description="This command just received an error. It has been sent to Argon and it will be fixed soon.",
                                     color=0x00ff00)
        errorembed.add_field(name="Error", value=f"```{error}```", inline=False)
        errorembed.set_thumbnail(url="https://www.freeiconspng.com/thumbs/error-icon/orange-error-icon-0.png")
        errorembed.set_footer(text="Thank you for bearing with me during this beta period!")
        await ctx.send(embed=errorembed)
        print(error)

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
        errorembed = discord.Embed(title=f"Oops!",
                                     description="This command just received an error. It has been sent to Argon and it will be fixed soon.",
                                     color=0x00ff00)
        errorembed.add_field(name="Error", value=f"```{error}```", inline=False)
        errorembed.set_thumbnail(url="https://www.freeiconspng.com/thumbs/error-icon/orange-error-icon-0.png")
        errorembed.set_footer(text="Thank you for bearing with me during this beta period!")
        await ctx.send(embed=errorembed)
        print(error)

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
        errorembed = discord.Embed(title=f"Oops!",
                                     description="This command just received an error. It has been sent to Argon and it will be fixed soon.",
                                     color=0x00ff00)
        errorembed.add_field(name="Error", value=f"```{error}```", inline=False)
        errorembed.set_thumbnail(url="https://www.freeiconspng.com/thumbs/error-icon/orange-error-icon-0.png")
        errorembed.set_footer(text="Thank you for bearing with me during this beta period!")
        await ctx.send(embed=errorembed)
        print(error)

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
        errorembed = discord.Embed(title=f"Oops!",
                                     description="This command just received an error. It has been sent to Argon and it will be fixed soon.",
                                     color=0x00ff00)
        errorembed.add_field(name="Error", value=f"```{error}```", inline=False)
        errorembed.set_thumbnail(url="https://www.freeiconspng.com/thumbs/error-icon/orange-error-icon-0.png")
        errorembed.set_footer(text="Thank you for bearing with me during this beta period!")
        await ctx.send(embed=errorembed)
        print(error)

    @commands.command()
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def dumbfight(self, ctx, member:discord.Member=None):
        if member == None:
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
                                value=f"{ctx.author.mention} lost against {member.mention} and {ctx.author.mention} has been muted for {duration} seconds. <a:RobloxDancee:830440782657486890>",
                                inline=True)
                embed.set_footer(text=f"Exercise more tbh {ctx.author.name}")
                await ctx.send(embed=embed)
                await asyncio.sleep(duration)
                await channel.set_permissions(ctx.author, overwrite=None)

    @dumbfight.error
    async def dumbfight_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            cooldown= error.retry_after
            await ctx.send(f"Imagine not having patience smh, is it so hard to wait for another {round(cooldown, 1)} seconds?")
        else:
            errorembed = discord.Embed(title=f"Oops!",
                                     description="This command just received an error. It has been sent to Argon and it will be fixed soon.",
                                     color=0x00ff00)
            errorembed.add_field(name="Error", value=f"```{error}```", inline=False)
            errorembed.set_thumbnail(url="https://www.freeiconspng.com/thumbs/error-icon/orange-error-icon-0.png")
            errorembed.set_footer(text="Thank you for bearing with me during this beta period!")
            await ctx.send(embed=errorembed)
            print(error)

    @commands.command(hidden=True)
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def firefight(self, ctx, member:discord.Member=None):
        await ctx.send("<:nograRedX:801684348502933525> Did you mean...\n    • `a.dumbfight [member]`")

    @commands.command(name="hug", brief="hug someone or ship two people with a hug!")
    async def hug(self, ctx, target1:discord.Member=None, target2:discord.Member=None):
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
        if target1 == None:
            await ctx.send("You need to tell me who you want to hug <:sadsit:826716508750086195>")
        else:
            if target2 == None:
                hug1, hug2 = ctx.author, target1
                hugembed = discord.Embed(title="", color=0x8B95C9)
                hugembed.add_field(name=f"owo how cute", value=f"{hug1.mention} hugs {hug2.mention}, owo how cute <:nyaFlowers:832598466474803221>")
                hugembed.set_image(url=str(random.choice(huggif)))
                await ctx.send(f"{hug1.mention} {hug2.mention}", embed=hugembed)
            else:
                hug1, hug2 = target1, target2
                hugembed = discord.Embed(title="", color=0x8B95C9)
                hugembed.add_field(name=f"owo how cute", value=f"{hug1.mention} hugs {hug2.mention}, owo how cute <:nyaFlowers:832598466474803221>")
                hugembed.set_image(url=str(random.choice(huggif)))
                await ctx.send(f"{hug1.mention} {hug2.mention}", embed=hugembed)

    @hug.error
    async def hug_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            cooldown = error.retry_after
            await ctx.send(
                f"Imagine not having patience smh, is it so hard to wait for another {round(cooldown, 1)} seconds?")
        else:
            errorembed = discord.Embed(title=f"Oops!",
                                     description="This command just received an error. It has been sent to Argon and it will be fixed soon.",
                                     color=0x00ff00)
            errorembed.add_field(name="Error", value=f"```{error}```", inline=False)
            errorembed.set_thumbnail(url="https://www.freeiconspng.com/thumbs/error-icon/orange-error-icon-0.png")
            errorembed.set_footer(text="Thank you for bearing with me during this beta period!")
            await ctx.send(embed=errorembed)
            print(error)

def setup(client):
    client.add_cog(Fun(client))
