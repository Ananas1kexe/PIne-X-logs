import disnake
from disnake.ext import commands
from dotenv import load_dotenv
import logging
import os
import asyncio
from colorama import Fore, init

init()

load_dotenv()

intents = disnake.Intents.all()
intents.messages = True

bot = commands.AutoShardedBot(command_prefix='p$', intents=intents, help_command=None)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', handlers=[logging.FileHandler('bot.log', encoding='utf-8'), logging.StreamHandler()])


bot.load_extensions("cogs")

@bot.event
async def on_ready():

    shards = bot.shard_count
        
    logging.info(f'Bot has started as {Fore.GREEN}{bot.user}{Fore.RESET} ✅')
    logging.info(f'Servering in {len(bot.guilds)}')

    logging.info(f'Shards: {shards}')
    # for guild in self.bot.guilds:
    #     logging.info(f' - {guild.name}')
        
    statuse = [
        disnake.Game('Official bot of PINE X'),
        disnake.Activity(type=disnake.ActivityType.watching, name='pine-x.vercel.app'),
    ]
    while True:
        for status in statuse:
            await bot.change_presence(activity=status)
            await asyncio.sleep(10)


@bot.event
async def on_close():
    if hasattr(bot, 'db'):
        await bot.db.close() 

try:
    bot.run(os.getenv('TOKEN'))
except Exception as e:
    logging.error(f'Error occured: {e}')