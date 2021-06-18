import sr_api
import discord
import random
import os
import aiosqlite
import json
import asyncio
import datetime
import aiofiles
from discord.ext import commands
from prsaw import RandomStuff
import ka as ka

restart_reason = "removed customizable prefixes again!"
owners = [801234598334955530, 814226043924643880]



prefix = "rap "
rs = RandomStuff(async_mode = True)
client = commands.Bot(command_prefix = prefix, intents=discord.Intents.all(), allowed_mentions=discord.AllowedMentions(roles=False, everyone=False), case_insensitive=True, owner_ids=owners)
client.sr_api = sr_api.Client()
client.launch_time = datetime.datetime.utcnow()
client.warnings = {}
bot = client
client.bldb = aiosqlite.connect("db/bl.sqlite")
smoother = True
client.reaction_roles = []
client.load_extension('jishaku')

note = "Note from owner:```fix\nworking on antiswearing.. -ks\n```"


class bcolors:
  HEADER = '\033[95m'
  OKBLUE = '\033[94m'
  OKCYAN = '\033[96m'
  OKGREEN = '\033[92m'
  WARNING = '\033[93m'
  FAIL = '\033[91m'
  ENDC = '\033[0m'
  BOLD = '\033[1m'
  UNDERLINE = '\033[4m'

@client.event
async def on_guild_join(guild):

    client.warnings[guild.id] = {}
    chan = client.get_channel(855136624623222784)

    embed = discord.Embed(
      title = "<a:Raptor_Join:851812194798796811> | New Server Joined!",
      description = f"I just joined {guild.name}!",
      color = 0x00ff00
    )
    embed.set_footer(
      text = "Thanks for inviting me!",
      icon_url = client.user.avatar_url
    )
    await chan.send(embed=embed)
    
    for channel in guild.text_channels:
            if channel.permissions_for(guild.me).send_messages:

                guild = discord.Embed(title = "Hi there! I'm Raptor, a fun bot with moderation abilities, and economy system, and more!", description = f"Use `{prefix}help` to see all of my commands but here's some information to get you started!", color = discord.Colour.dark_green())
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
                  value = "Raptor can easily moderate your server  using commands such as purge, kick, ban, lock and more! Also, change its prefix using the setprefix command!"
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
                guild.set_thumbnail(url = "https://media.discordapp.net/attachments/845365628223356988/855135611480047626/Raptor.png")
                guild.set_footer(text = "Please give me all admin permissions otherwise my commands might not work.")

                await channel.send(embed = guild)
                break

   



@client.event
async def on_guild_remove(guild):
    
    chanel = client.get_channel(855136624623222784)
    
    embed = discord.Embed(
      title = "<a:Raptor_Leave:851812497354522654> | Just Left A Server..",
      description = f"Just left server {guild.name}, goodbye..",
      color = 0xff0000
    )
    embed.set_footer(
      text = "Goodbye..",
      icon_url = client.user.avatar_url
    )
    await chanel.send(embed=embed)

@client.event
async def on_message(message):
    if not message.author.bot:    
        if message.content == '<@!829836500970504213>':
            await message.reply(f'The prefix that you can always use is: \n`{prefix} `')
            return

        elif client.user.mentioned_in(message):
            await message.add_reaction("<a:RaptorIsTriggered:851476363281432577>")


        elif message.content.startswith("r!hack"):
            await message.add_reaction("<a:PepeHack:851502755448356916>")
    
        elif message.channel.name == 'raptor-chatbot': 
            response = await rs.get_ai_response(message.content)
            await message.reply(response)  

    await client.process_commands(message)

num = random.randint(1, 10)
@client.event
async def on_ready():
    await client.bldb

    cursor = await client.bldb.cursor()

    await cursor.execute("""
      CREATE TABLE IF NOT EXISTS blacklist(
        guild_id INTEGER,
        user_id INTEGER,
        blacklisted BOOL
      )""")
    await client.bldb.commit()
    channel = client.get_channel(855129871650127957)
    embed = discord.Embed(
    title = "Online!",
    description = f"**New Updates!**\n```fix\n{restart_reason}\n```",
    color = 0x00ff00
    )
    
    if num == 5:
        await channel.send(embed=embed)
    else:
        pass
    print(f"{client.user} is ready. Remember to update restart_reason and note in main.py!")
    print(f"""{bcolors.BOLD}{bcolors.OKGREEN}
  _______  _______  _______ _________ _______  _______ 
  (  ____ )(  ___  )(  ____ )\__   __/(  ___  )(  ____ )
  | (    )|| (   ) || (    )|   ) (   | (   ) || (    )|
  | (____)|| (___) || (____)|   | |   | |   | || (____)|
  |     __)|  ___  ||  _____)   | |   | |   | ||     __)
  | (\ (   | (   ) || (         | |   | |   | || (\ (   
  | ) \ \__| )   ( || )         | |   | (___) || ) \ \__
  |/   \__/|/     \||/          )_(   (_______)|/   \__/
                                                        

    """)
    await client.change_presence(activity=discord.Game(name = f"in {len(client.guilds)} servers | {prefix}help"))
    await client.change_presence(activity=discord.Game(name = f"with {len(client.users)}in {len(client.guilds)} servers | {prefix}help"))
    await client.change_presence(activity=discord.Streaming(name = f"Raptor | {prefix}help", url = "https://www.twitch.tv/raptor_bot_discord"))
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name = f"to {len(client.guilds)} servers | {prefix}help"))
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name = f" over {len(client.guilds)} servers | {prefix}help"))

        
    async with aiofiles.open("reaction_roles.txt", mode="r") as file:
        lines = await file.readlines()
        for line in lines:
            data = line.split(" ")
            bot.reaction_roles.append((int(data[0]), int(data[1]), data[2].strip("\n")))

async def ch_pr():
    await client.wait_until_ready()

    statuses = [f"{prefix}help",f"Raptor | {prefix}help",f"in {len(client.guilds)} servers | {prefix}help",f"my economy | {prefix}help",f"Support Server: https://discord.gg/CwAAxx7YyJ | {prefix}help", f"with {len(client.users)} users | {prefix}help", f"with {len(set(client.commands))} commands | {prefix}help"]

    while not client.is_closed():

        status = random.choice(statuses)
        
        await client.change_presence(activity=discord.Game(name = status))

        await asyncio.sleep(10)
client.loop.create_task(ch_pr())

@client.event
async def on_command_error(ctx,error):

    if isinstance(error,commands.MissingRequiredArgument):
      em = discord.Embed(title = "Missing Required Argument", description = f"Please enter all required arguments. If you don't understand what you are missing, then  use **r!help {ctx.command.name}** to see the required arguments.", color = ctx.author.color)
      await ctx.send()
    elif isinstance(error,commands.CommandNotFound):
      em = discord.Embed(title = "Whoops.. Dropped some code..", description = "Command not found. Be sure to use **r!help** to see all of my commands!", color = ctx.author.color)
      await ctx.send(embed = em)
    elif isinstance(error, commands.errors.CommandOnCooldown):  
        em = discord.Embed(title = "Spam isn't cool!", description = 'The command **{}** is still on cooldown for {:.2f} seconds.'.format(ctx.command.name, error.retry_after), color = ctx.author.color)
        return await ctx.send(embed = em)
    elif isinstance(error, commands.BadArgument):
        embed = discord.Embed(title="Error", description=str(error))
        await ctx.send(embed=embed)

    elif ctx.author.id not in owners:
        await ctx.send("You are not the owner of this bot so you can't use this command")
        return
    if isinstance(error,commands.BotMissingPermissions):
        embed = discord.Embed(
          title = "Sorry!",
          description = f"I are missing the required permissions to use the command {ctx.command.name}.",
          color = 0xff0000 #red <----
        )
        await ctx.send(content=ctx.author.mention, embed=embed)
        return


    elif isinstance(error, commands.errors.MissingPermissions):
        embed = discord.Embed(
          title = "Sorry!",
          description = f"You are missing the required permissions to use the command.",
          color = 0xff0000 #red <----
        )
        
        await ctx.send(content=ctx.author.mention, embed=embed)
        return

    elif isinstance(error, discord.errors.NotFound):
        await ctx.send("Couldn't find that error, sorry.")
        return
    else:
        raise error
        await ctx.send("Error 101")



for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        try:
            client.load_extension(f"cogs.{filename[:-3]}")
        except Exception as e:
            print(e)

ka.keep_alive()
client.run(os.environ['TOKEN'])