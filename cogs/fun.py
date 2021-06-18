import discord
import datetime
import time
import asyncio
import googlesearch
import random
import requests
import praw
from dpy_button_utils.confirmation import ButtonConfirmation
import wikipedia
import aiohttp
import urllib, re
import giphy_client
from giphy_client.rest import ApiException
from discord.ext import commands



err_color = discord.Color.red()
color = 0x0da2ff
yt_key = "AIzaSyDVMJyIjsAal6dssgA0bQmGVGblH7pS2Bw"
class Fun(commands.Cog):
    """ Category for fun commands """
    def __init__(self, client):
        self.client = client
        self.malid = None
        self.loop = asyncio.get_event_loop()
        self.bot = client
        self.session = aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=30))
        
   # events
    @commands.Cog.listener()
    async def on_ready(self):
        print('Fun cog is ready.')

    @commands.command()
    async def funfact(self, ctx):
        response = requests.get("https://useless-facts.sameerkumar.website/api")
        data = response.json()
        fact = data['data']
        await ctx.send(fact)

    
  


    @commands.command(aliases=['ar'])
    async def addreaction(self, ctx, msg: discord.Message=None, emoji=None):
        try:
            await msg.add_reaction(emoji)
            await ctx.send("Did it!")
        except:
            await ctx.send("Error 101")

    @commands.command(aliases=['gi', 'google'])
    async def googleit(self, ctx, amount_of_results:int=5, *, term):
        res = googlesearch.search(term, num_results=amount_of_results, lang="en")
        em = discord.Embed(title='Google Search',description="Here you go!")
        index = 0
        try:
            for i in res:
                index += 1
                em.add_field(name = index, value = i, inline = False)
            await ctx.message.channel.send(embed=em)
        except:
            await ctx.send("error 404 not found")

        



    @commands.command(description='Sends a random year fact.')
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def yearfact (self, ctx):

        async with aiohttp.ClientSession() as cs:

            async with cs.get(f"http://numbersapi.com/random/year?json") as r:
                data = await r.json()

                embed = discord.Embed(title= data['number'], description=data['text'], colour=0x529dff)

                embed.set_footer(text=f"Requested by {ctx.author}, Fact from numbersapi.com", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
    # command
    

    @commands.command(aliases=["fancy"])
    async def fancify(self, ctx, *, text):
        """Makes text fancy!"""
        try:
            def strip_non_ascii(string):
                """Returns the string without non ASCII characters."""
                stripped = (c for c in string if 0 < ord(c) < 127)
                return ''.join(stripped)

            text = strip_non_ascii(text)
            if len(text.strip()) < 1:
                return await ctx.send(":x: ASCII characters only please!")
            output = ""
            for letter in text:
                if 65 <= ord(letter) <= 90:
                    output += chr(ord(letter) + 119951)
                elif 97 <= ord(letter) <= 122:
                    output += chr(ord(letter) + 119919)
                elif letter == " ":
                    output += " "
            await ctx.send(output)

        except:
            await ctx.send("Error 101... Try again later")

    


    roasts = ["You’re the reason God created the middle finger.",
          "You’re a grey sprinkle on a rainbow cupcake.",
          "If your brain was dynamite, there wouldn’t be enough to blow your hat off.",
          "You are more disappointing than an unsalted pretzel.",
          "Light travels faster than sound which is why you seemed bright until you spoke.",
          "We were happily married for one month, but unfortunately we’ve been married for 10 years.",
          "Your kid is so annoying, he makes his Happy Meal cry.",
          "You have so many gaps in your teeth it looks like your tongue is in jail.",
          "Your secrets are always safe with me. I never even listen when you tell me them.",
          "I’ll never forget the first time we met. But I’ll keep trying."
          "I forgot the world revolves around you.My apologies, how silly of me.",
          "I only take you everywhere I go just so I don’t have to kiss you goodbye.",
          "Hold still.I’m trying to imagine you with personality.",
          "Our kid must have gotten his brain from you! I still have mine.",
          "Your face makes onions cry.",
          "The only way my husband would ever get hurt during an activity is if the TV exploded.",
          "You look so pretty.Not at all gross, today.",
          "It’s impossible to underestimate you."]


    

    @commands.command()
    async def roast(self, ctx, member:discord.Member=None):
        if member == None:
            return await ctx.send("I can't roast nobody!")
        if member.bot:
            return await ctx.send("Back off from my kind buddy")
        if member == self.client.user:
            return await ctx.send("Why do you wanna yomomma me?")
        if member == ctx.author:
            return await ctx.send("Why do you wanna roast yourself?")
        else:
            await ctx.send(member.mention)
            await ctx.send(random.choice(self.roasts))

    choices = ['Yo momma so fat when she walked past the TV I missed three episodes',
           'Yo momma so fat she needs cheat codes for Wii Fit',
           'Yo momma so fat when she went to KFC and they asker her what size of bucket, she said "The one on the roof"',
           'Yo momma so fat, I took a picture of her last Christmas and it\'s still printing',
           'Yo momma so fat and old when God said "Let there be light" he asked your momma to step out of the way',
           'Yo momma so fat when she stept out in a yellow jacket people yell TAXI',
           'Yo momma so fat I tried driving around her and I ran out of gas',
           'Yo momma so fat it took Thanos two snaps to kill her',
           'Yo momma so fat she sued Nintendo for guessing her weight',
           'Yo momma so dumb, she tripped over WiFi',
           'Yo momma so fat she has two watches, one for each timezone',
           'Yo momma so fat she left the house in high heels and came back in flip flops',
           'Yo momma so fat her blood type is Nutella',
           'Yo momma so fat she uses Google Earth to take a selfie',
           'Yo momma so fat even Dora could not explore her',
           'Yo momma so fat she jumped in the air and got stuck',
           'Yo momma so fat that when we were born, she gave the hospital stretch marks',
           'Yo momma so fat she wears a sock on each toe',
           'Yo momma so fat the army uses her underwear as parachutes',
           'Yo momma so fat her patronus is a cake',
           'Yo momma so fat when she tripped over on 4th Ave, she landed on 12th',
           'Yo momma so fat the only way she burns calories is when her food is on fire',
           'Yo momma so fat she won all 75 Hunger Games',
           'Yo momma so fat when she steps on a scale it says "One at a time please"',
           'Yo momma so fat she got her own area code',
           'Yo momma so fat even Kirby can'' eat her',
           'Yo momma so fat when she went to the beach Greenpeace threw her into the ocean',
           'Yo momma so fat a vampire bit her and got Type 2 diabetes',
           'Yo momma so fat she uses butter for her chapstick',
           'Yo momma so fat when she walks backwards she beeps',
           'Yo momma so fat she puts mayo on her diet pills']


    

    @commands.command()
    async def yomomma(self, ctx, member:discord.Member=None):
        if member == None:
            return await ctx.send("I can't yomomma nobody!")
        if member.bot:
            return await ctx.send("Back off from my kind buddy")
        if member == ctx.author:
            return await ctx.send("Why do you wanna yomomma yourself?")
        if member == self.client.user:
            return await ctx.send("Why do you wanna yomomma me?")
        else:
            await ctx.send(member.mention)
            await ctx.send(random.choice(self.choices))





    @commands.group(invoke_without_command=True)
    async def anime(self, ctx):
        """
        Anime gif commands
        """
        em = discord.Embed(title = "Anime Commands!", description = "Anime commands are: `rap anime wink`, `rap anime pat`, `rap anime hug`, `rap anime facepalm`, `rap anime quote`", color = ctx.author.color)
        em.set_footer(text = "Enjoy!")
        await ctx.send(embed = em)

    @anime.command(name='wink')
    async def _anime_wink(self, ctx):
        """
        anime wink gif
        """
        try:
            image = await self.bot.sr_api.get_gif('wink')
        except:  # noqa: E722
            return await ctx.send('Error with API, please try again later')
        embed = discord.Embed(title='Wink')
        embed.set_image(url=image.url)
        await ctx.send(embed=embed)

    @anime.command(name='pat')
    async def _anime_pat(self, ctx):
        """
        anime pat gif
        """
        try:
            image = await self.bot.sr_api.get_gif('pat')
        except:  # noqa: E722
            return await ctx.send('Error with API, please try again later')
        embed = discord.Embed(title='Pat')
        embed.set_image(url=image.url)
        await ctx.send(embed=embed)

    @anime.command(name='hug')
    async def _anime_hug(self, ctx):
        """
        anime hug gif
        """
        try:
            image = await self.bot.sr_api.get_gif('hug')
        except:  # noqa: E722
            return await ctx.send('Error with API, please try again later')
        embed = discord.Embed(title='Hug')
        embed.set_image(url=image.url)
        await ctx.send(embed=embed)

    @anime.command(name='quote')
    async def _quote(self, ctx):
        """
        random anime quote
        """
        try:
            quote = await self.client.sr_api.anime_quote()
        except:  # noqa: E722
            return await ctx.send_error('Error with API, please try again later')
        embed = discord.Embed(title=quote.character, description=quote.quote, color = discord.Colour.random())
        embed.set_author(name=quote.anime)
        await ctx.send(embed=embed)


    @anime.command(name='facepalm', aliases=['fp'])
    async def _anime_facepalm(self, ctx):
        """
        anime facepalm gif
        """
        try:
            image = await self.bot.sr_api.get_gif('face-palm')
        except:  # noqa: E722
            return await ctx.send('Error with API, please try again later')
        embed = discord.Embed(title='Face Palm')
        embed.set_image(url=image.url)
        await ctx.send(embed=embed)

    @commands.command(aliases=["howhot", "hot"])
    async def hotrate(self, ctx, *, user: discord.Member = None):
        """ Returns a random percent for how hot is a discord user """
        user = user or ctx.author

        r = random.randint(1, 100)
        hot = r

        if hot > 25:
            emoji = "❤"
        elif hot > 50:
            emoji = "💖"
        elif hot > 75:
            emoji = "💞"
        else:
            emoji = "💔"

        await ctx.send(f"**{user.name}** is **{hot:.2f}%** hot {emoji}")

    @commands.command(name='minecraft', aliases=['mcuser'])
    async def _minecraft(self, ctx, *, username):
        """
        minecraft user lookup
        """
        try:
            user = await self.bot.sr_api.mc_user(username)
        except:  # noqa: E722
            return await ctx.send('Error with API, please try again later')
        embed = discord.Embed(title=user.name, description=user.formatted_history)
        embed.set_author(name=f'UUID: {user.uuid}')
        await ctx.send(embed=embed)



    @commands.command()
    async def fact(self, ctx):
      K = open("txt/facts.txt", "r")
      fact = K.readlines()
      embed = discord.Embed(
        title = "Random Raptor Fact!",
        description = random.choice(fact),
        color = 0x00ff00
      )
      await ctx.send(embed=embed)

    @commands.command()
    async def art(self, ctx):
        embed=discord.Embed(
        title = "Cool ASCII Art!",
        description = """
 ```fix
  _______  _______  _______ _________ _______  _______ 
  (  ____ )(  ___  )(  ____ )\__   __/(  ___  )(  ____ )
  | (    )|| (   ) || (    )|   ) (   | (   ) || (    )|
  | (____)|| (___) || (____)|   | |   | |   | || (____)|
  |     __)|  ___  ||  _____)   | |   | |   | ||     __)
  | (\ (   | (   ) || (         | |   | |   | || (\ (   
  | ) \ \__| )   ( || )         | |   | (___) || ) \ \__
  |/   \__/|/     \||/          )_(   (_______)|/   \__/
        ```""",
        color = 0x00ff00
        )
        await ctx.send(embed=embed)

    @commands.command()
    async def dance(self, ctx):
        dance1 = discord.Embed(title=f'{ctx.author} dances', description='Hes probably very happy because yugoslavia reunited', color=0x000000)
        dance1.set_image(url='https://media1.tenor.com/images/75f0038c50cc4e2262077eef48f576c3/tenor.gif?itemid=12740205')
        #dance1.set_footer(text='*Bot created by tamrol073#6998(github: tamrol077)*')
        dance2 = discord.Embed(title=f'{ctx.author} dances', description='Hes probably very happy because yugoslavia reunited', color=0x000000)
        dance2.set_image(url='https://media.tenor.com/images/c3b9522dbfe8be78ff4dc305c999013e/tenor.gif')
        #dance2.set_footer(text='*Bot created by tamrol073#6998(github: tamrol077)*')
        dance3 = discord.Embed(title=f'{ctx.author} dances',
        description='Hes probably very happy because yugoslavia reunited', color=0x000000)
        dance3.set_image(url='https://media1.tenor.com/images/d736d9c410f88cb56a0f44a455e46464/tenor.gif?itemid=12740209')
        #dance3.set_footer(text='*Bot created by tamrol073#6998(github: tamrol077)*')
        dance4 = discord.Embed(title=f'{ctx.author} dances',
        description='Hes probably very happy because yugoslavia reunited', color=0x000000)
        dance4.set_image(url='https://media1.tenor.com/images/61cf901b1c520204c5c185d4a4244b78/tenor.gif?itemid=13410605')
        #dance4.set_footer(text='*Bot created by tamrol073#6998(github: tamrol077)*')
        dances = [dance1, dance2, dance3, dance4]
        await ctx.send(embed=random.choice(dances))

    @commands.command()
    async def suicide(self, ctx):
        suicideembed = discord.Embed(title=f'{ctx.author} kills themself', description="their probably sad", color=0x000000)
        suicideembed.set_image(
                url='https://media1.giphy.com/media/c6DIpCp1922KQ/giphy.gif')
            
        suicideembed2 = discord.Embed(title=f'{ctx.author} kills themself',
                description="their probably sad",
                color=0x000000)
        suicideembed2.set_image(
            url='https://media1.tenor.com/images/041dddf7d24b9ba3d591e0bed2ce38c7/tenor.gif?itemid=4524247')
        
        suicideembed3 = discord.Embed(title=f'{ctx.author} kills themself',
                                    description="their probably sad",
                                    color=0x000000)
        suicideembed3.set_image(url='https://i.makeagif.com/media/9-14-2015/vyNnjt.gif')

        suicideembed4 = discord.Embed(title=f'{ctx.author} kills himself',
                                    description="He's probably sad",
                                    color=0x000000)
        suicideembed4.set_image(url='https://thumbs.gfycat.com/SnarlingTameEquine-max-1mb.gif')
        suicideembed5 = discord.Embed(title=f'{ctx.author} commits kermit suicide',
                                    description="He's probably sad",
                                    color=0x000000)
        suicideembed5.set_image(url='https://media2.giphy.com/media/13kJc5CTOnqdQk/giphy.gif')
        
        suicidio = [suicideembed, suicideembed2, suicideembed3, suicideembed4, suicideembed5]
        await ctx.send(embed=random.choice(suicidio))


    @commands.command()
    async def drink(self, ctx):
        salve = random.randint(1,15)
        boss = [f'{ctx.author} remains sober after {salve} shots!',f'{ctx.author} gets drunk after {salve} shots!']
        poo = random.choice(boss)
        deshqiperine = ['https://media1.tenor.com/images/4a6e5632592a753d5ddd4ecef30357e6/tenor.gif?itemid=3558432','https://media1.tenor.com/images/8e830da5d0e3e08ae2469e9bf6afc5c9/tenor.gif?itemid=8561333']
        if salve > 7:
            embed = discord.Embed(title=f'{ctx.author} drinks a shot like a true slav!', description=f'{ctx.author.mention} drinks a shot like true slav', color=0x000000)
            embed.add_field(name='Very epic, hes a true slav', value=poo, inline=False)
            embed.set_image(url=random.choice(deshqiperine))
            #embed.set_footer(text='Bot made by (tamrol077 on github)(Discord: tamrol073#6998)')
        else:
            embed = discord.Embed(title=f'{ctx.author} drinks a shot like a true slav!', description=f'{ctx.author.mention} drinks a shot like true slav', color=0x000000)
            embed.add_field(name=f'{ctx.author} gets drunk after {salve} shots!', value='What a big shame', inline=False)
            embed.set_image(url=random.choice(deshqiperine))
            #embed.set_footer(text='Bot made by (tamrol077 on github)(Discord: tamrol073#6998)')
        await ctx.send(embed=embed)

    


    @commands.command(aliases=['fite'])
    async def fight(self, ctx, user: discord.Member,):
        if user == None:
            return await ctx.send("You cant fight yourself??")
        elif await ButtonConfirmation(ctx, f"You want to fight {user.mention}?", destructive=True, confirm="YES", cancel="No").run():
            

            win = random.randint(1, 2)

            if win == 1:
                lose = user
                win = ctx.author
            else:
                lose = ctx.author
                win = user

            await ctx.send("%s beat %s!" % (win.mention, lose.mention,))

        else:
            return await ctx.send("Ok then")

    
    @commands.command()
    async def hack(self, ctx, user:discord.Member=None):
        if user == None:
            await ctx.send("I can't hack nobody ya dumb-dumb")
            return
        if user is ctx.author:
            await ctx.send("What? Why would you want to hack yourself?")
            return
        if user.id == 829836500970504213:
            await ctx.send("I work so hard for you guys and this is what I get? Wow :clap: :(")
            return
        if user.bot:
            await ctx.send("Back off from my kind you weirdo.")
            return
        if user.id == 801234598334955530:
            await ctx.send("Want me to hack the owner?\n**FINE.**")
        em = discord.Embed(title = "Hack Complete!", description = f"{user.mention} is now hacked.", color = ctx.author.color)
        n = open("txt/ip.txt", "r")
        adf = n.readlines()
        a = open("txt/email.txt", "r")
        adfr = a.readlines()
        
        b = open("txt/credit.txt", "r")
        sdfg = b.readlines()

        
        em.add_field(name = ":e_mail: Email:", value = random.choice(adfr))
        async with aiohttp.ClientSession() as ses:
            async with ses.get('https://api.happi.dev/v1/generate-password?apikey=3e7850ObbtDYPtJQ1a98mQugZH0uF3B9ymBa04LHIVe8TzAM8lvJfBaK&limit=100&length=11&num=1&upper=1&symbols=0') as f:
                if f.status in range(200, 299):
                    dat = await f.json()
                    img = dat['passwords']
                    em.add_field(name = ":lock: Password:", value = random.choice(img))
                    await ses.close()
                else:
                    await ctx.reply(f"Error when trying to hack {ctx.author}.")
                    await ses.close()
        use = user.display_name
        message = await ctx.send(f" ▁ Locating {use}")
        await asyncio.sleep(1)
        await message.edit(content=f" ▂ Locating {use}")
        await asyncio.sleep(1)
        await message.edit(content=f" ▃ Locating {use}")
        await asyncio.sleep(1)
        await message.edit(content=f" ▅ Locating {use}")
        await asyncio.sleep(1)
        await message.edit(content=f" ▆ Found {use}!")
        await asyncio.sleep(1)
        await message.edit(content=f" ▇ Installing `virus.exe` on {use}'s computer")
        await asyncio.sleep(1)
        await message.edit(content=f" ▉ Installing `virus.exe` on {use}'s computer")
        await asyncio.sleep(1)
        await message.edit(content=f" █ Installing `virus.exe` on {use}'s computer")
        await asyncio.sleep(1)
        await message.edit(content=f" ▁ Installed `virus.exe` on {use}'s computer!")
        await asyncio.sleep(1)
        await message.edit(content=f" ▃ Installing `hack.exe` on {use}'s computer")
        await asyncio.sleep(1)
        await message.edit(content=f" ▅ Installing `hack.exe` on {use}'s computer")
        await asyncio.sleep(1)
        await message.edit(content=f" ▆ Installing `hack.exe` on {use}'s computer")
        await asyncio.sleep(1)
        await message.edit(content=f" ▇ Installed `hack.exe` on {use}'s computer!")
        await asyncio.sleep(1)
        await message.edit(content=f" ▁ Opening `virus.exe` on {use}'s computer")
        await asyncio.sleep(1)
        await message.edit(content=f" ▏ Opening `virus.exe` on {use}'s computer")
        await asyncio.sleep(1)
        await message.edit(content=f" ▔ Opening `virus.exe` on {use}'s computer")
        await asyncio.sleep(1)
        await message.edit(content=f" ▕ Opened `virus.exe` on {use}'s computer!")
        await asyncio.sleep(1)
        await message.edit(content=f" ▁ Opening `hack.exe` on {use}'s computer")
        await asyncio.sleep(1)
        await message.edit(content=f" ▏ Opening `hack.exe` on {use}'s computer")
        await asyncio.sleep(1)
        await message.edit(content=f" ▔ Opening `hack.exe` on {use}'s computer")
        await asyncio.sleep(1)
        await message.edit(content=f" ▕ Opened `hack.exe` on {use}'s computer!")
        await asyncio.sleep(1)
        await message.edit(content=f" ▂ Finding {use}'s password")
        await asyncio.sleep(1)
        await message.edit(content=f" ▅ Finding {use}'s password")
        await asyncio.sleep(1)
        await message.edit(content=f" ▆ Finding {use}'s password")
        await asyncio.sleep(1)
        await message.edit(content=f" ▇ Found {use}'s password!")
        await asyncio.sleep(1)
        await message.edit(content=f" / Finding {use}'s email")
        await asyncio.sleep(1)
        await message.edit(content=f" - Finding {use}'s email")
        await asyncio.sleep(1)
        await message.edit(content=f" \ Finding {use}'s email")
        await asyncio.sleep(1)
        await message.edit(content=f" | Found {use}'s email!")
        await asyncio.sleep(1)
        await message.edit(content=f" / Finding {use}'s IP")
        await asyncio.sleep(1)
        await message.edit(content=f" - Finding {use}'s IP")
        await asyncio.sleep(1)
        await message.edit(content=f" \ Finding {use}'s IP")
        await asyncio.sleep(1)
        await message.edit(content=f" | Found {use}'s IP!")
        await asyncio.sleep(1)
        await message.edit(content=f" / Finding {use}'s credit card number")
        await asyncio.sleep(1)
        await message.edit(content=f" - Finding {use}'s credit card number")
        await asyncio.sleep(1)
        await message.edit(content=f" \ Finding {use}'s credit card number")
        await asyncio.sleep(1)
        await message.edit(content=f" | Found {use}'s credit card number!")
        await asyncio.sleep(1)
        await message.edit(content=f"Hack Complete! Info Found 🔽")
        await asyncio.sleep(1)
        
        em.add_field(name = ":computer: IP Address:", value = random.choice(adf))
        em.add_field(name = ":credit_card: Credit Card Num.:", value = random.choice(sdfg))
        em.add_field(name = ":sunglasses: Hacker:", value = ctx.author.mention)
        em.add_field(name = ":disguised_face: Who Got *totally* Hacked:", value = user.mention)
        em.set_footer(text = "This hack is **totally** real and **completely** dangerous.")
        await ctx.send(embed = em)



        
            

    

    @commands.command()
    async def hug(self,ctx):
        await ctx.send("Let's start with these hugs! Answer these questions within 15 seconds!")

        questions = ["Who do you want to send the hug to?", 
                    "How many hugs do you want to send?",
                    "Why do you want to send these hugs?",
                    "Which channel do you want me to send these hugs in? (Please make sure that i have access to see that channel)"]

        answers = []

        def check(m):
            return m.author == ctx.author 

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
            c_id = int(answers[3][2:-1])
        except Exception as e:
            print(e)

        channel = self.client.get_channel(c_id)

        howmanyhugs = answers[1]
        
        sender = ctx.author

        whotosendto = answers[0]

        reason = answers[2]


        await ctx.send(f"I will send {howmanyhugs} hugs to {whotosendto} in {channel.mention} for the reason of {reason}!")




        embed = discord.Embed(title = f"{sender} sent you {howmanyhugs} hugs!", description = ":hugging:", color = ctx.author.color)
        embed.set_author(name="Hugs!")
        embed.add_field(name = "Reason:", value = reason, inline = False)
        embed.set_footer(text = f"Yay!")

        await channel.send(whotosendto)
        await channel.send(embed = embed)



    @commands.command()
    async def rate(self, ctx, *, thing: commands.clean_content):
        """ Rates what you desire """
        rate_amount = random.randint(0, 100)
        await ctx.send(f"I'd rate `{thing}` a **{round(rate_amount, 4)} / 100**")

    @commands.command(brief='Rickrolls someone...', description='Rickrolls someone... See thier reaction!')
    async def rickroll(self, ctx):
        em = discord.Embed(title = "Rickroll!", description = "Have Fun :P", color = ctx.author.color)
        em.set_image(url = 'https://media.tenor.com/images/a1505c6e6d37aa2b7c5953741c0177dc/tenor.gif')
        await ctx.send(embed = em)

    @commands.command(brief='troll', description='troll')
    async def troll(self, ctx):
        em = discord.Embed(title = "Troll!", description = "Have Fun :P", color = ctx.author.color)
        em.set_image(url = 'https://media1.tenor.com/images/56b2b212b5a14ce62cafd056ce954500/tenor.gif?itemid=5259835')
        await ctx.send(embed = em)

    @commands.command(aliases=['8ball'])
    async def eightball(self, ctx, *, msg):
        responses = ["It is certain.",
                 "It is decidedly so.",
                 "Without a doubt.",
                 "Yes - definitely.",
                 "You may rely on it.",
                 "As I see it, yes.",
                 "Most likely.",
                 "Outlook good.",
                 "Yes.",
                 "Signs point to yes.",
                 "Reply hazy, try again.",
                 "Ask again later.",
                 "Better not tell you now.",
                 "Cannot predict now.",
                 "Concentrate and ask again.",
                 "Don't count on it.",
                 "My reply is no.",
                 "My sources say no.",
                 "Outlook not so good.",
                 "Very doubtful."]
        
        question = msg
        embed = discord.Embed(title = f"**Question:** {question}", description = f"The answer to your question is **{random.choice(responses)}**", color = ctx.author.color)
        embed.set_author(name = "8Ball!", icon_url = "https://cdn.discordapp.com/emojis/832386089314549791.gif?v=1")
        await ctx.send(embed = embed)

    @commands.command()
    async def joke(self, ctx):
        f = open("txt/joke.txt", "r")
        abcdefg = f.readlines()
        await ctx.send(random.choice(abcdefg))



    @commands.command()
    async def quote(self, ctx):
        z = open("txt/quote.txt", "r")
        asd = z.readlines()
        await ctx.send(random.choice(asd))

    @commands.command()
    async def pun(self, ctx):
        a = open("txt/pun.txt", "r")
        asdf = a.readlines()
        await ctx.send(random.choice(asdf))

    @commands.command(help="Sends a bubblewrap made just for you!", aliases=['bw', 'pop'])
    async def bubblewrap(self, ctx):
        bw = discord.Embed(title = "<:BubbleGum:837747657890988063> Enjoy your bubblewrap!", description = '||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop|| \n||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop|| \n||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop|| \n||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop|| \n||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop|| \n||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop|| \n||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop|| \n||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop|| \n||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop|| \n||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop|| \n||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop|| \n||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop|| \n||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop|| \n||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop|| \n', color = ctx.author.color)
        await ctx.send(embed = bw)

    @commands.command(aliases=["kekp", "kekpor"])
    async def kekportal(self, ctx):
        obi = "<:obi:826144216643665980>"
        por = "<a:PortalGIF:837002013367730220>"*3
        onepor = "<a:PortalGIF:837002013367730220>"
        kek = "<:kekportal:826127450710868028>"
        top = obi*5
        layer = f"{obi}{por}{obi}\n"
        layers = layer*3
        bottom_layer = obi + onepor + kek + onepor + obi + "\n"
        await ctx.send(top + "\n" + layers + bottom_layer + top)


    @commands.command(aliases=['simp'])
    async def simprate(self, ctx, member: discord.Member = None):
        if member == None:
            member = ctx.author
        
        rando = random.randrange(0, 100)

        await ctx.send(f"{member.mention} is {rando}% simp.")

    @commands.command(aliases=['gay'])
    async def gayrate(self, ctx, member: discord.Member = None):
        if member == None:
            member = ctx.author
        
        rando = random.randrange(0, 100)

        await ctx.send(f"{member.mention} is {rando}% gay.")


    @commands.command()
    async def meme(self, ctx):
        reddit = praw.Reddit(client_id = "sZZuDCdqBSYETg",
                         client_secret = "rT3ln6yKSTNzBOp2weZ-LzCpw0AHmQ",
                         username = "Avocado_Man_At_YT",
                         password = "Super567",
                         user_agent = "raptorpraw")
        
        subreddit = reddit.subreddit("memes")
        all_subs = []

        top = subreddit.top(limit = 50)

        for submission in top:
            all_subs.append(submission)
        
        random_sub = random.choice(all_subs)

        name = random_sub.title

        url = random_sub.url


        embed = discord.Embed(title=name, color=discord.Colour.blue())
        embed.set_image(url=url)
        await ctx.send(embed=embed)
    
    
    @commands.command()
    async def catmeme(self, ctx):
        reddit = praw.Reddit(client_id = "sZZuDCdqBSYETg",
                         client_secret = "rT3ln6yKSTNzBOp2weZ-LzCpw0AHmQ",
                         username = "Avocado_Man_At_YT",
                         password = "Super567",
                         user_agent = "raptorpraw")
        
        subreddit = reddit.subreddit("catmeme")
        all_subs = []

        top = subreddit.top(limit = 50)

        for submission in top:
            all_subs.append(submission)
        
        random_sub = random.choice(all_subs)

        name = random_sub.title

        url = random_sub.url


        embed = discord.Embed(title=name, color=discord.Colour.blue())
        embed.set_image(url=url)
        await ctx.send(embed=embed)

    @commands.command()
    async def gif(self, ctx, *, search_query):

        api_key = 'bAGi8KzF1EcNw6GsopzXIFtRwC6np4zE'
        api_instance = giphy_client.DefaultApi()

        try:

            api_response = api_instance.gifs_search_get(api_key,search_query, limit=10, rating='g')
            lst = list(api_response.data)
            gif = random.choice(lst)

            giff = discord.Embed(title=search_query, description=f"Made by {gif.username}", color = ctx.author.color)
            giff.set_image(url=f'https://media.giphy.com/media/{gif.id}/giphy.gif')
            await ctx.send(embed = giff)
        except ApiException as e:
            await ctx.send("Error 101. Try again later")
            print("Error when calling gif api")
            print(e)

    @commands.command()
    async def sticker(self, ctx, *, search_query):

        api_key = 'bAGi8KzF1EcNw6GsopzXIFtRwC6np4zE'
        api_instance = giphy_client.DefaultApi()

        try:

            api_response = api_instance.stickers_search_get(api_key,search_query, limit=10, rating='g')
            lst = list(api_response.data)
            gif = random.choice(lst)

            giff = discord.Embed(title=search_query, description=f"Made by {gif.username}", color = ctx.author.color)
            giff.set_image(url=f'https://media.giphy.com/media/{gif.id}/giphy.gif')
            await ctx.send(embed = giff)
        except ApiException as e:
            await ctx.send("Error 101. Try again later")
            print("Error when calling gif api")
            print(e)
    
    @commands.command(name="token", aliases=['bottoken', 'faketoken'])
    async def _token(self, ctx):
        """
        Get a discord bot token lol
        """
        try:
            token = await self.client.sr_api.bot_token()
        except:  # noqa: E722
            return await ctx.send_error('Error with API, please try again later')
        await ctx.send(token)

    @commands.command(aliases=['def'])
    async def define(self, ctx, search_term):
        def wiki_summary(self, arg):
            definition = wikipedia.summary(arg, sentences=3, chars=1000, auto_suggest=True, redirect=True)
            return definition

        try:
            try:
                words = ctx.message.content.split()
                impor_words = words[1:]
                src = discord.Embed(title="Searching... Found!", description=wiki_summary(self, impor_words), color = ctx.author.color)
                await ctx.send(embed=src)
            except wikipedia.exceptions.DisambiguationError as e:
                e = list(e)
                await ctx.send(wiki_summary(random.choice(e)))
        except:
            await ctx.send("Not found")


    @commands.command(aliases=['dog'])
    async def dogfact(self, ctx):
        async with aiohttp.ClientSession() as ses:
            async with ses.get('https://some-random-api.ml/facts/dog') as r:
                if r.status in range(200, 299):
                    data = await r.json()
                    fact = data['fact']
                    em = discord.Embed(
                        title='Dog Fact',
                        description=f'{fact}',
                        color = ctx.author.color
                    )
        async with aiohttp.ClientSession() as ses:
            async with ses.get('https://some-random-api.ml/img/dog') as f:
                if r.status in range(200, 299):
                    dat = await f.json()
                    img = dat['link']
                    em.set_image(url=f'{img}')
                    await ctx.send(embed=em)
                    await ses.close()
                else:
                    await ctx.reply("Error when trying to get a dog fact.")
                    await ses.close()

    @commands.command(aliases=['koala'])
    async def koalafact(self, ctx):
        async with aiohttp.ClientSession() as ses:
            async with ses.get('https://some-random-api.ml/facts/koala') as r:
                if r.status in range(200, 299):
                    data = await r.json()
                    fact = data['fact']
                    em = discord.Embed(
                        title='Koala Fact',
                        description=f'{fact}',
                        color = ctx.author.color
                    )
        async with aiohttp.ClientSession() as ses:
            async with ses.get('https://some-random-api.ml/img/koala') as f:
                if r.status in range(200, 299):
                    dat = await f.json()
                    img = dat['link']
                    em.set_image(url=f'{img}')
                    await ctx.send(embed=em)
                    await ses.close()
                else:
                    await ctx.reply("Error when trying to get a koala fact.")
                    await ses.close()


    @commands.command(aliases=['cat'])
    async def catfact(self, ctx):
        async with aiohttp.ClientSession() as ses:
            async with ses.get('https://some-random-api.ml/facts/cat') as r:
                if r.status in range(200, 299):
                    data = await r.json()
                    fact = data['fact']
                    em = discord.Embed(
                        title='Cat Fact',
                        description=f'{fact}',
                        color = ctx.author.color
                    )
        async with aiohttp.ClientSession() as ses:
            async with ses.get('https://some-random-api.ml/img/cat') as f:
                if r.status in range(200, 299):
                    dat = await f.json()
                    img = dat['link']
                    em.set_image(url=f'{img}')
                    await ctx.send(embed=em)
                    await ses.close()
                else:
                    await ctx.reply("Error when trying to get a cat fact.")
                    await ses.close()

    @commands.command(aliases=['fox'])
    async def foxfact(self, ctx):
        async with aiohttp.ClientSession() as ses:
            async with ses.get('https://some-random-api.ml/facts/fox') as r:
                if r.status in range(200, 299):
                    data = await r.json()
                    fact = data['fact']
                    em = discord.Embed(
                        title='Fox Fact',
                        description=f'{fact}',
                        color = ctx.author.color
                    )
        async with aiohttp.ClientSession() as ses:
            async with ses.get('https://some-random-api.ml/img/fox') as f:
                if r.status in range(200, 299):
                    dat = await f.json()
                    img = dat['link']
                    em.set_image(url=f'{img}')
                    await ctx.send(embed=em)
                    await ses.close()
                else:
                    await ctx.reply("Error when trying to get a fox fact.")
                    await ses.close()

    @commands.command(aliases=['bird'])
    async def birdfact(self, ctx):
        async with aiohttp.ClientSession() as ses:
            async with ses.get('https://some-random-api.ml/facts/bird') as r:
                if r.status in range(200, 299):
                    data = await r.json()
                    fact = data['fact']
                    em = discord.Embed(
                        title='Bird Fact',
                        description=f'{fact}',
                        color = ctx.author.color
                    )
        async with aiohttp.ClientSession() as ses:
            async with ses.get('https://some-random-api.ml/img/bird') as f:
                if r.status in range(200, 299):
                    dat = await f.json()
                    img = dat['link']
                    em.set_image(url=f'{img}')
                    await ctx.send(embed=em)
                    await ses.close()
                else:
                    await ctx.reply("Error when trying to get a bird fact.")
                    await ses.close()

    @commands.command(aliases=['panda'])
    async def pandafact(self, ctx):
        async with aiohttp.ClientSession() as ses:
            async with ses.get('https://some-random-api.ml/facts/panda') as r:
                if r.status in range(200, 299):
                    data = await r.json()
                    fact = data['fact']
                    em = discord.Embed(
                        title='Panda Fact',
                        description=f'{fact}',
                        color = ctx.author.color
                    )
        async with aiohttp.ClientSession() as ses:
            async with ses.get('https://some-random-api.ml/img/panda') as f:
                if r.status in range(200, 299):
                    dat = await f.json()
                    img = dat['link']
                    em.set_image(url=f'{img}')
                    await ctx.send(embed=em)
                    await ses.close()
                else:
                    await ctx.reply("Error when trying to get a panda fact.")
                    await ses.close()

    
    @commands.command(aliases=["efypyamid", 'efypyr', 'emojifypyr'])
    async def emojifypyramid(self, ctx, *, msg):
        letters = ["a", "b", "c", "d", "e", "f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]

        others = {"1":"one", "2":"two", "3":"three", "4":"four","5":"five","6":"six","7":"seven","8":"eight","9":"nine","0":"zero", "?":"question", "!":"exclamation", "#":"hash", "*":"asterisk", "+":"heavy_plus_sign", "-":"heavy_minus_sign"}

        msg = msg.lower()

        message = []
        send=""

        for i in msg:
            message.append(i)

        for i in message:
            if i not in letters and i not in others and i != " " and i != "\n":
                await ctx.reply(f"Invalid Character in message: `{i}`")
                send = ""
                break
            else:
                if i in letters:
                    send = send + f":regional_indicator_{i}:"
                elif i == " ":
                    send = send + " "
                elif i == "\n":
                    send = send + "\n"
                else:
                    send = send + f":{others[i]}:"

            await ctx.send(send)

    @commands.command(aliases=["efy"])
    async def emojify(self, ctx, *, msg):
        letters = ["a", "b", "c", "d", "e", "f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]

        others = {"1":"one", "2":"two", "3":"three", "4":"four","5":"five","6":"six","7":"seven","8":"eight","9":"nine","0":"zero", "?":"question", "!":"exclamation", "#":"hash", "*":"asterisk", "+":"heavy_plus_sign", "-":"heavy_minus_sign"}

        msg = msg.lower()

        message = []
        send=""

        for i in msg:
            message.append(i)

        for i in message:
            if i not in letters and i not in others and i != " " and i != "\n":
                await ctx.reply(f"Invalid Character in message: `{i}`")
                send = ""
                break
            else:
                if i in letters:
                    send = send + f":regional_indicator_{i}:"
                elif i == " ":
                    send = send + " "
                elif i == "\n":
                    send = send + "\n"
                else:
                    send = send + f":{others[i]}:"

        await ctx.send(send)

    @commands.command(aliases=['elephant'])
    async def elephantfact(self, ctx):
        async with aiohttp.ClientSession() as ses:
            async with ses.get('https://some-random-api.ml/facts/elephant') as r:
                if r.status in range(200, 299):
                    data = await r.json()
                    fact = data['fact']
                    em = discord.Embed(
                        title='Elephant Fact',
                        description=f'{fact}',
                        color = ctx.author.color
                    )
                    await ctx.send(embed=em)
                    await ses.close()
                else:
                    await ctx.reply("Error when trying to get an elephant fact.")
                    await ses.close()

    @commands.command(aliases=['giraffe'])
    async def giraffefact(self, ctx):
        async with aiohttp.ClientSession() as ses:
            async with ses.get('https://some-random-api.ml/facts/giraffe') as r:
                if r.status in range(200, 299):
                    data = await r.json()
                    fact = data['fact']
                    em = discord.Embed(
                        title='Giraffe Fact',
                        description=f'{fact}',
                        color = ctx.author.color
                    )
                    await ctx.send(embed=em)
                    await ses.close()
                else:
                    await ctx.reply("Error when trying to get a giraffe fact.")
                    await ses.close()

    @commands.command(aliases=['racoon'])
    async def racoonfact(self, ctx):
        async with aiohttp.ClientSession() as ses:
            async with ses.get('https://some-random-api.ml/facts/racoon') as r:
                if r.status in range(200, 299):
                    data = await r.json()
                    fact = data['fact']
                    em = discord.Embed(
                        title='Racoon Fact',
                        description=f'{fact}',
                        color = ctx.author.color
                    )
        async with aiohttp.ClientSession() as ses:
            async with ses.get('https://some-random-api.ml/img/racoon') as f:
                if r.status in range(200, 299):
                    dat = await f.json()
                    img = dat['link']
                    em.set_image(url=f'{img}')
                    await ctx.send(embed=em)
                    await ses.close()
                else:
                    await ctx.reply("Error when trying to get a racoon fact.")
                    await ses.close()
    @commands.command(aliases=['whale'])
    async def whalefact(self, ctx):
        async with aiohttp.ClientSession() as ses:
            async with ses.get('https://some-random-api.ml/facts/whale') as r:
                if r.status in range(200, 299):
                    data = await r.json()
                    fact = data['fact']
                    em = discord.Embed(
                        title='Whale Fact',
                        description=f'{fact}',
                        color = ctx.author.color
                    )
        async with aiohttp.ClientSession() as ses:
            async with ses.get('https://some-random-api.ml/img/whale') as f:
                if r.status in range(200, 299):
                    dat = await f.json()
                    img = dat['link']
                    em.set_image(url=f'{img}')
                    await ctx.send(embed=em)
                    await ses.close()
                else:
                    await ctx.reply("Error when trying to get a whale fact.")
                    await ses.close()

    @commands.command(aliases=['kangaroo'])
    async def kangaroofact(self, ctx):
        async with aiohttp.ClientSession() as ses:
            async with ses.get('https://some-random-api.ml/facts/kangaroo') as r:
                if r.status in range(200, 299):
                    data = await r.json()
                    fact = data['fact']
                    em = discord.Embed(
                        title='Kangaroo Fact',
                        description=f'{fact}',
                        color = ctx.author.color
                    )
        async with aiohttp.ClientSession() as ses:
            async with ses.get('https://some-random-api.ml/img/kangaroo') as f:
                if r.status in range(200, 299):
                    dat = await f.json()
                    img = dat['link']
                    em.set_image(url=f'{img}')
                    await ctx.send(embed=em)
                    await ses.close()
                else:
                    await ctx.reply("Error when trying to get a kangaroo fact.")
                    await ses.close()

    @commands.command()
    async def beer(self, ctx, user: discord.Member = None, *, reason: commands.clean_content = ""):
        """ Give someone a beer! 🍻 """
        if not user or user.id == ctx.author.id:
            return await ctx.send(f"**{ctx.author.name}**: paaaarty!🎉🍺")
        if user.id == self.client.user.id:
            return await ctx.send("*drinks beer with you* 🍻")
        if user.bot:
            return await ctx.send(f"I would love to give beer to the bot **{ctx.author.name}**, but I don't think it will respond to you :/")

        beer_offer = f"**{user.name}**, you got a 🍺 offer from **{ctx.author.name}**"
        beer_offer = beer_offer + f"\n\n**Reason:** {reason}" if reason else beer_offer
        msg = await ctx.send(beer_offer)

        def reaction_check(m):
            if m.message_id == msg.id and m.user_id == user.id and str(m.emoji) == "🍻":
                return True
            return False

        try:
            await msg.add_reaction("🍻")
            await self.client.wait_for("raw_reaction_add", timeout=30.0, check=reaction_check)
            await msg.edit(content=f"**{user.name}** and **{ctx.author.name}** are enjoying a lovely beer together 🍻")
        except asyncio.TimeoutError:
            await msg.delete()
            await ctx.send(f"well, doesn't seem like **{user.name}** wanted a beer with you **{ctx.author.name}** ;-;")
        except discord.Forbidden:
            # Yeah so, bot doesn't have reaction permission, drop the "offer" word
            beer_offer = f"**{user.name}**, you got a 🍺 from **{ctx.author.name}**"
            beer_offer = beer_offer + f"\n\n**Reason:** {reason}" if reason else beer_offer
            await msg.edit(content=beer_offer)

    @commands.group(pass_without_invoke=True)
    async def chatbot(self, ctx):
        em = discord.Embed(
            title = "Chatbot!",
            color = ctx.author.color,
            timestamp = datetime.datetime.now()
        )
        em.add_field(name = "Start", value = "Use `rap chatbot start` to start the chatbot!")
        em.add_field(name = "End", value = "Use `rap chatbot end` to stop the chatbot! Please only use this if you have used `rap chatbot start`.")
        em.set_footer(text = "Chatbot set up by Dragonic#9230", icon_url = "https://images-ext-2.discordapp.net/external/tjuvF_0QIEvojcvmrcTcA8QXu8qzmLqTPLjOOl-uMYY/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/776944535141482506/86516d7d022b3e6e5026517980716c11.webp")
        await ctx.send(embed = em)

    @commands.bot_has_permissions(administrator=True)
    @chatbot.command()
    async def start(self, ctx):
        channel = await ctx.guild.create_text_channel("raptor-chatbot")
        await ctx.send("Chatbot is now setup. Go check it out in " + channel.mention + " !")

    @commands.has_permissions(administrator=True)
    @commands.bot_has_permissions(administrator=True)
    @chatbot.command()
    async def stop(self, ctx, channel:discord.TextChannel):
        if channel.name == "raptor-chatbot":
            await channel.delete()
            await ctx.send("Chatbot stopped. Use `rap chatbot start` to start it again!")

        else:
            await ctx.send("Either you haven't used `rap chatbot start` or you have manually deleted it.")


    @commands.command()
    async def video(self, ctx, *, video_name):
        query_string = urllib.parse.urlencode({
            'search_query': video_name
        })
        htm_content = urllib.request.urlopen(
            'http://www.youtube.com/results?' + query_string
        )
        search_results = re.findall( r"watch\?v=(\S{11})", htm_content.read().decode())
        await ctx.send('http://www.youtube.com/watch?v=' + search_results[0])
    
    

def setup(client):
    client.add_cog(Fun(client))