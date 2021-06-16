# |------------------------------------------------------------------------------------|
# |                                                                                    |
# |                                                                                    |
# |                               API Cog for Nogra Bot                                |
# |                               Written by Argon#0002                                |
# |                               Commands in this cog:                                |
# |                                     cats, dogs                                     |
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
import aiohttp


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


start_time = time.time()


class APIs(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Cogs \"APIs\" has loaded")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id == 800184970298785802:
            return
        if isinstance(message.channel,
                      discord.channel.DMChannel) and message.author != self.client.user and "orange" in message.content or "Orange" in message.content:
            await message.channel.send(
                "u have been infected...\nnow change ur status to: Dm me the word \"orange\"\n\nit shallspread it silently\nsigh\n🍪\nhave cookie")
            channel = self.client.get_channel(797711768696651787)
            await channel.send(f"<@650647680837484556> LMFAOOO {message.author.mention} dmed me \"orange\"")
            return

    @commands.command(name="dogs", brief="cute dogs", description="Sends you pictures of cute dogs!")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def dogs(self, ctx):
        async with aiohttp.ClientSession() as session:
            request1 = await session.get("https://dog.ceo/api/breeds/image/random")
            request2 = await session.get("https://dog-facts-api.herokuapp.com/api/v1/resources/dogs?number=1")
            jsondata1 = await request1.json()
            jsondata2 = await request2.json()
            imagelink = jsondata1["message"]
        for i in jsondata2:
            fact = i['fact']
            dogembed = discord.Embed(title="A random dog!", description=fact, color=discord.Color.random())
            dogembed.set_image(url=imagelink)
        await ctx.send(embed=dogembed)

    @dogs.error
    async def dogs_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            cooldown = error.retry_after
            await ctx.send(
                f"As this command requires an external API, you need to wait for **{secondstotiming(cooldown)}** to prevent requests being spammed to this API.")
            return
        else:
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
    client.add_cog(APIs(client))
