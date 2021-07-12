# |------------------------------------------------------------------------------------|
# |                                                                                    |
# |                                                                                    |
# |                               AFK Cog for Nogra Bot                                |
# |                               Written by Argon#0002                                |
# |                               Commands in this cog:                                |
# |                                        afk                                         |
# |                                                                                    |
# |                                                                                    |
# |------------------------------------------------------------------------------------
from discord.ext import commands
import discord
import datetime
import time
import pytz
from pytz import timezone
import asyncio
import json
import math
import postbin
import traceback
from cogs.nograhelpers import *
import sqlite3
import os


def gettraceback(error):
    etype = type(error)
    trace = error.__traceback__
    lines = traceback.format_exception(etype, error, trace)
    traceback_text = ''.join(lines)
    return traceback_text


start_time = time.time()

class Afk(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.description = "<:nograafk:862735866857652224> Tell people you're AFK"

    @commands.Cog.listener()
    async def on_ready(self):
        db = sqlite3.connect('databases/config.sqlite')
        cursor = db.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS afk(guild_id integer, member_id integer, time integer, message text)")
        print("Cog \"AFK\" loaded")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or message.author == self.client.user:
            return
        timenow = time.time()
        config = sqlite3.connect('databases/config.sqlite')
        cursor = config.cursor()
        result = cursor.execute('SELECT * FROM afk WHERE guild_id = ? and member_id = ? and time < ? ',
                                (message.guild.id, message.author.id, timenow,)).fetchall()
        print(len(result))
        if len(result) == 0:
            result = cursor.execute('SELECT * FROM afk WHERE guild_id = ? and time < ?',
                                    (message.guild.id, timenow,)).fetchall()
            if len(result) > 0:
                for afkdetail in result:
                    member = self.client.get_user(afkdetail[1])
                    if member.mentioned_in(message):
                        current_time = time.time()
                        afk_duration = int(round(current_time - afkdetail[3]))
                        afk_embed = discord.Embed(title="", color=0x00ff00)
                        afk_embed.set_author(name=f"{member.name}#{member.discriminator}",
                                             icon_url=str(member.avatar_url))
                        afk_embed.add_field(name=f"{member.name} is AFK", value=afkdetail[2], inline=True)
                        afk_embed.set_footer(text=f"{member.name} has been AFK for {secondstotiming(afk_duration)}.")
                        await message.channel.send(embed=afk_embed)
        else:
            result = result[0]
            if "[AFK] " in message.author.display_name:
                newname = message.author.display_name.replace("[AFK]", "")
                await message.author.edit(nick=newname)
            print(result)
            print(result[0])
            print(result[1])
            print(result[2])
            cursor.execute("DELETE FROM afk where guild_id = ? and member_id = ?", (result[0], result[1],))
            config.commit()
            await message.channel.send(f"Welcome back {message.author.mention}! I have removed your AFK status.")
        cursor.close()
        config.close()

    @commands.command(name="afkclear", brief="Removes afk status", description="Removes the AFK status of a member.")
    @commands.has_permissions(manage_messages=True)
    async def afkclear(self, ctx, member: discord.Member):
        await ctx.send(f"Are you sure you want to remove **{member.name}#{member.discriminator}**'s AFK status?")
        yn = await self.client.wait_for("message", check=lambda m: m.channel == ctx.channel and m.author == ctx.author,
                                        timeout=20.0)
        if yn.lower() in ["y", "yes"]:
            config = sqlite3.connect('databases/config.sqlite')
            cursor = config.cursor()
            cursor.execute("DELETE FROM afk where guild_id = ? and member_id = ?",
                           (ctx.guild.id, member.id,))
            config.commit()
            await ctx.send(f"AFK status for **{member.name}#{member.discriminator}** removed.")
            cursor.close()
            config.close()

    @commands.command(name="afk", brief="Let everyone know you are AFK",
                      description="Sets an AFK status which will tell others why you are AFK when you are pinged.")
    async def afk(self, ctx, *, message="I am AFK!"):
        config = sqlite3.connect('databases/config.sqlite')
        cursor = config.cursor()
        result = cursor.execute('SELECT * FROM afk WHERE guild_id = ? and member_id = ?',
                                (ctx.guild.id, ctx.author.id,)).fetchall()
        if len(result) > 0:
            await ctx.send(
                "You have already set an AFK status, wait until your AFK status is removed (30 seconds) to set a new AFK status.")
            return
        member = ctx.author
        if len(message) > 1024:
            await ctx.send("Your message for your AFK status is too long, try making it below 1024 characters.",
                           delete_after=5.0)
        if len(member.display_name) > 26:
            await ctx.send("Your nickname could not be changed because it exceeds nickname character limits.",
                           delete_after=3.0)
        else:
            try:
                await member.edit(nick=f"[AFK] {member.display_name}")
            except discord.Forbidden:
                await ctx.send("I do not have the permission to change your nickname.", delete_after=5.0)
        time_now = time.time()
        time_now = round(time_now) + 30
        async with ctx.typing():
            sql = "INSERT INTO afk(guild_id, member_id, time, message) VALUES(?,?,?,?)"
            val = (ctx.guild.id, ctx.author.id, time_now, message)
            cursor.execute(sql, val)
            config.commit()
            cursor.close()
            config.close()
        await ctx.send(f"{member.mention} You are now AFK. message: {message}")

    @afk.error
    async def afk_error(self, ctx, error):
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


def setup(client):
    client.add_cog(Afk(client))
