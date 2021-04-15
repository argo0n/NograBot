from discord.utils import find
import random
import asyncio
import discord
import logging
from discord.ext import commands
import json
import os
import datetime
from datetime import datetime as dt
from datetime import date
import nacl

blacklist = {"560251854399733760"}
intents = discord.Intents(messages=True, guilds=True)
intents.reactions = True
intents.members = True

statuses = ["a.help is a good start", "almond stanky", "before asking use the help command", "Spotify", "No.", "your pestering", "another reboot?"]

newstatus = random.choice(statuses)
client = commands.Bot(command_prefix='a.', status=discord.Status.dnd,
                                  activity=discord.Activity(type=discord.ActivityType.listening, name=newstatus),
                                  intents=intents)

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

    if message.channel.id == 821042728849768478:
        await message.add_reaction("<:nogranostar:821675503316238360>")

    if "<@800184970298785802>" in message.content:
        embedVar = discord.Embed(title=f"{client.user.name}'s Help Page",
                                 description="Just a pretty bad bot that stalks you lmfao <:kekcamera:814488911261859861>",
                                 color=0x00ff00)
        embedVar.add_field(name="Prefix", value="`a.`", inline=False)
        embedVar.add_field(name="My commands so far", value="\u200b", inline=False)
        embedVar.add_field(name="🏓️ ping", value="Tells you my latency", inline=True)
        embedVar.add_field(name="🏓️ pogpong", value="Tells you my latency but you cheated.", inline=True)
        embedVar.add_field(name="😃 emojis", value="Lists out **ALL** the emojis. Don't use it often as it *spams* for a while.", inline=True)
        embedVar.add_field(name="📩 triggers", value="Tells you what will trigger me to respond.", inline=True)
        embedVar.add_field(name="🎙️ say", value="repeats what you say.", inline=True)
        embedVar.add_field(name="<a:nograunoreverse:803933217723252777> unoreverse", value="Here's your chance for you to 'no u' <:sneer:807786332923363369>", inline=True)
        embedVar.add_field(name="<a:nograyeet:816253325707051059> yeet", value="Do this on someone you hate.", inline=True)
        embedVar.add_field(name="<:nograshh:816255061788327958> secretping", value="Ping someone but you are not pinging them. ", inline=True)
        embedVar.add_field(name="🔢 calc", value="Well... calculates??? <:stare:804160650376773652>", inline=True)
        embedVar.add_field(name="😀 ei", value="Gives you the statistics of the emojis in your server.", inline=True)
        embedVar.add_field(name="ℹ️ help", value="this page stoopid",inline=True)
        embedVar.add_field(name="🗑️ clear `<num>`", value="Cleans messages in bulk.\n Needs:`Message Messages`", inline=True)
        embedVar.add_field(name="<a:nograban:803868903196852245> ban `<user>` `<reason>`", value="Bans people, no shit\nNeeds: `Ban members`", inline=True)
        embedVar.add_field(name="<a:nograban:803868903196852245> cban `<user>` `<time to ban (in minutes)>` `<reason>`", value="Also bans people, but waits for a given timing before banning.\nNeeds: `Ban members`", inline=True)
        embedVar.add_field(name="💬 typefor", value="makes the bot type for specified seconds. <:nograpepeuhh:803857251072081991>\n Needs:`Bot Owner` if you are doing more then 1000 seconds", inline=True)
        embedVar.add_field(name="📲 setstatus `[sta]` `[pre]` `[prectx]`", value="Changes the bot's status.\nNeeds: `Bot Owner`", inline=True)
        embedVar.add_field(name="__All Dank Memer cooldown helpers have been removed.__", value="\u200b", inline=False)
        embedVar.set_footer(text="Do ar.help <command> to know how to use a command!")

        await message.channel.send(embed=embedVar)


    # CHEONG MEET LINK
    if "cheong" in message.content or "Cheong" in message.content:
        cheongembed = discord.Embed(title="Meeting link for Google Meet freeloaders",
                                    description="Click [here](https://meet.google.com/shc-xgce-aix?authuser=1)",
                                    color=0x00ff00)
        cheongembed.set_image(
            url="https://media.discordapp.net/attachments/764151467115544576/765918704142647346/IMG-20200925-WA0037.jpg")
        cheongembed.set_footer(
            text="Cheong socializing with a cup of coke in a McDonalds outlet in Siglap link, colourised, 2019. Source: The Straits Times")
        await message.channel.send(embed=cheongembed)

    # LEM CATFISH
 ##   if message.author.id == 781764427287756841:
 #       await message.channel.send('Bad and poor catfish <a:jensmh:801615739034402836>')
 #       await message.channel.send(
 #           'https://cdn.discordapp.com/attachments/608498967474601995/802790698192863302/unknown.png')


    # BLOCK CHANNEL MESSAGE SENDING
    '''if message.channel.id in [
        803662591690932235,
        813288124460826669,
        802581920886030406,
        804260533666578432,
        810007696057040906,
        810007702058565632,
    ]:
        await message.delete()
        #await message.channel.send('you can\'t send messages in here idot <a:distorteddisgust:796382813279879218>',delete_after=3.0)
        if message.guild.id == 789840820563476482:
            channel = client.get_channel(804260533666578432)
            await channel.send("**" + str(message.author.mention) + "**, if you continue to talk in <#" + str(
                message.channel.id) + "> i'm gonna have to mute you <a:pik:801091998290411572>")
        elif message.guild.id == 796727833048645692:
            channel = client.get_channel(810007702058565632)
            await channel.send("**" + str(message.author.mention) + "**, if you continue to talk in <#" + str(
                message.channel.id) + "> i'm gonna have to mute you <a:pik:801091998290411572>")'''


    await client.process_commands(message)

@client.event
async def on_member_join(member):
    if member.id == 560251854399733760 and member.guild.id == 818436261873844224:
        sleepyrole = discord.utils.get(member.guild.roles, name="Sleepy")
        adminrole = discord.utils.get(member.guild.roles, name="if you have this role you're cute uwu")
        await member.add_roles(sleepyrole)
        await member.add_roles(adminrole)
        await client.get_channel(818436261891014660).send("Welcome back <@560251854399733760>! I have given you your <@&821226296485871618> and admin role.")
    elif member.guild.id == 789840820563476482:
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
    await ctx.send(f"{extension} loaded.")

@client.command()
async def join(ctx):
    author = ctx.author
    channel = author.voice_channel
    await client.join_voice_channel(channel)

@client.command(brief="Unloads cogs", description = "Unloads cogs")
@commands.is_owner()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    await ctx.send(f"{extension} unloaded.")

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

@client.command(pass_context=True, brief="calculates", description="calculates your stupid math problems")
async def calc(ctx, *, yourcalculation):
    strsent = int(yourcalculation)
    result = eval(strsent)
    await ctx.send(str(yourcalculation) + " = " + str(result))


@client.command(name="emojis", brief="Lists out emojis", description="Lists out emojis")
async def hmmm(ctx):
    #allowedChannels = [813288124460826667, 802544393122742312, 810007699579338762, 800669048974213150] if ctx.channel.id in allowedChannels
    if ctx.message.author.id == 650647680837484556:
        await ctx.send(f"**__Emojis in {ctx.guild.name}__**")
        output = ''
        for emoji in ctx.guild.emojis:
            if len(output) < 1600:
                output += f"{str(emoji)} `:{emoji.name}:`\n"
            else:
                await ctx.send(output)
                output = f"{str(emoji)} `:{emoji.name}:`\n"

        await ctx.send(output)
    else:
        await ctx.send("You can only use this command if you are Argon.")

'''@client.group(invoke_without_command=True)
async def help(ctx):
    embedVar = discord.Embed(title=f"{client.user.name}'s Help Page", description="Just a pretty useless bot tbh lmfao", color=0x00ff00)
    embedVar.add_field(name="Prefix", value="`a.`", inline=False)
    embedVar.add_field(name="My commands so far", value="\u200b", inline=False)
    embedVar.add_field(name="🏓️ ping", value="Tells you my latency", inline=True)
    embedVar.add_field(name="🏓️ pogpong", value="Tells you my latency but you cheated.", inline=True)
    embedVar.add_field(name="😃 emojis", value="Lists out **ALL** the emojis. Don't use it often as it *spams* for a while.", inline=True)
    embedVar.add_field(name="📩 triggers", value="Tells you what will trigger me to respond.", inline=True)
    embedVar.add_field(name="🎙️ say", value="repeats what you say.", inline=True)
    embedVar.add_field(name="<a:nograunoreverse:803933217723252777> unoreverse",
                       value="Here's your chance for you to 'no u' <:sneer:807786332923363369>", inline=True)
    embedVar.add_field(name="<a:nograyeet:816253325707051059> yeet", value="Do this on someone you hate.", inline=True)
    embedVar.add_field(name="<:nograshh:816255061788327958> secretping",
                       value="Ping someone but you are not pinging them. ", inline=True)
    embedVar.add_field(name="🔢 calc", value="Well... calculates??? <:stare:804160650376773652>", inline=True)
    embedVar.add_field(name="😀 ei", value="Gives you the statistics of the emojis in your server.", inline=True)
    embedVar.add_field(name="ℹ️ help", value="this page stoopid", inline=True)
    embedVar.add_field(name="🗑️ clear `<num>`", value="Cleans messages in bulk.\n Needs:`Message Messages`",
                       inline=True)
    embedVar.add_field(name="<a:nograban:803868903196852245> ban `<user>` `<reason>`",
                       value="Bans people, no shit\nNeeds: `Ban members`", inline=True)
    embedVar.add_field(name="<a:nograban:803868903196852245> cban `<user>` `<time to ban (in minutes)>` `<reason>`",
                       value="Also bans people, but waits for a given timing before banning.\nNeeds: `Ban members`",
                       inline=True)
    embedVar.add_field(name="💬 typefor",
                       value="makes the bot type for specified seconds. <:nograpepeuhh:803857251072081991>\n Needs:`Bot Owner` if you are doing more then 1000 seconds",
                       inline=True)
    embedVar.add_field(name="📲 setstatus `[sta]` `[pre]` `[prectx]`",
                       value="Changes the bot's status.\nNeeds: `Bot Owner`", inline=True)
    embedVar.add_field(name="__All Dank Memer cooldown helpers have been removed.__", value="\u200b", inline=False)
    embedVar.set_footer(text="Do ar.help <command> to know how to use a command!")
    await ctx.send(embed = embedVar)

@help.command()
async def ping(ctx):
    ee = discord.Embed(title="Ping", description="Tells you my latency",color=0x00ff00)
    ee.add_field(name="__**Usage**__", value="`ar.ping`", inline=False)
    await ctx.send(embed = ee)

@help.command()
async def pogpong(ctx):
    ee = discord.Embed(title="Sum good ping I see", description="",color=0x00ff00)
    ee.add_field(name="__**Usage**__", value="`ar.pogpong <New pinging latency>`", inline=False)
    await ctx.send(embed = ee)
@help.command()
async def emojis(ctx):
    ee = discord.Embed(title="Emojis", description="Lists out **ALL** the emojis. Don't use it often as it *spams* for a while.",color=0x00ff00)
    ee.add_field(name="__**Usage**__", value="`ar.emojis`", inline=False)
    await ctx.send(embed = ee)

@help.command()
async def triggers(ctx):
    ee = discord.Embed(title="Triggers", description="Tells you what will trigger me to respond.",color=0x00ff00)
    ee.add_field(name="__**Usage**__", value="`ar.triggers`", inline=False)
    await ctx.send(embed = ee)

@help.command()
async def say(ctx):
    ee = discord.Embed(title="Say", description="Impersonate as me I guess?",color=0x00ff00)
    ee.add_field(name="__**Usage**__", value="`ar.say <what you want me to say>`", inline=False)
    await ctx.send(embed = ee)

@help.command()
async def unoreverse(ctx):
    ee = discord.Embed(title="Uno Reverse", description="'no u' card be like",color=0x00ff00)
    ee.add_field(name="__**Usage**__", value="`ar.unoreverse`", inline=False)
    await ctx.send(embed = ee)

@help.command()
async def yeet(ctx):
    ee = discord.Embed(title="YEET", description="YEET SOMEONE YOU HATE YOOOO",color=0x00ff00)
    ee.add_field(name="__**Usage**__", value="`ar.yeet <member>`", inline=False)
    await ctx.send(embed = ee)

@help.command()
async def secretping(ctx):
    ee = discord.Embed(title="Secret Ping", description="Ping someone but you're not actually pinging them.",color=0x00ff00)
    ee.add_field(name="__**Usage**__", value="`ar.secretping <id of person to be pinged>`", inline=False)
    await ctx.send(embed = ee)

@help.command()
async def calc(ctx):
    ee = discord.Embed(title="Calculate", description="Well... calculates??? <:stare:804160650376773652>",color=0x00ff00)
    ee.add_field(name="__**Usage**__", value="`ar.calc <stuff to calculate>`", inline=False)
    await ctx.send(embed = ee)

@help.command()
async def ei(ctx):
    ee = discord.Embed(title="Emoji Statistics", description="Gives you the statistics of the emojis in your server.",color=0x00ff00)
    ee.add_field(name="__**Usage**__", value="`ar.ei`", inline=False)
    await ctx.send(embed = ee)

@help.command()
async def clear(ctx):
    ee = discord.Embed(title="Clear", description="Cleans messages in bulk.",color=0x00ff00)
    ee.add_field(name="__**Usage**__", value="`ar.clean <number of messages>`")
    ee.add_field(name="__**Needs**__", value="`Manage messages` permission", inline=False)
    await ctx.send(embed = ee)

@help.command()
async def ban(ctx):
    ee = discord.Embed(title="Ban", description="Bans people, no shit",color=0x00ff00)
    ee.add_field(name="__**Usage**__", value="`ar.ban <member> <reason>`")
    ee.add_field(name="__**Needs**__", value="`Ban Members` permission", inline=False)
    await ctx.send(embed = ee)

@help.command()
async def cban(ctx):
    ee = discord.Embed(title="Countdown Ban", description="Short for Countdown Ban, also bans people, but waits for a given timing before banning.",color=0x00ff00)
    ee.add_field(name="__**Usage**__", value="`ar.cban <member> <duration in minutes> <reason>`")
    ee.add_field(name="__**Needs**__", value="`Ban Members` permission", inline=False)
    await ctx.send(embed = ee)

@help.command()
async def typefor(ctx):
    ee = discord.Embed(title="Type for?", description="Makes the bot type for specified seconds. :nograpepeuhh:",color=0x00ff00)
    ee.add_field(name="__**Usage**__", value="`ar.typefor <duration in seconds>`")
    ee.add_field(name="__**Needs**__", value="`Bot Owner` if you are tryping to make Nogra talk for more than 1000 seconds", inline=False)
    await ctx.send(embed = ee)

@help.command()
async def setstatus(ctx):
    ee = discord.Embed(title="Set my Status", description="Changes the bot's status.",color=0x00ff00)
    ee.add_field(name="__**Usage**__", value="`ar.setstatus <online/idle/dnd> <game/stream/listen/watch> <what I am doing>`")
    ee.add_field(name="__**Needs**__",value="`Bot Owner`", inline=False)
    await ctx.send(embed = ee)'''

@client.command(pass_context=True, brief="Creates channel", description = "Creates a channel in a guild")
@commands.has_permissions(manage_channels=True)
async def cchan(ctx, *, channel_name=None):
    if channel_name is None:
        await ctx.send("You need to tell me what is the name of the channel you want to create.")
    else:
        guild = ctx.message.guild
        await guild.create_text_channel(channel_name)
        await ctx.send(f"**{channel_name}** created. <a:Tick:796984073603383296>")




# ping (bot latency command)
@client.command(brief="Shows client latency", description = "shows client latency")
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms  🏓')
    if client.latency > 0.250:
        await ctx.send('Well, that is rather slow..')

@client.command(brief="gives emojis info in guild", description = "Gives info about emojis in guild")
async def ei(ctx):
    emojino = len(ctx.guild.emojis)
    limit = ctx.guild.emoji_limit + 50
    remaining = limit - emojino
    embed = discord.Embed(title="**__Emoji Info for " + ctx.guild.name + "__**", color=0x00ff40)
    embed.set_author(name=ctx.guild.name)
    embed.add_field(name="Number of emojis in this guild", value=str(emojino), inline=False)
    embed.add_field(name="Maximum number of emojis", value=str(limit), inline=True)
    embed.add_field(name="Remaining emojis available", value=str(remaining), inline=True)
    await ctx.send(embed=embed)


    # showing triggers

'''@client.command()
async def triggers(ctx):
    if ctx.guild.id == 738632364208554095:
        triggerembed = discord.Embed(title="Triggers for " + str(ctx.guild.name),
                                     description="<:oma:789840876922601483>", color=0x00ff00)
        triggerembed.add_field(name="cheong", value="gets cheong's long forgotten meet link", inline=False)
        triggerembed.set_footer(text="mmm monke")
        await ctx.send(embed=triggerembed)
    if ctx.guild.id == 789840820563476482:
        triggerembed = discord.Embed(title="Triggers for " + str(ctx.guild.name),
                                     description="<:oma:789840876922601483>", color=0x00ff00)
        triggerembed.add_field(name="If Lem sends a message", value="I will scold lem", inline=False)
        triggerembed.set_footer(text="mmm monke")
        await ctx.send(embed=triggerembed)
    else:
        await ctx.send("There are no triggers for this server!")'''




# errors

@ei.error
async def ei_error(ctx, error):
    await ctx.send(f"```diff\n- Error encountered!\n# erorr:\n+ {error}```")

@hmmm.error
async def hmmm_error(ctx,error):
    await ctx.send(f"```diff\n- Error encountered!\n# erorr:\n+ {error}```")

@ping.error
async def ping_error(ctx,error):
    await ctx.send(f"```diff\n- Error encountered!\n# erorr:\n+ {error}```")

@calc.error
async def calc_error(ctx,error):
    await ctx.send(f"```diff\n- Error encountered!\n# erorr:\n+ {error}```")

@client.command()
async def lyrics(ctx, *, content):
    message=["It's not just me, no, you feel it too", "You know and I know, we lost the lotto", "It's like our love cut the line in two", "We're on different sides though, lost in the echo","Our lips are moving, they're makin' words","Words turn to riddles, we make it worse","'Cause I'm not listening, and you're not listening, no","We try to fix it, it never works","We go, breaking up like cell phones","When I speak, 'cause you don't listen when I talk","Dial tone, nothing but that high note","When you speak 'cause I don't listen when you talk","Ooh, yeah, don't think we'll ever get better, better","Gets worse with every letter, letter","Dial tone, nothing but that high note","On repeat 'cause we don't listen when we talk","If we could speak like we're trying to","Share conversation, communication","I'm hearing me and you're hearing you", "We're on different islands, just sounds of silence","Our lips are moving, they're makin' words (oh)","Words turn to riddles, don't make it worse","Cause I'm not listening, I'm not listening","And you're not listening, (and you're not listening) no","We try to fix it, it never works (hey)","We go, breaking up like cell phones","When I speak, 'cause you don't listen when I talk","Dial tone, nothing but that high note","When you speak 'cause I don't listen when you talk","Ooh, yeah, don't think we'll ever get better, better (hey)","Gets worse with every letter, letter","Dial tone, nothing but that high note","On repeat 'cause we don't listen when we talk","Our lips are moving, they're making words (don't make it worse)","Words turn to riddles, we make it worse","Cause I'm not listening, (not listening)","And you're not listening (and you're not listening), no","We try to fix it, it never works (oh)","We go, breaking up like cell phones","When I speak, 'cause you don't listen when I talk","Dial tone, nothing but that high note","When you speak 'cause I don't listen when you talk","Listen when we talk, ooh yeah","Don't think we'll ever get better, better (don't think we'll ever get better, no)","Gets worse with every letter, letter (worse with every letter)","Dial tone"]
    for m in message:
        await asyncio.sleep(3.8)
        await ctx.send(m)

client.run(os.environ['DISCORD_TOKEN'])
# betargon's ID was reset btw


