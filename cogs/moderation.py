# |------------------------------------------------------------------------------------|
# |                                                                                    |
# |                                                                                    |
# |                            Moderation Cog for Nogra Bot                            |
# |                               Written by Argon#0002                                |
# |                               Commands in this cog:                                |
# |                clear, uptime, invite, abuse, stopabusing, ban, cban                |
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
import postbin
import traceback
import json
import random
from cogs.nograhelpers import *


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

class Moderation(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Cog \"Moderation\" loaded")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.client.user:
            return
        with open('nograresources/shutup.json', 'r', encoding='utf8') as f:
            channeldetails = json.load(f)

        if str(message.guild.id) not in channeldetails:
            channeldetails[str(message.guild.id)] = {
                'blacklist_channels': [],
                'logging_channels': None,
            }

            with open('nograresources/shutup.json', 'w', encoding='utf8') as f:
                json.dump(channeldetails, f, sort_keys=True, indent=4, ensure_ascii=False)
            await message.channel.send("The shut-up feature is now online for Nogra. You can prevent people from talking in a channel while keeping their perms to send messages.\nUse `a.shutup add/remove [channel]` to make a channel shut up and `a.idot add/remove [channel]` if you want people to get pinged for why they cannot talk.")
        else:
            blacklisted_channels = channeldetails[str(message.guild.id)]['blacklist_channels']
            if len(blacklisted_channels) != 0:
                if message.channel.id in blacklisted_channels:
                    await message.delete()
                    idotchannels = channeldetails[str(message.guild.id)]['logging_channels']
                    if idotchannels is not None:
                        idotchannel = self.client.get_channel(idotchannels)
                        await idotchannel.send("**" + str(message.author.mention) + "**, if you continue to talk in <#" + str(message.channel.id) + "> i'm gonna have to mute you <a:pik:801091998290411572>")

    @commands.command(pass_context=True, name="shutup", brief="Sets blacklisted channels for talking",
                      description="Sets channels where people can talk but will have their messages deleted.")
    @commands.has_permissions(manage_messages=True)
    async def shutup(self, ctx, addremoveview=None, channel: discord.TextChannel = None):
        prefix = await self.client.get_prefix(ctx)
        prefix = prefix[2]
        if addremoveview is None:
            await ctx.send(
                "```\n[p]shutup [add/remove/view] [channel]\n          ^^^^^^^^^^^^^^^^^\nYou missed out add/remove/view!```")
            return
        addremoveview = addremoveview.lower()
        with open('nograresources/shutup.json', 'r', encoding='utf8') as f:
            channeldetails = json.load(f)
        blacklisted_channels = channeldetails[str(ctx.guild.id)]['blacklist_channels']
        if addremoveview == "view":
            if len(blacklisted_channels) == 0:
                output = f"You have not added any channels yet. Use `{prefix}shutup add [channel]` to do so!"
            else:
                output = ""
                for i in blacklisted_channels:
                    if len(output) < 1024:
                        output += f"<#{i}>\n"
            colors = [0xFFE4E1, 0x00FF7F, 0xD8BFD8, 0xDC143C, 0xFF4500, 0xDEB887, 0xADFF2F, 0x800000, 0x4682B4,
                      0x006400, 0x808080, 0xA0522D, 0xF08080, 0xC71585, 0xFFB6C1, 0x00CED1]
            embed = discord.Embed(title=f"Blacklisted channels in {ctx.guild.name}", color=random.choice(colors))
            embed.add_field(name="\u200b", value=output, inline=False)
            await ctx.send(embed=embed)
        elif addremoveview == "add":
            if channel is None:
                await ctx.send(
                    "```\n[p]idot [set/remove/view] [channel]\n                          ^^^^^^^^^\nYou missed out [channel]!```")
                return
            with open('nograresources/shutup.json', 'r', encoding='utf8') as f:
                channeldetails = json.load(f)
            blacklisted_channels = channeldetails[str(ctx.guild.id)]['blacklist_channels']
            if channel.id in blacklisted_channels:
                await ctx.send(f"{channel.name} is already blacklisted!")
                return
            blacklisted_channels.append(channel.id)
            channeldetails[str(ctx.guild.id)]['blacklist_channels'] = blacklisted_channels
            with open('nograresources/shutup.json', 'w', encoding='utf8') as f:
                json.dump(channeldetails, f, sort_keys=True, indent=4, ensure_ascii=False)
            await ctx.send(f"<a:Tick:796984073603383296> {channel.mention} successfully added to blacklist list.\nMessages sent in **{channel.name}** will be deleted from now onwards.")
            return
        elif addremoveview == "remove":
            if channel is None:
                await ctx.send(
                    "```\n[p]idot [set/remove/view] [channel]\n                          ^^^^^^^^^\nYou missed out [channel]!```")
                return
            with open('nograresources/shutup.json', 'r', encoding='utf8') as f:
                channeldetails = json.load(f)
            blacklisted_channels = channeldetails[str(ctx.guild.id)]['blacklist_channels']
            if channel.id not in blacklisted_channels:
                await ctx.send(f"{channel.name} was never blacklisted.")
                return
            blacklisted_channels.remove(channel.id)
            channeldetails[str(ctx.guild.id)]['blacklist_channels'] = blacklisted_channels
            with open('nograresources/shutup.json', 'w', encoding='utf8') as f:
                json.dump(channeldetails, f, sort_keys=True, indent=4, ensure_ascii=False)
            await ctx.send(f"<a:Tick:796984073603383296> {channel.mention} removed from blacklist list.\nMessages sent in **{channel.name}** will no longer be deleted.")
            return
        else:
            await ctx.send("Your first option needs to be a `add`/`remove`/`view` so that I will know whether to add, remove or view channels.")

    @commands.command(pass_context=True, name="idot", brief="Sets logging channel",
                      description="If people talk in blacklisted channels, use this command to log their talking here.")
    @commands.has_permissions(manage_channels=True)
    async def idot(self, ctx, setremoveview=None, channel: discord.TextChannel = None):
        prefix = await self.client.get_prefix(ctx)
        prefix = prefix[2]
        if setremoveview is None:
            await ctx.send(
                "```\n[p]idot [add/remove/view] [channel]\n        ^^^^^^^^^^^^^^^^^\nYou missed out add/remove/view!```")
            return
        setremoveview = setremoveview.lower()
        with open('nograresources/shutup.json', 'r', encoding='utf8') as f:
            channeldetails = json.load(f)
        logging_channels = channeldetails[str(ctx.guild.id)]['logging_channels']
        if setremoveview == "view":
            if logging_channels is None:
                output = f"You have not added any channels yet. Use `{prefix}idot add [channel` to do so!"
            else:
                output = f"<#{logging_channels}>"
            colors = [0xFFE4E1, 0x00FF7F, 0xD8BFD8, 0xDC143C, 0xFF4500, 0xDEB887, 0xADFF2F, 0x800000, 0x4682B4,
                      0x006400, 0x808080, 0xA0522D, 0xF08080, 0xC71585, 0xFFB6C1, 0x00CED1]
            embed = discord.Embed(title=f"Logging channels in {ctx.guild.name}", color=random.choice(colors))
            embed.add_field(name="\u200b", value=output, inline=False)
            await ctx.send(embed=embed)
        elif setremoveview == "remove":
            with open('nograresources/shutup.json', 'r', encoding='utf8') as f:
                channeldetails = json.load(f)
            logging_channels = channeldetails[str(ctx.guild.id)]['logging_channels']
            if logging_channels is None:
                await ctx.send("You have not set a logging channel.")
                return
            channeldetails[str(ctx.guild.id)]['logging_channels'] = None
            with open('nograresources/shutup.json', 'w', encoding='utf8') as f:
                json.dump(channeldetails, f, sort_keys=True, indent=4, ensure_ascii=False)
            await ctx.send(
                "<a:Tick:796984073603383296> Removed the logging channel.")
        elif setremoveview == "set":
            if channel is None:
                await ctx.send("```\n[p]idot [set/remove/view] [channel]\n                          ^^^^^^^^^\nYou missed out [channel]!\n```")
                return
            with open('nograresources/shutup.json', 'r', encoding='utf8') as f:
                channeldetails = json.load(f)
            logging_channels = channeldetails[str(ctx.guild.id)]['logging_channels']
            if logging_channels is not None and logging_channels == channel.id:
                await ctx.send(f"{channel.name} is already set as the logging channel!.")
                return
            channeldetails[str(ctx.guild.id)]['logging_channels'] = channel.id
            with open('nograresources/shutup.json', 'w', encoding='utf8') as f:
                json.dump(channeldetails, f, sort_keys=True, indent=4, ensure_ascii=False)
            await ctx.send(f"<a:Tick:796984073603383296> Successfully set {channel.mention} as the logging channel.\nWhen a message is sent in blacklisted channels, it will be logged here.")
        else:
            await ctx.send("Your first option needs to be a `set`/`remove`/`view` so that I will know whether to set, remove or add channels.")

    @commands.command(pass_context=True, name="purge", brief="Purges messages", description="purges messages",
                      aliases=["clear"])
    @commands.has_permissions(manage_channels=True)
    async def purge(self, ctx, number=None):
        if number is None:
            await ctx.send("Try again, but do tell me how many messages do you want to clear.")
        else:
            number = int(number)
            await ctx.channel.purge(limit=number + 1, check=lambda msg: not msg.pinned)
            await ctx.send(str(number) + " messages were cleared in bulk. <a:Tick:796984073603383296>",
                           delete_after=3.0)
            # choosing a channel to send the ar.lear mod log if command is used in different servers

            if ctx.guild.id == 738632364208554095:
                channel = self.client.get_channel(762898168803229707)
            if ctx.guild.id == 781056775544635412:
                channel = self.client.get_channel(781064310758572063)
            if ctx.guild.id == 789840820563476482:
                channel = self.client.get_channel(802786241799651330)
            if ctx.guild.id == 818436261873844224:
                channel = self.client.get_channel(821042412624412733)
            else:
                channel = self.client.get_channel(818436261891014663)
            timestamp = ctx.message.created_at
            clearembed = discord.Embed(title="`Clear` action done with Nogra", color=0xff0000)
            clearembed.set_author(name=str(ctx.author.name) + "#" + str(ctx.author.discriminator),
                                  icon_url=str(ctx.author.avatar_url))
            clearembed.add_field(name=str(number) + " messages deleted", value="in " + str(ctx.channel.mention),
                                 inline=False)
            clearembed.set_footer(text="ID: " + str(ctx.author.id) + " • " + str(timestamp))
            await channel.send(embed=clearembed)

    @commands.command(pass_context=True, name="uptime", brief="Uptime go brr", description="Shows you Nogra's uptime.")
    async def uptime(self, ctx):
        current_time = time.time()
        current_datetime = datetime.datetime.now(timezone("UTC"))
        difference = int(round(current_time - start_time))
        embed = discord.Embed(colour=0xc8dc6c)
        embed.set_author(name=self.client.user.name, icon_url=str(self.client.user.avatar_url))
        embed.add_field(name="Time of last reboot", value=timetosgtime(utcbootime), inline=True)
        embed.add_field(name="Time now", value=timetosgtime(current_datetime), inline=True)
        embed.add_field(name="Uptime", value=secondstotiming(difference), inline=False)
        embed.set_footer(text="Time is in GMT+8 (Asia/Singapore)")
        try:
            await ctx.send(embed=embed)
        except discord.HTTPException:
            await ctx.send("Current uptime: " + secondstotiming(difference))

    @commands.command(name="invite", brief="Invite the bot", description="Gives you invite links for Nogra")
    async def invite(self, ctx):
        embed = discord.Embed(colour=0x00FF00)
        embed.set_author(name=f"Add {self.client.user.name} to your server!", icon_url=str(self.client.user.avatar_url))
        embed.add_field(name="Recommended Invite Link",
                        value="[Nogra with only necessary permissions](https://discord.com/oauth2/authorize?client_id=800184970298785802&permissions=1544416503&scope=bot)")
        embed.add_field(name="Admin Invite Link",
                        value="[Nogra with Admin Invite Permission](https://discord.com/api/oauth2/authorize?client_id=800184970298785802&permissions=8&scope=bot)")
        embed.set_thumbnail(url=str(self.client.user.avatar_url))
        try:
            await ctx.send(embed=embed)
        except discord.HTTPException:
            await ctx.send(f"Invite {self.client.user.name} to your server with only necessary permissions here **(Recommended): https://discord.com/api/oauth2/authorize?client_id=800184970298785802&permissions=8&scope=bot\n")

    @uptime.error
    async def uptime_error(self, ctx, error):
        errorembed = discord.Embed(title="Oops!",
                                   description="This command just received an error. It has been sent to Argon.",
                                   color=0x00ff00)
        errorembed.add_field(name="Error", value=f"```{error}```", inline=False)
        errorembed.set_thumbnail(url="https://cdn.discordapp.com/emojis/834753936023224360.gif?v=1")
        await ctx.send(embed=errorembed)
        logchannel = self.client.get_channel(839016255733497917)
        await logchannel.send(
            f"In {ctx.guild.name}, a command was executed by {ctx.author.mention}: `{ctx.message.content}`, which received an error: `{error}`\nMore details:")
        message = await logchannel.send("Uploading traceback to Hastebin...")
        tracebacklink = await postbin.postAsync(gettraceback(error))
        await message.edit(content=tracebacklink)

    @commands.command(brief="ban hammer", description = "Bans members")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member = None, *, reason=None):
        if member is None or member == ctx.message.author:
            await ctx.send("You cannot ban yourself...")
            return
        if member.top_role >= ctx.author.top_role:
            await ctx.send(
                f"You cannot ban {member.name} as your highest role is the same as or lower than your target's highest role.")
            return
        if reason is None:
            reason = "No specified reason"
        message = f"You have been banned from {ctx.guild.name} for: {reason}"
        if not member.bot:
            try:
                await member.send(message)
            except discord.errors.Forbidden:
                pass
        await member.ban(reason=reason)
        await ctx.send(f"{member} is banned for: {reason}")

    @commands.command(brief="Ban members with a countdown in minutes", description = "Ban members with a countdown specified by you")
    @commands.has_permissions(ban_members=True)
    async def cban(self, ctx, member: discord.Member = None, duration=None, *, reason=None):
        if member.bot:
            await member.ban(reason=reason)
            await ctx.send(f"{member} is banned for: {reason}")
        if member is None or member == ctx.message.author:
            await ctx.send("You cannot ban yourself...")
            return
        if duration is None:
            await ctx.send(
                "You need to specify how long before " + member.name + " is banned. <:nograpepeuhh:803857251072081991>")
        if member.top_role >= ctx.author.top_role:
            await ctx.send(f"You cannot ban {member.name} as your highest role is the same as or lower than your target's highest role.")
            return
        timer = int(duration) * 60
        await ctx.send("Alright, I will ban " + member.name + " in " + duration + " minutes.")
        await asyncio.sleep(timer)
        if reason is None:
            reason = "no specified reason"
        message = f"You have been banned from {ctx.guild.name} for: {reason}"
        if not member.bot:
            try:
                await member.send(message)
            except discord.errors.Forbidden:
                pass
        await member.ban(reason=reason)
        await ctx.send(f"{member} is banned for: {reason}")


    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You are missing the permission `Ban Members`.")
        elif isinstance(error, commands.MemberNotFound):
            await ctx.send("You did not provide a proper user. It has to be a mention or user ID.")
            return
        else:
            errorembed = discord.Embed(title="Oops!",
                                       description="This command just received an error. It has been sent to Argon.",
                                       color=0x00ff00)
            errorembed.add_field(name="Error", value=f"```{error}```", inline=False)
            errorembed.set_thumbnail(url="https://cdn.discordapp.com/emojis/834753936023224360.gif?v=1")
            await ctx.send(embed=errorembed)
            logchannel = self.client.get_channel(839016255733497917)
            await logchannel.send(
                f"In {ctx.guild.name}, a command was executed by {ctx.author.mention}: `{ctx.message.content}`, which received an error: `{error}`\nMore details:")
            message = await logchannel.send("Uploading traceback to Hastebin...")
            tracebacklink = await postbin.postAsync(gettraceback(error))
            await message.edit(content=tracebacklink)

    @cban.error
    async def cban_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            error = error.original
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("wheeze you don't even have permissions to ban people")
        elif isinstance(error, ValueError):
            await ctx.send("You did not provide a proper countdown number.")
            return
        elif isinstance(error, commands.MemberNotFound):
            await ctx.send("You did not provide a proper user. It has to be a mention or user ID.")
            return
        else:
            errorembed = discord.Embed(title="Oops!",
                                       description="This command just received an error. It has been sent to Argon.",
                                       color=0x00ff00)
            errorembed.add_field(name="Error", value=f"```{error}```", inline=False)
            errorembed.set_thumbnail(url="https://cdn.discordapp.com/emojis/834753936023224360.gif?v=1")
            await ctx.send(embed=errorembed)
            logchannel = self.client.get_channel(839016255733497917)
            await logchannel.send(
                f"In {ctx.guild.name}, a command was executed by {ctx.author.mention}: `{ctx.message.content}`, which received an error: `{error}`\nMore details:")
            message = await logchannel.send("Uploading traceback to Hastebin...")
            tracebacklink = await postbin.postAsync(gettraceback(error))
            await message.edit(content=tracebacklink)

    @purge.error
    async def purge_error(self, ctx, error):
        if isinstance(error, ValueError):
            await ctx.send("You did not provide a proper number of messages to be blacklisted.")
            return
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You are missing the permission: `Manage Messages`.")
            return
        errorembed = discord.Embed(title="Oops!",
                                   description="This command just received an error. It has been sent to Argon.",
                                   color=0x00ff00)
        errorembed.add_field(name="Error", value=f"```{error}```", inline=False)
        errorembed.set_thumbnail(url="https://cdn.discordapp.com/emojis/834753936023224360.gif?v=1")
        await ctx.send(embed=errorembed)
        logchannel = self.client.get_channel(839016255733497917)
        await logchannel.send(
            f"In {ctx.guild.name}, a command was executed by {ctx.author.mention}: `{ctx.message.content}`, which received an error: `{error}`\nMore details:")
        message = await logchannel.send("Uploading traceback to Hastebin...")
        tracebacklink = await postbin.postAsync(gettraceback(error))
        await message.edit(content=tracebacklink)

    @shutup.error
    async def shutup_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You need `Manage Channels` to use this command.")
            return
        if isinstance(error, commands.ChannelNotFound):
            await ctx.send("You did not provide a proper channel. It has to be a mention or ID.")
            return
        errorembed = discord.Embed(title="Oops!",
                                   description="This command just received an error. It has been sent to Argon.",
                                   color=0x00ff00)
        errorembed.add_field(name="Error", value=f"```{error}```", inline=False)
        errorembed.set_thumbnail(url="https://cdn.discordapp.com/emojis/834753936023224360.gif?v=1")
        await ctx.send(embed=errorembed)
        logchannel = self.client.get_channel(839016255733497917)
        await logchannel.send(
            f"In {ctx.guild.name}, a command was executed by {ctx.author.mention}: `{ctx.message.content}`, which received an error: `{error}`\nMore details:")
        message = await logchannel.send("Uploading traceback to Hastebin...")
        tracebacklink = await postbin.postAsync(gettraceback(error))
        await message.edit(content=tracebacklink)

    @idot.error
    async def idot_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You need `Manage Channels` to use this command.")
            return
        if isinstance(error, commands.ChannelNotFound):
            await ctx.send("You did not provide a proper channel. It has to be a mention or ID.")
            return
        errorembed = discord.Embed(title="Oops!",
                                   description="This command just received an error. It has been sent to Argon.",
                                   color=0x00ff00)
        errorembed.add_field(name="Error", value=f"```{error}```", inline=False)
        errorembed.set_thumbnail(url="https://cdn.discordapp.com/emojis/834753936023224360.gif?v=1")
        await ctx.send(embed=errorembed)
        logchannel = self.client.get_channel(839016255733497917)
        await logchannel.send(
            f"In {ctx.guild.name}, a command was executed by {ctx.author.mention}: `{ctx.message.content}`, which received an error: `{error}`\nMore details:")
        message = await logchannel.send("Uploading traceback to Hastebin...")
        tracebacklink = await postbin.postAsync(gettraceback(error))
        await message.edit(content=tracebacklink)



def setup(client):
    client.add_cog(Moderation(client))
