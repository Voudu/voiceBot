import discord
from discord.ext import commands

from dotenv import load_dotenv
import os

import asyncio

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.typing = False
intents.presences = False


extension = ['cogs.music', 'cogs.parrot']

bot = commands.Bot(command_prefix="!", intents=intents)

if __name__ == '__main__':
    for ext in extension:
        bot.load_extension(ext)

bot.run(os.getenv('TOKEN'))