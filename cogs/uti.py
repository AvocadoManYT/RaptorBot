import discord
import json
import datetime
from main import prefix as pre, owners
from datetime import datetime
from discord.ext import commands
import asyncio
import random
import aiofiles
import requests
import json
import aiohttp
import inspect

sniped_messages = {}

class Utility(commands.Cog):
    """ Category for utility commands """
    def read_jsona(filename):
        with open(f"{filename}.json", "r") as file:
            data = json.load(file)
        return data
    
    def __init__(self, client):
        self.client = client

    # events
    @commands.Cog.listener()
    async def on_ready(self):
        print('Utils cog is ready.')

    # commands

    @commands.command(aliases=['rr', 'reactrole'])
    async def reactionrole(self, ctx, role: discord.Role=None, msg: discord.Message=None, emoji=None):
        if role.position > ctx.author.top_role.position:
          await ctx.channel.send("**:x: | That role is over your top role!**")
          return
        if role != None and msg != None and emoji != None:
            await msg.add_reaction(emoji)
            self.client.reaction_roles.append((role.id, msg.id, str(emoji.encode("utf-8"))))
            
            async with aiofiles.open("reaction_roles.txt", mode="a") as file:
                emoji_utf = emoji.encode("utf-8")
                await file.write(f"{role.id} {msg.id} {emoji_utf}\n")

            await ctx.channel.send("Reaction has been set.")
            
        else:
            await ctx.send("Invalid arguments. Maybe the msg id is invalid or emoji is invalid :shrug:")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        for role_id, msg_id, emoji in self.client.reaction_roles:
            if msg_id == payload.message_id and emoji == str(payload.emoji.name.encode("utf-8")):
                await payload.member.add_roles(self.client.get_guild(payload.guild_id).get_role(role_id))
                return

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        for role_id, msg_id, emoji in self.client.reaction_roles:
            if msg_id == payload.message_id and emoji == str(payload.emoji.name.encode("utf-8")):
                guild = self.client.get_guild(payload.guild_id)
                await guild.get_member(payload.user_id).remove_roles(guild.get_role(role_id))
                return

            
    @commands.command()
    async def feedback(self, ctx):
        await ctx.send("Let's start with this feedback session! Answer these questions within 20 seconds!")

        questions = ["How much out of ten do you rate me? (i.e. 7/10)", 
                    "What is your feedback about me?",
                    ]

        answers = []

        
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        for i in questions:
            await ctx.send(i)

            try:
                msg = await self.client.wait_for('message', timeout=20.0, check=check)
            except asyncio.TimeoutError:
                await ctx.send('You didn\'t answer in time, please be quicker next time!')
                return
            else:
                answers.append(msg.content)
       


        channel = self.client.get_channel(855915040288276490)

        

        rate = answers[0]

        feedback = answers[1]

        await ctx.send(f"Thanks for sending feedback!")


        embed = discord.Embed(title = "New Feedback!", description = f"Sent by: <@{ctx.author.id}>", color = ctx.author.color)



        embed.add_field(name=f'Rating:', value=rate)
        embed.add_field(name=f"Feedback:", value=feedback)


        await channel.send(embed = embed)

    @commands.command()
    async def suggest(self, ctx):
        await ctx.send("Let's start with this seggestion session! Answer these questions within 30 seconds!")

        questions = ["Tell me your suggestion"
                    ]

        answers = []

        
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        for i in questions:
            await ctx.send(i)

            try:
                msg = await self.client.wait_for('message', timeout=30.0, check=check)
            except asyncio.TimeoutError:
                await ctx.send('You didn\'t answer in time, please be quicker next time!')
                return
            else:
                answers.append(msg.content)
       


        channel = self.client.get_channel(855915040288276490)

        

        suggest = answers[0]



        await ctx.send(f"Thanks for sending feedback! If we use it, we will be sure to credit you!")


        embed = discord.Embed(title = "New Suggestion!", description = f"Sent by: <@{ctx.author.id}>", color = ctx.author.color)



        embed.add_field(name=f'Suggestion:', value=suggest)



        await channel.send(embed = embed)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        sniped_messages[message.guild.id] = (message.content, message.author, message.channel.name, message.created_at)


    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        
        file = "json/afk.json"
        with open(file, 'r') as f:
            data = json.load(f)
        if str(message.guild.id) not in list(data):
            data[str(message.guild.id)] = {
                "AFK": {}
            }
            with open(file, 'w') as f:
                json.dump(data, f, indent = 4)
        
        
        for i in message.mentions:
            if str(i.id) in list(data[str(message.guild.id)]['AFK']):
                if data[str(message.guild.id)]['AFK'][str(i.id)] != '':
                    reason = 'Reason: ' + data[str(message.guild.id)]['AFK'][str(i.id)]
                else:
                    reason = ''
                await message.channel.send(f'**`{i.name}`** is AFK. {reason}')
                break

        

    


    

    # commands

    @commands.command(help="Repeats your message.",aliases=['echo'])
    async def say(self, ctx, *, message):
        await ctx.message.delete()
        await ctx.send(message)


    @commands.command(help="Embeds your message!")
    async def embed(self, ctx, *, message = None):
        if message == None:
            await ctx.send("Send something to embed. ;-;")
        else:
            await ctx.message.delete()
            e = discord.Embed(title = message)
            await ctx.send(embed = e)


    @commands.command(help="Starts a poll with custom everything!.",aliases=["pl"])
    async def poll(self, ctx, *, msg):
        channel = ctx.channel
        try:
            title, op1, op2 = msg.split("or")
        
            txt = f"React with <a:Yestick:831948152273633332> for {op1} or <a:Notick:831948152503533569> for {op2}"
        except:
            await channel.send("Correct Syntax: [title] or [Choice1] or [Choice2]")
            return

        embed = discord.Embed(title= f"Question: {title}", description = txt, color = discord.Color.dark_green())
        embed.set_author(name=f"Poll from {ctx.author.display_name}!", icon_url=ctx.author.avatar_url)
        message_ = await channel.send(embed=embed)
        await message_.add_reaction("<a:Yestick:831948152273633332>")
        await message_.add_reaction("<a:Notick:831948152503533569>")
        await ctx.message.delete()

    @commands.command(help="Starts a yes and no poll.",aliases=["ynpoll", "ynpl"])
    async def yesnopoll(self, ctx, *, message):
        channel = ctx.channel
        try:
            title = message
        
            txt = f"React with <a:Yestick:831948152273633332> for Yes or <a:Notick:831948152503533569> for No."
        except:
            await channel.send("Correct Syntax: <prefix>ynpl [title]")
            return

        embed = discord.Embed(title= f"Question: {title}", description = txt, color = discord.Color.dark_green())
        embed.set_author(name=f"Poll from {ctx.author.display_name}!", icon_url=ctx.author.avatar_url)
        message_ = await channel.send(embed=embed)
        await message_.add_reaction("<a:Yestick:831948152273633332>")
        await message_.add_reaction("<a:Notick:831948152503533569>")
        await ctx.message.delete()



    @commands.command(help="Shows the bot's ping.")
    async def ping(self, ctx):
      em1 = discord.Embed(title = "<a:8104LoadingEmote:851517649389486180>", color = ctx.author.color)
      em = discord.Embed(title="Pong! 🏓", description=f"{round(self.client.latency * 1000)}ms" , color = ctx.author.color)
      msg = await ctx.send(embed = em1)
      await asyncio.sleep(5)
      await msg.edit(embed = em)

    

    
            

       


    @commands.command(help="Change other people\'s nickname.", aliases=['cnick','cname','cnewname'])
    @commands.has_permissions(manage_nicknames=True)
    async def changenickname(self, ctx, person:discord.Member, *, newname):
        try:
            await person.edit(nick = f"{newname}")
            await ctx.reply(f"Changed {person}\'s name in this server to {newname}!")
            return
        except:
            await ctx.send("can\'t")


    @commands.command(help="Changes your nickname.", aliases=['nick','name','newname'])
    @commands.has_permissions(manage_nicknames=True)
    async def nickname(self, ctx, *, newname):
        try:
            await ctx.author.edit(nick = f"{newname}")
            await ctx.reply(f"Changed your name in this server to {newname}!")
            return
        except:
            await ctx.send("can\'t")


    @commands.command(help="Starts a reminder for you and reminds that much time later. Use s for seconds, m for minutes, h for hours and d for days.")
    async def remind(self, ctx, amount_of_time, task):
        
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

        converted_time = convert(self, amount_of_time)

        if converted_time == -1:
            await ctx.send("You didn't answer the question in time.")
            return

        if converted_time == -2:
            await ctx.send("The time must be an integer.")
            return

        
        await ctx.send(f"Your reminder has been started for **{task}** and will end in **{amount_of_time}**.")

        await asyncio.sleep(converted_time)
        try:
            await ctx.author.send(f"Your reminder for **{task}** has been finished in the server {ctx.guild.name}!")
        except:
            await ctx.send(f"{ctx.author.mention} your reminder for **{task}** has been finished!")

    @commands.command()
    async def timer(self, ctx, amount_of_time):
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

        con_tm = convert(self, amount_of_time)

        if con_tm == -1:
            await ctx.send("You didn't answer the question in time.")
            return

        if con_tm == -2:
            await ctx.send("The time must be an integer.")
            return

        tm = discord.Embed(
            title = f"Timer for {amount_of_time}",
            color = ctx.author.color,
            timestamp = datetime.now()
        )
        tm.set_author(name = "Timer!", icon_url = "https://i.pinimg.com/originals/01/28/46/0128468e98f1312cb40ef96218f4f6a5.gif")
        my_msg = await ctx.send(embed = tm)

        await asyncio.sleep(con_tm)
        try:
            await ctx.author.send(f"{ctx.author.mention}, your timer for {amount_of_time} has ended in the server {ctx.guild.name}!")
        except:
            await ctx.send(f"{ctx.author.mention}, your timer for {amount_of_time} has ended!")

        win = discord.Embed(title = f"Your timer for {amount_of_time} has ended!", color = discord.Colour.red())
        win.set_author(name = "Timer Ended!", icon_url = "https://cdn.dribbble.com/users/459831/screenshots/2728135/stopwatch.gif")
        await my_msg.edit(embed=win)






    @commands.command(aliases=['av'])
    async def avatar(self, ctx, member:discord.Member=None):
        if member == None:
            member = ctx.author
        em = discord.Embed(
            title = member,
            color = ctx.author.color
        )
        em.set_image(url=member.avatar_url)
        await ctx.send(embed=em)



    @commands.command()
    async def choose(self, ctx, *options: str):
        if len(options) <= 1:
            await ctx.send('You need at least two options')
            return
        if len(options) > 10:
            await ctx.send('You cannot have more than 10 options.')
            return
        else:
            await ctx.send(f"{ctx.author} I choose `{random.choice(options)}`")

    @commands.command(aliases=['rc', 'run', 'eval'])
    @commands.is_owner()
    async def run_code(self, ctx, *, code):
        language_specifiers = ["python", "py", "javascript", "js", "html", "css", "php", "md", "markdown", "go", "golang", "c", "c++", "cpp", "c#", "cs", "csharp", "java", "ruby", "rb", "coffee-script", "coffeescript", "coffee", "bash", "shell", "sh", "json", "http", "pascal", "perl", "rust", "sql", "swift", "vim", "xml", "yaml"]
        loops = 0
        while code.startswith("`"):
            code = "".join(list(code)[1:])
            loops += 1
            if loops == 3:
                loops = 0
                break
        for language_specifier in language_specifiers:
            if code.startswith(language_specifier):
                code = code.lstrip(language_specifier)
        while code.endswith("`"):
            code = "".join(list(code)[0:-1])
            loops += 1
            if loops == 3:
                break
        code = "\n".join(f"    {i}" for i in code.splitlines()) #Adds an extra layer of indentation
        code = f"async def eval_expr():\n{code}" #Wraps the code inside an async function
        def send(text): #Function for sending message to discord if code has any usage of print function
            self.client.loop.create_task(ctx.send(text))
        env = {
            "bot": self.client,
            "client": self.client,
            "ctx": ctx,
            "print": send,
            "_author": ctx.author,
            "_message": ctx.message,
            "_channel": ctx.channel,
            "_guild": ctx.guild,
            "_me": ctx.me
        }
        env.update(globals())
        try:
            exec(code, env)
            eval_expr = env["eval_expr"]
            result = await eval_expr()
            if result:
                em = discord.Embed(title = "Code ran!", description = result, color = ctx.author.color)
                await ctx.send(embed = em)
        except:
            emb = discord.Embed(title = "Got An error", description = f"```{self.traceback.format_exc()}```", color = ctx.author.color)
            await ctx.send(embed = emb)

    @commands.command()
    async def AFK(self, ctx, *, reason=None):
        cn = ctx.author.display_name
        if reason == None:
            reason2 = 'I set your AFK \n Be sure to remove your afk with rap remafk or rap removeafk when you come back!'
            reason = ''
            try:
                await ctx.author.edit(nick=f"[AFK] {cn}")
            except:
                pass
        else:
            reason2 = f'I set your AFK, status: {reason} \n Be sure to remove your afk with rap remafk or rap removeafk when you come back!'
            try:
                await ctx.author.edit(nick=f"[AFK] {cn}")
            except:
                pass
        with open("json/afk.json", "r") as f:
            data = json.load(f)
        if str(ctx.author.id) in list(data[str(ctx.guild.id)]['AFK']):
            await ctx.channel.send('You\'re already afk :/ \n Use rap remafk or rap removeafk to remove your afk!')
            return

        
        data[str(ctx.guild.id)]['AFK'][str(ctx.author.id)] = reason
        await ctx.channel.send(f'{ctx.author.mention} {reason2}')
        

        with open("json/afk.json", "w") as f:
            json.dump(data,f, indent = 4)
        try:
            await ctx.author.edit(nick='[AFK]'+ctx.author.name)
        except:
            pass

    

    @commands.group(invoke_without_command=True)
    async def covid(self, ctx):
        embed = discord.Embed(
            title = "COVID-19 Command",
            colour = ctx.author.colour,
            description = f"""
            **So you need some help?**
            **__Commands__**
            **{pre}covid world** - This will return the global cases.
            **{pre}covid country <country>** - This will return the COVID-19 cases for the specified country
            Command Example: rap covid country US
            To input a country it must be the abbreviation [here](https://sustainablesources.com/resources/country-abbreviations/) is a list of all country abbreviations.
            """
        )
        await ctx.send(embed = embed)


    @covid.command()
    async def world(self, ctx):
        embed = discord.Embed(
            title = "COVID-19 Global Satistics",
            colour = ctx.author.colour
        )
        api = requests.get("https://covid19.mathdro.id/api").json()
        confirmedCases = api["confirmed"]["value"]
        recoveredCases = api["recovered"]["value"]
        deaths = api["deaths"]["value"]
        embed.add_field(name = "Infected People", value = confirmedCases)
        embed.add_field(name = "People Recovered", value = recoveredCases)
        embed.add_field(name = "Deaths", value = deaths)
        embed.set_image(url = "https://covid19.mathdro.id/api/og")
        await ctx.send(embed = embed)

    @covid.command()
    async def country(self, ctx, country):
        embed = discord.Embed(
            title = f"COVID-19 Satistics for {country}",
            colour = ctx.author.colour
        )
        api = requests.get(f"https://covid19.mathdro.id/api/countries/{country}").json()
        confirmedCases = api["confirmed"]["value"]
        recoveredCases = api["recovered"]["value"]
        deaths = api["deaths"]["value"]
        embed.add_field(name = "Infected People", value = confirmedCases)
        embed.add_field(name = "People Recovered", value = recoveredCases)
        embed.add_field(name = "Deaths", value = deaths)
        embed.set_image(url = f"https://covid19.mathdro.id/api/countries/{country}/og")
        await ctx.send(embed = embed)

        await ctx.send(content=None, embed=embed)

    @commands.command()
    async def reverse(self, ctx, *, text: str):
        """ !poow ,ffuts esreveR
        Everything you type after reverse will of course, be reversed
        """
        t_rev = text[::-1].replace("@", "@\u200B").replace("&", "&\u200B")
        await ctx.send(f"🔁 {t_rev}")

    

    

    

    @commands.command()
    async def weather(self, ctx, *, city: str):

        api_key = "34c0a5e7f6715c2976afdbad44fd2626"
        base_url = "http://api.openweathermap.org/data/2.5/weather?"

        city_name = city
        complete_url = base_url + "appid=" + api_key + "&q=" + city_name
        response = requests.get(complete_url)
        x = response.json()
        channel = ctx.message.channel
        
        if x["cod"] != "404":
            async with channel.typing():
                y = x["main"]
                current_temperature = y["temp"]
                current_temperature_celsiuis = str(round(current_temperature - 273.15))
                current_pressure = y["pressure"]
                current_humidity = y["humidity"]
                z = x["weather"]
                weather_description = z[0]["description"]

                
                embed = discord.Embed(title=f"Weather in {city_name}",
                                color=ctx.guild.me.top_role.color,
                                timestamp=ctx.message.created_at,)
                embed.add_field(name="Descripition", value=f"**{weather_description}**", inline=False)
                embed.add_field(name="Temperature(C)", value=f"**{current_temperature_celsiuis}°C**", inline=False)
                embed.add_field(name="Humidity(%)", value=f"**{current_humidity}%**", inline=False)
                embed.add_field(name="Atmospheric Pressure(hPa)", value=f"**{current_pressure}hPa**", inline=False)
                embed.set_thumbnail(url="https://i.ibb.co/CMrsxdX/weather.png")
                embed.set_footer(text=f"Requested by {ctx.author.name}")

            await channel.send(embed=embed)
        else:
            await channel.send("City not found.")

    @commands.command()
    async def snipe(self, ctx):
        try:
            contents, author, channel_name, time = self.client.sniped_messages[ctx.guild.id]
            
        except:
            await ctx.channel.send("Couldn't find a message to snipe!")
            return

        embed = discord.Embed(description=contents, color=discord.Color.purple(), timestamp=time)
        embed.set_author(name=f"{author.name}#{author.discriminator}", icon_url=author.avatar_url)
        embed.set_footer(text=f"Deleted in : #{channel_name}")

        await ctx.channel.send(embed=embed)


    @commands.command()
    async def invites(self, ctx):
        totalInvites = 0
        for i in await ctx.guild.invites():
            if i.inviter == ctx.author:
                totalInvites += i.uses
        await ctx.send(f"You've invited {totalInvites} member{'' if totalInvites == 1 else 's'} to the server!")


    

    

    

    @commands.command(aliases=['remafk'])
    async def removeafk(self, ctx):
        message = ctx

        with open("json/afk.json", "r") as f:
            data = json.load(f)
            if str(message.author.id) in list(data[str(message.guild.id)]['AFK']):
                data[str(message.guild.id)]["AFK"].pop(str(message.author.id))
                await message.channel.send(f'Welcome Back, I removed your AFK!')
                try:
                    await ctx.author.edit(nick=f"{ctx.author.name}")
                except:
                    pass
            else:
                await ctx.send("You\'re not afk :/")
        with open("json/afk.json", "w") as f:
            json.dump(data, f, indent=4)

def setup(client):
    client.add_cog(Utility(client))