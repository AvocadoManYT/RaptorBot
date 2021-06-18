import discord
import platform
import asyncio
import json
import datetime
import os
import typing
from utils import formats, time as tim
from typing import Union
from collections import Counter
import time
import psutil
from discord.ext import commands

obj_Disk = psutil.disk_usage('/')
start_time = time.time()


class Info(commands.Cog):
    """ Category for info commands """

    def __init__(self, client):
        self.client = client
        self.process = psutil.Process(os.getpid())

    # events
    @commands.Cog.listener()
    async def on_ready(self):
        print('Info cog is ready.')

    # commands

    @commands.command(aliases=['si'])
    @commands.guild_only()
    async def serverinfo(self, ctx, *, guild_id: int = None):
        """Shows info about the current server."""

        if guild_id is not None and await self.bot.is_owner(ctx.author):
            guild = self.bot.get_guild(guild_id)
            if guild is None:
                return await ctx.send(f'Invalid Guild ID given.')
        else:
            guild = ctx.guild

        roles = [role.name.replace('@', '@\u200b') for role in guild.roles]

        if not guild.chunked:
            async with ctx.typing():
                await guild.chunk(cache=True)

        # figure out what channels are 'secret'
        everyone = guild.default_role
        everyone_perms = everyone.permissions.value
        secret = Counter()
        totals = Counter()
        for channel in guild.channels:
            allow, deny = channel.overwrites_for(everyone).pair()
            perms = discord.Permissions((everyone_perms & ~deny.value) | allow.value)
            channel_type = type(channel)
            totals[channel_type] += 1
            if not perms.read_messages:
                secret[channel_type] += 1
            elif isinstance(channel, discord.VoiceChannel) and (not perms.connect or not perms.speak):
                secret[channel_type] += 1

        e = discord.Embed()
        e.title = guild.name
        guild = ctx.guild

        description = str(guild.description)
        region = str(guild.region)
        memberCount = str(guild.member_count)
        icon = str(guild.icon_url)
        embed = e
        e.add_field(name = "Description:", value = description)
        embed.set_thumbnail(url=icon)
        embed.add_field(name="Region", value=region)
        embed.add_field(name="Member Count", value=memberCount)
        embed.add_field(name="Role Count", value=len(ctx.guild.roles))
        embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
        e.description = f'**ID**: {guild.id}\n**Owner**: {guild.owner}'
        if guild.icon:
            e.set_thumbnail(url=guild.icon_url)

        channel_info = []
        key_to_emoji = {
            discord.TextChannel: '<:text:854459874360819734>',
            discord.VoiceChannel: '<:voice:854459874402238485>',
        }
        for key, total in totals.items():
            secrets = secret[key]
            try:
                emoji = key_to_emoji[key]
            except KeyError:
                continue

            if secrets:
                channel_info.append(f'{emoji} {total} ({secrets} locked)')
            else:
                channel_info.append(f'{emoji} {total}')

        info = []
        features = set(guild.features)
        all_features = {
            'PARTNERED': 'Partnered',
            'VERIFIED': 'Verified',
            'DISCOVERABLE': 'Server Discovery',
            'COMMUNITY': 'Community Server',
            'FEATURABLE': 'Featured',
            'WELCOME_SCREEN_ENABLED': 'Welcome Screen',
            'INVITE_SPLASH': 'Invite Splash',
            'VIP_REGIONS': 'VIP Voice Servers',
            'VANITY_URL': 'Vanity Invite',
            'COMMERCE': 'Commerce',
            'LURKABLE': 'Lurkable',
            'NEWS': 'News Channels',
            'ANIMATED_ICON': 'Animated Icon',
            'BANNER': 'Banner'
        }

        

        e.add_field(name='Channels', value='\n'.join(channel_info))
        

        if guild.premium_tier != 0:
            boosts = f'Level {guild.premium_tier}\n{guild.premium_subscription_count} boosts'
            last_boost = max(guild.members, key=lambda m: m.premium_since or guild.created_at)
            if last_boost.premium_since is not None:
                boosts = f'{boosts}\nLast Boost: {last_boost} ({tim.human_timedelta(last_boost.premium_since, accuracy=2)})'
            e.add_field(name='Boosts', value=boosts, inline=False)

        bots = sum(m.bot for m in guild.members)
        fmt = f'Total: {guild.member_count} ({formats.plural(bots):bot})'

        e.add_field(name='Members', value=fmt, inline=False)
        e.add_field(name='Roles', value=', '.join(roles) if len(roles) < 10 else f'{len(roles)} roles')

        emoji_stats = Counter()
        for emoji in guild.emojis:
            if emoji.animated:
                emoji_stats['animated'] += 1
                emoji_stats['animated_disabled'] += not emoji.available
            else:
                emoji_stats['regular'] += 1
                emoji_stats['disabled'] += not emoji.available

        fmt = f'Regular: {emoji_stats["regular"]}/{guild.emoji_limit}\n' \
              f'Animated: {emoji_stats["animated"]}/{guild.emoji_limit}\n' \

        if emoji_stats['disabled'] or emoji_stats['animated_disabled']:
            fmt = f'{fmt}Disabled: {emoji_stats["disabled"]} regular, {emoji_stats["animated_disabled"]} animated\n'

        fmt = f'{fmt}Total Emoji: {len(guild.emojis)}/{guild.emoji_limit*2}'
        e.add_field(name='Emoji', value=fmt, inline=False)
        e.set_footer(text='Created').timestamp = guild.created_at
        await ctx.send(embed=e)

    async def say_permissions(self, ctx, member, channel):
        permissions = channel.permissions_for(member)
        e = discord.Embed(colour=member.colour)
        avatar = member.avatar_url_as(static_format='png')
        e.set_author(name=str(member), url=avatar)
        allowed, denied = [], []
        for name, value in permissions:
            name = name.replace('_', ' ').replace('guild', 'server').title()
            if value:
                allowed.append(name)
            else:
                denied.append(name)

        e.add_field(name='Allowed', value='\n'.join(allowed))
        e.add_field(name='Denied', value='\n'.join(denied))
        await ctx.send(embed=e)

    @commands.command(help="Sends how many members there are in the server.",aliases=['mc'])
    async def membercount(self, ctx):
        await ctx.send(f"This server has {ctx.guild.member_count} members!")
    
    @commands.command(help="Sends how many users use me!",aliases=['uc'])
    async def usercount(self, ctx):
        await ctx.send(f"{len(self.client.users)} users use me!")

    @commands.command(help="Sends how many commands I have.",aliases=['cc'])
    async def commandcount(self, ctx):
        await ctx.send(f"I have {len(set(self.client.commands))} commands!")


    @commands.command(help="Sends how many servers I am in!.",aliases=['sc'])
    async def servercount(self, ctx): 
        await ctx.send(f"I am in {len(self.client.guilds)} servers!")
        



    @commands.command(help="Shows info about the channel",aliases=['ci'])
    async def channelinfo(self, ctx, channel:discord.TextChannel=None):
        if channel == None:
            channel = ctx.channel
        async with channel.typing():
            em = discord.Embed(title = "Channel Info!", description = "Info about the channel", color = ctx.author.color)
            em.add_field(name = "Name", value = f"`{channel.name}`")
            em.add_field(name = "Mention", value = f"{channel.mention}")
            em.add_field(name = "Id", value = f"`{channel.id}`")
            em.add_field(name = "Category Id", value = f"`{channel.category_id}`")
            em.add_field(name = "Topic", value = f"`{channel.topic}`")
            em.add_field(name = "Slowmode", value = f"`{channel.slowmode_delay}`")
            em.add_field(name = "Position", value = f"`{channel.position}`")
            em.add_field(name = "Type", value = f"`{channel.type}`")
            em.add_field(name = "NSFW?", value = f"`{channel.is_nsfw()}`")
            em.add_field(name = "Announcments?", value = f"`{channel.is_news()}`")
            em.add_field(name = "Created At", value = f"`{channel.created_at}`")
            
            await ctx.send(embed = em)



    @commands.command(help="Shows info about the user",aliases=['ui'])
    async def userinfo(self, ctx, member : discord.Member=None):
        if member is None:
            member = ctx.author
        Who = discord.Embed(title = f"Who is {member.name}?" , description = member.mention , color = discord.Colour.dark_green())
        Who.add_field(name = "Username" , value = f'`{member.name}`', inline = True)  
        Who.add_field(name = 'Discriminator', value = f'`{member.discriminator}`', inline = True)
        Who.add_field(name = "ID", value = f'`{member.id}`' , inline = False)
        Who.add_field(name = 'Account Created', value = f'`{member.created_at}`', inline= True)
        Who.add_field(name="Status:", value=f'`{str(member.status)}`')
        Who.add_field(name = 'Top Role', value = f"<@&{member.top_role.id}>",inline= True)
        Who.add_field(name = 'Role Color', value = f'`{ctx.author.color}`',inline= True)
        Who.add_field(name="Created Account On:", value=member.created_at.strftime("`%a, %#d %B %Y, %I:%M %p UTC`"))
        Who.add_field(name="Joined Server On:", value=member.joined_at.strftime("`%a, %#d %B %Y, %I:%M %p UTC`"))
        perms = ', '.join(perm for perm, value in member.guild_permissions if value)
        Who.add_field(name="Server Perms:", value=f'`{perms}`')
        roles = [role.name.replace('@', '@\u200b') for role in getattr(member, 'roles', [])]
        role = ', '.join(roles) if len(roles) < 10 else f'{len(roles)} roles'
        if roles:
            Who.add_field(name='Roles', value=f"`{role}`", inline=False)
        Who.set_thumbnail(url = member.avatar_url)
        Who.set_footer(icon_url = ctx.author.avatar_url, text = f"Requested by {ctx.author}")
        await ctx.send(embed=Who)
    
    @commands.command(aliases=["statistics"])
    @commands.cooldown(1, 5, commands.BucketType.user) 
    async def stats(self, ctx):
        delta_uptime = datetime.datetime.utcnow() - self.client.launch_time
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        embed = discord.Embed(title=f'{self.client.user.name} Stats', colour=ctx.author.colour)
        embed.add_field(name="• Bot Name:", value=f'`{self.client.user.name}`')
        embed.add_field(name="• Bot Id:", value=f'`{self.client.user.id}`')
        embed.add_field(name="• Python Version:", value=f'`{platform.python_version()}`')
        embed.add_field(name="• Discord.py Version:", value=f'`{discord.__version__}`')
        embed.add_field(name="• Total Guilds:", value=f'`{len(self.client.guilds)}`')
        embed.add_field(name="• Total Users:", value=f'`{len(set(self.client.get_all_members()))}`')
        embed.add_field(name="• Total Commands:", value=f'`{len(set(self.client.commands))}`')
        embed.add_field(name="• Total Cogs:", value= f'`{len(set(self.client.cogs))}`')
        embed.add_field(name="• Total CPU Usage:", value=f'`{round(psutil.cpu_percent())} MB`')
        embed.add_field(name="• Total RAM:", value=f'`{round(psutil.virtual_memory()[2])} MB`')
        embed.add_field(name="• Total Spaced Used:", value=f'`{round(obj_Disk.used / (1024.0 ** 3))} MB`')
        embed.add_field(name="• Uptime:", value=f"`{days}d, {hours}h, {minutes}m, {seconds}s`", inline=True)
        
        embed.add_field(name="• Bot Developers:", value="<@801234598334955530> `&` <@814226043924643880>")
        embed.set_thumbnail(url=self.client.user.avatar_url)
        embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested {ctx.author.name}#{ctx.author.discriminator}")
        await ctx.send(embed=embed)

    @commands.command(aliases=['ri'])
    async def roleinfo(self, ctx, role: typing.Optional[discord.Role]):
        role = role or ctx.guild.default_role
        if not isinstance(role, discord.Role):
            return await ctx.send(f"Please ping a role.")

        em = discord.Embed(description=f'Roleinfo for {role.mention}', color=role.color)
        em.title = role.name
        perms = ""
        if role.permissions.administrator:
            perms += "Administrator, "
        if role.permissions.create_instant_invite:
            perms += "Create Instant Invite, "
        if role.permissions.kick_members:
            perms += "Kick Members, "
        if role.permissions.ban_members:
            perms += "Ban Members, "
        if role.permissions.manage_channels:
            perms += "Manage Channels, "
        if role.permissions.manage_guild:
            perms += "Manage Guild, "
        if role.permissions.add_reactions:
            perms += "Add Reactions, "
        if role.permissions.view_audit_log:
            perms += "View Audit Log, "
        if role.permissions.read_messages:
            perms += "Read Messages, "
        if role.permissions.send_messages:
            perms += "Send Messages, "
        if role.permissions.send_tts_messages:
            perms += "Send TTS Messages, "
        if role.permissions.manage_messages:
            perms += "Manage Messages, "
        if role.permissions.embed_links:
            perms += "Embed Links, "
        if role.permissions.attach_files:
            perms += "Attach Files, "
        if role.permissions.read_message_history:
            perms += "Read Message History, "
        if role.permissions.mention_everyone:
            perms += "Mention Everyone, "
        if role.permissions.external_emojis:
            perms += "Use External Emojis, "
        if role.permissions.connect:
            perms += "Connect to Voice, "
        if role.permissions.speak:
            perms += "Speak, "
        if role.permissions.mute_members:
            perms += "Mute Members, "
        if role.permissions.deafen_members:
            perms += "Deafen Members, "
        if role.permissions.move_members:
            perms += "Move Members, "
        if role.permissions.use_voice_activation:
            perms += "Use Voice Activation, "
        if role.permissions.change_nickname:
            perms += "Change Nickname, "
        if role.permissions.manage_nicknames:
            perms += "Manage Nicknames, "
        if role.permissions.manage_roles:
            perms += "Manage Roles, "
        if role.permissions.manage_webhooks:
            perms += "Manage Webhooks, "
        if role.permissions.manage_emojis:
            perms += "Manage Emojis, "

        if perms is None:
            perms = "None"
        else:
            perms = perms.strip(", ")

        thing = str(role.created_at.__format__('%A, %B %d, %Y'))
        em.add_field(name='Id', value=f'`{str(role.id)}`')
        em.add_field(name='Mention', value=f'{role.mention}')
        em.add_field(name='Created At', value=f'`{thing}`')
        em.add_field(name='Hoisted', value=f'`{str(role.hoist)}`')
        em.add_field(name='Position from bottom', value=f'`{str(role.position)}`')
        em.add_field(name='Managed by Integration', value=f'`{str(role.managed)}`')
        em.add_field(name='Mentionable', value=f'`{str(role.mentionable)}`')
        em.add_field(name='People in this role', value=f'`{str(len(role.members))}`')
        em.add_field(name='Role Perms', value=f'`{perms}`')
        em.set_footer(text=f"Requested by {ctx.author}")

        await ctx.send(embed=em)

def setup(client):
    client.add_cog(Info(client))