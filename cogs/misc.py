import discord
from discord.ext import commands
from main import restart_reason as rr, owners, note
import datetime
from datetime import datetime

class Miscellaneous(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Misc is ready")

    @commands.command()
    async def developer(self, ctx):
        embed=discord.Embed(
        title = "Developers of Raptor!",
        description = f"The active developers of Raptor are:\n<@801234598334955530> - **Main Developer**\nAND\n<@814226043924643880> - **Secondary Developer**!",
        color = 0x00ff00)
        embed.set_footer(text = "Thank you for using Raptor!")
        embed.set_author(
        name = "Developers of Raptor!", icon_url = self.client.user.avatar_url
    )
    
        await ctx.send(embed=embed)

    @commands.command(help="Sends the links where you can vote for me!")
    async def vote(self, ctx):
        vtlk = discord.Embed(title = "Vote for Me!", description ="Vote for me by using these links!", color = ctx.author.color)
        vtlk.add_field(name = "Top.gg", value = "[Click Here](https://top.gg/bot/829836500970504213/vote)")
        vtlk.add_field(name = "Discord Bot List", value = "[Click Here](https://discordbotlist.com/bots/raptor/upvote)")
        await ctx.send(embed = vtlk)

    @commands.command()
    async def ownertest(self, ctx):
        if ctx.author.id not in owners:
            await ctx.send("This command is owner only!")
            return
        else:
            embed = discord.Embed(
            title = "Owner Only!",
            description = note
            )
            await ctx.send(embed=embed)

    

    @commands.command(help="Sends the links where you can review me!")
    async def review(self, ctx):
        vtlk = discord.Embed(title = "Review Me!", description ="Review me by using these links!", color = ctx.author.color)
        vtlk.add_field(name = "Top.gg", value = "[Click Here](https://top.gg/bot/829836500970504213)")
        vtlk.add_field(name = "Discord Bot List", value = "[Click Here](https://discordbotlist.com/bots/raptor)")
        await ctx.send(embed = vtlk)

    @commands.command(help="Sends the link for the support server")
    async def support(self, ctx):
        em = discord.Embed(title = "Support Server", description = "[Click Here](https://discord.gg/CwAAxx7YyJ)", color = ctx.author.color)
        await ctx.send(embed = em)
    
    @commands.command(help="Sends the link to invite Raptor!")
    async def invite(self, ctx):
        em = discord.Embed(title = "Invite Me!", description = "[Click Here](https://discord.com/api/oauth2/authorize?client_id=829836500970504213&permissions=8&redirect_uri=https%3A%2F%2Fraptor-dbot.glitch.me%2Fthx.html&response_type=code&scope=bot%20applications.commands%20identify)", color = ctx.author.color)
        em.set_footer(text = f"Requested by {ctx.author}", icon_url = ctx.author.avatar_url)
        await ctx.reply(embed = em)

    @commands.command(help=f"Shows how long Raptor has been online for and other stuff.")
    async def uptime(self, ctx):
        delta_uptime = datetime.utcnow() - self.client.launch_time
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        em = discord.Embed(
            title = "Raptor",
            description = "Raptor the bot's uptime command!",
            color = ctx.author.color
        )
        em.add_field(name = "Uptime", value = f"```fix\nI have been online for {days} days, {hours} hours, {minutes} minutes and {seconds} seconds!```")
        em.add_field(name = "Reason For Last Restart", value = f"```fix\n{rr}```")
        await ctx.send(embed = em)


    @commands.command(help="Sends the link to my website!")
    async def website(self, ctx):
        em = discord.Embed(title="Go check my website out!", description = "[Click Here](https://raptor-dbot.glitch.me/)", color = ctx.author.color)
        await ctx.send(embed = em)

    @commands.command()
    async def avm(self, ctx):
        em = discord.Embed(
            title = "Join Raptor's owner's server; Avocado Man's Community or AVM!",
            description = ":pray: Pls Join",
            url = "https://discord.gg/k36haH6m9T",
            timestamp = datetime.now(),
            color = ctx.author.color
        )
        await ctx.send(embed = em)

def setup(client):
    client.add_cog(Miscellaneous(client))