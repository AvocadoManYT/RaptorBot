import discord
import asyncio
import json
import aiofiles
from discord.ext import commands

class Moderation(commands.Cog):
    """ Category for moderation commands """

    def __init__(self, client):
        self.client = client

    # events
    @commands.Cog.listener()
    async def on_ready(self):
        print('mod cog is ready.')

        

    # commands
    

    
    @commands.command()
    async def getbans(self, ctx):
        """Lists all banned users on the current server."""
        
        if ctx.message.author.guild_permissions.ban_members:
            x = await ctx.message.guild.bans()
            x = '\n'.join([str(y.user) for y in x])
            embed = discord.Embed(title="List of Banned Members", description=x, colour=0xFFFFF)
            return await ctx.send(embed=embed)
        else:
            await ctx.send("You don't have the perm `ban_member` which is required to use this command")

    @commands.command(help="Create a role!")
    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_permissions(manage_roles= True)
    async def createrole(self, ctx, name, *, reason = "No reason provided"):
            await ctx.guild.create_role(name, reason)
            await ctx.send(f"Created a role called {name} for the reson of {reason}!")


    @commands.command()
    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_permissions(manage_roles= True)
    async def addrole(self, ctx, user : discord.Member, *, role : discord.Role):
        if role.position > user.top_role.position:
            return await ctx.send('You\'re not high enough in the role heiarchy to do that.')
        if role in user.roles:
            await ctx.send(f"{user.mention} already has {role.mention}.")
        else:
            await user.add_roles(role)
            await ctx.send(f"Added {role.mention} to {user.mention}!")



    @commands.command(aliases=['remrole'])
    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_permissions(manage_roles= True)
    async def removerole(self, ctx, user : discord.Member, *, role : discord.Role):
        if role.position > user.top_role.position:
            return await ctx.send('You\'re not high enough in the role heiarchy to do that.')
        if role in user.roles:
            await user.remove_roles(role)
            await ctx.send(f"Removed {role.mention} from {user.mention}!")
        else:
            await ctx.send(f"{user.mention} doesn\'t have {role.mention}")
        



    @commands.command()
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(manage_channels= True)
    async def lock(self, ctx):
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
        purge_embed = discord.Embed(title="This channel is on *lockdown*", description="**This channel is on lockdown**! You **have not** been muted! Please wait for the channel to re open again!")
        await ctx.send(embed = purge_embed)
        if not ctx.author.has_permissions.manage_channels:
            return await ctx.send("I am sorry but you do not have the Manage Channels permission required for this command.")
        if not ctx.channel.permissions(ctx.guild.default_role, send_messages=False):
            await ctx.send("This channel is already locked.")


        
        

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(manage_channels= True)
    async def unlock(self, ctx):
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
        purge_embed = discord.Embed(title="This channel is no longer on *lockdown*", description="**This channel has reopened!** You may continue talking.")
        await ctx.send(embed = purge_embed)




    @commands.command(aliases=['c_t','ct'])
    @commands.has_permissions(administrator=True)
    @commands.bot_has_permissions(administrator=True)
    async def create_text(self, ctx, *, name = None):
        if name == None:
            await ctx.send("Please enter a name for the new channel.")
        if not commands.has_permissions(administrator=True):
            await ctx.reply("You dont have admin buddy.")
        else:
            await ctx.send(f"I have created the channel with the name of {name}!")
            await ctx.guild.create_text_channel(name)



    @commands.command(aliases=['cl_t','clt'])
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(manage_channels= True)
    async def clone_text(self, ctx, channel:discord.TextChannel):
        if not commands.has_permissions(manage_channels=True):
            await ctx.reply("You dont have the Manage Channel perms buddy.")
        else:
            await channel.clone()
            await ctx.send(f"I have cloned {channel}!")


    @commands.command(aliases=['d_c','dc'])
    @commands.has_permissions(administrator=True)
    @commands.bot_has_permissions(administrator=True)
    async def delete_channel(self, ctx, channel : discord.TextChannel):
        if channel == None:
            await ctx.send("Please enter the name for the channel you want deleted.")
        if not commands.has_permissions(administrator=True):
            await ctx.reply("You dont have admin buddy.")
        else:
            await ctx.send(f"I have deleted {channel.mention}!")
            await channel.delete()

        

    @commands.command(aliases=['setslow','ssm'])
    @commands.has_permissions(administrator = True)
    @commands.bot_has_permissions(administrator=True)
    async def setslowmode(self, ctx, seconds: int):
        await ctx.channel.edit(slowmode_delay=seconds)
        await ctx.send(f"Set the slowmode delay in this channel to {seconds} seconds!")


    @commands.command(aliases=['removeslow','rsm'])
    @commands.has_permissions(administrator = True)
    @commands.bot_has_permissions(administrator=True)
    async def removeslowmode(self, ctx):
        await ctx.channel.edit(slowmode_delay=0)
        await ctx.send(f"Turned off the slowmode!")

        

    @commands.command(aliases=['p'])
    @commands.has_permissions(manage_messages = True)
    @commands.bot_has_permissions(manage_messages=True)
    async def purge(self, ctx,amount=1):
        am = amount + 1
        await ctx.channel.purge(limit = am)
        await ctx.send(f"I have purged {amount} messages!")
        await asyncio.sleep(5)
        await ctx.channel.purge(limit = 1)
        if amount == 0:
                await ctx.send("You need to put an amount of messages to purge")
        


    @commands.command(aliases=['k'])
    @commands.has_permissions(kick_members = True)
    @commands.bot_has_permissions(kick_members = True)
    async def kick(self, ctx,member : discord.Member,*,reason= "No reason Provided"):
        try:
            await member.send(f"You have been kicked from {ctx.guild.name}. Reason: " +reason)
        except:
            await ctx.send("The user mentioned has their dm's closed so the dm has not been sent but they will still get kicked.")
        await member.kick(reason=reason)
        await ctx.send(member.name + " has been kicked from this server. Reason: " +reason)


    @commands.command(aliases=['b'])
    @commands.has_permissions(ban_members = True)
    @commands.bot_has_permissions(ban_members = True)
    async def ban(self, ctx, member : discord.Member,*,reason= "No reason Provided"):
      if member == ctx.author:
        await ctx.send("**:x: | Why would you want to ban yourself?!**")
        return
      else:
        await ctx.send(member.name + f" has been banned from {ctx.guild.name}. Reason: " +reason)
        try:
            await member.send(f"You have been banned from {ctx.guild.name}. Reason: " +reason)
        except:
            await ctx.send(f"{member.mention}\'s dms are closed.")
        await member.ban(reason=reason)
        await ctx.channel.purge(limit = 1)



    @commands.command(aliases=['ub'])
    @commands.has_permissions(ban_members = True)
    @commands.bot_has_permissions(ban_members = True)
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        
        member_name, member_discriminator = member.split('#')
        for ban_entry in banned_users:
            user = ban_entry.user
            
            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)

            else:
                await ctx.send("Could not find that user. Maybe try again?")
                await ctx.channel.send(f"I have unbanned {user.mention}!")


    
    @commands.command()
    @commands.is_owner()
    async def nuke(self, ctx):
        await ctx.channel.purge()
        await asyncio.sleep(2)
        await ctx.send(ctx.author.mention)
        await ctx.send("<a:Yestick:831948152273633332> I have nuked the channel!")

def setup(client):
    client.add_cog(Moderation(client))