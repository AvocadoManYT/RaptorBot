import discord
from discord.ext import commands
from main import restart_reason as rr, owners, note
import datetime
import json
import DiscordUtils
from datetime import datetime
from discord.ext.commands import Cog as c, command as cmd


class Miscellaneous(commands.Cog):
    """ Cog for miscellaneous commands"""
    async def open_accoun(self, user):
        with open("json/cmdusage.json", "r") as f:
            
            data = json.load(f)

        if str(user.id) in data:
            return False
        else:
            data[str(user.id)] = {}
            data[str(user.id)]["cmdcount"] = 0

            with open("json/cmdusage.json", "w") as f:
                json.dump(data,f)
            return True

    async def open_account(self, user):
        with open("mainbank.json", "r") as f:
            users = json.load(f)
            

        if str(user.id) in users:
            return False
        else:
            users[str(user.id)] = {}
            users[str(user.id)]["wallet"] = 0
            users[str(user.id)]["bank"] = 0
            users[str(user.id)]["bankspace"] = 0
            users[str(user.id)]["gambles"] = {}
            users[str(user.id)]["gambles"]["dice"] = {}
            users[str(user.id)]["gambles"]["dice"]["win"] = 0
            users[str(user.id)]["gambles"]["dice"]["loss"] = 0
            users[str(user.id)]["gambles"]["slots"] = {}
            users[str(user.id)]["gambles"]["slots"]["win"] = 0
            users[str(user.id)]["gambles"]["slots"]["loss"] = 0
            users[str(user.id)]["gambles"]["bet"] = {}
            users[str(user.id)]["gambles"]["bet"]["win"] = 0
            users[str(user.id)]["gambles"]["bet"]["loss"] = 0

            with open("mainbank.json", "w") as f:
                json.dump(users,f)
            return True

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Misc is ready")

    @c.listener()
    async def on_command_completion(self, ctx):
        await self.open_accoun(ctx.author)
        with open("json/cmdusage.json", "r") as f:
            data = json.load(f)

        data[str(ctx.author.id)]["cmdcount"] += 1

        msg = ctx
        with open("json/cmdusage.json", "w") as f:
            json.dump(data, f)
        with open("mainbank.json", "r") as f:
            users = json.load(f)
        await self.open_account(msg.author)
        users[str(msg.author.id)]["bankspace"] += 2
        with open("mainbank.json", "w") as f:
            json.dump(users, f)

    async def get_g_stats(self, user, mode, worl):
        with open("mainbank.json", "r") as f:
            users = json.load(f)
        
        return users[str(user.id)]["gambles"][mode][worl]

    @cmd(aliases=['pro'])
    async def profile(self, ctx, member:discord.Member=None):
        if member == None:
            member = ctx.author
        with open("json/cmdusage.json", "r") as f:
            data = json.load(f)
        cmd_usage = data[str(member.id)]["cmdcount"]
        cmd = int(cmd_usage) + 1
        embed = discord.Embed(title = f"{member}'s Profile", color = member.color)
        embed.add_field(name = "Economy", value = "Press :one: to go to your economy stats")
        embed.add_field(name = "Gambling", value = "Press :two: to go to your gambling stats")
        embed.add_field(name = "Other", value = "Press :three: to go to your other stats")
        embed.add_field(name = "Clear", value = "Press :lock: to clear all reactions")
        embed.add_field(name = "Home", value = "Press 🏠 to come back to this page")
        await self.open_account(member)
        user =  member
        with open("mainbank.json", "r") as f:
            users = json.load(f)
        wallet_amt = users[str(user.id)]["wallet"]
        bank_amt = users[str(user.id)]["bank"]
        bankspace = users[str(user.id)]["bankspace"]
        net_worth = bank_amt + wallet_amt
        embe = discord.Embed(title = "Economy Stats", description = f"*These are your economy stats!*", color = discord.Color.random())
        embe.add_field(name = "Wallet Balance :dollar:", value = f"`△ {wallet_amt}`")
        embe.add_field(name = "Bank Balance :bank:", value = f"`△ {bank_amt}`")
        embe.add_field(name = "Bankspace :bank:", value = f"` {bankspace}`")
        embe.add_field(name = "Net Worth :moneybag:", value = f"`△ {net_worth}`")
        embe.set_thumbnail(url = member.avatar_url)
        embe.set_footer(text = f"Requested By {ctx.author}", icon_url = ctx.author.avatar_url)
        emb = discord.Embed(title = "Gamble Stats", description = f"*These are your gamble stats!*",color = discord.Color.random())
        slw = int(await self.get_g_stats(member, "slots", "win"))
        sll = int(await self.get_g_stats(member, "slots", "loss"))
        if sll == 0:
            sll = 1
        wsl = round((slw / sll) *100)
        if slw == 0:
            slw = 1
        lsl = 100 - int(wsl)
        btw = int(await self.get_g_stats(member, "bet", "win"))
        btl = int(await self.get_g_stats(member, "bet", "loss"))
        if btl == 0:
            btl = 1
        wbt = round((btw / btl) *100)
        if btw == 0:
            btw = 1
        lbt = 100 - int(wbt)
        dcw = int(await self.get_g_stats(member, "dice", "win"))
        dcl = int(await self.get_g_stats(member, "dice", "loss"))
        if dcl == 0:
            dcl = 1
        wdc = round((dcw / dcl) *100)
        if dcw == 0:
            dcw = 1
        ldc = 100 - int(wdc)
        emb.add_field(name = "Slots Winrate 🎰", value = f"`{wsl}%`")
        emb.add_field(name = "Bet Winrate <:bet:854449628899835914>", value = f"`{wbt}%`")
        emb.add_field(name = "Dice Winrate <:BlueDice:836718117031772202>", value = f"`{wdc}%`")
        emb.add_field(name = "Slots Lossrate 🎰", value = f"`{lsl}%`")
        emb.add_field(name = "Bet Lossrate <:bet:854449628899835914>", value = f"`{lbt}%`")
        emb.add_field(name = "Dice Lossrate <:BlueDice:836718117031772202>", value = f"`{ldc}%`")
        emb.set_thumbnail(url = member.avatar_url)
        emb.set_footer(text = f"Requested By {ctx.author}", icon_url = ctx.author.avatar_url)
        em = discord.Embed(title = "Other Stats", description = f"*These are your other stats!*", color = discord.Color.random())
        em.add_field(name = "Commands Used <:Cmd:854449628988964915>", value = f"`{cmd}`")
        em.set_thumbnail(url = member.avatar_url)
        em.set_footer(text = f"Requested By {ctx.author}", icon_url = ctx.author.avatar_url)
        embeds = [embed, embe, emb, em]
        paginator = DiscordUtils.Pagination.CustomEmbedPaginator(ctx)
        paginator.add_reaction('1️⃣', "page 1")
        paginator.add_reaction('2️⃣', "page 2")
        paginator.add_reaction('3️⃣', "page 3")
        paginator.add_reaction('🔐', "clear")
        paginator.add_reaction('🏠', "page 0")
        await paginator.run(embeds)


    @commands.command()
    async def setup(self, ctx):
        guild = discord.Embed(title = "Hi there! I'm Raptor, a fun bot with moderation abilities, and economy system, and more!", description = "Use `rap help` to see all of my commands but here's some information to get you started!", color = discord.Colour.dark_green())
        guild.add_field(
        name = "Economy",
        value = "Raptor has a great ecomony that let's you work, buy stuff, see the money leaderboard and more!"
        )
        guild.add_field(
        name = "Music",
        value = "Raptor can play your favorite music and songs! Be sure that you are in a voice channel then use its commands such as play, loop, queue and more!"
        )
        guild.add_field(
        name = "Moderate",
        value = "Raptor can easily moderate your server  using commands such as purge, kick, ban, lock and more!"
        ) 
        guild.add_field(
        name = "Info",
        value = "Raptor can show you info about anything including the server, channels, users and roles!"
        )                 
        guild.add_field(
        name = "Fun",
        value = "Raptor lets you enjoy and have using it's fun commands! Commands include kill, troll, drink, animal facts, gifs and more!"
        )     
        guild.add_field(
        name = "Games",
        value = "Raptor can let you play your favorite games such as chess, connect4, survival, hangman and more!"
        )    
        guild.add_field(
        name = "Giveaway",
        value = "Raptor can create givaways, reroll them, end them and so much more!"
        )  
        guild.add_field(
        name = "Utility",
        value = "Raptor can help you with utility items such as afk, invites and more!"
        )      
        guild.add_field(
        name = "Math",
        value = "Raptor can help you with math problems as it can do the basic math as well as square rooting and more!"
        )    
        guild.add_field(
        name = "Images",
        value = "Raptor can manipulate images and make them look funny! Command examples are kannagen, wanted, rip and more!"
        )    
        guild.set_thumbnail(url = "https://media.discordapp.net/attachments/806574171513421867/833767333151244319/Raptor.jpeg")
        guild.set_footer(text = "Please give me all admin permissions otherwise my commands might not work.")

        await ctx.channel.send(embed = guild)

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
    async def note(self, ctx):
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
        em = discord.Embed(title = "Support Server", description = "[Click Here](https://discord.gg/89xvwGe36C)", color = ctx.author.color)
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