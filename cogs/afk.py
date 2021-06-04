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
import discord, datetime, time
import pytz
from pytz import timezone
import asyncio
import json
import math
import postbin, traceback

def gettraceback(error):
    etype = type(error)
    trace = error.__traceback__
    lines = traceback.format_exception(etype, error, trace)
    traceback_text = ''.join(lines)
    return traceback_text

start_time = time.time()
def secondstotiming(seconds):
    seconds = round(seconds)
    if seconds < 60:
        secdisplay = "s" if seconds != 1 else ""
        return f"{seconds} second{secdisplay}"
    else:
        minutes = math.trunc(seconds/60)
        if minutes < 60:
            seconds = seconds - minutes*60
            mindisplay = "s" if minutes != 1 else ""
            secdisplay = "s" if seconds != 1 else ""
            return f"{minutes} minute{mindisplay} and {seconds} second{secdisplay}"
        else:
            hours = math.trunc(minutes/60)
            if hours < 24:
                minutes = minutes - hours*60
                seconds = seconds - minutes*60 - hours*60*60
                hdisplay = "s" if hours != 1 else ""
                mindisplay = "s" if minutes != 1 else ""
                secdisplay = "s" if seconds != 1 else ""
                return f"{hours} hour{hdisplay}, {minutes} minute{mindisplay} and {seconds} second{secdisplay}"
            else:
                days = math.trunc(hours/24)
                if days < 7:
                    hours = hours - days*24
                    minutes = minutes - hours * 60
                    seconds = seconds - minutes * 60 - hours * 60 * 60
                    ddisplay = "s" if days != 1 else ""
                    hdisplay = "s" if hours != 1 else ""
                    mindisplay = "s" if minutes != 1 else ""
                    secdisplay = "s" if seconds != 1 else ""
                    return f"{days} day{ddisplay}, {hours} hour{hdisplay}, {minutes} minute{mindisplay} and {seconds} second{secdisplay}"
                else:
                    weeks = math.trunc(days/7)
                    days = days - weeks*7
                    hours = hours - days * 24
                    minutes = minutes - hours * 60
                    seconds = seconds - minutes * 60 - hours * 60 * 60
                    wdisplay = "s" if weeks != 1 else ""
                    ddisplay = "s" if days != 1 else ""
                    hdisplay = "s" if hours != 1 else ""
                    mindisplay = "s" if minutes != 1 else ""
                    secdisplay = "s" if seconds != 1 else ""
                    return f"{weeks} week{wdisplay}, {days} day{ddisplay}, {hours} hour{hdisplay}, {minutes} minute{mindisplay} and {seconds} second{secdisplay}"

class Afk(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Cog \"AFK\" loaded")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or message.author == self.client.user:
            return
        with open('resources/test.json', 'r', encoding='utf8') as f:
            timenow = time.time()
            afkdetails = json.load(f)
            k = list(afkdetails.keys())
            if str(message.author.id) in k:
                afktime = afkdetails[str(message.author.id)]['time']
                if timenow < afktime:
                    await message.channel.send(f"You still have {round(afktime - timenow)} more seconds to talk. ")
                    return
                else:
                    if "[AFK] " in message.author.display_name:
                        newname = message.author.display_name.replace("[AFK]", "")
                        await message.author.edit(nick=newname)
                    del afkdetails[str(message.author.id)]
                    with open('resources/test.json', 'w', encoding='utf8') as f:
                        json.dump(afkdetails, f, sort_keys=True, indent=4, ensure_ascii=False)
                        await message.channel.send(f"Welcome back {message.author.name}! I have removed your AFK status.")
            else:
                for i in k:
                    userid = int(i)
                    guildid = afkdetails[i]['guild_id']
                    afktime = afkdetails[i]['time']
                    afkmessage = afkdetails[i]['message']
                    guild = self.client.get_guild(guildid)
                    member = guild.get_member(userid)
                    if guild == message.guild and member.mentioned_in(message):
                        current_time = time.time()
                        afk_duration = int(round(current_time - afktime))
                        afk_embed = discord.Embed(title="", color=0x00ff00)
                        afk_embed.set_author(name=f"{member.name}#{member.discriminator}", icon_url=str(member.avatar_url))
                        afk_embed.add_field(name=f"{member.name} is AFK", value=afkmessage, inline=True)
                        afk_embed.set_footer(text=f"{member.name} has been AFK for {secondstotiming(afk_duration)}.")
                        await message.channel.send(embed=afk_embed)

    @commands.command(name="afk", brief="Let everyone know you are AFK",
                      description="Sets an AFK status which will tell others why you are AFK when you are pinged.")
    async def afk(self, ctx, *, message = "I am AFK!"):
        member = ctx.author
        if len(message) > 1024:
            await ctx.send("Your message for your AFK status is too long, try making it below 1024 characters.", delete_after = 5.0)
        if len(member.display_name) > 26:
            await ctx.send("Your nickname could not be changed because it exceeds nickname character limits.", delete_after = 3.0)
        else:
            try:
                await member.edit(nick=f"[AFK] {member.display_name}")
            except discord.Forbidden:
                await ctx.send("I do not have permission to change your nickname.")
        time_now = time.time()
        time_now = round(time_now)
        async with ctx.typing():
            await asyncio.sleep(1)
            with open('resources/test.json', 'r') as f:
                user = json.loads(f.read())
                k = list(user.keys())
                if str(ctx.author.id) in k:
                    await ctx.send("You have already set an AFK status, wait until your AFK status is removed (30 seconds) to set a new AFK status.")
                    return
                else:
                    user[str(ctx.author.id)] = {}
                    user[str(ctx.author.id)]['guild_id'] = ctx.guild.id
                    user[str(ctx.author.id)]['time'] = time_now+30
                    user[str(ctx.author.id)]['message'] = message
                    with open('resources/test.json', 'w', encoding='utf8') as f:
                        json.dump(user,f,sort_keys=True,indent=4,ensure_ascii=False)
                        await ctx.send(f"{member.mention} You are now AFK. message: {message}")

    @afk.error
    async def afk_error(self, ctx, error):
        errorembed = discord.Embed(title=f"Oops!",
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
    client.add_cog(Afk(client))
