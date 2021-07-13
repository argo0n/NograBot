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
import PIL
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
from PIL import Image, ImageFilter
import pyimgur

IMGUR_CLIENT_ID = os.environ['IMGUR_API_ID']
im = pyimgur.Imgur(IMGUR_CLIENT_ID)


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


class Imgen(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.description = "🖼️ Image Generation"

    async def cog_command_error(self, ctx, error):
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
        if isinstance(error, commands.CommandInvokeError):
            error = error.original
        if isinstance(error, PIL.UnidentifiedImageError):
            await ctx.send(
                f"I could not open this image. Supported image formats: `.jpg`, `.jfif`, `.jpeg`, `.j2p`, `.bmp`, `.png`, `.apng`, `.ico`, `.gif`, `.pcx`, `.dds`, `.dib`, `.eps`, `.icns`, `.im`, `.msp` in the form of an **attachment** or **image link**.\nIf the file you provided is one of these formats, it is most likely the image is corrupted.")
        else:
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
    async def on_ready(self):
        print("Cogs \"Image Generation\" has loaded")

    @commands.command(name="spoilerbanner", brief="Spoiler banner",
                      description="Converts the image link that you give into a banner with a spoiler tag. Kinda realistic. \nTakes in specific image formats, resizes them into the proper dimensions, and returns it as a png.")
    async def spoilerbanner(self, ctx, imagelink=None):
        newfilename = f"temp/attach{random.randint(1, 9999999)}.png"
        if ctx.message.attachments:
            attachment = ctx.message.attachments[0]
            try:
                await attachment.save(newfilename)
                ima = Image.open(newfilename)
            except (discord.HTTPException, discord.NotFound) as e:
                await ctx.send("I could not open the attachment, so I'm using the link supplied with the command.")
                os.remove(newfilename)
        else:
            opener = urllib.request.build_opener()
            opener.addheaders = [('User-agent', 'Mozilla/5.0')]
            urllib.request.install_opener(opener)
            urllib.request.urlretrieve(imagelink, newfilename)
            ima = Image.open(newfilename)
        ima = ima.resize((1200, 480))
        ima = ima.filter(ImageFilter.GaussianBlur(radius=30))
        spoiler = Image.open("assets/imgen/spoilertagfull.png")
        ima.paste(spoiler, (0, 0), spoiler)
        filename = f"temp/{random.randint(1, 9999999)}.png"
        ima.save(filename, optimize=True, quality=50)
        file = discord.File(filename)
        try:
            await ctx.send(file=file)
        except discord.HTTPException:
            message = await ctx.send("The image is too large. Sending via Imgur instead...")
            result = im.upload_image(filename,
                                     title=f"Image generated for {ctx.author.name}#{ctx.author.discriminator}")
            await message.edit(content=result.link)
        os.remove(newfilename)
        os.remove(filename)

    @commands.command(name="nsfw", brief="not what you think it is",
                      description="Generates an NSFW image of a member. Only takes in a member.")
    async def nsfw(self, ctx, member: discord.Member = None):
        memberfilename = f"temp/{random.randint(1, 9999999)}.png"
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        urllib.request.install_opener(opener)
        urllib.request.urlretrieve(str(member.avatar_url), memberfilename)
        ima = Image.open(memberfilename).convert('RGBA')
        ima = ima.resize((185, 185))
        ima = ima.rotate(45, expand=True)
        main = Image.open("assets/imgen/mainnsfw.png")
        backg = main.copy()
        backg.paste(ima, (130, -10), ima)
        filename = f"temp/{random.randint(1, 9999999)}.png"
        backg.save(filename, optimize=True, quality=50)
        file = discord.File(filename)
        try:
            await ctx.send(file=file)
        except discord.HTTPException:
            message = await ctx.send("The image is too large. Sending via Imgur instead...")
            result = im.upload_image(filename,
                                     title=f"Image generated for {ctx.author.name}#{ctx.author.discriminator}")
            await message.edit(content=result.link)
        os.remove(filename)
        os.remove(memberfilename)


def setup(client):
    client.add_cog(Imgen(client))
