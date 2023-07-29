import discord
from discord.ext import commands
from config import Config
import asyncio
from asyncio import sleep

PREFIX = Config.prefix
TOKEN = Config.bot_token

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, num):
        msg = []
        async for x in ctx.channel.history(limit=int(num)):
            msg.append(x)
        await ctx.channel.delete_messages(msg)
        print(num + ' messages removed from the channel')
        warning = await ctx.send(num + ' messages removed from the channel')

        # Wait to remove the warning message
        await sleep(3)
        await warning.delete()

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, user: commands.MemberConverter, reason=None):
        await user.ban()
        await ctx.send('The user has been banned\nReason: ' + str(reason))
        print('A user has been banned')

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def tempban(self, ctx, user: commands.MemberConverter, time, d, reason=None):
        await user.ban()
        await ctx.send('The user has been banned for ' + str(time) + ' ' + str(d) +'\nReason: ' + str(reason))
        print('A user has been banned')

        if d == "s" or d == "seconds":
            await asyncio.sleep(int(time))
            await user.unban()
        elif d == "m" or d == "minutes":
            await asyncio.sleep(int(time)*60)
            await user.unban()
        elif d == "h" or d == "hours":
            await asyncio.sleep(int(time)*60*60)
            await user.unban()
        elif d == "d" or d == "days":
            await asyncio.sleep(int(time)*60*60*24)
            await user.unban()

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, user: commands.MemberConverter, reason=None):
        await user.kick()
        await ctx.send('The user has been kicked from the server\nReason: ' + str(reason))
        print('A user has been kicked')

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def mute(self, ctx, user: commands.MemberConverter, time, d, reason=None):
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        await user.add_roles(role)
        await ctx.send(str(user) + ' has been muted for ' + str(time) + ' ' + str(d) +'\nReason: ' + str(reason))

        if d == "s" or d == "seconds":
            await asyncio.sleep(int(time))
        elif d == "m" or d == "minutes":
            await asyncio.sleep(int(time)*60)
        elif d == "h" or d == "hours":
            await asyncio.sleep(int(time)*60*60)
        elif d == "d" or d == "days":
            await asyncio.sleep(int(time)*60*60*24)

        await user.remove_roles(role)