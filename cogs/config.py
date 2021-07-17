# |------------------------------------------------------------------------------------|
# |                                                                                    |
# |                                                                                    |
# |                          Configuration Cog for Nogra Bot                           |
# |                               Written by Argon#0002                                |
# |                               Commands in this cog:                                |
# |                clear, uptime, invite, abuse, stopabusing, ban, cban                |
# |                                                                                    |
# |                                                                                    |
# |------------------------------------------------------------------------------------
from discord.ext import commands, tasks
import sqlite3
import discord
import datetime
import time
from discord.ext.commands.errors import RoleNotFound
import pytz
import traceback
from pytz import timezone
import asyncio
import postbin
import traceback
import json
import random
from cogs.nograhelpers import *
import os
from typing import Union



def get_prefix(client, message):
    with open('nograresources/prefixes.json', 'r') as f:
        prefixes = json.load(f)
        guildprefixes = prefixes[str(message.guild.id)]
    return commands.when_mentioned_or(guildprefixes)(client, message)


def gettraceback(error):
    etype = type(error)
    trace = error.__traceback__
    lines = traceback.format_exception(etype, error, trace)
    return ''.join(lines)


timeformat = "%Y-%m-%d %H:%M:%S"
durationformat = "%-dd %-Hh %-Mm %-Ss"


def timetosgtime(x):
    utctime = x
    sgttime = utctime.astimezone(timezone("Asia/Singapore"))
    return sgttime.strftime(timeformat)

start_time = time.time()
utcbootime = datetime.datetime.now(timezone("UTC"))

class Config(commands.Cog):

    def __init__(self, client):
        self.description = "🛡️ Keep your server safe and healthy."
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        db = sqlite3.connect('databases/commandsettings.sqlite')
        cursor = db.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS enable(guild_id integer, command text, limit_type text, id integer)")
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS disable(guild_id integer, command text, limit_type text, id integer)")
        print("Cog \"Config\" loaded")

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.BadUnionArgument):
            await ctx.send(f"{error} Only text channels, members, or roles are accepted.")
            return
        if isinstance(error, commands.ChannelNotFound):
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
            await ctx.send(f"{error}\nIt has to be a mention or user ID.")
        if isinstance(error, commands.RoleNotFound):
            await ctx.send(
                f"{error}\nIt has to be a mention, role ID or role name. If you did state the role name, try adding `\"` around the role name.")
            return
        if isinstance(error, commands.CommandInvokeError):
            error = error.original
        if isinstance(error, ValueError):
            await ctx.send(
                "I expected a number somwhere in your command, but I got something else instead. Check if the numbers I require are just integers.")
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
        pass

    @commands.group(invoke_without_command=True, name="enable", brief = "emable a command", description = "Enable a command which was previously disabled. Use this command without any other words to see how to use it.", aliases = ["allow"])
    async def enable(self, ctx):
        print("HI")

    @enable.command(name="list", brief="Shows enabled commands rule on this server.", description="Shows enabled commands rule on this server.")
    @commands.has_permissions(administrator = True)
    async def list(self, ctx):
        db = sqlite3.connect('databases/commandsettings.sqlite')
        cursor = db.cursor()
        result = cursor.execute("SELECT * FROM enable WHERE guild_id = ?", (ctx.guild.id,)).fetchall()
        if len(result) == 0:
            content = "There are no enabled rules here!"
        else:
            rules = []
            count = 1
            for rule in result:
                rules.append(f"{count}. {rule}")
                count += 1
        await ctx.send("\n".join(rules))

    @enable.command(name="remove", brief="Remove an enabled rule.", description="Remove an enabled rule by specifying the rule number..")
    @commands.has_permissions(administrator = True)
    async def remove(self, ctx, ruleno = None):
        db = sqlite3.connect('databases/commandsettings.sqlite')
        cursor = db.cursor()
        result = cursor.execute("SELECT * FROM enable WHERE guild_id = ?", (ctx.guild.id,)).fetchall()
        if len(result) < 1:
            await ctx.send("There are no rules to be removed!")
            return
        if ruleno is None:
            await ctx.send("You need to specify which rule to be removed.")
            return
        if int(ruleno) < 1:
            await ctx.send("You need to specify which rule to be removed.")
            return
        ruleno = int(ruleno) - 1
        deleteentry = result[ruleno]
        print(deleteentry)
        if "member" in deleteentry[2]:
            member = ctx.guild.get_member(deleteentry[3])
            target = "unknown member" if member is None else f"{member.name}#{member.discriminator}"
            print(target)
        elif "channel" in deleteentry[2]:
            channel = self.client.get_channel(deleteentry[3])
            target = "unknown or deleted channel"if channel is None else f"{channel.name}#{channel.disciminator}"
        elif "role" in deleteentry[2]:
            role = ctx.guild.get_role(deleteentry[3])
            target = "unknown or deleted role" if role is None else f"{role.name}"
        elif "all" in deleteentry[2]:
            target = "everyone"
        else:
            await ctx.send("There was en error in parsing the database to remove the rule. Please contact Argon#0002 and let him know about this error.\nERROR CODE:`NO_PROPERTYPE_TARGET`")
            return
        await ctx.send(f"Are you sure you want to remove the enabled command **{deleteentry[1]}** for **{target}**? `[y/n]`")
        db = sqlite3.connect('databases/commandsettings.sqlite')
        cursor = db.cursor()
        result = cursor.execute("SELECT * FROM enable WHERE guild_id = ?", (ctx.guild.id,)).fetchall()
        try:
            yn = await self.client.wait_for("message",
                                            check=lambda m: m.channel == ctx.channel and m.author == ctx.author,
                                            timeout=20.0)
        except asyncio.TimeoutError:
            await ctx.send("Since you took too long to respond, the rule will not be removed.")
            return
        if yn.content.lower() in ["y", "yes"]:
            cursor.execute("DELETE FROM enable WHERE guild_id = ? and command = ? and limit_type = ? and id = ?", (deleteentry[0], deleteentry[1], deleteentry[2], deleteentry[3])).fetchall()
            db.commit()
            cursor.close()
            db.close()
            await ctx.send(f"Rule {ruleno+1} has been removed.")
        else:
            await ctx.send("Aborting this operation.")
            cursor.close()
            db.close()
        

    @enable.command(name="add", brief="Add a rule for a command to be enabled", description="Add a rule for a command to be enabled")
    @commands.has_permissions(administrator = True)
    async def add(self, ctx, commandname = None, enableparty: Union[discord.Member, discord.Role, discord.TextChannel, str] = None):
        if commandname is None or enableparty is None:
            await ctx.send("You missed out one or more required arguments. This is the proper usage: `enable <command> <disabledparty>`")
            return
        command = self.client.get_command(commandname)
        if commandname.lower() == "all":
            command = "all"
        elif type(command) is None:
            await ctx.send(f"`{commandname}` is not a proper command.")
            return
        db = sqlite3.connect('databases/commandsettings.sqlite')
        if isinstance(enableparty, discord.Member):
            limittype = "member"
        if isinstance(enableparty, discord.Role):
            limittype = "role"
        if isinstance(enableparty, discord.TextChannel):
            limittype = "channel"
        if "all" in enableparty or str(ctx.guild.default_role) in ctx.message.content or "everyone" in enableparty:
            limittype = "all"
        else:
            await ctx.send(f"You can only choose {commandname} to be enabled for a **member, role, channel or everyone.**")
            return
        #limittype = str(type(enableparty))
        print(limittype, type(limittype))
        cursor = db.cursor()
        if limittype in ["member", "role", "channel"]:
            result = cursor.execute("SELECT * FROM enable WHERE guild_id = ? and command = ? and limit_type = ? and id = ?", (ctx.guild.id,command.name, limittype, enableparty.id)).fetchall()
            if len(result) >= 1:
                await ctx.send("There is already a rule for the same requirement.")
                return
            sql = "INSERT INTO enable(guild_id , command, limit_type, id) VALUES(?,?,?,?)"
            val = (ctx.guild.id, command.name, limittype, enableparty.id)
            cursor.execute(sql, val)
            print(limittype)
            print(limittype[2:])
            await ctx.send(f"The command `{command}` has been enabled for the {limittype} **{enableparty.name}**.")
        else:
            result = cursor.execute("SELECT * FROM enable WHERE guild_id = ? and command = ? and limit_type = ? and id = ?", (ctx.guild.id,command.name, limittype, enableparty)).fetchall()
            if len(result) >= 1:
                await ctx.send("There is already a rule for the same requirement.")
                return
            sql = "INSERT INTO enable(guild_id , command, limit_type, id) VALUES(?,?,?,?)"
            val = (ctx.guild.id, command.name, limittype, enableparty)
            cursor.execute(sql, val)
            print(limittype)
            print(limittype[2:])
            await ctx.send(f"The command `{command}` has been enabled for **everyone**.")
        db.commit()
        cursor.close()
        db.close()

    @commands.group(invoke_without_command=True, name="disable", brief = "emable a command", description = "Disable a command. Use this command without any other words to see how to use it.")
    async def disable(self, ctx):
        print("HI")

    @disable.command(name="list", brief="Shows disabled commands rules on this server.", description="Shows disabled commands rules on this server.")
    @commands.has_permissions(administrator = True)
    async def list(self, ctx):
        db = sqlite3.connect('databases/commandsettings.sqlite')
        cursor = db.cursor()
        result = cursor.execute("SELECT * FROM disable WHERE guild_id = ?", (ctx.guild.id,)).fetchall()
        rules = []
        count = 1
        for rule in result:
            rules.append(f"{count}. {rule}")
            count += 1
        await ctx.send("\n".join(rules))

    @disable.command(name="remove", brief="Remove an disabled rule.", description="Remove an disabled rule by specifying the rule number.")
    @commands.has_permissions(administrator = True)
    async def remove(self, ctx, ruleno = None):
        db = sqlite3.connect('databases/commandsettings.sqlite')
        cursor = db.cursor()
        result = cursor.execute("SELECT * FROM disable WHERE guild_id = ?", (ctx.guild.id,)).fetchall()
        if len(result) < 1:
            await ctx.send("There are no rules to be removed!")
            return
        if ruleno is None:
            await ctx.send("You need to specify which rule to be removed.")
            return
        if int(ruleno) < 1:
            await ctx.send("You need to specify which rule to be removed.")
            return
        ruleno = int(ruleno) - 1
        deleteentry = result[ruleno]
        print(deleteentry)
        if "member" in deleteentry[2]:
            member = ctx.guild.get_member(deleteentry[3])
            target = "unknown member" if member is None else f"{member.name}#{member.discriminator}"
            print(target)
        elif "channel" in deleteentry[2]:
            channel = self.client.get_channel(deleteentry[3])
            target = "unknown or deleted channel"if channel is None else f"{channel.name}#{channel.disciminator}"
        elif "role" in deleteentry[2]:
            role = ctx.guild.get_role(deleteentry[3])
            target = "unknown or deleted role" if role is None else f"{role.name}"
        elif "all" in deleteentry[2]:
            target = "everyone"
        else:
            await ctx.send("There was en error in parsing the database to remove the rule. Please contact Argon#0002 and let him know about this error.\nERROR CODE:`NO_PROPERTYPE_TARGET`")
            return
        await ctx.send(f"Are you sure you want to remove the disabled command **{deleteentry[1]}** for **{target}**? `[y/n]`")
        db = sqlite3.connect('databases/commandsettings.sqlite')
        cursor = db.cursor()
        result = cursor.execute("SELECT * FROM disable WHERE guild_id = ?", (ctx.guild.id,)).fetchall()
        try:
            yn = await self.client.wait_for("message",
                                            check=lambda m: m.channel == ctx.channel and m.author == ctx.author,
                                            timeout=20.0)
        except asyncio.TimeoutError:
            await ctx.send("Since you took too long to respond, the rule will not be removed.")
            return
        if yn.content.lower() in ["y", "yes"]:
            cursor.execute("DELETE FROM disable WHERE guild_id = ? and command = ? and limit_type = ? and id = ?", (deleteentry[0], deleteentry[1], deleteentry[2], deleteentry[3])).fetchall()
            db.commit()
            cursor.close()
            db.close()
            await ctx.send(f"Rule {ruleno+1} has been removed.")
        else:
            await ctx.send("Aborting this operation.")
            cursor.close()
            db.close()
        

    @disable.command(name="add", brief="Add a rule for a command to be disabled", description="Add a rule for a command to be disabled")
    @commands.has_permissions(administrator = True)
    async def add(self, ctx, commandname = None, disableparty: Union[discord.Member, discord.Role, discord.TextChannel, str] = None):
        if commandname is None or disableparty is None:
            await ctx.send("You missed out one or more required arguments. This is the proper usage: `disable <command> <disabledparty>`")
            return
        command = self.client.get_command(commandname)
        if commandname.lower() == "all":
            command = "all"
        elif type(command) is None:
            await ctx.send(f"`{commandname}` is not a proper command.")
            return
        db = sqlite3.connect('databases/commandsettings.sqlite')
        if isinstance(disableparty, discord.Member):
            limittype = "member"
        if isinstance(disableparty, discord.Role):
            limittype = "role"
        if isinstance(disableparty, discord.TextChannel):
            limittype = "channel"
        if "all" in disableparty or str(ctx.guild.default_role) in ctx.message.content or "everyone" in disableparty:
            limittype = "all"
        else:
            await ctx.send(f"You can only choose {commandname} to be disabled for a **member, role, channel or everyone.**")
            return
        #limittype = str(type(disableparty))
        print(limittype, type(limittype))
        cursor = db.cursor()
        if limittype in ["member", "role", "channel"]:
            result = cursor.execute("SELECT * FROM disable WHERE guild_id = ? and command = ? and limit_type = ? and id = ?", (ctx.guild.id,command.name, limittype, disableparty.id)).fetchall()
            if len(result) >= 1:
                await ctx.send("There is already a rule for the same requirement.")
                return
            sql = "INSERT INTO disable(guild_id , command, limit_type, id) VALUES(?,?,?,?)"
            val = (ctx.guild.id, command.name, limittype, disableparty.id)
            cursor.execute(sql, val)
            print(limittype)
            print(limittype[2:])
            await ctx.send(f"The command `{command}` has been disabled for the {limittype} **{disableparty.name}**.")
        else:
            result = cursor.execute("SELECT * FROM disable WHERE guild_id = ? and command = ? and limit_type = ? and id = ?", (ctx.guild.id,command.name, limittype, disableparty)).fetchall()
            if len(result) >= 1:
                await ctx.send("There is already a rule for the same requirement.")
                return
            sql = "INSERT INTO disable(guild_id , command, limit_type, id) VALUES(?,?,?,?)"
            val = (ctx.guild.id, command.name, limittype, disableparty)
            cursor.execute(sql, val)
            print(limittype)
            print(limittype[2:])
            await ctx.send(f"The command `{command}` has been disabled for **everyone**.")
        db.commit()
        cursor.close()
        db.close()



def setup(client):
    client.add_cog(Config(client))
