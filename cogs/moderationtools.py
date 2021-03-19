import discord
from discord.ext import commands

class Example(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('This message should appear succesfully.')

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id == 821640987003977778 and "roblox.com" not in message.content:
            await message.delete()
            await message.channel.send(
                f"{message.author.mention} this channel is for posting ROBLOX games only! :c\nIf you want to talk about the game, do it in <#818436261891014660> or <#821033003823923212>",
                delete_after=3.0)

        if message.channel.id in [
            803662591690932235,
            813288124460826669,
            802581920886030406,
            804260533666578432,
            810007696057040906,
            810007702058565632,
        ]:
            await message.delete()
            # await message.channel.send('you can\'t send messages in here idot <a:distorteddisgust:796382813279879218>',delete_after=3.0)
            if message.guild.id == 789840820563476482:
                channel = self.client.get_channel(804260533666578432)
                await channel.send("**" + str(message.author.mention) + "**, if you continue to talk in <#" + str(
                    message.channel.id) + "> i'm gonna have to mute you <a:pik:801091998290411572>")
            elif message.guild.id == 796727833048645692:
                channel = self.client.get_channel(810007702058565632)
                await channel.send("**" + str(message.author.mention) + "**, if you continue to talk in <#" + str(
                    message.channel.id) + "> i'm gonna have to mute you <a:pik:801091998290411572>")


    @commands.command()
    async def test(self, ctx):
        await ctx.send("This message should appear successfully. If so, congratulations on making a cog.")


def setup(client):
    client.add_cog(Example(client))
