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
from discord.ext import commands, tasks
import sqlite3
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

class timestringError(Exception):
    def __init__(self, message="You did not send a proper duration/timestring. \nAn example of a proper duration would be `1d2h3m4s` to represent 1 day, 2 hours, 3 minutes and 4 seconds."):            
        self.message = message
        super().__init__(self.message)

class Moderation(commands.Cog):

    def __init__(self, client):
        self.description = "🛡️ Keep your server safe and healthy."
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Cog \"Moderation\" loaded")

    async def cog_command_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.ChannelNotFound):
            await ctx.send(error)
            return

        if isinstance(error, timestringError):
            await ctx.send("You did not send a proper duration/timestring. \nAn example of a proper duration would be `1d2h3m4s` to represent 1 day, 2 hours, 3 minutes and 4 seconds.")
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
        if message.author == self.client.user or isinstance(message.channel, discord.DMChannel):
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

    @commands.command(name="role", brief = "add/remove roles", description="Adds or remove roles from a member.")    
    @commands.has_permissions(manage_roles = True)                    
    async def role(self, ctx, member:discord.Member = None, *, role:discord.Role = None):
        if role in member.roles:
            try:
                await member.remove_roles(role, reason=f"Role removal for {member.name}#{member.discriminator} requested by {ctx.author.name}#{ctx.author.discriminator}")
                await ctx.send(f"Removed **{role.name}** from **{member.name}#{member.discriminator}**.")
            except discord.errors.Forbidden:
                await ctx.send(f"I do not have the permission to remove **{role.name}** from **{member.name}#{member.discriminator}**.")
                return
        else:
            try:
                await member.add_roles(role, reason=f"Role addition for {member.name}#{member.discriminator} requested by {ctx.author.name}#{ctx.author.discriminator}")
                await ctx.send(f"Added **{role.name}** to **{member.name}#{member.discriminator}**.")
            except discord.errors.Forbidden:
                await ctx.send(f"I do not have the permission to add **{role.name}** to **{member.name}#{member.discriminator}**.")
                return

    @commands.command(name="temprole", brief = "add/remove roles", description="Adds or remove roles from a member.", aliases = ["temporaryrole"])
    async def role(self, ctx, member:discord.Member = None, *, role:discord.Role = None):
        if role in member.roles:
            try:
                await member.remove_roles(role, reason=f"Role removal for {member.name}#{member.discriminator} requested by {ctx.author.name}#{ctx.author.discriminator}")
                await ctx.send(f"Removed **{role.name}** from **{member.name}#{member.discriminator}**.")
            except discord.errors.Forbidden:
                await ctx.send(f"I do not have the permission to remove **{role.name}** from **{member.name}#{member.discriminator}**.")
                return
        else:
            try:
                await member.add_roles(role, reason=f"Role addition for {member.name}#{member.discriminator} requested by {ctx.author.name}#{ctx.author.discriminator}")
                await ctx.send(f"Added **{role.name}** to **{member.name}#{member.discriminator}**.")
            except discord.errors.Forbidden:
                await ctx.send(f"I do not have the permission to add **{role.name}** to **{member.name}#{member.discriminator}**.")
                return


    @commands.command(name="slowmode", brief="Sets slowmode", description="Sets or changes the slowmode in a channel.",
                      aliases=["sm"])
    @commands.has_permissions(manage_messages=True)
    async def slowmode(self, ctx, channel:Union[discord.TextChannel, str] = None, duration = None):
        if channel is None:
            await ctx.channel.edit(slowmode_delay = 0, reason = f"Channel edit requested by {ctx.author.name}#{ctx.author.discriminator}")
            await ctx.send(f"The slowmode in {ctx.channel.name} has been changed to **0 seconds.**")

        if isinstance(channel, discord.TextChannel):
            if duration is None:
                duration = 0
                await channel.edit(slowmode_delay = duration, reason = f"Channel edit requested by {ctx.author.name}#{ctx.author.discriminator}")
                await ctx.send(f"The slowmode in {channel.name} has been changed to **{secondstotiming(duration)}**.")
                return
            duration = stringtotime(duration)
            if duration is None:
                raise timestringError
            duration = int(duration)
            if duration is None:
                duration = 0
            if duration > 21600:
                duration = 21600
            if duration < 0:
                duration = 0
            await channel.edit(slowmode_delay = duration, reason = f"Channel edit requested by {ctx.author.name}#{ctx.author.discriminator}")
            await ctx.send(f"The slowmode in {channel.name} has been changed to **{secondstotiming(duration)}**.")
        elif isinstance(channel, str):
            duration = stringtotime(channel)
            if duration is None:
                raise timestringError
            duration = int(duration)
            if duration > 21600:
                duration = 21600
            if duration < 0:
                duration = 0
            await ctx.channel.edit(slowmode_delay = duration, reason = f"Channel edit requested by {ctx.author.name}#{ctx.author.discriminator}")
            await ctx.send(f"The slowmode in {ctx.channel.name} has been changed to **{secondstotiming(duration)}**.")



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

    @commands.command(name="leave", brief="Makes the bot leave", description="Makes the bot leave.", aliases=["bye", "goodbye"])
    @commands.has_permissions(manage_guild=True)
    async def leave(self, ctx):
        if ctx.author.id in [642318626044772362, 749983318795354122]:
            await ctx.send("You have been locked from using this command. Ask the developer for more information.")
            return
        await ctx.send(
            f"**WARNING**\nAre you sure you want to remove {self.client.user.name} from {ctx.guild.name}? This will erase all configurations you have set to Nogra.`(y/n)`")
        try:
            confirmation = await self.client.wait_for("message",check=lambda m: m.channel == ctx.channel and m.author == ctx.author, timeout=20.0) 
        except asyncio.TimeoutError:
            await ctx.send("I did not get a response from you.")
            return
        if "y" in confirmation.content or "Y" in confirmation.content:
            requester = ctx.author
            reasons = [
                ("1️⃣", "No longer needed it", "We will try to make our features more inclusive for your use. "), 
                ("2️⃣", "It didn't meet my needs", "You can always DM the developer about a suggestion, but we are always working to include more features. "), 
                ("3️⃣", "Found an alternative bot", "There will always be bots which have the same or higher capabilities with us, and we understand that. "), 
                ("4️⃣", "Quality was less than expected", f"You can always report bugs to the developer, or suggest how we can improve {self.client.user.name}. "), 
                ("5️⃣", "It was not easy to use", "As much as we made it accessible, we may have been shortsighted for some features. You can inform DM the developer if it is not easy to use, or ask for support. "), 
                ("6️⃣", "It was not easy to reach support", f"As {self.client.user.name} is still a fairly small bot, a server is not required for support. Instead, you can DM the developer, Argon#0002. "), 
                ("7️⃣", "Others", "Thank you for your input! ")]
            survey = ""
            for reason in reasons:
                survey += f"{reason[0]} {reason[1]}\n"
            try:
                await requester.send(f"Before {self.client.user.name} leaves your server, I would like to ask you to answer this survey. If you do not want to answer the survey, you can leave it untouched until I leave your server.\nWhat was the primary reason for removing {self.client.user.name} from your server?\n{survey}Type the appropriate number corresponding to your reason.")
            except discord.HTTPException:
                await ctx.send(f"{requester.mention} I am now leaving **{ctx.guild.name}**.")
                await ctx.guild.leave()
                return
            else:
                await ctx.send("Please check your DMs!")
                try:
                    option = await self.client.wait_for("message",check=lambda m: m.content in ["1", "2", "3", "4", "5", "6", "7"] and isinstance(m.channel, discord.DMChannel) and m.author == ctx.author, timeout=20.0) 
                except asyncio.TimeoutError:
                    pass
                else:
                    option = int(option.content)
                    if option == 7:
                        await requester.send(f"Please tell us why you are removing Nogra from your server, within 2 minutes.")
                        try:
                            feedback = await self.client.wait_for("message",check=lambda m: isinstance(m.channel, discord.DMChannel) and m.author == ctx.author, timeout=120.0) 
                        except asyncio.TimeoutError:
                            pass
                    option = option-1
                    logchannel = self.client.get_channel(861956356419616808)
                    leaveembed = discord.Embed(title=f"Just removed {self.client.user.name} from the server {ctx.guild.name}.")
                    leaveembed.set_author(name = f"{ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})", icon_url=ctx.author.avatar_url)
                    leaveembed.add_field(name="Reason", value =reasons[option][1], inline=False)
                    leaveembed.set_thumbnail(url="https://cdn.discordapp.com/emojis/755954448009920592.gif?v=1")
                    if 'feedback' in locals():
                        leaveembed.add_field(name="Additional Information", value =f"\u200b{feedback.content}", inline=False)
                    leaveembed.set_footer(text=f"{self.client.user.name}#{self.client.user.discriminator}", icon_url=self.client.user.avatar_url)
                    await logchannel.send(embed=leaveembed)
                    await requester.send(f"{reasons[option][2]} Thank you for inviting {self.client.user.name}!")
                await requester.send(f"I have left **{ctx.guild.name}**.")
            await ctx.guild.leave()
            return
        else:
            await ctx.send("I'll be staying here then <:thethumb:852486551867097089>")
            return

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
                        value=f"[Nogra with only necessary permissions](https://discord.com/oauth2/authorize?client_id={self.client.user.id}&permissions=1544416503&redirect_uri=https://nogra.me/thank-you&response_type=code&scope=bot)")
        embed.add_field(name="Admin Invite Link",
                        value=f"[Nogra with Admin Invite Permission](https://discord.com/api/oauth2/authorize?client_id={self.client.user.id}&permissions=8&redirect_uri=https://nogra.me/thank-you&response_type=code&scope=bot)")
        embed.set_thumbnail(url=str(self.client.user.avatar_url))
        try:
            await ctx.send(embed=embed)
        except discord.HTTPException:
            await ctx.send(f"Invite {self.client.user.name} to your server with only necessary permissions here **(Recommended): https://discord.com/api/oauth2/authorize?client_id=800184970298785802&permissions=8&redirect_uri=https://nogra.me/thank-you&response_type=code&scope=bot\n")

    @commands.command(brief="ban hammer", description = "Bans members")
    @commands.has_permissions(create_instant_invite =  True, kick_members = True, ban_members =  True, administrator = False, manage_channels =  True, manage_guild =  True, add_reactions =  True, view_audit_log =  True, priority_speaker = False, stream = False, read_messages =  True, send_messages =  True, send_tts_messages =  True, manage_messages =  True, embed_links =  True, attach_files =  True, read_message_history =  True, mention_everyone = False, external_emojis =  True, view_guild_insights =  True, change_nickname =  True, manage_nicknames =  True, manage_roles =  True, manage_webhooks = False, manage_emojis =  True)
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




def setup(client):
    client.add_cog(Moderation(client))
