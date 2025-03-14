import disnake
import aiosqlite
import logging
from config import guild_join_channel  
from disnake.utils import format_dt
from disnake.ext import commands

class Events(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def get_channel(self, guild: disnake.Guild):
        async with aiosqlite.connect('main.db') as db:
            async with db.execute('SELECT channel FROM channel_log WHERE server_id = ?', (guild.id,)) as cursor:
                row = await cursor.fetchone()
                channel_id = row[0] if row else None
        if channel_id:
            return guild.get_channel(channel_id)
        return None

    async def get_role(self, guild: disnake.Guild):
        async with aiosqlite.connect('main.db') as db:
            async with db.execute('SELECT role FROM channel_log WHERE server_id = ?', (guild.id,)) as cursor:
                row = await cursor.fetchone()
                role_id = row[0] if row else None
        if role_id:
            return guild.get_role(role_id)
        return None

    @commands.Cog.listener()
    async def on_member_join(self, member: disnake.Member):
        mod_channel = await self.get_channel(member.guild)
        if mod_channel is None:
            return

        mod_role = await self.get_role(member.guild)


        embed = disnake.Embed(
            title='User joined',
            description=(
                '**Member:**\n'
                f'{member.mention} (@{member.name})\n'
                '**Member ID:**\n'
                f'`{member.id}`'
            ),
            color=disnake.Color.green()
        )
        if mod_role:
            await mod_channel.send(f'||{mod_role.mention}||', embed=embed)
        else:
            await mod_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member: disnake.Member):
        mod_channel = await self.get_channel(member.guild)
        if mod_channel is None:
            return

        mod_role = await self.get_role(member.guild)


        joined = format_dt(member.joined_at, style='F') if member.joined_at else "Unknown"
        embed = disnake.Embed(
            title='User has logged out',
            description=(
                '**Member:**\n'
                f'{member.mention} (@{member.name})\n'
                '**Member ID:**\n'
                f'`{member.id}`\n'
                '**Joined:**\n'
                f'{joined}'
            ),
            color=disnake.Color.orange()
        )
        if mod_role:
            await mod_channel.send(f'||{mod_role.mention}||', embed=embed)
        else:
            await mod_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_ban(self, guild: disnake.Guild, user: disnake.User):
        mod_channel = await self.get_channel(guild)
        if mod_channel is None:
            return

        mod_role = await self.get_role(guild)


        embed = disnake.Embed(
            title='User has banned',
            description=(
                '**Member:**\n'
                f'{user.mention} (@{user.name})\n'
                '**Member ID:**\n'
                f'`{user.id}`'
            ),
            color=disnake.Color.dark_red()
        )
        if mod_role:
            await mod_channel.send(f'||{mod_role.mention}||', embed=embed)
        else:
            await mod_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_unban(self, guild: disnake.Guild, user: disnake.User):
        mod_channel = await self.get_channel(guild)
        if mod_channel is None:
            return

        mod_role = await self.get_role(guild)


        embed = disnake.Embed(
            title='User has unbanned',
            description=(
                '**Member:**\n'
                f'{user.mention} (@{user.name})\n'
                '**Member ID:**\n'
                f'`{user.id}`'
            ),
            color=disnake.Color.green()
        )
        if mod_role:
            await mod_channel.send(f'||{mod_role.mention}||', embed=embed)
        else:
            await mod_channel.send(embed=embed)
    @commands.Cog.listener()
    async def on_member_update(self, before: disnake.Member, after: disnake.Member):
        mod_channel = await self.get_channel(after.guild)
        if mod_channel is None:
            return

        mod_role = await self.get_role(after.guild)


        embed = disnake.Embed(
            title='Member updated',
            description=(
                '**Before:**\n'
                f'{before.mention} (@{before.name})\n'
                '**After:**\n'
                f'{after.mention} (@{after.name})\n'
                '**Member ID:**\n'
                f'`{after.id}`'
            ),
            color=disnake.Color.blue()
        )
        if mod_role:
            await mod_channel.send(f'||{mod_role.mention}||', embed=embed)
        else:
            await mod_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_delete(self, message: disnake.Message):
        if not message.guild:
            return
        if message.author.bot:
            return

        mod_channel = await self.get_channel(message.guild)
        if mod_channel is None:
            return

        mod_role = await self.get_role(message.guild)

        embed = disnake.Embed(
            title='Message deleted',
            description=(
                '**Member:**\n'
                f'{message.author.mention} (@{message.author.name})\n'
                '**Member ID:**\n'
                f'`{message.author.id}`\n'
                '**Message Contents:**\n'
                f'{message.content if message.content else "Empty message"}'
            ),
            color=disnake.Color.red()
        )
        embed.timestamp = disnake.utils.utcnow()
        embed.set_footer(text='Message deleted at')
        if mod_role:
            await mod_channel.send(f'||{mod_role.mention}||', embed=embed)
        else:
            await mod_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before: disnake.Message, after: disnake.Message):
        if not after.guild:
            return

        mod_channel = await self.get_channel(after.guild)
        if mod_channel is None:
            return

        mod_role = await self.get_role(after.guild)


        embed = disnake.Embed(
            title='Message edited',
            description=(
                '**Member:**\n'
                f'{after.author.mention} (@{after.author.name})\n'
                '**Member ID:**\n'
                f'`{after.author.id}`\n'
                '**New Content:**\n'
                f'{after.content}\n'
                '**Old Content:**\n'
                f'{before.content}'
            ),
            color=disnake.Color.gold()
        )
        embed.timestamp = disnake.utils.utcnow()
        embed.set_footer(text='Message edited at')
        if mod_role:
            await mod_channel.send(f'||{mod_role.mention}||', embed=embed)
        else:
            await mod_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_join(self, guild: disnake.Guild):
        dc = guild.owner.dm_channel
        if dc is None:
            dc = await guild.owner.create_dm()
        if dc is None:
            try:
                dc = guild.system_channel
            except disnake.Forbidden:
                dc = None

        guild_count = len(self.bot.guilds)
        user_count = sum(len(guild.members) for guild in self.bot.guilds)
        embed_owner = disnake.Embed(
            title='Thank you for adding PINE X Logs to your server!',
            description=(
                f'The `PINE X Logs` bot was successfully added to **{guild.name}**.\n'
                'Set up the bot using configuration commands, check the [documentation](https://pine-x.vercel.app/documentation) or use the `/help-set` command.\n\n'
                f'Prefix: `p!`\n'
                f'Guilds: `{guild_count}` | Users: `{user_count}`'
            ),
            color=disnake.Color.from_rgb(52, 89, 149)
        )
        embed_owner.set_author(
            name='PINE X Logs',
            url='https://pine-x.vercel.app',
            icon_url=self.bot.user.display_avatar.url
        )
        support_btn = disnake.ui.Button(label='Server support', url='https://discord.gg/KmskWpN5nb', style=disnake.ButtonStyle.link)
        website_btn = disnake.ui.Button(label='Website', url='https://pine-x.vercel.app/', style=disnake.ButtonStyle.link)
        invite_btn = disnake.ui.Button(label='Invite PINE X', url='https://discord.com/oauth2/authorize?client_id=1291690669294882836', style=disnake.ButtonStyle.link)
        view = disnake.ui.View()
        view.add_item(support_btn)
        view.add_item(website_btn)
        view.add_item(invite_btn)
        if dc:
            await dc.send(embed=embed_owner, view=view)

        channel = self.bot.get_channel(guild_join_channel)
        if channel:
            avatar = guild.icon.url if guild.icon else None
            banner = guild.banner.url if guild.banner else None
            first_text_channel = next((c for c in guild.text_channels if c.permissions_for(guild.me).create_instant_invite), None)
            invite = None
            if first_text_channel:
                invite = await first_text_channel.create_invite(max_age=3600, max_uses=5)
            embed_join = disnake.Embed(
                title='Guild joined',
                description=(
                    f'**Name:** {guild.name}\n'
                    f'**Guild ID:** {guild.id}\n'
                    f'**Owner:** {guild.owner.mention} (@{guild.owner.name})\n'
                    f'**Owner ID:** `{guild.owner.id}`\n'
                    f'**Member Count:** `{guild.member_count}`'
                ),
                color=disnake.Color.from_rgb(52, 89, 149)
            )
            if avatar:
                embed_join.set_thumbnail(url=avatar)
            if banner:
                embed_join.set_image(url=banner)
            if invite:
                await channel.send(content=invite, embed=embed_join)
            else:
                await channel.send(embed=embed_join)

def setup(bot: commands.Bot):
    bot.add_cog(Events(bot))
