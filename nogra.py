from discord.utils import find
import random
import discord
# import logging
from discord.ext import commands
import json
import os
import postbin
import traceback
from cogs.nograhelpers import *
import contextlib
import datetime


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


blacklist = {"560251854399733760"}
intents = discord.Intents(messages=True, guilds=True)
intents.presences = True
intents.reactions = True
intents.members = True

statuses = ["a.help is a good start", "almond stanky", "before asking use the help command", "Spotify", "No.",
            "your pestering", "another reboot?"]

newstatus = random.choice(statuses)
client = commands.Bot(command_prefix=get_prefix, status=discord.Status.dnd,
                      activity=discord.Activity(type=discord.ActivityType.listening, name=newstatus),
                      intents=intents, strip_after_prefix=True)

client._BotBase__cogs = commands.core._CaseInsensitiveDict()

INITIAL_EXTENSIONS = [
    'cogs.admin',
    'cogs.afk',
    'cogs.apis',
    'cogs.dankmemer',
    'cogs.fun',
    'cogs.moderation',
    'cogs.utility'
]
for extension in INITIAL_EXTENSIONS:
    try:
        client.load_extension(extension)
    except Exception as e:
        print('Failed to load extension {}\n{}: {}'.format(extension, type(e).__name__, e))


class HelpEmbed(discord.Embed):  # Our embed with some preset attributes to avoid setting it multiple times
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.timestamp = datetime.datetime.utcnow()
        text = f"Use help [category] to see the commands in a category and help [command] to see its syntax."
        self.set_footer(text=text)
        self.color = discord.Color.random()


class MyHelp(commands.HelpCommand):
    def __init__(self):
        super().__init__(  # create our class with some aliases and cooldown
            command_attrs={
                "help": "The help command for the bot",
                "aliases": ['commands']
            }
        )

    async def send(self, **kwargs):
        """a short cut to sending to get_destination"""
        await self.get_destination().send(**kwargs)

    async def send_bot_help(self, mapping):
        # foundation of help command
        ctx = self.context
        embed = HelpEmbed(title=f"{ctx.me.display_name}'s Help Page")
        embed.set_thumbnail(url=ctx.me.avatar_url)
        usable = 0
        for cog, commands in mapping.items():  # iterating through our mapping of cog: commands
            filtered_commands = await self.filter_commands(commands)
            if filtered_commands:
                # if no commands are usable in this category, we don't want to display it
                amount_commands = len(filtered_commands)
                usable += amount_commands
                if cog:  # getting attributes dependent on if a cog exists or not
                    name = cog.qualified_name
                    description = cog.description or "No description"
                    embed.add_field(name=f"{name} [{amount_commands}]", value=description)

        embed.description = f"Thank you for using {client.user.name}!"

        await self.send(embed=embed)

    async def on_help_command_error(self, ctx, error):
        if not isinstance(error, commands.BadArgument):
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
        embed = discord.Embed(title="Error", description=str(error))
        await ctx.send(embed=embed)

    async def send_command_help(self, command):
        signature = self.get_command_signature(command)
        embed = HelpEmbed(title=signature, description=command.description or "*Nothing to see here*")
        if command.cog:
            embed.add_field(name="Category", value=command.cog.qualified_name)
        if command._buckets and command._buckets._cooldown:
            cooldown = command._buckets._cooldown
            embed.add_field(
                name="Cooldown",
                value=f"{cooldown.rate} per {cooldown.per:.0f} seconds",
            )
        if command.aliases:
            embed.add_field(name="Aliases", value=", ".join(command.aliases), inline=False)
        if command.checks:
            permissions = []
            if command.cog.qualified_name == "Admin":
                permissions.append("Sudo Perms/Bot Owner")
            try:
                check = command.checks[0] # get the first check
                check(0) # This would raise an error, because `0` is passed as ctx
            except Exception as e:
                *frames, last_frame = traceback.walk_tb(e.__traceback__) # Iterate through the generator and get the last element
                frame = last_frame[0] # get the first element to get the trace
                permissionslist = frame.f_locals['perms']
                for permission in permissionslist:
                    permission = permission.replace("_", " ")
                    permission = permission.title()
                    permissions.append(permission)
            permissions = ", ".join(permissions)
            embed.add_field(name="Requirements", value=permissions, inline=False)
        channel = self.get_destination()
        await channel.send(embed=embed)

    async def send_help_embed(self, title, description, commands):  # a helper function to add commands to an embed
        embed = HelpEmbed(title=title, description=description or "No help found...")
        text = ""
        for command in commands:
                text += f"`{command.name}` - {command.description}\n"
        if command.cog:
            embed.add_field(name="Category", value=command.cog.qualified_name)
        embed.add_field(name="Sub-commands", value=text, inline=False)
        await self.send(embed=embed)

    async def send_group_help(self, group):
        """triggers when a `<prefix>help <group>` is called"""
        title = self.get_command_signature(group)
        await self.send_help_embed(title, group.description, group.commands)

    async def send_cog_help(self, cog):
        """triggers when a `<prefix>help <cog>` is called"""
        title = cog.qualified_name or "No"
        embed = HelpEmbed(title=f'{title} Category', description=cog.description or "No cog description")
        text = ""
        commandcount = 0
        for command in cog.get_commands():
            text += f"`{command.name}` - {command.description}\n"
            commandcount += 1
        embed.add_field(name=f"Commands in {title} ({commandcount})", value=text, inline=False)
        await self.send(embed=embed)


client.help_command = MyHelp()

'''client.remove_command("help")'''


@client.event
async def on_ready():
    print('Successfully connected to Discord as {0.user}'.format(client))
    botready = discord.Embed(title="Bot is ready!",
                             description="[Celebrate here](https://www.youtube.com/watch?v=dQw4w9WgXcQ)",
                             color=0x32CD32)
    botready.set_author(name=f"{client.user.name}", icon_url=client.user.avatar_url,
                        url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    status = client.get_channel(839045672111308820)
    await status.send(embed=botready)

@client.event
async def on_command_error(ctx, error):
    if ctx.command.cog:
        return
    if isinstance(error, discord.ext.commands.ChannelNotFound):
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
        await ctx.send(f"{error}\n It has to be a mention or user ID.")
        return
    if isinstance(error, commands.ExtensionFailed):
        await ctx.send(f"I failed to load this extension. Details:\n```{error}```")
    errorembed = discord.Embed(title="Oops!",
                                description="This command just received an error. It has been sent to the bot developer..",
                                color=0x00ff00)
    errorembed.add_field(name="Error", value=f"```{error}```", inline=False)
    errorembed.set_thumbnail(url="https://cdn.discordapp.com/emojis/834753936023224360.gif?v=1")
    await ctx.send(embed=errorembed)
    logchannel = client.get_channel(839016255733497917)
    await logchannel.send(
        f"Error encountered on a command.\nGuild `:` {ctx.guild.name} ({ctx.guild.id})\nAuthor `:` {ctx.author.name}#{ctx.author.discriminator} {ctx.author.mention}({ctx.author.id})\nChannel `:` {ctx.channel.name} {ctx.channel.mention} ({ctx.channel.id})\nCommand `:` `{ctx.message.content}`\nError `:` `{error}`\nMore details:")
    filename = random.randint(1, 9999999999)
    filename = f"temp/{filename}.txt"
    with open(filename, "w") as f:
        f.write(gettraceback(error))
    file = discord.File(filename)
    await logchannel.send(file=file)
    os.remove(filename)

# This is for the bot to react to various situations

@client.event
async def on_guild_remove(guild):
    with open('nograresources/prefixes.json', 'r') as f:
        prefixes = json.load(f)
    prefixes.pop(str(guild.id))
    with open('nograresources/prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)


@client.event
async def on_guild_join(guild):
    print(f"I have joined {guild.name}")
    with open('nograresources/prefixes.json', 'r') as f:
        prefixes = json.load(f)
    prefixes[str(guild.id)] = 'a.'
    with open('nograresources/prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

    with open('nograresources/shutup.json', 'r') as f:
        shutuplist = json.load(f)
    shutuplist[str(guild.id)] = {"blacklist_channels": [], "logging_channels": None}
    with open('nograresources/shutup.json', 'w') as f:
        json.dump(shutuplist, f, indent=4)
    general = find(lambda x: 'general' in x.name, guild.text_channels)
    if general is None:
        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).send_messages:
                general = channel
    if general is None:
        return
    print(f"general chat name: {general.name} | general chat mention: {general.mention}")
    if general and general.permissions_for(guild.me).send_messages:
        joinembed = discord.Embed(title="Thanks for using Nogra!",
                                  description="Nogra is a Discord bot with many different functions for your convenience and entertainment.",
                                  color=0x00ff00)
        joinembed.set_author(name=f"{client.user.name}", icon_url=str(client.user.avatar_url))
        joinembed.add_field(name="**__Not sure where to start?__**", value="\u200b", inline=False)
        joinembed.add_field(name="__Fun commands!__",
                            value=f"{client.user.name} Has a wide range of commands that are fun to use. You can send a fake Dank Memer blacklist message to someone, or mute them by dumbfighting them! Use `a.help Fun` to see what commands can be used.<:thumbsupthefuck:823214448579838012>",
                            inline=False)
        joinembed.add_field(name="__Moderation__",
                            value="Not all moderation commands are written yet, but for now we have `ban` and `cban` (countdown ban). Use these commands to moderate your server! <a:nograban:803868903196852245>",
                            inline=True)
        joinembed.add_field(name="__Dank Memer Help__",
                            value=f"Do you use Dank Memer? {client.user.name} has a few utilities related to Dank Memer, such as lottery and rob reminders. <:peepoguns:796022792381661225>",
                            inline=True)
        joinembed.add_field(name="__Userinfo commands__",
                            value=f"{client.user.name} user info is much more informative than that of other bots. Try it out with userinfo!",
                            inline=True)
        joinembed.add_field(name="\u200b",
                            value="By using Nogra, you agree to Nogra's [Terms of Service](https://nograbot.wixsite.com/home/terms) and [Privacy Policy](https://nograbot.wixsite.com/home/privacy).",
                            inline=False)
        joinembed.set_footer(
            text=f"Do a.help as a start. Enjoy using {client.user.name}! If you run into problems or find a bug, DM Argon#0002. Make sure you have enabled the permissions necessary for Nogra to function properly.")
        joinembed.set_thumbnail(url=str(client.user.avatar_url))
        await general.send(embed=joinembed)


@client.event
async def on_message(message):
    if isinstance(message.channel, discord.DMChannel):
        return
    ctx = await client.get_context(message)
    if ctx.valid:
        await client.invoke(ctx)
    else:
        if message.author == client.user:
            return
        if message.channel.id == 821042728849768478:
            await message.add_reaction("<:nogranostar:821675503316238360>")

        if client.user.mentioned_in(message):
            if message.role_mentions or message.mention_everyone or message.reference:
                return
            prefix = await client.get_prefix(message)
            prefix = prefix[2]
            pingembed = discord.Embed(title=f"My prefix here is `{prefix}`",
                                      description=f"Use `{prefix}help` to see my range of commands.")
            pingembed.set_author(name=client.user.name, icon_url=client.user.avatar_url)
            pingembed.set_footer(text=f"Use `{prefix}prefix [prefix]` to change my prefix!")
            await message.channel.send(embed=pingembed)

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


@client.event
async def on_member_join(member):
    with open('nograresources/lotterychoice.json', 'r') as f:
        lotterychoice = json.load(f)
    lotterychoice[str(member.id)] = "dm" if str(member.id) not in lotterychoice else lotterychoice[str(member.id)]
    with open('nograresources/lotterychoice.json', 'w') as f:
        json.dump(lotterychoice, f, indent=4)
    if member.guild.id == 789840820563476482:
        print("I detected someone joining the server.")
        await member.send("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
        await client.get_channel(789840820563476485).send(f"{member.mention} AAAAAA")

# Bot COMMANDS go here.

# clear (purge command)

@client.command(aliases = ["sr"])
@commands.is_owner()
async def softreboot(ctx):
    for extension in INITIAL_EXTENSIONS:
        if 'message' in locals():
            mcontent = message.content
            try:
                client.unload_extension(extension)
                await message.edit(content= f"{mcontent}\n{INITIAL_EXTENSIONS.index(extension)+1} of {len(INITIAL_EXTENSIONS)}: `{extension}` unloaded. <:nograred:830765450412425236>")
            except commands.ExtensionNotLoaded:
                await message.edit(content= f"{mcontent}\n{INITIAL_EXTENSIONS.index(extension)+1} of {len(INITIAL_EXTENSIONS)}: `{extension}` **was never loaded.** <:nograred:830765450412425236>")
                pass
            try:
                client.load_extension(extension)
                await message.edit(content=f"{mcontent}\n{INITIAL_EXTENSIONS.index(extension)+1} of {len(INITIAL_EXTENSIONS)}: `{extension}` successfully reloaded. <:nograonline:830765387422892033>")
            except commands.ExtensionFailed:
                await message.edit(content=f"{mcontent}\n{INITIAL_EXTENSIONS.index(extension)+1} of {len(INITIAL_EXTENSIONS)}: `{extension}` **failed to load, load it manually**. <:nograyellow:830765423112880148>")
        else:
            try:
                client.unload_extension(extension)
                message = await ctx.send(f"{INITIAL_EXTENSIONS.index(extension)+1} of {len(INITIAL_EXTENSIONS)}: `{extension}` unloaded. <:nograred:830765450412425236>")
            except commands.ExtensionNotLoaded:
                message = await ctx.send(f"{INITIAL_EXTENSIONS.index(extension)+1} of {len(INITIAL_EXTENSIONS)}: `{extension}` **was never loaded**. <:nograred:830765450412425236>")
                pass
            try:
                client.load_extension(extension)
                await message.edit(content=f"{INITIAL_EXTENSIONS.index(extension)+1} of {len(INITIAL_EXTENSIONS)}: `{extension}` successfully reloaded. <:nograonline:830765387422892033>")
            except commands.ExtensionFailed:
                await message.edit(content=f"{INITIAL_EXTENSIONS.index(extension)+1} of {len(INITIAL_EXTENSIONS)}: `{extension}` **failed to load, load it manually**. <:nograyellow:830765423112880148>")
    cogsoftreboot = discord.Embed(title="Soft Reboot completed", color=0x00ff00)
    cogsoftreboot.set_author(name=f"{ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar_url, url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    status = client.get_channel(839045672111308820)
    await status.send(embed=cogsoftreboot)


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

client.run(os.environ['NOGRAtoken'])
# betargon's ID was reset btw


