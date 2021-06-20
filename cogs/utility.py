# |------------------------------------------------------------------------------------|
# |                                                                                    |
# |                                                                                    |
# |                            argonafk Cog for Nogra Bot                              |
# |                               Written by Argon#0002                                |
# |                               Commands in this cog:                                |
# |                                         NA                                         |
# |                                                                                    |
# |                                                                                    |
# |------------------------------------------------------------------------------------
from discord.utils import find
import random
import asyncio
import discord
import logging
from discord.ext import commands, menus
import json
import os
from datetime import datetime, date
import time
import nacl
from pytz import timezone
import postbin
import traceback
from cogs.nograhelpers import *
import requests
from colorthief import ColorThief
import urllib.request


def rgb_to_hex(rgb):
    return '%02x%02x%02x' % rgb


class EmbedPageSource(menus.ListPageSource):
    async def format_page(self, menu, item):
        if len(item) > 4:
            color = f"0x{item[4]}"
            color = int(color, 16)
        else:
            color = 0xFFFFFF
        embed = discord.Embed(title=item[0], description=item[1], color=color)
        if len(item) > 2:
            embed.set_thumbnail(url=item[2])
        if len(item) > 3:
            embed.set_image(url=item[3])
        return embed


def gettraceback(error):
    etype = type(error)
    trace = error.__traceback__
    lines = traceback.format_exception(etype, error, trace)
    traceback_text = ''.join(lines)
    return traceback_text


start_time = time.time()


class utility(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Cogs \"Utility\" has loaded")

    @commands.command()
    async def changelog(self, ctx):
        with ctx.typing():
            channel = self.client.get_channel(852477760089489449)
            messagelist = await channel.history(limit=30).flatten()
            messagecontents = []
            for message in messagelist:
                version = message.content.split("\n")[0]
                messagecontents.append((version, message.content))
            items = messagecontents
            menu = menus.MenuPages(EmbedPageSource(items, per_page=1))
            await menu.start(ctx)

    @commands.command(brief="gives emojis info in guild", description="Gives info about emojis in guild")
    async def emojiinfo(self, ctx):
        emojino = len(ctx.guild.emojis)
        limit = ctx.guild.emoji_limit + 50
        remaining = limit - emojino
        embed = discord.Embed(title="**__Emoji Info for " + ctx.guild.name + "__**", color=0x00ff40)
        embed.set_author(name=ctx.guild.name)
        embed.add_field(name="Number of emojis in this guild", value=str(emojino), inline=False)
        embed.add_field(name="Maximum number of emojis", value=str(limit), inline=True)
        embed.add_field(name="Remaining emojis available", value=str(remaining), inline=True)
        await ctx.send(embed=embed)

    @commands.command(brief="Shows client latency", description="shows client latency")
    async def ping(self, ctx):
        await ctx.send(f'Pong! {round(self.client.latency * 1000)}ms  🏓')
        if self.client.latency > 0.250:
            await ctx.send('Well, that is rather slow..')

    @commands.command(pass_context=True, brief="Creates channel", description="Creates a channel in a guild",
                      aliases=["cchan", "cc"])
    @commands.has_permissions(manage_channels=True)
    async def createchannel(self, ctx, *, channel_name=None):
        if channel_name is None:
            await ctx.send("You need to tell me what is the name of the channel you want to create.")
        else:
            guild = ctx.message.guild
            await guild.create_text_channel(channel_name)
            await ctx.send(f"**{channel_name}** created. <a:Tick:796984073603383296>")

    @commands.command(pass_context=True, brief="Shows my permissions",
                      description=f"Does a command not work? You can check whether I have the required permissions using this command.",
                      aliases=["permissions", "checkperms"])
    @commands.has_permissions(manage_permissions=True)
    async def checkpermissions(self, ctx, *, channel: discord.TextChannel = None):
        if channel is None:
            channel = ctx.channel
        member = ctx.guild.me
        botpermissions = channel.permissions_for(member)
        output = ""
        voice_permissions = ["connect", "speak", "mute_members", "deafen_members", "move_members",
                             "use_voice_activation"]
        for permission in iter(botpermissions):
            if permission[0] in voice_permissions:
                pass
            elif permission[1] == True:
                spacingno = 21 - len(permission[0])
                spacing = " " * spacingno
                output += f"+ {permission[0]}{spacing} =  True\n"

            elif permission[1] == False:
                spacingno = 21 - len(permission[0])
                spacing = " " * spacingno
                output += f"- {permission[0]}{spacing} = False\n"
            permissions = discord.Embed(title=f"{self.client.user.name}'s permissions in {channel.name}",
                                        description=f"```diff\n{output}\n```", color=discord.Color.random())
            permissions.set_footer(
                text=f"Does a command not work? You can check whether {self.client.user.name} has the required permissions using this command.")
        await ctx.send(embed=permissions)

    @commands.command(pass_context=True, brief="calculates", description="calculates your stupid math problems")
    async def calc(self, ctx, *, yourcalculation):
        if "^" in yourcalculation:
            yourcalculation = yourcalculation.replace("^", "**")
        result = eval(yourcalculation)
        await ctx.send(str(yourcalculation) + " = " + str(result))

    @commands.command(name="emojis", brief="Lists out emojis", description="Lists out emojis")
    async def hmmm(self, ctx):
        # allowedChannels = [813288124460826667, 802544393122742312, 810007699579338762, 800669048974213150] if ctx.channel.id in allowedChannels
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

    @commands.command(name="chatchart", brief="Lists portions of messages sent by members", description = "Shows the percentage of messages sent by various members")
    async def chatchart(self, ctx, channel:discord.TextChannel=None):
        count = {}
        if channel is None:
            channel = ctx.channel
        with ctx.typing():
            messagelist = await channel.history(limit=1000).flatten()
            messageno = len(messagelist)
            for message in messagelist:
                authorid = message.author.id
                if authorid not in count:
                    count[authorid] = 1
                else:
                    count[authorid] += 1
            output = ""
            for ele in count:
                if len(output) < 1800:
                    percentage = round((count[ele]/messageno)*100, 1)
                    output += f"<@{ele}>: {percentage}%\n"
                    colors = [0xFFE4E1, 0x00FF7F, 0xD8BFD8, 0xDC143C, 0xFF4500, 0xDEB887, 0xADFF2F, 0x800000, 0x4682B4,
                              0x006400, 0x808080, 0xA0522D, 0xF08080, 0xC71585, 0xFFB6C1, 0x00CED1]
                    embed = discord.Embed(title = f"Chat chart for {channel.name}", color=random.choice(colors))
                    embed.add_field(name="\u200b", value=output, inline=False)
                    embed.set_footer(text="this will be made into a pie chart soon!")
        await ctx.send(embed=embed)

    @createchannel.error
    async def createchannel_error(self, ctx, error):
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

    @emojiinfo.error
    async def emojiinfo_error(self, ctx, error):
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

    @hmmm.error
    async def hmmm_error(self, ctx, error):
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

    @ping.error
    async def ping_error(self, ctx, error):
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

    @checkpermissions.error
    async def checkpermissions_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.ChannelNotFound):
            await ctx.send(error)
            return
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You are missing the permission `Manage Permissions`.")
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

    @calc.error
    async def calc_error(self, ctx, error):
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

    @chatchart.error
    async def chatchart_error(self, ctx, error):
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

    @commands.command(pass_context=True)
    @commands.has_permissions(manage_guild=True)
    async def prefix(self, ctx, prefix):  # command: bl!changeprefix ...
        with open('nograresources/prefixes.json', 'r') as f:
            prefixes = json.load(f)
        prefixes[str(ctx.guild.id)] = prefix
        with open('nograresources/prefixes.json', 'w', encoding="utf8") as f:
            json.dump(prefixes, f, sort_keys=True, indent=4, ensure_ascii=False)
        await ctx.send(
            f' <a:Tick:796984073603383296> The prefix for **{ctx.guild.name}** has been changed to: `{prefix}`')

    @prefix.error
    async def prefix_error(self, ctx, error):
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

    @commands.command(name="userinfo", brief="gives you info about a user",
                      description="Gives you information about a user.", aliases=["ui", "userinformation"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def userinfo(self, ctx, member: discord.Member = None):
        today = datetime.today()
        prefix = await self.client.get_prefix(ctx)
        prefix = prefix[2]
        if member is None:
            member = ctx.author
        userinfo = discord.Embed(title=f"User info for {member.name}#{member.discriminator} ({member.id})",
                                 description="Oh hey, that's me!" if member == self.client.user else None,
                                 color=member.colour)
        acccreationdate = member.created_at
        userinfo.add_field(name="Account created on",
                           value=f"{acccreationdate.strftime('%a, %m/%d/%Y, %H:%M:%S UTC')}, {(today - acccreationdate).days} days ago",
                           inline=True)
        joindate = member.joined_at
        userinfo.add_field(name=f"Joined {ctx.guild.name} on",
                           value=f"{joindate.strftime('%a, %m/%d/%Y, %H:%M:%S UTC')}, {(today - joindate).days} days ago",
                           inline=True)
        if member.bot:
            userinfo.add_field(name="Account is a bot", value="<:bottag:855278053311774740>", inline=True)
        userinfo.add_field(name="Nickname", value=member.display_name if member.display_name != member.name else "None",
                           inline=False)
        boostdate = member.premium_since
        userinfo.add_field(name=f"Boosted {ctx.guild.name} <a:nograboostspin:855159445813198919>",
                           value=f"Yes, since {boostdate.strftime('%a, %m/%d/%Y, %H:%M:%S UTC')}, {(today - boostdate).days} days ago" if boostdate is not None else "No",
                           inline=False)
        userinfo.add_field(name="Highest role in this server", value=member.top_role.mention, inline=True)
        status = member.status
        if status == discord.Status.online:
            statusoutput = "<:nograonline:830765387422892033> Online"
        elif status == discord.Status.idle:
            statusoutput = "<:nograyellow:830765423112880148> Idle"
        elif status == discord.Status.dnd:
            statusoutput = "<:nograred:830765450412425236> Do Not Disturb"
        elif status == discord.Status.offline:
            statusoutput = "<:nograoffline:830765506792259614> Offline"
        else:
            statusoutput = "Unknown"
        userinfo.add_field(name="Status", value=statusoutput, inline=True)
        activitylist = member.activities
        for activity in activitylist:
            if isinstance(activity, discord.CustomActivity):
                customstatus = activity.name
                userinfo.add_field(name="Custom status", value=customstatus, inline=True)
            elif isinstance(activity, discord.Spotify):
                artists = ", ".join(activity.artists)
                userinfo.add_field(name="Spotify status <:nograspotify:855151063530471465>",
                                   value=f"Listening to **{artists}** - **{activity.title}**, know more in `{prefix}spotify`",
                                   inline=False)
            elif isinstance(activity, discord.Game):
                userinfo.add_field(name="Activity status 🎮",
                                   value=f"Playing **{activity.name}**, know more in `{prefix}game`",
                                   inline=False)
            elif isinstance(activity, discord.Activity):
                userinfo.add_field(name="Activity status 🎮",
                                   value=f"Playing **{activity.name}**, know more in `{prefix}game`",
                                   inline=False)
            elif isinstance(activity, discord.Streaming):
                userinfo.add_field(name="Activity status 🎮",
                                   value=f"Streaming **[{activity.name}]({activity.url})**, know more in `{prefix}game`",
                                   inline=False)
            else:
                print(f"unrecognised activity, type is {type(activity)}")

        '''userinfo.add_field(name="Account created on", value=member.created_at, inline=True)
        userinfo.add_field(name="Account created on", value=member.created_at, inline=True)
        userinfo.add_field(name="Account created on", value=member.created_at, inline=True)'''
        userinfo.set_thumbnail(url=member.avatar_url)
        await ctx.send(embed=userinfo)

    @userinfo.error
    async def userinfo_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            cooldown = error.retry_after
            await ctx.send(
                f"To prevent requests being spammed to the API, you have to wait for another **{secondstotiming(cooldown)}**.")
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

    @commands.command(name="spotify", brief="shows you what you're listening to",
                      description="Shows you what you are listening to on Spotify.", aliases=["nowplaying"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def spotify(self, ctx, member: discord.Member = None):
        today = datetime.now(timezone("UTC"))
        today = today.replace(tzinfo=None)
        if member is None:
            member = ctx.author
        activitylist = member.activities
        for activity in activitylist:
            if isinstance(activity, discord.Spotify):
                artists = ", ".join(activity.artists)
                spotify = discord.Embed(title=f"{member.name} is listening to",
                                        description=f"[{artists} - {activity.title}](https://open.spotify.com/track/{activity.track_id})",
                                        color=activity.color)
                spotify.set_author(name=f"{member.name}#{member.discriminator}", icon_url=member.avatar_url)
                spotify.set_footer(text=f"Powered by Spotify®", icon_url="https://i.imgur.com/zNBmzpl.png")
                spotify.set_thumbnail(url=activity.album_cover_url)
                listenduration = today - activity.start
                listenduration = round(listenduration.total_seconds())
                songend = round(activity.duration.total_seconds())
                position = (listenduration / songend) * 20
                position = round(position)
                duration = "────────────────────"
                bar = f" ◄◄⠀▐▐⠀►► {durationdisplay(listenduration)} / {durationdisplay(songend)} ───○ 🔊"
                duration = list(duration)
                duration.insert(position, "⚪")
                duration = "".join(duration)
                spotify.add_field(name=duration, value=bar, inline=False)
                spotify.add_field(name="Song album", value=activity.album, inline=False)
                await ctx.send(embed=spotify)
                return
        spotify = discord.Embed(title=f"{member.name} is listening to",
                                description=f"[Nothing!](https://open.spotify.com/track/3cdhgO3vgHyOIADMXokd2t?si=f7078aa59889446e)",
                                color=0x1DB954)
        spotify.set_author(name=f"{member.name}#{member.discriminator}", icon_url=member.avatar_url)
        spotify.set_thumbnail(
            url="https://lh3.googleusercontent.com/proxy/2MW-6rV-ik6QiqydtV2T5d6PEM5894IXD990hxcCp17slr5F0bj0u1xypl-0MkChbMD6MabQDSCFGFGCm6w03EMSptzUIU9Y_u1eDgzOzC_27YoSOvRFgHUw4gLfaHrB2i_ImlYuJKPOTZg3-RD1bTAYv1-S4pIHU2UkyMZ0")
        spotify.set_footer(text=f"Powered by Spotify®", icon_url="https://i.imgur.com/zNBmzpl.png")
        duration = "⚪────────────────────"
        bar = f" ◄◄⠀\▶⠀►► 0:00 / 4:31 ───○ 🔊"
        duration = list(duration)
        duration = "".join(duration)
        spotify.add_field(name=duration, value=bar, inline=False)
        spotify.add_field(name="Song album", value="Science & Faith", inline=False)
        spotify.add_field(name="Are you actually listening to something?",
                          value="Check `Settings > Connections` if you have enabled `Display Spotify as your status`. <a:catdiscovibingwaveOwO:854383648986628175>",
                          inline=False)
        await ctx.send(embed=spotify)

    @spotify.error
    async def spotify_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            cooldown = error.retry_after
            await ctx.send(
                f"To prevent requests being spammed to the API, you have to wait for another **{secondstotiming(cooldown)}**.")
            return
        if isinstance(error, commands.MemberNotFound):
            await ctx.send(error)
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

    @commands.command(name="color", brief="pfp color time",
                      description="Gets dominant and matching colors of your profile picture.", aliases=["colour"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def color(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        avatarurl = member.avatar_url
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        urllib.request.install_opener(opener)
        urllib.request.urlretrieve(f"{avatarurl}", "avatar")
        color_thief = ColorThief('avatar')
        palette = color_thief.get_palette(color_count=6)
        messagecontents = []
        for color in palette:
            hexcode = rgb_to_hex(color)
            messagecontents.append((f"{ctx.author.name}'s Profile Picture Color", f"HEX: `{hexcode}`\nRGB=`{color}`",
                                    f"https://singlecolorimage.com/get/{hexcode}/300x300", f"{avatarurl}", hexcode))
        items = messagecontents
        menu = menus.MenuPages(EmbedPageSource(items, per_page=1))
        await menu.start(ctx)

    @color.error
    async def color_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.MemberNotFound):
            await ctx.send(error)
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

    @commands.command(name="gameprofile", brief="Shows you what you are doing/playing.",
                      description="Shows you what you are doing/playing.", aliases=["game", "activity", "status"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def gameprofile(self, ctx, member: discord.Member = None):
        # sourcery no-metrics
        today = datetime.now(timezone("UTC"))
        today = today.replace(tzinfo=None)
        if member is None:
            member = ctx.author
        activitylist = member.activities
        if not activitylist:
            activityembed = discord.Embed(title=f"{member.name} isn't doing anything now!", color=member.color)
            activityembed.set_author(name=f"{member.name}#{member.discriminator}", icon_url=member.avatar_url)
            await ctx.send(embed=activityembed)
            return
        for activity in activitylist:
            if isinstance(activity, discord.Game):
                activityembed = discord.Embed(title=f"{member.name} is playing:", color=member.color)
                activityembed.set_author(name=f"{member.name}#{member.discriminator}", icon_url=member.avatar_url)
                if activity.start:
                    starttime = activity.start
                    duration = today - activity.start
                    duration = duration.total_seconds()
                    start = f"Started playing at {starttime.strftime('%a, %m/%d/%Y, %H:%M:%S UTC')}, {secondstotiming(duration)} ago"
                else:
                    start = ""
                if activity.end:
                    starttime = activity.end
                    duration = activity.end - today
                    duration = duration.total_seconds()
                    stop = f"\nWill stop playing at {starttime.strftime('%a, %m/%d/%Y, %H:%M:%S UTC')}, {secondstotiming(duration)} later"
                else:
                    stop = ""
                output = start + stop
                if output:
                    output = output
                else:
                    output = "Nothing to show here ¯\_(ツ)_/¯"
                activityembed.add_field(name=activity.name, value=output, inline=False)
                await ctx.send(embed=activityembed)
                return
            elif isinstance(activity, discord.Activity):
                activityembed = discord.Embed(title=f"{member.name} is playing:", color=member.color)
                activityembed.set_author(name=f"{member.name}#{member.discriminator}", icon_url=member.avatar_url)
                if activity.start:
                    starttime = activity.start
                    duration = today - activity.start
                    duration = duration.total_seconds()
                    start = f"Started playing at {starttime.strftime('%a, %m/%d/%Y, %H:%M:%S UTC')}\n ╹── ({secondstotiming(duration)} ago"
                else:
                    start = ""
                if activity.end:
                    starttime = activity.end
                    duration = activity.end - today
                    duration = duration.total_seconds()
                    stop = f"\nWill stop playing at {starttime.strftime('%a, %m/%d/%Y, %H:%M:%S UTC')}\n ╹── {secondstotiming(duration)} later"
                else:
                    stop = ""
                keydetails = ""
                if activity.details:
                    keydetails += f"**{activity.details}**\n"
                if activity.state:
                    keydetails += f"**{activity.state}\n**"
                    output = start + stop
                if output:
                    keydetails += output
                if activity.large_image_url:
                    activityembed.set_thumbnail(url=f'{activity.large_image_url}')
                activityembed.add_field(name=activity.name, value=keydetails, inline=False)
                await ctx.send(embed=activityembed)
                return
            elif isinstance(activity, discord.Streaming):
                if activity.platform == "Twitch" or activity.platform not in ["YouTube", "Twitch"]:
                    platform = "Twitch <:nogratwitch:855401374795563009>"
                elif activity.platform == "YouTube":
                    platform = "YouTube <:nograyoutube:855401359003090956>"
                activityembed = discord.Embed(title=f"{member.name} is streaming:",
                                              description=f'[{activity.name} on {platform}]({activity.url} "{activity.name} on {activity.platform}")',
                                              color=member.color)
                activityembed.set_author(name=f"{member.name}#{member.discriminator}", icon_url=member.avatar_url)
                activityembed.add_field(name="Steam details", value=f"Playing {activity.game}", inline=False)
                await ctx.send(embed=activityembed)
                return
        activityembed = discord.Embed(title=f"{member.name} isn't doing anything now!", color=member.color)
        activityembed.set_author(name=f"{member.name}#{member.discriminator}", icon_url=member.avatar_url)
        await ctx.send(embed=activityembed)

    @gameprofile.error
    async def gameprofile_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            cooldown = error.retry_after
            await ctx.send(
                f"To prevent requests being spammed to the API, you have to wait for another **{secondstotiming(cooldown)}**.")
            return
        if isinstance(error, commands.MemberNotFound):
            await ctx.send(error)
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
    client.add_cog(utility(client))
