from discord.utils import find
import random
import asyncio
import discord
import logging
from discord.ext import commands
import json
import os
import datetime, time
from datetime import datetime as dt
from datetime import date
import nacl
from pytz import timezone
from discord.ext.buttons import Paginator
import postbin, traceback

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
    await client.get_channel(816249246129979392).send("<@650647680837484556> Nogra has come online/just rebooted.")


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
        joinembed = discord.Embed(title="Thanks for inviting me!",
                                 description="This is a Python bot, expect bugs to occur when using me.",
                                 color=0x00ff00)
        joinembed.set_author(name=f"{client.user.name}", icon_url=str(client.user.avatar_url))
        joinembed.add_field(name="**__Pre-use Configuration__**", value="\u200b", inline=False)
        joinembed.add_field(name="__Admin role commands__", value=f"{client.user.name} has a command which can be used to add the Admin role to users easily. To use that in this guild, make sure the role is named \"admin\" and that it is below Nogra's highest role.",inline=False)
        joinembed.add_field(name="__Emoji Utilities__", value=f"Give {client.user.name} the permission to see and manage emojis so that {client.user.name} can show them in its respective emoji commands.", inline=True)
        joinembed.add_field(name=f"__{client.user.name}'s permissions__", value=f"If you invited Nogra with the necessary permissions link, you will not need to worry if {client.user.name} ever gets exploited.", inline=True)
        joinembed.set_footer(text=f"Do a.help as a start. Enjoy using {client.user.name}! If you run into problems or find a bug, DM Argon#0002.")
        joinembed.set_thumbnail(url=str(client.user.avatar_url))
        try:
            await general.send(embed=joinembed)
        except discord.HTTPException:
            message = f"Thanks for inviting me!\nThis is a Python bot, expect bugs to occur when using me.\n\n**__Pre-use Configuration__**\n\n__Admin role commands__\n    • {client.user.name} has a command which can be used to add the Admin role to users easily. To use that in this guild, make sure the role is named \"admin\" and that it is below Nogra's highest role.\n__Emoji Utilities\n    • Give {client.user.name} the permission to see and manage emojis so that {client.user.name} can show them in its respective emoji commands.\n__{client.user.name}'s permissions__\n    • If you invited Nogra with the necessary permissions link, you will not need to worry if {client.user.name} ever gets exploited.\n\nDo a.help as a start. Enjoy using {client.user.name}! If you run into problems or find a bug, DM Argon#0002.\n\n- Nogra"
            await general.send(message)

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
        server = member.guild
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
    cogload = discord.Embed(title=f"Cog Loaded",description=f"`cogs.{extension}`",color=0x00ff00)
    cogload.set_author(name=f"{ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar_url, url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    status = client.get_channel(839045672111308820)
    await status.send(embed=cogload)
    logchannel = client.get_channel(839016255733497917)

@client.command(brief="Unloads cogs", description = "Unloads cogs")
@commands.is_owner()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    await ctx.send(f"`{extension}` unloaded.")
    cogunload = discord.Embed(title=f"Cog Unloaded",description=f"`cogs.{extension}`",color=0xff0000)
    cogunload.set_author(name=f"{ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar_url, url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    status = client.get_channel(839045672111308820)
    await status.send(embed=cogunload)
    logchannel = client.get_channel(839016255733497917)

@client.command(brief="Reboots a cog", description = "Reboots a cog", aliases= ["cr"])
@commands.is_owner()
async def cogreboot(ctx, extension):
    message = await ctx.send(f"<:nograred:830765450412425236> Rebooting `{extension}`:")
    client.unload_extension(f'cogs.{extension}')
    await message.edit(content=f"<:nograoffline:830765506792259614> `{extension}` unloaded.")
    await message.edit(content=f"<:nograyellow:830765423112880148> Restarting `{extension}`...")
    client.load_extension(f'cogs.{extension}')
    await message.edit(content=f"<:nograonline:830765387422892033> `{extension}` loaded successfully.")
    await ctx.send(f"`{extension}` unloaded.")
    rebootcog = discord.Embed(title=f"Cog Rebooted",description=f"`cogs.{extension}`",color=0xffff00)
    rebootcog.set_author(name=f"{ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar_url, url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    status = client.get_channel(839045672111308820)
    await status.send(embed=rebootcog)
    logchannel = client.get_channel(839016255733497917)

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')
@load.error
async def load_error(ctx, error):
    if "not be loaded" in error:
        await ctx.send(f"The cog is either already loaded or not found.")
    else:
        errorembed = discord.Embed(title=f"Oops!",
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
    if "not been loaded" in error:
        await ctx.send(f"The cog is either already unloaded or not found.")
    else:
        errorembed = discord.Embed(title=f"Oops!",
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
async def cogreboot(ctx,error):
    errorembed = discord.Embed(title=f"Oops!",
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


