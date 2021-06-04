# |------------------------------------------------------------------------------------|
# |                                                                                    |
# |                                                                                    |
# |                         RobloxServerOnly Cog for Nogra Bot                         |
# |                               Written by Argon#0002                                |
# |                               Commands in this cog:                                |
# |                          kicc, allow, admon, cutie, uglie                          |
# |                                                                                    |
# |                                                                                    |
# |------------------------------------------------------------------------------------
import discord
from discord.ext import commands
import asyncio
import postbin, traceback

def gettraceback(error):
    etype = type(error)
    trace = error.__traceback__
    lines = traceback.format_exception(etype, error, trace)
    traceback_text = ''.join(lines)
    return traceback_text

class RobloxServerOnly(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Cogs \"RobloxServerOnly\" has loaded")

    @commands.command(brief="kicks everyone out of frenzy's sleeping channel", description = "kicks everyone out of freny's sleeping channel")
    async def kicc(self, ctx):
        if ctx.author.id in [560251854399733760, 650647680837484556]:
            if ctx.guild.id == 818436261873844224:
                channel = self.client.get_channel(821033788262842438)
                overwrite = discord.PermissionOverwrite()
                overwrite.send_messages = False
                overwrite.read_messages = False
                await ctx.send("Yeeted everyone out of your bedroom. <a:nograexcitedwave:821394571522342922>")
                await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
            else:
                await ctx.send("You are using this in the wrong guild!")
        else:
            await ctx.send("imagine not being frenzy or argon lol")

    @kicc.error
    async def kicc_error(self, ctx, error):
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

    @commands.command(brief="Lets everyone into frenzy's sleeping channel", description = "Gives everyone read message perms in frenzy's sleeping channel")
    async def allow(self, ctx):
        if ctx.author.id in [560251854399733760, 650647680837484556]:
            if ctx.guild.id == 818436261873844224:
                channel = self.client.get_channel(821033788262842438)
                overwrite = discord.PermissionOverwrite()
                overwrite.send_messages = True
                overwrite.read_messages = True
                await ctx.send("I opened the door do your bedroom. <a:nograexcitedwave:821394571522342922>")
                await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
            else:
                await ctx.send("You are using this in the wrong guild!")
        else:
            await ctx.send("imagine not being frenzy or argon lol")

    @allow.error
    async def allow_error(self, ctx, error):
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

    @commands.command(brief="Better than cutie role", description = "Gives elevated admin role for a while")
    async def admon(self, ctx, member: discord.Member = None, durationinseconds=None):
        if ctx.guild.id != 818436261873844224:
            await ctx.send("You are using this in the wrong guild!")
        else:
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
                        await ctx.send(
                            f"Given the elevated admin role to {member.mention} for {durationinseconds} seconds.")
                        intdurationinseconds = int(durationinseconds)
                        await asyncio.sleep(intdurationinseconds)
                    await member.remove_roles(var)
                    await ctx.send(f"Removed the elevated admin role from {member.mention}.")
                else:
                    await ctx.send("No dmads for you <:nograsweg:818474291757580328>")

    @admon.error
    async def admon_error(self, ctx, error):
        if isinstance(error, commands.MemberNotFound):
            await ctx.send(f"You did not provide a proper user. It has to be a mention or user ID.")
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

    @commands.command()
    async def cutie(self, ctx):
        if ctx.author.id != 650647680837484556:
            await ctx.send("you can only call others a cutie if you are argon <a:nograkekgiggle:821318605274218516>")
        else:
            var = discord.utils.get(ctx.guild.roles, name="if you have this role you're cute uwu")
            memberid = [730974500111515648, 680331233624195132, 604212608941424640, 264019387009204224,
                        642318626044772362, 651047556360699911, 560251854399733760]
            for m in memberid:
                m = ctx.guild.get_member(m)
                await m.add_roles(var)
                await ctx.send(f"Power of cuteness granted to **{m.name}#{m.discriminator}**")
            await ctx.send("`if you have this role you're cute uwu` Role given to everyone. ")
            return

    @commands.command()
    async def uglie(self, ctx):
        if ctx.author.id != 650647680837484556:
            await ctx.send("you can only call others ugly if you are argon <a:nograkekgiggle:821318605274218516>")
        else:
            var = discord.utils.get(ctx.guild.roles, name="if you have this role you're cute uwu")
            memberid = [730974500111515648, 680331233624195132, 604212608941424640, 264019387009204224,
                        642318626044772362, 651047556360699911, 560251854399733760]
            for m in memberid:
                m = ctx.guild.get_member(m)
                await m.remove_roles(var)
                await ctx.send(f"Power of ugliness granted to ****{m.name}#{m.discriminator}****")
            await ctx.send("`if you have this role you're cute uwu` Role removed from everyone. ")

    @cutie.error
    async def cutie_error(self, ctx, error):
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

    @uglie.error
    async def uglie_error(self, ctx, error):
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
    client.add_cog(RobloxServerOnly(client))