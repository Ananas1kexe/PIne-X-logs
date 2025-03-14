import disnake 
import time
from config import version
from disnake.ext import commands
from disnake.utils import format_dt

start_time = time.time()

class commands_bot(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @commands.slash_command()
    async def info(self, inter: disnake.AppCommandInter):
        uptime_sec = int(time.time() - start_time)
        
        days, remainder = divmod(uptime_sec, 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes, seconds  = divmod(remainder, 60)

        shards = self.bot.shard_count
        guilds = len(self.bot.guilds)
        
        uptime = f'{days}d {hours}h {minutes}m' if days > 0 else f'{hours}h {minutes}m {seconds}s'
        embed = disnake.Embed(
            title='About bot',
            description=(
                f'Version: {version}\n'
                f'Uptime: `{uptime}`\n\n'
                f'Total shards: `{shards}`\n'
                f'Total guilds: `{guilds}`\n'

            ),
            color=disnake.Color.from_rgb(52,89,149)
            )
        await inter.response.send_message(embed=embed)
    
    
    @commands.slash_command(name='server_info', description='about server')
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def sever_info(self, inter: disnake.AppCommandInter):

            
        guild = inter.guild


        first_text_channel = next((channel for channel in guild.text_channels if channel.permissions_for(guild.me).create_instant_invite), None)
        if first_text_channel:
            invite = await first_text_channel.create_invite(max_age=3600, max_uses=5)        
        server_icon = guild.icon.url if guild.icon else None
        member_count = guild.member_count
        roles_count =len(guild.roles)
        text_channel = len([channel for channel in guild.text_channels if isinstance(channel, disnake.TextChannel)])
        voice_channel = len([channel for channel in guild.voice_channels if isinstance(channel, disnake.VoiceChannel)])
        created_at = format_dt(guild.created_at, style='F')
        
        embed = disnake.Embed(
            title=f'{guild.name} Information', 
            color=disnake.Color.from_rgb(52,89,149)
        )
        embed.add_field(name='** Guild name: **', value=f'{guild.name}', inline=False)
        embed.add_field(name='** Guild ID: **', value=f'`{guild.id}`', inline=False)
        embed.add_field(name='** Owner name: **', value=f'{guild.owner.mention} (@{guild.owner.name})', inline=False)
        embed.add_field(name='** Owner ID: **', value=f'`{guild.owner.id}`', inline=False)
        embed.add_field(name='** Member count: **', value=f'`{member_count}`', inline=False)
        embed.add_field(name='** Roles count: **', value=f'`{roles_count}`', inline=False)
        embed.add_field(name='** Text channel: **', value=f'`{text_channel}`', inline=False)
        embed.add_field(name='** Voice channel: **', value=f'`{voice_channel}`', inline=False)
        embed.add_field(name='** Created: **', value=f'{created_at}', inline=False)

        embed.set_thumbnail(url=server_icon)
        await inter.response.send_message(f'{invite}', embed=embed, ephemeral=True)
        
        
    
    
    
def setup(bot: commands.Bot):
    bot.add_cog(commands_bot(bot))