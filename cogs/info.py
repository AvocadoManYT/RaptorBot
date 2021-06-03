import discord
import platform
import asyncio
import json
import datetime
import os
import typing
import DiscordUtils
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
        

    @commands.command(help="Shows info about the server",aliases=['si'])
    async def serverinfo(self, ctx):
        name = str(ctx.guild.name)
        description = str(ctx.guild.description)

        owner = f'`{str(ctx.guild.owner)}`'
        _id = f'`{str(ctx.guild.id)}`'
        region = f'`{str(ctx.guild.region)}`'
        memberCount = f'`{str(ctx.guild.member_count)}`'

        icon = str(ctx.guild.icon_url)

        embed = discord.Embed(
            title=name + " Server Information",
            description=f"Description = {description}",
            color=discord.Color.blue()
        )
        embed.set_thumbnail(url=icon)
        embed.add_field(name="Owner", value=owner, inline=True)
        embed.add_field(name="Server ID", value=_id, inline=True)
        embed.add_field(name="Region", value=region, inline=True)
        embed.add_field(name="Member Count", value=memberCount, inline=True)
        embed.add_field(name="Role Count", value=f'`{len(ctx.guild.roles)}`', inline=True)
        embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)

        await ctx.send(embed=embed)

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
        current_time = time.time()
        uname = platform.uname()
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
        
        embed.add_field(name="• Bot Developers:", value="<@801234598334955530>")
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