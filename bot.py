from config import Config

import discord
from discord.ext import commands

from discord.ext import commands
from tts import *
from verification import *
from moderation import *


PREFIX = Config.prefix
TOKEN = Config.bot_token

bot = commands.Bot(command_prefix=PREFIX, intents=discord.Intents.all())

bot.setup = False
bot.role_name = Config.role_name
bot.message_id = Config.message_id
bot.channel_id = Config.channel_id
bot.add_cog(TTSBot(bot))

@bot.event
async def on_ready():
    print(bot.user.name + " is online!")



openai.api_key = Config.openapikey

#bot.run("MTA2NzEwMjM1NTkzNTQ2NTUzNQ.GHuEiT.Y-9ihlYIEJo_gbSFtseoad1_y-4YpSPQf_MjCw")

bot.run(TOKEN)