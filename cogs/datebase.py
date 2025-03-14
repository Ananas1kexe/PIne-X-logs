import disnake
import aiosqlite
import logging

from disnake.ext import commands


class datebase(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.db = None
    @commands.Cog.listener()
    async def on_ready(self):
        try:
            self.db = await aiosqlite.connect('main.db')
            await self.db.execute('''CREATE TABLE IF NOT EXISTS channel_log (
                server_id INTEGER PRIMARY KEY,
                channel INTEGER,
                role INTEGER
                )
            ''')
            await self.db.commit()
        except Exception as e:
            logging.error(f'произошла ошибка {e}')
    
def setup(bot: commands.Bot):
    bot.add_cog(datebase(bot))