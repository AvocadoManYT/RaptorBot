import discord
from discord.ext import commands
from main import owners
import json
import inspect
from discord.ext.commands import Cog as c

class Owner(c, name = "OwnerOnly"):
    """ Cog for commands that only <@801234598334955530> and <@814226043924643880> should use """
    def __init__(self, client):
        self.client = client

    @c.listener()
    async def on_ready(self):
        print("Owner only cmds are ready")

    

    


        

    
    @commands.command(help="Dm's a person if their dms are open.")
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def dm(self, ctx, user_id=None, *, msg=None):
        if ctx.author.id in owners:
            if user_id != None and msg != None:
                try:
                    target = await self.client.fetch_user(user_id)
                    await target.send(msg)

                    await ctx.channel.send("'" + msg + "' sent to: " + target.name)

                except:
                    await ctx.channel.send("Couldn't dm the given user.")
            else:
                await ctx.channel.send("You didn't provide a user's id and/or a message.")
        else:
            await ctx.send("You're not my owner")

    @commands.command(aliases=['gc', 'getcode'])
    async def get_code(self, ctx, *, cmd):
        try:
            if ctx.author.id in owners:
                command = self.client.get_command(cmd)
                embed = discord.Embed(title=f"**{cmd}!**", color = ctx.author.color)
                embed.add_field(name = "Code:", value = f"```py\n{inspect.getsource(command.callback)}```")
                await ctx.send(embed = embed)
            else:
                await ctx.send("You're not my owner.")
        except:
            await ctx.send("Either that is not a command or the code it too long to display.")

def setup(client):
    client.add_cog(Owner(client))