import discord
import json
import datetime
from main import restart_reason as rr, prefix as pre, prefixes
from datetime import datetime
from discord.ext import commands
import asyncio
import random
import requests
import json
import aiohttp
import inspect

sniped_messages = {}

class Utils(commands.Cog):
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
        print('misc cog is ready.')

    # commands

    @commands.command(help="Sends the links where you can vote for me!")
    async def vote(self, ctx):
        vtlk = discord.Embed(title = "Vote for Me!", description ="Vote for me by using these links!", color = ctx.author.color)
        vtlk.add_field(name = "Top.gg", value = "[Click Here](https://top.gg/bot/829836500970504213/vote)")
        vtlk.add_field(name = "Discord Bot List", value = "[Click Here](https://discordbotlist.com/bots/raptor/upvote)")
        await ctx.send(embed = vtlk)

    

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
        em = discord.Embed(title = "Invite Me!", description = "[Click Here](https://discord.com/api/oauth2/authorize?client_id=829836500970504213&permissions=4260887158&redirect_uri=https%3A%2F%2Fraptor-dbot.glitch.me%2Fthx.html&response_type=code&scope=bot%20applications.commands%20identify)", color = ctx.author.color)
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
        em.add_field(name = "Uptime", value = f"```I have been online for {days} days, {hours} hours, {minutes} minutes and {seconds} seconds!```")
        em.add_field(name = "Reason For Last Restart", value = f"```{rr}```")
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

    @commands.Cog.listener()
    async def on_ready(self):
        print('Utils cog is ready.')

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        sniped_messages[message.guild.id] = (message.content, message.author, message.channel.name, message.created_at)


    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        
        file = "afk.json"
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
    async def ping(self, ctx, member:discord.Member=None):
        if member == None:
            member = ctx.author
        em = discord.Embed(title="Pong! 🏓", description=f"{round(self.client.latency * 1000)}ms" , color = discord.Colour.dark_green())
        await ctx.send(embed = em)

    

    @commands.command(help="Dm's a person if their dms are open.")
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def dm(self, ctx, user_id=None, *, msg=None):
        if user_id != None and msg != None:
            try:
                target = await self.client.fetch_user(user_id)
                await target.send(msg)

                await ctx.channel.send("'" + msg + "' sent to: " + target.name)

            except:
                await ctx.channel.send("Couldn't dm the given user.")
            

        else:
            await ctx.channel.send("You didn't provide a user's id and/or a message.")


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

    @commands.command(aliases=['afk', 'Afk', 'aFk', 'afK','AFk', 'aFK', 'AfK'])
    async def AFK(self, ctx, *, reason=None):
        if reason == None:
            reason2 = 'I set your AFK \n Be sure to remove your afk with r!remafk or r!removeafk when you come back!'
            reason = ''
        else:
            reason2 = f'I set your AFK, status: {reason} \n Be sure to remove your afk with r!remafk or r!removeafk when you come back!'
        with open("afk.json", "r") as f:
            data = json.load(f)
        if str(ctx.author.id) in list(data[str(ctx.guild.id)]['AFK']):
            await ctx.channel.send('You\'re already afk :/ \n Use r!remafk or r!removeafk to remove your afk!')
            return

        
        data[str(ctx.guild.id)]['AFK'][str(ctx.author.id)] = reason
        await ctx.channel.send(f'{ctx.author.mention} {reason2}')
        

        with open("afk.json", "w") as f:
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
            Command Example: r!covid country US
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

    @commands.command(aliases=["howhot", "hot"])
    async def hotrate(self, ctx, *, user: discord.Member = None):
        """ Returns a random percent for how hot is a discord user """
        user = user or ctx.author

        random.seed(user.id)
        r = random.randint(1, 100)
        hot = r / 1.17

        if hot > 25:
            emoji = "❤"
        elif hot > 50:
            emoji = "💖"
        elif hot > 75:
            emoji = "💞"
        else:
            emoji = "💔"

        await ctx.send(f"**{user.name}** is **{hot:.2f}%** hot {emoji}")

    

    

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


    

    @commands.command(aliases=['gc', 'getcode'])
    async def get_code(self, ctx, *, cmd):
        owners = [801234598334955530]
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

    @commands.command(aliases=['remafk'])
    async def removeafk(self, ctx):
        message = ctx

        with open("afk.json", "r") as f:
            data = json.load(f)
            if str(message.author.id) in list(data[str(message.guild.id)]['AFK']):
                data[str(message.guild.id)]["AFK"].pop(str(message.author.id))
                await message.channel.send(f'Welcome Back, I removed your AFK!')
            else:
                await ctx.send("You\'re not in afk :/")
        with open("afk.json", "w") as f:
            json.dump(data, f, indent=4)

    @commands.command(name = "prefixes", aliases=['pre', 'prefix'])
    async def prefixs(self, ctx):
        e = "My Prefixes :arrow_down: \n \n"
        index = 0
        for prefix in prefixes:
            index += 1
            e += f"**{index}.** {prefix}\n"
        em = discord.Embed(title = "Prefixes!",description = e, color = ctx.author.color)
        em.set_footer(text = "These are my prefixes!")
        await ctx.send(embed = em)

def setup(client):
    client.add_cog(Utils(client))