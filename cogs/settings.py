import disnake
import aiosqlite
import logging

from disnake.ext import commands


class setting(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    
    @commands.slash_command(name='set-channel', description='Установить канал для логов')
    async def set_channel(self, inter: disnake.AppCommandInter, channel: disnake.TextChannel):
        if not channel.permissions_for(inter.guild.me).send_messages:
            embed = disnake.Embed(
                title='Ошибка',
                description='У бота нет прав на отправку сообщений в этот канал.',
                color=disnake.Color.red()
            )
            return await inter.response.send_message(embed=embed)
        async with aiosqlite.connect('main.db') as db:
            async with db.execute("SELECT role FROM channel_log WHERE server_id = ?", (inter.guild.id,)) as cursor:
                row = await cursor.fetchone()
            if row is not None:
                await db.execute("UPDATE channel_log SET channel = ? WHERE server_id = ?", (channel.id, inter.guild.id))
            else:
                await db.execute("INSERT INTO channel_log (server_id, channel) VALUES (?, ?)", (inter.guild.id, channel.id))
            await db.commit()
        
        note = self.bot.get_channel(channel.id)
        if note:
            embed_note = disnake.Embed(
                title='Проверка канала',
                description='Этот канал установлен для логов',
                color=disnake.Color.orange()
            )
            await note.send(embed=embed_note)
        
        embed = disnake.Embed(
            title='Настройка сохранена',
            description=f'Логовый канал установлен: {channel.mention}',
            color=disnake.Color.green()
        )
        await inter.response.send_message(embed=embed)
        
    @commands.slash_command(name='set-role', description='Установить роль для упоминания')
    async def set_role(self, inter: disnake.AppCommandInter, role: disnake.Role):
        if role.id == inter.guild.default_role.id:
            embed = disnake.Embed(
                description="Невозможно установить роль @everyone для упоминания.",
                color=disnake.Color.red()
            )
            await inter.response.send_message(embed=embed, ephemeral=True)
            return
        async with aiosqlite.connect('main.db') as db:
            async with db.execute("SELECT channel FROM channel_log WHERE server_id = ?", (inter.guild.id,)) as cursor:
                row = await cursor.fetchone()
            if row is not None:
                await db.execute("UPDATE channel_log SET role = ? WHERE server_id = ?", (role.id, inter.guild.id))
            else:
                await db.execute("INSERT INTO channel_log (server_id, role) VALUES (?, ?)", (inter.guild.id, role.id))
            await db.commit()
        
        embed = disnake.Embed(
            title='Настройка сохранена',
            description=f'Роль для упоминания установлена: {role.mention}',
            color=disnake.Color.green()
        )
        await inter.response.send_message(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(setting(bot))
