import discord
from discord.ext import commands
import asyncio


class RobloxServerOnly(commands.Cog):

    def __init__(self, client):
        self.client = client


    @commands.command()
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
        await ctx.send(f"```diff\n- Error encountered!\n# erorr:\n+ {error}```")

    @commands.command()
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
        await ctx.send(f"```diff\n- Error encountered!\n# erorr:\n+ {error}```")

    @commands.command()
    async def admon(self, ctx, member: discord.Member = None, durationinseconds=None):
        if ctx.guild.id != 818436261873844224:
            ctx.send("You are using this in the wrong guild!")
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
        await ctx.send(f"```diff\n- Error encountered!\n# erorr:\n+ {error}```")

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
        await ctx.send(f"```diff\n- Error encountered!\n# erorr:\n+ {error}```")

    @uglie.error
    async def uglie_error(self, ctx, error):
        await ctx.send(f"```diff\n- Error encountered!\n# erorr:\n+ {error}```")

def setup(client):
    client.add_cog(RobloxServerOnly(client))