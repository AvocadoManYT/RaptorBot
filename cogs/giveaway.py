import discord
import datetime
import asyncio
import random
from discord.ext import commands

class Giveaway(commands.Cog):
    """ Category for giveaway commands """

    def __init__(self, client):
        self.client = client
        self.cancelled = False

    # events
    @commands.Cog.listener()
    async def on_ready(self):
        print('Giveaway cog is online.')

    # commands
    
    
    @commands.command()
    async def gstart(self, ctx, mins : int, * , prize: str):
        await ctx.message.delete()
        gstart = discord.Embed(title = "Giveaway!", description = f"{prize}", color = ctx.author.color)
        
        print(f'A gaw started at {datetime.datetime.utcnow()}')
        end = datetime.datetime.utcnow()

        gstart.add_field(name = "Hosted By:", value = f"{ctx.author.mention}", inline = True)
        gstart.add_field(name = "Ends At:", value = f"{end} UTC", inline = False)
        gstart.set_footer(text = f"Ends {mins} minutes from now!")

        my_msg = await ctx.send(embed = gstart)

        await my_msg.add_reaction("<a:PartyConfetti:833535697981014064>")

        await asyncio.sleep(mins*60)

        new_msg = await ctx.channel.fetch_message(my_msg.id)

        try:
            users = await new_msg.reactions[0].users().flatten()
            users.pop(users.index(self.client.user))

            print(users)

            winner = random.choice(users)

            await ctx.send(f"Congratulation! {winner.mention} won {prize}!")

            win = discord.Embed(title = "Prize:", description = prize)
            win.add_field(name = "Winner:", value = winner.mention)
            win.add_field(name = "Hosted By:", value = ctx.author)
            win.set_author(name = "Giveaway Ended!")
            await my_msg.edit(embed=win)
        except:
            await ctx.send("No one joined the giveaway :/")
            win = discord.Embed(title = "Prize:", description = prize)
            win.add_field(name = "Winner:", value = "No one")
            win.add_field(name = "Hosted By:", value = ctx.author)
            win.set_author(name = "Giveaway Ended!")
            await my_msg.edit(embed=win)

        



    @commands.command()
    async def gcreate(self, ctx):
        await ctx.send("Let's start with this giveaway! Answer these questions within 15 seconds!")

        questions = ["Which channel should it be hosted in?", 
                    "What should be the duration of the giveaway? (s|m|h|d)",
                    "What is the prize of the giveaway?",
                    "What emoji do you want as the reaction? (pls only send a defualt emoji)"]

        answers = []

        def convert(self, time):
            pos = ["s","m","h","d"]

            time_dict = {"s" : 1, "m" : 60, "h" : 3600 , "d" : 3600*24}

            unit = time[-1]

            if unit not in pos:
                return -1
            try:
                val = int(time[:-1])
            except:
                return -2


            return val * time_dict[unit]
        
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        for i in questions:
            await ctx.send(i)

            try:
                msg = await self.client.wait_for('message', timeout=15.0, check=check)
            except asyncio.TimeoutError:
                await ctx.send('You didn\'t answer in time, please be quicker next time!')
                return
            else:
                answers.append(msg.content)
        try:
            c_id = int(answers[0][2:-1])
        except:
            await ctx.send(f"You didn't mention a channel properly. Do it like this:{ctx.channel.mention} next time.")
            return

        channel = self.client.get_channel(c_id)

        time = convert(self, answers[1])
        if time == -1:
            await ctx.send(f"You didn't answer the time with a proper unit. Use (s|m|h|d) next time!")
            return
        elif time == -2:
            await ctx.send(f"The time must be an integer. Please enter an integer next time")
            return            

        prize = answers[2]

        emoji = answers[3]

        await ctx.send(f"The Giveaway will be in {channel.mention} and will last {answers[1]}!")


        embed = discord.Embed(title = prize, description = f"Hosted by: {ctx.author.mention}", color = ctx.author.color)

        embed.set_author(name='Giveaway', icon_url='https://media.discordapp.net/attachments/829073409564606516/841356504997036102/3461-giveaway.gif')

        embed.add_field(name=f'React with {emoji} to join the giveaway!', value='Enjoy!')

        embed.set_footer(text = f"Ends {answers[1]} from now!")
        my_msg = await channel.send(embed = embed)


        await my_msg.add_reaction(emoji)


        await asyncio.sleep(time)


        new_msg = await channel.fetch_message(my_msg.id)


        users = await new_msg.reactions[0].users().flatten()
        users.pop(users.index(self.client.user))

        winner = random.choice(users)

        await channel.send(f"Congratulations! {winner.mention} won **{prize}**!")

        win = discord.Embed(title = "Prize:", description = prize, color = ctx.author.color)
        win.add_field(name = "Winner:", value = winner.mention)
        win.add_field(name = "Hosted By:", value = ctx.author, inline = False)
        win.set_author(name = "Giveaway Ended!")
        await my_msg.edit(embed=win)


    @commands.command()
    async def greroll(self, ctx, channel : discord.TextChannel, id_ : int):
        try:
            new_msg = await channel.fetch_message(id_)
        except:
            await ctx.send("The id was entered incorrectly.")
            return
        
        users = await new_msg.reactions[0].users().flatten()
        users.pop(users.index(self.client.user))

        winner = random.choice(users)

        await channel.send(f"Congratulations! The new winner is {winner.mention}.!")

    @commands.command()
    async def gdonate(self, ctx, amount, _time, winners, requirement, *, message):
        await ctx.message.add_reaction("✅")
        embed = discord.Embed(title='Someone wants to donate!', description = f"Donator = {ctx.author}", color = ctx.author.color)
        embed.add_field(name="Amount", value = amount)
        embed.add_field(name="Time", value = _time, inline=True)
        embed.add_field(name="Winners", value = winners, inline=False)
        embed.add_field(name="Requirements", value = requirement, inline=True)
        embed.add_field(name="Message", value = message, inline=False)
        embed.set_footer(text=f"Thank {ctx.author} in chat!", icon_url=ctx.author.avatar_url)
        await ctx.send(embed = embed)

    @commands.command(aliases=['gdm', 'gdonatemsg', 'gdmsg', 'gdmessage'])
    async def gdonatemessage(self, ctx, member:discord.Member, *, message):
        em = discord.Embed(title="Someone donated for a giveaway!",color = ctx.author.color)
        em.add_field(name=f'Donated By {member}', value = f'Message: {message}')
        em.set_footer(text='Thank in chat')
        await ctx.message.delete()
        await ctx.send(embed = em)

    @commands.command()
    async def gend(self, ctx, channel : discord.TextChannel, id_: int):
        try:
            msg = await channel.fetch_message(id_)
            newEmbed = discord.Embed(title="Giveaway Cancelled", description="The giveaway has been cancelled!!")
            #Set Giveaway cancelled
            self.cancelled = True
            await msg.edit(embed=newEmbed) 
        except:
            embed = discord.Embed(title="Failure!", description="Cannot cancel giveaway", color = discord.Color.red())
            await ctx.send(emebed=embed)
def setup(client):
    client.add_cog(Giveaway(client))    