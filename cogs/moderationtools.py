import discord
from discord.ext import commands

class Example(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('This message should appear succesfully.')

    @commands.command()
    async def test(self, ctx):
        await ctx.send("This message should appear successfully. If so, congratulations on making a cog.")


def setup(client):
    client.add_cog(Example(client))
