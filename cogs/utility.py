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
from discord.ext import commands
import json
import os
import datetime, time
from datetime import datetime as dt
from datetime import date
import nacl
from pytz import timezone
import postbin, traceback

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

    @commands.command(pass_context=True, brief="Creates channel", description="Creates a channel in a guild", aliases=["cchan", "cc"])
    @commands.has_permissions(manage_channels=True)
    async def createchannel(self, ctx, *, channel_name=None):
        if channel_name is None:
            await ctx.send("You need to tell me what is the name of the channel you want to create.")
        else:
            guild = ctx.message.guild
            await guild.create_text_channel(channel_name)
            await ctx.send(f"**{channel_name}** created. <a:Tick:796984073603383296>")

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
        if channel == None:
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
                    output = output + f"<@{ele}>: {percentage}%\n"
                    colors = [0xFFE4E1, 0x00FF7F, 0xD8BFD8, 0xDC143C, 0xFF4500, 0xDEB887, 0xADFF2F, 0x800000, 0x4682B4,
                              0x006400, 0x808080, 0xA0522D, 0xF08080, 0xC71585, 0xFFB6C1, 0x00CED1]
                    embed = discord.Embed(title = f"Chat chart for {channel.name}", color=random.choice(colors))
                    embed.add_field(name="\u200b", value=output, inline=False)
                    embed.set_footer(text="this will be made into a pie chart soon!")
        await ctx.send(embed=embed)


    @createchannel.error
    async def createchannel_error(self, ctx, error):
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

    @emojiinfo.error
    async def emojiinfo_error(self, ctx, error):
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

    @hmmm.error
    async def hmmm_error(self, ctx, error):
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

    @ping.error
    async def ping_error(self, ctx, error):
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

    @calc.error
    async def calc_error(self, ctx, error):
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

    @chatchart.error
    async def chatchart_error(self, ctx, error):
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
    client.add_cog(utility(client))
