from config import Config

import discord
from discord.ext import commands

import asyncio
from asyncio import sleep


PREFIX = Config.prefix
TOKEN = Config.bot_token

bot = commands.Bot(command_prefix=PREFIX, intents=discord.Intents.all())

bot.setup = False
bot.role_name = Config.role_name
bot.message_id = Config.message_id
bot.channel_id = Config.channel_id

@bot.event
async def on_ready():
    print(bot.user.name + " is online!")

#
# Verification
#

# Setup Embed
@bot.command()
async def setup(ctx):
    try:
        message_id = int(bot.message_id)
    except ValueError:
        return await ctx.send("Invalid Message ID passed")
    except Exception as e:
        raise e

    try:
        channel_id = int(bot.channel_id)
    except ValueError:
        return await ctx.send("Invalid Channel ID passed")
    except Exception as e:
        raise e
    
    channel = bot.get_channel(channel_id)
    
    if channel is None:
        return await ctx.send("Channel Not Found")
    
    message = await channel.fetch_message(message_id)
    
    if message is None:
        return await ctx.send("Message Not Found")
    
    await message.add_reaction("✅")
    await ctx.send("Setup Successful")
    
    bot.setup = True

# Add role
@bot.event
async def on_raw_reaction_add(payload):
    if bot.setup != True:
        return print(f"Bot is not set up\nType {PREFIX}setup to setup the bot")
    
    if payload.message_id == int(bot.message_id):
        if str(payload.emoji) == "✅":
            guild = bot.get_guild(payload.guild_id)
            if guild is None:
                return print("Guild Not Found\nTerminating Process")
            try:
                role = discord.utils.get(guild.roles, name=bot.role_name)
            except:
                return print("Role Not Found\nTerminating Process")
            
            member = guild.get_member(payload.user_id)
            
            if member is None:
                return
            try:
                await member.add_roles(role)
            except Exception as e:
                raise e

# Remove role
@bot.event
async def on_raw_reaction_remove(payload):
    if bot.setup != True:
        return print(f"Bot is not set up\nType {PREFIX}setup to setup the bot")
    
    if payload.message_id == int(bot.message_id):
        if str(payload.emoji) == "✅":
            guild = bot.get_guild(payload.guild_id)
            if guild is None:
                return print("Guild Not Found\nTerminating Process")
            try:
                role = discord.utils.get(guild.roles, name=bot.role_name)
            except:
                return print("Role Not Found\nTerminating Process")
            
            member = guild.get_member(payload.user_id)
            
            if member is None:
                return
            try:
                await member.remove_roles(role)
            except Exception as e:
                raise e


#
# Moderation
#

# Purge messages
@bot.command()
@commands.has_permissions(manage_messages=True)
async def purge(ctx, num):
    msg = []
    async for x in ctx.channel.history(limit=int(num)):
        msg.append(x)
    await ctx.channel.delete_messages(msg)
    print(num + ' messages removed from the channel')
    warning = await ctx.send(num + ' messages removed from the channel')

    # Wait to remove the warning message
    await sleep(3)
    await warning.delete()

# Ban users
@bot.command()
@commands.has_permissions(manage_messages=True)
async def ban(ctx, user: discord.Member, reason=None):
    await user.ban()
    await ctx.send('The user has been banned\nReason: ' + str(reason))
    print('A user has been banned')

# Temp Ban users
@bot.command()
@commands.has_permissions(manage_messages=True)
async def tempban(ctx, user: discord.Member, time, d, reason=None):
    await user.ban()
    await ctx.send('The user has been banned for ' + str(time) + ' ' + str(d) +'\nReason: ' + str(reason))
    print('A user has been banned')

    if d == "s" or d == "seconds":
        await asyncio.sleep(int(time))
        user.unban()
    elif d == "m" or d == "minutes":								
        await asyncio.sleep(int(time*60))
        user.unban()
    elif d == "h" or d == "hours":
        await asyncio.sleep(int(time*60*60))
        user.unban()
    elif d == "d" or d == "days":
        await asyncio.sleep(int(time*60*60*24))
        user.unban()

# Kick users
@bot.command()
@commands.has_permissions(manage_messages=True)
async def kick(ctx, user: discord.Member, reason=None):
    await user.kick()
    await ctx.send('The user has been kicked from the server\nReason: ' + str(reason))
    print('A user has been kicked')

# Temp Mute users
@bot.command()
@commands.has_permissions(manage_messages=True)
async def mute(ctx, user: discord.Member, time, d, reason=None):
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    await user.add_roles(role)
    await ctx.send(str(user) + ' has been muted for ' + str(time) + ' ' + str(d) +'\nReason: ' + str(reason))

    if d == "s" or d == "seconds":
        await asyncio.sleep(int(time))
    elif d == "m" or d == "minutes":								
        await asyncio.sleep(int(time*60))
    elif d == "h" or d == "hours":
        await asyncio.sleep(int(time*60*60))
    elif d == "d" or d == "days":
        await asyncio.sleep(int(time*60*60*24))

    await user.remove_roles(role)

bot.run(TOKEN)