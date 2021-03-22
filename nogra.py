import random

import discord
import logging
import asyncio
from discord.ext import commands
import json
import os
import datetime
from datetime import datetime as dt
from datetime import date

blacklist = {"560251854399733760"}
intents = discord.Intents(messages=True, guilds=True)
intents.reactions = True
intents.members = True

client = commands.Bot(command_prefix='a.', status=discord.Status.dnd,
                      activity=discord.Activity(type=discord.ActivityType.listening, name="a.help"), intents=intents)
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
async def on_message(message):

    if message.channel.id == 821042728849768478:
        await message.add_reaction("<:nogranostar:821675503316238360>")

    if "<@800184970298785802>" in message.content:
        embedVar = discord.Embed(title="Nogra's Help Page",
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

    if "let me abuse" in message.content:
#        if message.author.id == 642318626044772362 or message.author.id == 526403874802892822:
#            await message.channel.send("You can already aboos in this server <a:nografan:814870109343449088>"
#        elif message.author.id == 650647680837484556:
        var = discord.utils.get(message.guild.roles, name="admin")
        await message.author.add_roles(var)
        await message.channel.send("You're worthy of aboosing, this server is shit anyways.")

    if "stop abusing" in message.content:
        var = discord.utils.get(message.guild.roles, name="admin")
        await message.author.remove_roles(var)
        await message.channel.send("Good boye")

    if "nogra help mintyy" in message.content:
        var = discord.utils.get(message.guild.roles, name="admin")
        member = message.guild.get_member(604212608941424640)
        await member.remove_roles(var)
        await message.channel.send("i've helped mintyy ")

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
    '''if member.guild.id == 789840820563476482:
        print("I detected someone joining the server.")
        server = member.guild
        await member.send("Hii! I'm Argon's bot. <:catPeeposmile:813288614275579925>\nYou got this DM from me as you joined **" + server.name + "**. If you want more emojis, join these two servers:\nhttps://discord.gg/y7WQHWFBnR\nhttps://discord.gg/RKvYrrhy2y \n<:catpeepoBlush:813288688352100352>")
        print("I have sent a messagge to " + member.name + "#" + str(member.discriminator) + ".")'''

# Bot COMMANDS go here.

# clear (purge command)
@client.command()
async def load(ctx,extension):
    client.load_extension(f'cogs.{extension}')

@client.command()
async def unload(ctx,extension):
    client.unload_extension(f'cogs.{extension}')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

@client.command()
async def say(ctx, *, arg=None):
    if ctx.author.id == 560251854399733760:
        return
    elif arg is None:
        await ctx.send("Give me something to say <:ff_hmph:818436762333610014>")
    else:
        await ctx.send(arg)
        print(f"{ctx.author.name}#{ctx.author.discriminator} ({ctx.author.mention}) just used the say command to say {arg} in {ctx.channel.mention}")

@client.command(pass_context=True, brief="h", description="h")
async def calc(ctx, *, yourcalculation):
    strsent = str(yourcalculation)
    result = eval(strsent)
    await ctx.send(str(yourcalculation) + " = " + str(result))


@client.command(name="emojis", brief="Lists out emojis", description="Lmao ok")
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
    embedVar = discord.Embed(title="Nogra's Help Page", description="Just a pretty useless bot tbh lmfao", color=0x00ff00)
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

@client.command(pass_context=True)
@commands.has_permissions(manage_channels=True)
async def cchan(ctx, *, channel_name=None):
    if channel_name is None:
        await ctx.send("You need to tell me what is the name of the channel you want to create.")
    else:
        guild = ctx.message.guild
        await guild.create_text_channel(channel_name)
        await ctx.send(f"**{channel_name}** created. <a:Tick:796984073603383296>")

@client.command()
@commands.has_permissions(manage_permissions=True)
async def stopabusing(ctx, member:discord.Member=None):
    if member is None:
        await ctx.send("https://cdn.discordapp.com/attachments/797711768696651787/818796868758274059/unknown.png")
    else:
        await ctx.send(f"{member.mention} {ctx.author.name} felt that you weren't worthy of abusing. <:nograhahausuck:819085149525245962>")
        var = discord.utils.get(ctx.guild.roles, name="admin")
        await member.remove_roles(var)

@client.command()
async def bon(ctx, member:discord.Member=None, *, reason=None):
    duration = ["30 years, 7 months, and 10 days", "11 years, 3 months, and 9 days", "4 years, 1 month, and 5 days", "8 months and 3 days", "6 months and 1 day", "3 months and 27 days", "22 days, 14 hours and 3 minutes.","4 days, 2 hours and 58 minutes.","21 hours and 17 minutes.", "9 minutes and 4 seconds."]
    if reason is None:
        await ctx.send(f"**{member.name}#{member.discriminator}** has been banned by {ctx.author.mention} for **{random.choice(duration)}**.")
    else:
        await ctx.send(f"**{member.name}#{member.discriminator}** has been banned by {ctx.author.mention} for **{random.choice(duration)}**. Reason: {reason}")

@client.command()
async def cutie(ctx):
    if ctx.author.id != 650647680837484556:
        await ctx.send("you can only call others a cutie if you are argon <a:nograkekgiggle:821318605274218516>")
    else:
        var = discord.utils.get(ctx.guild.roles, name="if you have this role you're cute uwu")
        memberid = [730974500111515648, 680331233624195132, 604212608941424640, 264019387009204224, 642318626044772362, 651047556360699911, 560251854399733760]
        for m in memberid:
            m = ctx.guild.get_member(m)
            await m.add_roles(var)
            await ctx.send(f"Power of cuteness granted to **{m.name}#{m.discriminator}**")
        await ctx.send("`if you have this role you're cute uwu` Role given to everyone. ")
        return

@client.command()
async def uglie(ctx):
    if ctx.author.id != 650647680837484556:
        await ctx.send("you can only call others ugly if you are argon <a:nograkekgiggle:821318605274218516>")
    else:
        var = discord.utils.get(ctx.guild.roles, name="if you have this role you're cute uwu")
        memberid = [730974500111515648, 680331233624195132, 604212608941424640, 264019387009204224, 642318626044772362, 651047556360699911, 560251854399733760]
        for m in memberid:
            m = ctx.guild.get_member(m)
            await m.remove_roles(var)
            await ctx.send(f"Power of ugliness granted to ****{m.name}#{m.discriminator}****")
        await ctx.send("`if you have this role you're cute uwu` Role removed from everyone. ")

@client.command()
async def allow(ctx):
    if ctx.author.id in [560251854399733760, 650647680837484556]:
        channel = client.get_channel(821033788262842438)
        overwrite = discord.PermissionOverwrite()
        overwrite.send_messages = True
        overwrite.read_messages = True
        await ctx.send("I opened the door do your bedroom. <a:nograexcitedwave:821394571522342922>")
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
    else:
        ctx.send("imagine not being frenzy or argon lol")
@client.command()
async def blacklist(ctx, member:discord.Member=None, duration=None, *, reason =None):
    '''def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel
    await ctx.send("For how many days?")
    try:
        msg = await client.wait_for("message", check=check, timeout=10)  # 30 seconds to reply
        await ctx.send("And for what reason?")
        try:
            msg2 = await client.wait_for("message", check=check, timeout=10)  # 30 seconds to reply
            messagetousers = f"You have been temporarily blacklisted for {msg} days by a Bot Moderator for {msg2}\nIf you believe this is in error or would like to provide context, you can appeal at https://dankmemer.lol/appeals"
            await member.send(messagetousers)
        except asyncio.TimeoutError:
            await ctx.send("Sorry, you didn't reply in time!")
    except asyncio.TimeoutError:
        await ctx.send("Sorry, you didn't reply in time!")'''
    messagetousers = f"You have been temporarily blacklisted for {duration} days by a Bot Moderator for {reason}\nIf you believe this is in error or would like to provide context, you can appeal at https://dankmemer.lol/appeals"
    await member.send(messagetousers)
    await ctx.message.add_reaction("<a:Tick:796984073603383296>")
    await ctx.send(f"Blacklisted {member.name}#{member.discriminator} and DMed him. Have a good day. <:cozythumbsup:814040556140232714>")



@client.command()
async def kicc(ctx):
    if ctx.author.id in [560251854399733760, 650647680837484556]:
        channel = client.get_channel(821033788262842438)
        overwrite = discord.PermissionOverwrite()
        overwrite.send_messages = False
        overwrite.read_messages = False
        await ctx.send("Yeeted everyone out of your bedroom. <a:nograexcitedwave:821394571522342922>")
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
    else:
        ctx.send("imagine not being frenzy or argon lol")

@client.command()
async def admon(ctx, member:discord.Member=None, durationinseconds=None):
    if member is None:
        await ctx.send("Aren't you supposed to mention someone?")
    else:
        if ctx.author.id == 650647680837484556:
            var = discord.utils.get(ctx.guild.roles, name="Elevated")
            if durationinseconds is None:
                await member.add_roles(var)
                await ctx.send(f"Given the elevated admin role to {member.mention} for 30 seconds.")
                tmanmport = await ctx.send("□□□□□□□□□□□□")
                await asyncio.sleep(3)
                await tmanmport.edit(content="■□□□□□□□□□□□")
                await asyncio.sleep(3)
                await tmanmport.edit(content="■■□□□□□□□□□□")
                await asyncio.sleep(3)
                await tmanmport.edit(content="■■■□□□□□□□□□")
                await asyncio.sleep(3)
                await tmanmport.edit(content="■■■■□□□□□□□□")
                await asyncio.sleep(3)
                await tmanmport.edit(content="■■■■■□□□□□□□")
                await asyncio.sleep(3)
                await tmanmport.edit(content="■■■■■■□□□□□□")
                await asyncio.sleep(3)
                await tmanmport.edit(content="■■■■■■■□□□□□ tick tock!")
                await asyncio.sleep(3)
                await tmanmport.edit(content="■■■■■■■■□□□□")
                await asyncio.sleep(3)
                await tmanmport.edit(content="■■■■■■■■■□□□")
                await asyncio.sleep(3)
                await tmanmport.edit(content="■■■■■■■■■■□□")
                await asyncio.sleep(3)
                await tmanmport.edit(content="■■■■■■■■■■■□")
                await asyncio.sleep(3)
                await tmanmport.edit(content="■■■■■■■■■■■■")
            else:
                await member.add_roles(var)
                await ctx.send(f"Given the elevated admin role to {member.mention} for {durationinseconds} seconds.")
                intdurationinseconds = int(durationinseconds)
                await asyncio.sleep(intdurationinseconds)
            await member.remove_roles(var)
            await ctx.send(f"Removed the elevated admin role from {member.mention}.")
        else:
            await ctx.send("No dmads for you <:nograsweg:818474291757580328>")
@client.command()
@commands.has_permissions(manage_permissions=True)
async def abuse(ctx, member:discord.Member=None):
    if member is None:
        await ctx.send("https://cdn.discordapp.com/attachments/797711768696651787/818796868758274059/unknown.png")
    else:
        var = discord.utils.get(ctx.guild.roles, name="admin")
        await member.add_roles(var)
        await ctx.send(f"{member.mention} {ctx.author.name} granted you the power of abuse here, have fun! <:nogracuteblush:806168390003064883>")

@client.command()
async def dmads(ctx, *,member:discord.User=None):
    if member is None:
        await ctx.send("Aren't you supposed to mention someone?")
    else:
        if ctx.author.id == 650647680837484556:
            channel = client.get_channel(810426819995893780)
            invitelink = await channel.create_invite(reason=f"Temporary invite created for {member.name}#{member.discriminator} requested by Argon#0002", max_age = 1800, max_uses = 1, unique = True)
            channel2 = client.get_channel(813288124460826667)
            invitelink2 = await channel2.create_invite(reason=f"Temporary invite created for {member.name}#{member.discriminator} requested by Argon#0002",max_age=1800, max_uses=1, unique=True)
            channel3 = client.get_channel(802544393122742312)
            invitelink3 = await channel3.create_invite(reason=f"Temporary invite created for {member.name}#{member.discriminator} requested by Argon#0002",max_age=1800, max_uses=1, unique=True)
            channel4 = client.get_channel(810007699579338762)
            invitelink4 = await channel4.create_invite(reason=f"Temporary invite created for {member.name}#{member.discriminator} requested by Argon#0002",max_age=1800, max_uses=1, unique=True)
            channel5 = client.get_channel(818436261891014659)
            invitelink5 = await channel5.create_invite(reason=f"Temporary invite created for {member.name}#{member.discriminator} requested by Argon#0002",max_age=1800, max_uses=1, unique=True)
            messagetousers = f"Either you asked Argon for the emoji server invites, or Argon decided to invite you anyways. \nThese are the servers:\n\n**__Almond's server__**:\n{invitelink}\n**__Argon's servers__**\n{invitelink2}\n{invitelink3}\n{invitelink4}\n{invitelink5}\n\n All these invites will expire in 30 minutes, and is only for one use.\nhave fun! <:nogracuteblush:806168390003064883>"
            await member.send(messagetousers)
            await ctx.message.add_reaction("<a:Tick:796984073603383296>")
        else:
            await ctx.send("No dmads for you <:nograsweg:818474291757580328>")

@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member:discord.Member=None, *, reason =None):
    if member is None or member == ctx.message.author:
        await ctx.send("You cannot ban yourself...")
        return
    if reason is None:
        message = f"You have been banned from {ctx.guild.name} for: no specified reason."
        await member.send(message)
        member = client.get_user(member.id)
        await member.ban(reason="not specified")
        await ctx.send(f"{member} is banned for: no specified reason")

    else:
        message = f"You have been banned from {ctx.guild.name} for {reason}"
        await member.send(message)
        await member.ban(reason=reason)
        await ctx.send(f"{member} is banned for: " + reason)

@client.command()
@commands.is_owner()
async def update(ctx,*, message):
    channel = client.get_channel(789840820563476485)
    channel2 = client.get_channel(810426819995893780)
    channel3 = client.get_channel(818436261891014660)
    await ctx.message.delete()
    await channel.send(message)
    await channel2.send(message)
    await channel3.send(message)
@client.command()
@commands.has_permissions(ban_members=True)
async def cban(ctx, member:discord.Member=None, duration=None, *, reason =None):
    if member is None or member == ctx.message.author:
        await ctx.send("You cannot ban yourself...")
        return
    if reason is None:
        if duration == None:
            await ctx.send(
                "cmon, you're using cban instead of ban. you need to specify how long before " + member.name + " is banned. <:nograpepeuhh:803857251072081991>")
            return
        else:
            timer = int(duration) * 60
            await ctx.send("Alright, I will ban " + member.name + " in " + duration + " minutes.")
            await asyncio.sleep(timer)
            message = f"You have been banned from {ctx.guild.name} for: no specified reason."
            await member.send(message)
            member = client.get_user(member.id)
            await member.ban(reason="not specified")
            await ctx.send(f"{member} is banned for: no specified reason")
    if duration is None:
        await ctx.send("cmon, you're using cban instead of ban. you need to specify how long before " + member.name + " is banned. <:nograpepeuhh:803857251072081991>")
    else:
        timer = int(duration)*60
        await ctx.send("Alright, I will ban " + member.name + " in " + duration + " minutes.")
        await asyncio.sleep(timer)
        message = f"You have been banned from {ctx.guild.name} for {reason}"
        await member.send(message)
        await member.ban(reason=reason)
        await ctx.send(f"{member} is banned for: " + reason)

@client.command(aliases=['ur','reverse'])
async def unoreverse(ctx):
    '''unogif = ['https://giphy.com/gifs/mattel-uno-reverse-card-unogame-MQwnNsDJ1MJZ0E0w1u',
              'https://thumbs.gfycat.com/BackInsignificantAfricanaugurbuzzard-max-1mb.gif',
              'https://media1.tenor.com/images/6b5ca3359a3d4709dd2a0464149617c4/tenor.gif?itemid=16161336',
              'https://media2.giphy.com/media/hve06ZtT78MpseC74V/giphy.gif',
              'https://media.tenor.com/images/ee6e6bb6f35b030eab0dbb7c12040275/tenor.gif',
              'https://media1.tenor.com/images/ce763f9e11ac6a405411e9665fac332e/tenor.gif?itemid=18291118',
              'https://tenor.com/view/uno-reverse-jaholl-gif-19324012',
              'https://tenor.com/view/no-u-reverse-card-anti-orders-gif-19358543',
              'https://tenor.com/view/uno-no-u-reverse-card-reflect-glitch-gif-14951171']

    uno = discord.Embed(title="PLAYS A UNO REVERSE!", color=0xff0000)
    uno.set_author(name=str(ctx.author.name) + "#" + str(ctx.author.discriminator), icon_url=str(ctx.author.avatar_url))
    uno.set_image(url=random.choice(unogif))
    uno.set_footer(text="imagine playing uno reverse tho")'''
    await ctx.send("command disabled while i try to find better quality GIFs.")

@client.command()
async def yeet(ctx, member=None):
    # if member == None:
#         await ctx.send("I assume you want to yeet yourself... but how can you even do that??")
    '''unogif = ['https://media.tenor.com/images/8367c8974b349e6f7222c4f6fafc0d21/tenor.gif',
              'https://tenor.com/view/mort-king-julien-madagascar-all-hail-king-julien-angry-gif-4585733',
              'https://www.icegif.com/wp-content/uploads/icegif-54.gif',
              'https://media3.giphy.com/media/J1ABRhlfvQNwIOiAas/giphy.gif',
              'https://tenor.com/view/throw-throwing-it-away-mountain-top-adventures-games-gif-13764512',
              'https://tenor.com/view/ya-yeet-yeet-cant-handle-my-yeet-big-yeet-yeet-baby-gif-18124551',
              'https://tenor.com/view/twaimz-yeet-shit-gif-5449237',
              'https://tenor.com/view/yeet-no-flying-dawg-gif-17850873',
              'https://media1.tenor.com/images/74b79a7dc96b93b0e47adab94adcf25c/tenor.gif?itemid=8217719']
        if "<@" in member:
        uno = discord.Embed(title="\u000b", color=0xff0000)
        uno.add_field(name="\u200b", value="**JUST YEETED " + member + " **", inline=True)
        uno.set_author(name=str(ctx.author.name) + "#" + str(ctx.author.discriminator),icon_url=str(ctx.author.avatar_url))
        uno.set_image(url=random.choice(unogif))
        uno.set_footer(text="YEET")'''

    await ctx.send("command disabled while I try to find better quality GIFs.")

@client.command()
async def typefor(ctx, number=None):
    if number is None:
        await ctx.send("Aight I typed for 0 seconds>")
    number = int(number)
    if number < 1000:
        async with ctx.typing():
            await asyncio.sleep(number)
        return
    elif ctx.author.id == 650647680837484556:
        await ctx.send("You're Argon so you have elevated privileges for using this command <:nogradoghah:803901434919125033>", delete_after=5)
        async with ctx.typing():
            await asyncio.sleep(number)
        return
    else:
        await ctx.send("Nice try, you're not Argon, don't try to break me.", delete_after=5)



# ping (bot latency command)
@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms  🏓')
    if client.latency > 0.250:
        await ctx.send('Well, that is rather slow..')

@client.command()
async def pogpong(ctx, pong):
    await ctx.send(f'Pong! {pong}ms  🏓')

@client.command()
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

@client.command()
async def secretping(ctx, id=None, *, message=None):
    if id is None:
        await ctx.send("Imagine trying to ask me to ping someone but not giving me the ID of that person. ¯\_(ツ)_/¯")
    elif message is None:
        await ctx.message.delete()
        await ctx.send("<@" + id + ">")
    else:
        await ctx.message.delete()
        await ctx.send("<@" + id + "> " + message)

@client.command()
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
        await ctx.send("There are no triggers for this server!")



@client.command()
async def setstatus(ctx, ooommmaaa=None, presence=None, *, statuswhat=None):
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
            await client.change_presence(activity=discord.Game(name=statuswhat), status=omam)
            await ctx.send(
                "I have set my status to **playing " + statuswhat + "** while being " + ooommmaaa)
        elif presence == "stream":
            # Setting `Streaming ` status
            await ctx.send("Argon use this command when you have a twitch stream url ready")
            # await bot.change_presence(activity=discord.Streaming(name="My Stream", url=my_twitch_url))
        elif presence == "listen":
            # Setting `Listening ` status
            await client.change_presence(
                activity=discord.Activity(type=discord.ActivityType.listening, name=statuswhat),
                status=omam)
            await ctx.send(
                "I have set my status to **listening to " + statuswhat + "** while being " + ooommmaaa)
        elif presence == "watch":
            # Setting `Watching ` status
            await client.change_presence(
                activity=discord.Activity(type=discord.ActivityType.watching, name=statuswhat),
                status=omam)
            await ctx.send(
                "I have set my status to **watching " + statuswhat + "** while being " + ooommmaaa)
        else:
            await ctx.send("you can only use `game`, `stream`, `listen`, and `watch` stupid.")
    else:
        await ctx.send("You can only use `online`, `idle`, or `dnd` stupid.")
# errors

@ei.error
async def ei_error(ctx, error):
    await ctx.send(f"```diff\n- Error encountered!\n# erorr:\n+ {error}```")

@blacklist.error
async def blacklist_error(ctx,error):
    await ctx.send(f"```diff\n- Error encountered!\n# erorr:\n+ {error}```")

@admon.error
async def admon_error(ctx,error):
    await ctx.send(f"```diff\n- Error encountered!\n# erorr:\n+ {error}```")

@secretping.error
async def secretping_error(ctx,error):
    await ctx.send(f"```diff\n- Error encountered!\n# erorr:\n+ {error}```")

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("wheeze you don't even have permissions to ban people")
    else:
        await ctx.send(f"```diff\n- Error encountered!\n# erorr:\n+ {error}```")

@stopabusing.error
async def stopabusing_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("lmfao no you need \"manage permissions\" to stop people from wrecking the server")
    else:
        await ctx.send(f"```diff\n- Error encountered!\n# erorr:\n+ {error}```")

@cban.error
async def cban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('You don\'t have the permission to ban others. Fuck off.')
    else:
        print(error)
@dmads.error
async def dmads_error(ctx, error):
    await ctx.send("I encountered an error while sending the invites. The user you pinged might have his DMs closed. More info about this error:")
    await ctx.send(f"```diff\n- Error encountered!\n# erorr:\n+ {error}```")

@say.error
async def say_error(ctx,error):
    await ctx.send(f"```diff\n- Error encountered!\n# erorr:\n+ {error}```")

@bon.error
async def bon_error(ctx,error):
    await ctx.send(f"```diff\n- Error encountered!\n# erorr:\n+ {error}```")

@unoreverse.error
async def unoreverse_error(ctx,error):
    await ctx.send(f"```diff\n- Error encountered!\n# erorr:\n+ {error}```")

@hmmm.error
async def hmmm_error(ctx,error):
    await ctx.send(f"```diff\n- Error encountered!\n# erorr:\n+ {error}```")

@allow.error
async def allow_error(ctx,error):
    await ctx.send(f"```diff\n- Error encountered!\n# erorr:\n+ {error}```")

@kicc.error
async def kicc_error(ctx,error):
    await ctx.send(f"```diff\n- Error encountered!\n# erorr:\n+ {error}```")

@yeet.error
async def yeet_error(ctx,error):
    await ctx.send(f"```diff\n- Error encountered!\n# erorr:\n+ {error}```")

@typefor.error
async def typefor_error(ctx,error):
    await ctx.send(f"```diff\n- Error encountered!\n# erorr:\n+ {error}```")

@ping.error
async def ping_error(ctx,error):
    await ctx.send(f"```diff\n- Error encountered!\n# erorr:\n+ {error}```")

@cutie.error
async def cutie_error(ctx,error):
    await ctx.send(f"```diff\n- Error encountered!\n# erorr:\n+ {error}```")

@uglie.error
async def uglie_error(ctx,error):
    await ctx.send(f"```diff\n- Error encountered!\n# erorr:\n+ {error}```")
@pogpong.error
async def pogpong_error(ctx,error):
    await ctx.send(f"```diff\n- Error encountered!\n# erorr:\n+ {error}```")

@setstatus.error
async def setstatus_error(ctx,error):
    await ctx.send(f"```diff\n- Error encountered!\n# erorr:\n+ {error}```")

@calc.error
async def calc_error(ctx,error):
    await ctx.send(f"```diff\n- Error encountered!\n# erorr:\n+ {error}```")

@abuse.error
async def abuse_error(ctx,error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("lmfao no you need manage permissions to let people abuse")
    else:
        await ctx.send(f"```diff\n- Error encountered!\n# erorr:\n+ {error}```")



'''with open("token.0", "r", encoding="utf-8") as f:
    bottoken = f.read()'''
client.run(os.environ['DISCORD_TOKEN'])
# betargon's ID was reset btw


