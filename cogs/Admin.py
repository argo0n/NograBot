from discord.ext import commands
import asyncio
import traceback
import discord
import inspect
import textwrap
import importlib
from contextlib import redirect_stdout
import contextlib
import io
import os
import re
import sys
import copy
import time
import subprocess
from typing import Union, Optional
from discord.ext.buttons import Paginator



# to expose to the eval command
import datetime
from collections import Counter

class Pag(Paginator):
    async def teardown(self):
        try:
            await self.page.clear_reactions()
        except discord.HTTPException:
            pass

class Admin(commands.Cog):
    def __init__(self, client):
        self.client = client

    def cleanup_code(self, content):
        """Automatically removes code blocks from the code."""
        # remove ```py\n```
        if content.startswith('```') and content.endswith('```'):
            return '\n'.join(content.split('\n')[1:-1])

    async def cog_check(self, ctx):
        return await self.client.is_owner(ctx.author)

    @commands.Cog.listener()
    async def on_ready(self):
        print('Cog \"Admin\" loaded')

    @commands.command(pass_context=True, name="edit", brief="Edit Nogra's messages", description="Edit's Nogra's messages")
    @commands.is_owner()
    async def edit(self, ctx,messageid:int=None, channel:discord.TextChannel=None,*, newmessage=None):
        if messageid is None:
            await ctx.send("You didn't give me a Message ID to edit.")
        elif channel is None:
            await ctx.send("You didn't give me a Channel where the message originated from.")
        elif newmessage is None:
            await ctx.send("You need to give me some message to edit bruh")
        else:
            message = await channel.fetch_message(messageid)
            if message.author.id == 800184970298785802:
                if ctx.author.id == 650647680837484556:
                    await message.edit(content=newmessage)
                    await ctx.message.add_reaction("<a:Tick:796984073603383296>")

                else:
                    await ctx.send("Only the bot owner (<@650647680837484556>) is allowed to edit Nogra's messages.")
            else:
                await ctx.send("That message was not sent by me, I can't edit it.")

    @commands.command(name="eval", aliases=["exec"])
    @commands.is_owner()
    async def _eval(self,ctx,*,code):

        local_variables = {
            "discord": discord,
            "commands": commands,
            "bot": self.client,
            "ctx": ctx,
            "channel": ctx.channel,
            "author": ctx.author,
            "guild": ctx.guild,
            "message": ctx.message
        }

        stdout = io.StringIO()

        try:
            with contextlib.redirect_stdout(stdout):
                exec(
                    f"async def func():\n{textwrap.indent(code, '    ')}", local_variables
                )

                obj = await local_variables["func"]()
                result = f"{stdout.getvalue()}\n-- {obj}\n"
        except Exception as e:
            result = "".join(traceback.format_exception(e, e, e.__traceback__))

        pager = Pag(
            timeout=100,
            use_defaults=True,
            entries=[result[i : i + 2000] for i in range(0, len(result), 2000)],
            length=1,
            prefix="```py\n",
            suffix="```"
        )

        await pager.start(ctx)
    '''@commands.command(pass_context=True)
    async def dm(self, ctx, *, message):'''

    @edit.error
    async def edit_error(self, ctx, error):
        await ctx.send(f"```diff\n- Error encountered!\n# erorr:\n+ {error}```")

    @commands.command(name="setstatus", brief="Edit Nogra's status", description="Edit's Nogra's (presence) status")
    async def setstatus(self, ctx, ooommmaaa=None, presence=None, *, statuswhat=None):
        if ctx.author.id != 650647680837484556:
            await ctx.send("You can only change the status of the bot if you are Argon!")
            return
        allstatus = ['online', 'idle', 'dnd']
        if ooommmaaa in allstatus:
            if ooommmaaa == 'dnd':
                omam = discord.Status.dnd
            elif ooommmaaa == 'idle':
                omam = discord.Status.idle
            elif ooommmaaa == 'online':
                omam = discord.Status.online
            if presence == "game":
                # Setting `Playing ` status
                await self.client.change_presence(activity=discord.Game(name=statuswhat), status=omam)
                await ctx.send(
                    "I have set my status to **playing " + statuswhat + "** while being " + ooommmaaa)
            elif presence == "stream":
                # Setting `Streaming ` status
                await ctx.send("Argon use this command when you have a twitch stream url ready")
                # await bot.change_presence(activity=discord.Streaming(name="My Stream", url=my_twitch_url))
            elif presence == "listen":
                # Setting `Listening ` status
                await self.client.change_presence(
                    activity=discord.Activity(type=discord.ActivityType.listening, name=statuswhat),
                    status=omam)
                await ctx.send(
                    "I have set my status to **listening to " + statuswhat + "** while being " + ooommmaaa)
            elif presence == "watch":
                # Setting `Watching ` status
                await self.client.change_presence(
                    activity=discord.Activity(type=discord.ActivityType.watching, name=statuswhat),
                    status=omam)
                await ctx.send(
                    "I have set my status to **watching " + statuswhat + "** while being " + ooommmaaa)
            else:
                await ctx.send("you can only use `game`, `stream`, `listen`, and `watch` stupid.")
        else:
            await ctx.send("You can only use `online`, `idle`, or `dnd` stupid.")

    @setstatus.error
    async def setstatus_error(ctx, error):
        await ctx.send(f"```diff\n- Error encountered!\n# erorr:\n+ {error}```")

    @commands.command()
    async def rmtag(self, ctx, website):
        if ctx.author.id != 650647680837484556:
            await ctx.send("You can only use this command if you are Argon!")
        await ctx.send("Installing dependencies Google/chrome...")
        message = await ctx.send("10% installed")
        await message.edit("30% installed")
        asyncio.sleep(1)
        await message.edit("50% installed")
        asyncio.sleep(1)
        await message.edit("70% installed")
        asyncio.sleep(1)
        await message.edit("99% installed")
        asyncio.sleep(1)
        await message.edit("Chrome Version 1.22.71 Chromium: 89.0.4389.114 (Official Build) (64-bit) installed")
        await ctx.send(f"Launching process with command `{website} --chrome`")
        await ctx.send("Requires authentication in" + website)
        await ctx.send("Parsing for login data...")
        await ctx.send("650647680837484556 found, logging in with 650647680837484556...")
        await ctx.send("Logged in as Argon#0002")
        await ctx.send("Finding cancerous tags...")
        cancerous = ["bodoh", "argon"]
        for c in cancerous:
            await asyncio.sleep(2)
            await ctx.send(f"Tag `{c}` found, deleting `{c}`...")
            await asyncio.sleep(3)
            await ctx.send("Returned HTML 100 Code: Success")
            await ctx.send("Parsing for any cancerous tags...")
        await ctx.send("None found.")
        await ctx.send(f"Killing instance of `{website} --chrome")
        await ctx.send("Killed. No instance of `chrome` found")
        await ctx.send("Shutting down system...")

    @rmtag.error
    async def rmtag_error(ctx, error):
        await ctx.send(f"```diff\n- Error encountered!\n# erorr:\n+ {error}```")


def clean_code(content):
    if content.startswith("```") and content.endswith("```"):
        return "\n".join(content.split("\n")[1:][:-3])
    '''@_eval.error
    async def _eval_error(self, ctx, error):
        await ctx.send(f"```diff\n- Error encountered!\n# erorr:\n+ {error}```")'''

def setup(client):
    client.add_cog(Admin(client))
