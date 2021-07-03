# |------------------------------------------------------------------------------------|
# |                                                                                    |
# |                                                                                    |
# |                              Admin Cog for Nogra Bot                               |
# |                               Written by Argon#0002                                |
# |                               Commands in this cog:                                |
# |                edit, eval, setstatus, rmtag, dmads, update, reboot                 |
# |                                                                                    |
# |                                                                                    |
# |------------------------------------------------------------------------------------
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
import postbin
import random
import json
from cogs.nograhelpers import *

def gettraceback(error):
    etype = type(error)
    trace = error.__traceback__
    lines = traceback.format_exception(etype, error, trace)
    traceback_text = ''.join(lines)
    return traceback_text

class Pag(Paginator):
    async def teardown(self):
        try:
            await self.page.clear_reactions()
        except discord.HTTPException:
            pass

class Admin(commands.Cog):
    def __init__(self, client):
        self.client = client

    @staticmethod
    def cleanup_code(content):
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
    async def evalu(self,ctx,*,code):

        local_variables = {
            "discord": discord,
            "commands": commands,
            "client": self.client,
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
                await self.client.change_presence(
                    activity=discord.Streaming(name=statuswhat, url="https://www.twitch.tv/nograbot", platform="Twitch",
                                               game="Among Us"))
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

    @commands.command()
    async def minecraft(self, ctx, *, member: discord.User = None):
        if member is None:
            await ctx.send("Aren't you supposed to mention someone?")
        else:
            if ctx.author.id == 650647680837484556:
                channel = self.client.get_channel(840073277715644419)
                invitelink = await channel.create_invite(
                    reason=f"Temporary invite created for {member.name}#{member.discriminator} requested by {ctx.author.name}#{ctx.author.discriminator}",
                    max_age=1800, max_uses=1, unique=True)
                channel2 = self.client.get_channel(840076120463900716)
                invitelink2 = await channel2.create_invite(
                    reason=f"Temporary invite created for {member.name}#{member.discriminator} requested by {ctx.author.name}#{ctx.author.discriminator}",
                    max_age=1800, max_uses=1, unique=True)
                channel3 = self.client.get_channel(840076340450558015)
                invitelink3 = await channel3.create_invite(
                    reason=f"Temporary invite created for {member.name}#{member.discriminator} requested by {ctx.author.name}#{ctx.author.discriminator}",
                    max_age=1800, max_uses=1, unique=True)
                channel4 = self.client.get_channel(840076417077215245)
                invitelink4 = await channel4.create_invite(
                    reason=f"Temporary invite created for {member.name}#{member.discriminator} requested by {ctx.author.name}#{ctx.author.discriminator}",
                    max_age=1800, max_uses=1, unique=True)
                messagetousers = f"**__MINECRAFT__**\n{invitelink}\n{invitelink2}\n{invitelink3}\n{invitelink4}\n\n All these invites will expire in 30 minutes, and is only for one use."
                await member.send(messagetousers)
                await ctx.message.add_reaction("<a:Tick:796984073603383296>")
            else:
                await ctx.send("No dmads for you <:nograsweg:818474291757580328>")

    @commands.command(name="message", brief="dms people",
                      description="Sends a message to someone requested by the developers.")
    @commands.is_owner()
    async def message(self, ctx, member=None):
        if member is None:
            await ctx.send("Mention someone you idiot")
            return
        member = int(member)
        member = self.client.get_user(member)
        if member.bot:
            await ctx.send("I can't DM bots.")
            return
        if member is None:
            await ctx.send("I could not find that member.")
            return
        await ctx.send("Type your message now.")
        try:
            msg = await self.client.wait_for("message",
                                             check=lambda m: m.channel == ctx.channel and m.author == ctx.author,
                                             timeout=120.0)
        except asyncio.TimeoutError:
            await ctx.send("Could not detect a message for the span of 2 minutes. Try again please.")
            return
        dmembed = discord.Embed(title="You received a message from the developer!", description=msg.content,
                                color=discord.Color.random())
        try:
            await member.send(embed=dmembed)
        except discord.errors.Forbidden:
            await ctx.send(f"{member.name}#{member.discriminator} has his DMs closed / blocked me.")
        else:
            await ctx.send("Message successfully sent <a:Tick:796984073603383296>")

    @commands.command()
    async def dmads(self, ctx, member: discord.User = None):
        if member is None:
            await ctx.send("Aren't you supposed to mention someone?")
        else:
            if ctx.author.id == 650647680837484556:
                channel = self.client.get_channel(810426819995893780)
                invitelink = await channel.create_invite(
                    reason=f"Temporary invite created for {member.name}#{member.discriminator} requested by {ctx.author.name}#{ctx.author.discriminator}",
                    max_age=1800, max_uses=1, unique=True)
                channel2 = self.client.get_channel(813288124460826667)
                invitelink2 = await channel2.create_invite(
                    reason=f"Temporary invite created for {member.name}#{member.discriminator} requested by {ctx.author.name}#{ctx.author.discriminator}",
                    max_age=1800, max_uses=1, unique=True)
                channel3 = self.client.get_channel(802544393122742312)
                invitelink3 = await channel3.create_invite(
                    reason=f"Temporary invite created for {member.name}#{member.discriminator} requested by {ctx.author.name}#{ctx.author.discriminator}",
                    max_age=1800, max_uses=1, unique=True)
                channel4 = self.client.get_channel(810007699579338762)
                invitelink4 = await channel4.create_invite(
                    reason=f"Temporary invite created for {member.name}#{member.discriminator} requested by {ctx.author.name}#{ctx.author.discriminator}",
                    max_age=1800, max_uses=1, unique=True)
                channel5 = self.client.get_channel(818436261891014659)
                invitelink5 = await channel5.create_invite(
                    reason=f"Temporary invite created for {member.name}#{member.discriminator} requested by {ctx.author.name}#{ctx.author.discriminator}",
                    max_age=1800, max_uses=1, unique=True)
                messagetousers = f"Either you asked Argon for the emoji server invites, or Argon decided to invite you anyways. \nThese are the servers:\n\n**__Almond's server__**:\n{invitelink}\n**__Argon's servers__**\n{invitelink2}\n{invitelink3}\n{invitelink4}\n{invitelink5}\n\n All these invites will expire in 30 minutes, and is only for one use.\nhave fun! <:nograblushsuit:831001647005564970>"
                await member.send(messagetousers)
                await ctx.message.add_reaction("<a:Tick:796984073603383296>")
            else:
                await ctx.send("No dmads for you <:nograsweg:818474291757580328>")

    @commands.command(brief="command to send a update message to various channels", description="command to send a update message to various channels")
    @commands.is_owner()
    async def update(self, ctx, *, message):
        await ctx.message.delete()
        channelids = [832081865749430285, 789840820563476485, 822112906014490634, 818436261891014660]
        for i in channelids:
            channel = self.client.get_channel(i)
            await channel.send(message)
    
    @commands.command()
    @commands.is_owner()
    async def shutdown(self, ctx):
        message = await ctx.send("<:nograred:830765450412425236> Logging off bot account and shutting down ")
        await asyncio.sleep(2)
        await message.edit(content="<:nograoffline:830765506792259614> Nogra is offline, manually reboot it.")
        await self.client.logout()

    async def cog_command_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.CheckFailure):
            await ctx.send("You're not the owner of Nogra!")
            return
        else:
            fulltraceback = gettraceback(error)
            errorembed = discord.Embed(title="Error encountered on an Admin Command.",
                                       description=f"```py\n{fulltraceback[0, 1024]}\n```",
                                       color=0x00ff00)
            errorembed.set_thumbnail(url="https://cdn.discordapp.com/emojis/834753936023224360.gif?v=1")
            await ctx.send(embed=errorembed)

def clean_code(content):
    if content.startswith("```") and content.endswith("```"):
        return "\n".join(content.split("\n")[1:][:-3])


def setup(client):
    client.add_cog(Admin(client))
