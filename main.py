from ka import keep_alive
import discord
import random
import os
import asyncio
import datetime
import aiofiles
from discord.ext import commands
from prsaw import RandomStuff



giphyapi = "7ZCAhzagQUOXk1xUQht7Om16H7N4lKLX"
owners = [801234598334955530, 814226043924643880]

prefixes = ["rap ", "r!", "dino ", "rt!"]
prefix = random.choice(prefixes)
rs = RandomStuff(async_mode = True)
client = commands.AutoShardedBot(command_prefix = prefixes, intents=discord.Intents.all(), allowed_mentions=discord.AllowedMentions(roles=False, everyone=False))
client.launch_time = datetime.datetime.utcnow()
client.warnings = {}
bot = client
smoother = True
client.load_extension('jishaku')
restart_reason = "antiswearing removed :/"

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
    chan = client.get_channel(849333490612305972)
    await chan.send(f"I got invited to a new server! Name = {guild.name} & ID = {guild.id}")
    
    for channel in guild.text_channels:
            if channel.permissions_for(guild.me).send_messages:

                guild = discord.Embed(title = "Hi there! I'm Raptor, a fun bot with moderation abilities, and economy system, and more!", description = "Use `r!help` to see all of my commands!", color = discord.Colour.dark_green())
                guild.add_field(name = "You can use the `r!setprefix` command to change my prefix for this server!", value = "Use `r!vote` to vote for me!")
                guild.set_thumbnail(url = "https://media.discordapp.net/attachments/806574171513421867/833767333151244319/Raptor.jpeg")
                guild.set_footer(text = "Please give me admin otherwise my commands might not work.")

                await channel.send(embed = guild)
                break



@client.event
async def on_guild_remove(guild):
    chanel = client.get_channel(849333503530500136)
    await chanel.send(f"I got kicked/banned from {guild.name}. :\ ID = {guild.id}")





@client.event
async def on_message(message):
    args = message.content.split(' ')
    if not message.author.bot:    
        if message.content == '<@!829836500970504213>':
            await message.reply(f'The prefix for this server is: \n`{random.choice(prefixes)}`')
            return

        elif client.user.mentioned_in(message):
            await message.add_reaction("<a:RaptorIsTriggered:851476363281432577>")

        elif message.content.startswith("im"):
            await message.channel.send(f"Hi {args[1]}, I'm Raptor.")

        elif message.content.startswith("i'm"):
            await message.channel.send(f"Hi {args[1]}, I'm Raptor.")

        elif message.content.startswith("Im"):
            await message.channel.send(f"Hi {args[1]}, I'm Raptor.")
        
        elif message.content.startswith("I'm"):
            await message.channel.send(f"Hi {args[1]}, I'm Raptor.")
        
        elif message.content.startswith("I am"):
            await message.channel.send(f"Hi {args[1]}, I'm Raptor.")
        
        elif message.content.startswith("i am"):
            await message.channel.send(f"Hi {args[1]}, I'm Raptor.")

        elif message.content.startswith("r!hack"):
            await message.add_reaction("<a:PepeHack:851502755448356916>")
    
        elif message.channel.name == 'raptor-chatbot': 
            response = await rs.get_ai_response(message.content)
            await message.reply(response)  

    await client.process_commands(message)

@client.command()
async def testinga(ctx):
    async for guild in client.fetch_guilds(limit=150):
      print(guild.name)

@client.event
async def on_ready():
  channel = client.get_channel(851524050223890502)
  embed = discord.Embed(
    title = "Online!",
    description = f"**New Updates!**\n```fix\n{restart_reason}\n```",
    color = 0x00ff00
  )
  await channel.send(embed=embed)
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

    elif isinstance(error, discord.ext.commands.errors.MissingPermissions):
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


@client.process_commands



def nothing():
  pass

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        try:
            client.load_extension(f"cogs.{filename[:-3]}")
        except Exception as e:
            print(e)

keep_alive()
client.run(os.environ['TOKEN'])