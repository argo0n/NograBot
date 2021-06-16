from discord.utils import find
import random
import asyncio
import discord
import logging
from discord.ext import commands
import json
import os
import datetime
import time
from datetime import datetime as dt
from datetime import date
import nacl
from pytz import timezone
from discord.ext.buttons import Paginator
import postbin
import traceback

def gettraceback(error):
    etype = type(error)
    trace = error.__traceback__
    lines = traceback.format_exception(etype, error, trace)
    traceback_text = ''.join(lines)
    return traceback_text

blacklist = {"560251854399733760"}
intents = discord.Intents(messages=True, guilds=True)
intents.reactions = True
intents.members = True

statuses = ["a.help is a good start", "almond stanky", "before asking use the help command", "Spotify", "No.", "your pestering", "another reboot?"]

newstatus = random.choice(statuses)
client = commands.Bot(command_prefix='a.', status=discord.Status.dnd,
                      activity=discord.Activity(type=discord.ActivityType.listening, name=newstatus),
                      intents=intents)
INITIAL_EXTENSIONS = [
    'cogs.admin',
    'cogs.abuse',
    'cogs.afk',
    'cogs.apis',
    'cogs.dankmemer',
    'cogs.fun',
    'cogs.moderation',
    'cogs.rso',
    'cogs.utility'
]

class MyNewHelp(commands.MinimalHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()
        for page in self.paginator.pages:
            emby = discord.Embed(description=page)
            await destination.send(embed=emby)
    async def send_command_help(self, command):
        embed = discord.Embed(title=self.get_command_signature(command))
        embed.add_field(name="Help", value=command.description)
        alias = command.aliases
        if alias:
            embed.add_field(name="Aliases", value=", ".join(alias), inline=False)

        channel = self.get_destination()
        await channel.send(embed=embed)

client.help_command = MyNewHelp()


'''client.remove_command("help")'''

@client.event
async def on_ready():
    print('Successfully connected to Discord as {0.user}'.format(client))
    botready = discord.Embed(title="Bot is ready!", description="[Celebrate here](https://www.youtube.com/watch?v=dQw4w9WgXcQ)", color=0x32CD32)
    botready.set_author(name=f"{client.user.name}", icon_url=client.user.avatar_url,
                         url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    status = client.get_channel(839045672111308820)
    await status.send(embed=botready)


@client.event
async def on_command_error(ctx, error):
    pass

# This is for the bot to react to various situations

@client.event
async def on_guild_join(guild):
    print(f"I have joined {guild.name}")
    general = find(lambda x: 'general' in x.name,  guild.text_channels)
    print(f"general chat name: {general.name} | general chat mention: {general.mention}")
    if general and general.permissions_for(guild.me).send_messages:
        joinembed = discord.Embed(title="Thanks for using Nogra!",
                                 description="Nogra is a Discord bot with many different functions for your convenience and entertainment.",
                                 color=0x00ff00)
        joinembed.set_author(name=f"{client.user.name}", icon_url=str(client.user.avatar_url))
        joinembed.add_field(name="**__Not sure where to start?__**", value="\u200b", inline=False)
        joinembed.add_field(name="__Fun commands!__", value=f"{client.user.name} Has a wide range of commands that are fun to use. You can send a fake Dank Memer blacklist message to someone, or mute them by dumbfighting them! Use `a.help Fun` to see what commands can be used.<:thumbsupthefuck:823214448579838012>",inline=False)
        joinembed.add_field(name="__Moderation__", value="Not all moderation commands are written yet, but for now we have `ban` and `cban` (countdown ban). Use these commands to moderate your server! <a:nograban:803868903196852245>", inline=True)
        joinembed.add_field(name="__Dank Memer Help__", value=f"Do you use Dank Memer? {client.user.name} has a few utilities related to Dank Memer, such as lottery and rob reminders. <:peepoguns:796022792381661225>", inline=True)
        joinembed.add_field(name="\u200b",
                            value="By using Nogra, you agree to Nogra's [Terms of Service](http://nogra.infinityfreeapp.com/nogra-tos/) and [Privacy Policy](http://nogra.infinityfreeapp.com/nogras-privacy-policy/).",
                            inline=False)
        joinembed.set_footer(text=f"Do a.help as a start. Enjoy using {client.user.name}! If you run into problems or find a bug, DM Argon#0002. Make sure you have enabled the permissions necessary for Nogra to function properly.")
        joinembed.set_thumbnail(url=str(client.user.avatar_url))
        await general.send(embed=joinembed)

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.channel.id == 821042728849768478:
        await message.add_reaction("<:nogranostar:821675503316238360>")

    if "<@800184970298785802>" in message.content:
        MyNewHelp()


    # CHEONG MEET LINK
    if "cheong" in message.content or "Cheong" in message.content:
        cheongembed = discord.Embed(title="Meeting link for Google Meet freeloaders",
                                    description="Click [here](https://meet.google.com/shc-xgce-aix?authuser=1)",
                                    color=0x00ff00)
        cheongembed.set_image(
            url="https://media.discordapp.net/attachments/764151467115544576/765918704142647346/IMG-20200925-WA0037.jpg")
        cheongembed.set_footer(
            text="Cheong socializing with a cup of coke in a McDonalds outlet in Siglap link, colourised, 2019. Source:")
        await message.channel.send(embed=cheongembed)

    await client.process_commands(message)

@client.event
async def on_member_join(member):
    if member.guild.id == 789840820563476482:
        print("I detected someone joining the server.")

        await member.send("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
        await client.get_channel(789840820563476485).send(f"{member.mention} AAAAAA")
        print("I have sent a messagge to " + member.name + "#" + str(member.discriminator) + ".")

# Bot COMMANDS go here.

# clear (purge command)
@client.command(brief="Loads cogs", description = "Loads cogs")
@commands.is_owner()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')
    await ctx.send(f"`{extension}` loaded.")
    cogload = discord.Embed(title="Cog Loaded", description=f"`cogs.{extension}`", color=0x00ff00)
    cogload.set_author(name=f"{ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar_url, url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    status = client.get_channel(839045672111308820)
    await status.send(embed=cogload)

@client.command(brief="Unloads cogs", description = "Unloads cogs")
@commands.is_owner()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    await ctx.send(f"`{extension}` unloaded.")
    cogunload = discord.Embed(title="Cog Unloaded", description=f"`cogs.{extension}`", color=0xff0000)
    cogunload.set_author(name=f"{ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar_url, url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    status = client.get_channel(839045672111308820)
    await status.send(embed=cogunload)

@client.command(brief="Reboots a cog", description = "Reboots a cog", aliases= ["cr"])
@commands.is_owner()
async def cogreboot(ctx, extension):
    message = await ctx.send(f"<:nograred:830765450412425236> Rebooting `{extension}`:")
    client.unload_extension(f'cogs.{extension}')
    await message.edit(content=f"<:nograoffline:830765506792259614> `{extension}` unloaded.")
    await message.edit(content=f"<:nograyellow:830765423112880148> Restarting `{extension}`...")
    client.load_extension(f'cogs.{extension}')
    await message.edit(content=f"<:nograonline:830765387422892033> `{extension}` loaded successfully.")
    rebootcog = discord.Embed(title="Cog Rebooted", description=f"`cogs.{extension}`", color=0xffff00)
    rebootcog.set_author(name=f"{ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar_url, url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    status = client.get_channel(839045672111308820)
    await status.send(embed=rebootcog)

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')
@load.error
async def load_error(ctx, error):
    if isinstance(error, commands.CommandInvokeError):
        error = error.original
    if isinstance(error, discord.ext.commands.CheckFailure):
        await ctx.send("You're not the owner of Nogra!")
        return
    if isinstance(error, discord.ext.commands.ExtensionError):
        await ctx.send("That cog was not found.")
        return
    else:
        errorembed = discord.Embed(title="Oops!",
                                   description="This command just received an error. It has been sent to Argon.",
                                   color=0x00ff00)
        errorembed.add_field(name="Error", value=f"```{error}```", inline=False)
        errorembed.set_thumbnail(url="https://cdn.discordapp.com/emojis/834753936023224360.gif?v=1")
        await ctx.send(embed=errorembed)
        logchannel = client.get_channel(839016255733497917)
        await logchannel.send(
            f"In {ctx.guild.name}, a command was executed by {ctx.author.mention}: `{ctx.message.content}`, which received an error: `{error}`\nMore details:")
        message = await logchannel.send("Uploading traceback to Hastebin...")
        tracebacklink = await postbin.postAsync(gettraceback(error))
        await message.edit(content=tracebacklink)


@unload.error
async def unload(ctx, error):
    if isinstance(error, commands.CommandInvokeError):
        error = error.original
    if isinstance(error, discord.ext.commands.CheckFailure):
        await ctx.send("You're not the owner of Nogra!")
        return
    if isinstance(error, discord.ext.commands.ExtensionError):
        await ctx.send("That cog was not found.")
        return
    if "not been loaded" in error:
        await ctx.send("The cog is either already unloaded or not found.")
    else:
        errorembed = discord.Embed(title="Oops!",
                                   description="This command just received an error. It has been sent to Argon.",
                                   color=0x00ff00)
        errorembed.add_field(name="Error", value=f"```{error}```", inline=False)
        errorembed.set_thumbnail(url="https://cdn.discordapp.com/emojis/834753936023224360.gif?v=1")
        await ctx.send(embed=errorembed)
        logchannel = client.get_channel(839016255733497917)
        await logchannel.send(
            f"In {ctx.guild.name}, a command was executed by {ctx.author.mention}: `{ctx.message.content}`, which received an error: `{error}`\nMore details:")
        message = await logchannel.send("Uploading traceback to Hastebin...")
        tracebacklink = await postbin.postAsync(gettraceback(error))
        await message.edit(content=tracebacklink)


@cogreboot.error
async def cogreboot(ctx, error):
    if isinstance(error, commands.CommandInvokeError):
        error = error.original
    if isinstance(error, discord.ext.commands.CheckFailure):
        await ctx.send("You're not the owner of Nogra!")
        return
    if isinstance(error, discord.ext.commands.ExtensionError):
        await ctx.send("That cog was not found.")
        return
    errorembed = discord.Embed(title="Oops!",
                               description="This command just received an error. It has been sent to Argon.",
                               color=0x00ff00)
    errorembed.add_field(name="Error", value=f"```{error}```", inline=False)
    errorembed.set_thumbnail(url="https://cdn.discordapp.com/emojis/834753936023224360.gif?v=1")
    await ctx.send(embed=errorembed)
    logchannel = client.get_channel(839016255733497917)
    await logchannel.send(
        f"In {ctx.guild.name}, a command was executed by {ctx.author.mention}: `{ctx.message.content}`, which received an error: `{error}`\nMore details:")
    message = await logchannel.send("Uploading traceback to Hastebin...")
    tracebacklink = await postbin.postAsync(gettraceback(error))
    await message.edit(content=tracebacklink)

client.run(os.environ['NOGRAtoken'])
# betargon's ID was reset btw


