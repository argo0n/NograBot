from discord.ext import commands
import discord
import datetime
from datetime import datetime as dt
from datetime import date
from datetime import datetime
import time
import math

start_time = time.time()
class Moderation(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('This message should appear succesfully.')

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id == 800184970298785802:
            return
        if message.channel.id in [
        803662591690932235,
        813288124460826669,
        802581920886030406,
        804260533666578432,
        810007696057040906,
        810007702058565632,
        ]:
            await message.delete()
            if message.guild.id == 789840820563476482:
                channel = self.client.get_channel(804260533666578432)
                await channel.send("**" + str(message.author.mention) + "**, if you continue to talk in <#" + str(
                    message.channel.id) + "> i'm gonna have to mute you <a:pik:801091998290411572>")
            elif message.guild.id == 796727833048645692:
                channel = self.client.get_channel(810007702058565632)
                await channel.send("**" + str(message.author.mention) + "**, if you continue to talk in <#" + str(
                    message.channel.id) + "> i'm gonna have to mute you <a:pik:801091998290411572>")

        if message.channel.id == 821640987003977778 and "roblox.com" not in message.content:
            await message.delete()
            await message.channel.send(
                f"{message.author.mention} this channel is for posting ROBLOX games only! :c\nIf you want to talk about the game, do it in <#818436261891014660> or <#821033003823923212>",
                delete_after=3.0)

    @commands.command(pass_context=True)
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, number=None):
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
                channel = self.client_get_channel(821042412624412733)
            # embed to be posted in modlogs
            timestamp = ctx.message.created_at
            clearembed = discord.Embed(title="`Clear` action done with Nogra", color=0xff0000)
            clearembed.set_author(name=str(ctx.author.name) + "#" + str(ctx.author.discriminator),
                                  icon_url=str(ctx.author.avatar_url))
            clearembed.add_field(name=str(number) + " messages deleted", value="in " + str(ctx.channel.mention),
                                 inline=False)
            clearembed.set_footer(text="ID: " + str(ctx.author.id) + " • " + str(timestamp))
            await channel.send(embed=clearembed)

    @commands.command(pass_context=True)
    async def uptime(self, ctx):
        current_time = time.time()
        difference = int(round(current_time - start_time))
        text = str(datetime.timedelta(seconds=difference))
        embed = discord.Embed(colour=0xc8dc6c)
        embed.add_field(name="Time since last reboot", value="1970-01-01 00:00:00", inline=True)
        embed.add_field(name="Time now", value="1970-01-01 00:00:00", inline=True)
        embed.add_field(name="Uptime", value=text)
        embed.set_footer(text="Time is in GMT+8 (Asia/Singapore)")
        try:
            await ctx.send(embed=embed)
        except discord.HTTPException:
            await ctx.send("Current uptime: " + text)

    '''@clear.error
    async def cog_command_error(self, ctx, error):
        await ctx.send(f"```diff\n- Error encountered!\n# erorr:\n+ {error}```")'''

    @uptime.error
    async def uptime_error(self, ctx, error):
        await ctx.send(f"```diff\n- Error encountered!\n# erorr:\n+ {error}```")

    @clear.error
    async def clear_error(self, ctx, error):
        await ctx.send(f"```diff\n- Error encountered!\n# erorr:\n+ {error}```")


def setup(client):
    client.add_cog(Moderation(client))
