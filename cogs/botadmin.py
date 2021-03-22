from discord.ext import commands
import asyncio
import traceback
import discord
import inspect
import textwrap
import importlib
from contextlib import redirect_stdout
import io
import os
import re
import sys
import copy
import time
import subprocess
from typing import Union, Optional

# to expose to the eval command
import datetime
from collections import Counter

class Admin(commands.Cog):

    def __init__(self, client):
        self.client = client
        self._last_result = None
        self.sessions = set()

    '''@commands.Cog.listener()
    async def on_ready(self):
        print('Cog Admin loaded')'''

    @commands.command(pass_context=True)
    #@commands.is_owner()
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

    @commands.command(pass_context=True, hidden=True, name='eval')
    async def _eval(self, ctx, *, body: str):
        """Evaluates a code"""

        env = {
            'bot': self.client,
            'ctx': ctx,
            'channel': ctx.channel,
            'author': ctx.author,
            'guild': ctx.guild,
            'message': ctx.message,
            '_': self._last_result
        }

        env.update(globals())

        body = self.cleanup_code(body)
        stdout = io.StringIO()

        to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

        try:
            exec(to_compile, env)
        except Exception as e:
            return await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')

        func = env['func']
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception as e:
            value = stdout.getvalue()
            await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
        else:
            value = stdout.getvalue()
            try:
                await ctx.message.add_reaction('\u2705')
            except:
                pass

            if ret is None:
                if value:
                    await ctx.send(f'```py\n{value}\n```')
            else:
                self._last_result = ret
                await ctx.send(f'```py\n{value}{ret}\n```')

    @edit.error
    async def edit_error(self, ctx, error):
        await ctx.send(f"```diff\n- Error encountered!\n# erorr:\n+ {error}```")

    @_eval.error
    async def _eval_error(self, ctx, error):
        await ctx.send(f"```diff\n- Error encountered!\n# erorr:\n+ {error}```")

def setup(client):
    client.add_cog(Admin(client))
