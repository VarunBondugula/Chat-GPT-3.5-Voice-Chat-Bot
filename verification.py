import discord
from discord.ext import commands
from config import Config

PREFIX = Config.prefix
TOKEN = Config.bot_token

class VerificationBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Setup Embed
    @commands.command()
    async def setup(self, ctx):  # Added self parameter here
        try:
            message_id = int(self.bot.message_id)  # Use self.bot to access the bot instance
        except ValueError:
            return await ctx.send("Invalid Message ID passed")
        except Exception as e:
            raise e

        try:
            channel_id = int(self.bot.channel_id)  # Use self.bot to access the bot instance
        except ValueError:
            return await ctx.send("Invalid Channel ID passed")
        except Exception as e:
            raise e

        channel = self.bot.get_channel(channel_id)  # Use self.bot to access the bot instance

        if channel is None:
            return await ctx.send("Channel Not Found")

        message = await channel.fetch_message(message_id)

        if message is None:
            return await ctx.send("Message Not Found")

        await message.add_reaction("✅")
        await ctx.send("Setup Successful")

        self.bot.setup = True  # Use self.bot to access the bot instance

    # Add role
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):  # Added self parameter here
        if self.bot.setup != True:  # Use self.bot to access the bot instance
            return print(f"Bot is not set up\nType {PREFIX}setup to setup the bot")

        if payload.message_id == int(self.bot.message_id):  # Use self.bot to access the bot instance
            if str(payload.emoji) == "✅":
                guild = self.bot.get_guild(payload.guild_id)  # Use self.bot to access the bot instance
                if guild is None:
                    return print("Guild Not Found\nTerminating Process")
                try:
                    role = discord.utils.get(guild.roles, name=self.bot.role_name)  # Use self.bot to access the bot instance
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
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):  # Added self parameter here
        if self.bot.setup != True:  # Use self.bot to access the bot instance
            return print(f"Bot is not set up\nType {PREFIX}setup to setup the bot")

        if payload.message_id == int(self.bot.message_id):  # Use self.bot to access the bot instance
            if str(payload.emoji) == "✅":
                guild = self.bot.get_guild(payload.guild_id)  # Use self.bot to access the bot instance
                if guild is None:
                    return print("Guild Not Found\nTerminating Process")
                try:
                    role = discord.utils.get(guild.roles, name=self.bot.role_name)  # Use self.bot to access the bot instance
                except:
                    return print("Role Not Found\nTerminating Process")

                member = guild.get_member(payload.user_id)

                if member is None:
                    return
                try:
                    await member.remove_roles(role)
                except Exception as e:
                    raise e