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
from cogs.nograhelpers import *
import json
import requests


def gettraceback(error):
    etype = type(error)
    trace = error.__traceback__
    lines = traceback.format_exception(etype, error, trace)
    return ''.join(lines)


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

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            cooldown = error.retry_after
            await ctx.send(
                f"As this command requires an external API, you need to wait for **{secondstotiming(cooldown)}** to prevent requests being spammed to this API.")
            return

    @commands.command(name="dogs", brief="cute dogs",
                      description="Sends you pictures of cute dogs along with a fact about them!")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def dogs(self, ctx):
        r = requests.get('https://api.thedogapi.com/v1/images/search',
                         headers={'x-api-key': 'df2a30e7-db77-4036-b071-e840da424a93'})
        jsondata1 = json.loads(r.text)
        jsondata1 = jsondata1[0]
        imagelink = jsondata1["url"]
        async with aiohttp.ClientSession() as session:
            request2 = await session.get("https://dog-facts-api.herokuapp.com/api/v1/resources/dogs?number=1")
            jsondata2 = await request2.json()
        for i in jsondata2:
            fact = i['fact']
            dogembed = discord.Embed(title="A random dog!", description=fact, color=discord.Color.random())
            dogembed.set_image(url=imagelink)
        await ctx.send(embed=dogembed)

    @dogs.error
    async def dogs_error(self, ctx, error):
        cog = ctx.cog
        if cog and cog._get_overridden_method(cog.cog_command_error) is not None:
            return
        errorembed = discord.Embed(title="Oops!",
                                   description="This command just received an error. It has been sent to the bot developer..",
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

    @commands.command(name="cats", brief="cute cats",
                      description="Sends you pictures of cute cats along with a fact about them!")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def cats(self, ctx):
        r = requests.get('https://api.thecatapi.com/v1/images/search',
                         headers={'x-api-key': 'db23dec2-5442-4f1d-ba5d-12f896996069'})
        async with aiohttp.ClientSession() as session:
            request2 = await session.get("https://catfact.ninja/fact")
        jsondata1 = json.loads(r.text)
        jsondata2 = await request2.json()
        jsondata1 = jsondata1[0]
        imagelink = jsondata1["url"]
        fact = jsondata2["fact"]
        catembed = discord.Embed(title="A random cat!", description=fact, color=discord.Color.random())
        catembed.set_image(url=imagelink)
        await ctx.send(embed=catembed)

    @cats.error
    async def cats_error(self, ctx, error):
        cog = ctx.cog
        if cog and cog._get_overridden_method(cog.cog_command_error) is not None:
            return
        if isinstance(error, commands.CommandOnCooldown):
            cooldown = error.retry_after
            await ctx.send(
                f"As this command requires an external API, you need to wait for **{secondstotiming(cooldown)}** to prevent requests being spammed to this API.")
            return
        errorembed = discord.Embed(title="Oops!",
                                   description="This command just received an error. It has been sent to the bot developer..",
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
