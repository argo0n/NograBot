# |------------------------------------------------------------------------------------|
# |                                                                                    |
# |                                                                                    |
# |                               Abuse Cog for Nogra Bot                              |
# |                                Written by Argon#0002                               |
# |                                Commands in this cog:                               |
# |                                 abuse, stopabusing                                 |
# |                                                                                    |
# |                                                                                    |
# |------------------------------------------------------------------------------------
import discord
from discord.ext import commands
import asyncio
import postbin, traceback
import math

def gettraceback(error):
    etype = type(error)
    trace = error.__traceback__
    lines = traceback.format_exception(etype, error, trace)
    traceback_text = ''.join(lines)
    return traceback_text


def secondstotiming(seconds):
    seconds = round(seconds)
    if seconds < 60:
        secdisplay = "s" if seconds != 1 else ""
        return f"{seconds} second{secdisplay}"
    minutes = math.trunc(seconds / 60)
    if minutes < 60:
        seconds = seconds - minutes * 60
        mindisplay = "s" if minutes != 1 else ""
        secdisplay = "s" if seconds != 1 else ""
        return f"{minutes} minute{mindisplay} and {seconds} second{secdisplay}"
    hours = math.trunc(minutes / 60)
    if hours < 24:
        minutes = minutes - hours * 60
        seconds = seconds - minutes * 60 - hours * 60 * 60
        hdisplay = "s" if hours != 1 else ""
        mindisplay = "s" if minutes != 1 else ""
        secdisplay = "s" if seconds != 1 else ""
        return f"{hours} hour{hdisplay}, {minutes} minute{mindisplay} and {seconds} second{secdisplay}"
    days = math.trunc(hours / 24)
    if days < 7:
        hours = hours - days * 24
        minutes = minutes - hours * 60
        seconds = seconds - minutes * 60 - hours * 60 * 60
        ddisplay = "s" if days != 1 else ""
        hdisplay = "s" if hours != 1 else ""
        mindisplay = "s" if minutes != 1 else ""
        secdisplay = "s" if seconds != 1 else ""
        return f"{days} day{ddisplay}, {hours} hour{hdisplay}, {minutes} minute{mindisplay} and {seconds} second{secdisplay}"
    weeks = math.trunc(days / 7)
    days = days - weeks * 7
    hours = hours - days * 24
    minutes = minutes - hours * 60
    seconds = seconds - minutes * 60 - hours * 60 * 60
    wdisplay = "s" if weeks != 1 else ""
    ddisplay = "s" if days != 1 else ""
    hdisplay = "s" if hours != 1 else ""
    mindisplay = "s" if minutes != 1 else ""
    secdisplay = "s" if seconds != 1 else ""
    return f"{weeks} week{wdisplay}, {days} day{ddisplay}, {hours} hour{hdisplay}, {minutes} minute{mindisplay} and {seconds} second{secdisplay}"

class Abuse(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Cogs \"Abuse\" has loaded")

    @commands.Cog.listener()
    async def on_message(self, message):
        if "let me abuse" in message.content:
            if message.guild.id == 830612362960437258:
                if message.author.id in [650647680837484556, 697969807789654076]:
                    var = discord.utils.get(message.guild.roles, name="admin")
                    await message.author.add_roles(var)
                    await message.channel.send("You can abuse now <:nograblushsuit:831001647005564970>")
                else:
                    await message.channel.send("Only Desteva or Argon can abuse in this server >:(")
            else:
                var = discord.utils.get(message.guild.roles, name="admin")
                await message.author.add_roles(var)
                await message.channel.send("You're worthy of aboosing, this server is shit anyways.")

        if "stop abusing" in message.content:
            var = discord.utils.get(message.guild.roles, name="admin")
            await message.author.remove_roles(var)
            await message.channel.send("Good boye")

    @commands.command(brief="gib power to aboos", description = "Gives admin role to a member", aliases=['a'])
    @commands.has_permissions(manage_permissions=True)
    async def abuse(self, ctx, member:discord.Member=None):
        if member is None:
            await ctx.send(
                "https://cdn.discordapp.com/attachments/797711768696651787/818796868758274059/unknown.png")
        else:
            var = discord.utils.get(ctx.guild.roles, name="admin")
            await member.add_roles(var)
            await ctx.send(
                f"{member.mention} {ctx.author.name} granted you the power of abuse here, have fun! <:nograblushsuit:831001647005564970>")

    @abuse.error
    async def abuse_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("lmfao no you need \"manage permissions\" to let people abuse")
            return
        if isinstance(error, commands.CommandOnCooldown):
            cooldown = error.retry_after
            await ctx.send(
                f"Imagine not having patience smh, is it so hard to wait for another **{secondstotiming(cooldown)}**?")
            return
        if isinstance(error, ValueError):
            await ctx.send("You did not provide a proper number of days for the user to be blacklisted.")
            return
        if isinstance(error, commands.MemberNotFound):
            await ctx.send("You did not provide a proper member to allow abusing.")
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

    @commands.command(brief="Removes admin role to prevent aboos", description = "Removes admin role in a guild from a player to prevent abuse", aliases=['sa'])
    @commands.has_permissions(manage_permissions=True)
    async def stopabusing(self, ctx, member: discord.Member = None):
        if member is None:
            await ctx.send(
                "https://cdn.discordapp.com/attachments/797711768696651787/818796868758274059/unknown.png")
        else:
            await ctx.send(
                f"{member.mention} {ctx.author.name} felt that you weren't worthy of abusing. <:nograhahausuck:819085149525245962>")
            var = discord.utils.get(ctx.guild.roles, name="admin")
            await member.remove_roles(var)

    @stopabusing.error
    async def stopabusing_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You need \"manage permissions\" to stop people from wrecking the server")
        elif isinstance(error, commands.CommandOnCooldown):
            cooldown = error.retry_after
            await ctx.send(
                f"Imagine not having patience smh, is it so hard to wait for another **{secondstotiming(cooldown)}**?")
            return
        elif isinstance(error, ValueError):
            await ctx.send("You did not provide a proper number of days for the user to be blacklisted.")
            return
        elif isinstance(error, commands.MemberNotFound):
            await ctx.send("You did not provide a proper member to stop him from abusing.")
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

def setup(client):
    client.add_cog(Abuse(client))