from ka import keep_alive
import discord
import random
import os
import asyncio
import datetime
import aiofiles
from discord.ext import commands
from prsaw import RandomStuff
from pretty_help import PrettyHelp, DefaultMenu

prefixes = ["rap ", "r!", "dino ", "rt!"]
prefix = random.choice(prefixes)
rs = RandomStuff(async_mode= True)
intents = discord.Intents.all()
client = commands.Bot(command_prefix = prefixes, intents=intents)
client.launch_time = datetime.datetime.utcnow()
client.warnings = {}
bot = client
smoother = True

restart_reason = "Added emoji command."

client.load_extension('jishaku')

ny = "Other"
it = "Raptor Help | All Cetgories"
menu = DefaultMenu('◀️', '▶️', '❌') # You can copy-paste any icons you want.
client.help_command = PrettyHelp(navigation=menu, no_category=ny, index_title = it, sort_commands=True) 








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
                guild.set_footer(text = "Please give me admin otherwise my commands might not work.", icon_url = "data:image/png;base64,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")

                await channel.send(embed = guild)
                break

@client.event
async def on_guild_remove(guild):
    chanel = client.get_channel(849333503530500136)
    await chanel.send(f"I got kicked/banned from {guild.name}. :\ ID = {guild.id}")



@client.event
async def on_message(message):
    if message.content == '<@!829836500970504213>':
        await message.reply(f'The prefix for this server is: \n`{random.choice(prefixes)}`')
        return
    if message.content == "raptor":
        await message.reply(f"Hello {message.author.mention}!")

    
    if not message.author.bot:
        if message.channel.name == 'raptor-chatbot': 
            response = await rs.get_ai_response(message.content)
            await message.reply(response)

    
        

    await client.process_commands(message)



@client.event
async def on_ready():
    print(f"{client.user} is ready. Remember to update restart_reason in main.py!")
    await client.change_presence(activity=discord.Game(name = f"in {len(client.guilds)} servers | {prefix}help"))
    await client.change_presence(activity=discord.Game(name = f"with {len(client.users)}in {len(client.guilds)} servers | {prefix}help"))
    await client.change_presence(activity=discord.Streaming(name = f"Raptor | {prefix}help", url = "https://www.twitch.tv/raptor_bot_discord"))
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name = f"to {len(client.guilds)} servers | {prefix}help"))
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name = f" over {len(client.guilds)} servers | {prefix}help"))

    for guild in client.guilds:
        client.warnings[guild.id] = {}

        async with aiofiles.open(f"warns/{guild.id}.txt", mode="r") as file:
            lines = await file.readlines()

            for line in lines:
                data = line.split(" ")
                member_id = int(data[0])
                admin_id = int(data[1])
                reason = " ".join(data[2:]).strip("\n")

                try:
                    client.warnings[guild.id][member_id][0] += 1
                    client.warnings[guild.id][member_id][1].append((admin_id, reason))

                except KeyError:
                    client.warnings[guild.id][member_id] = [1, [(admin_id, reason)]] 
    
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
      em = discord.Embed(title = "Missing Required Argument", description = f"Please enter all required arguments. If you don't understand what you are missing, then  use **<prefix>help {ctx.command.name}** to see the required arguments.", color = ctx.author.color)
      await ctx.send()
    if isinstance(error,commands.CommandNotFound):
      em = discord.Embed(title = "Uh oh.", description = "Command not found. Be sure to use **<prefix>help** to see all of my commands!", color = ctx.author.color)
      await ctx.send(embed = em)
    if isinstance(error, commands.errors.CommandOnCooldown):  
        em = discord.Embed(title = "Spam isn't cool fam.", description = 'The command **{}** is still on cooldown for {:.2f} seconds.'.format(ctx.command.name, error.retry_after), color = ctx.author.color)
        return await ctx.send(embed = em)
    if isinstance(error, commands.BadArgument):
        embed = discord.Embed(title="Error", description=str(error))
        await ctx.send(embed=embed)
    if isinstance(error, discord.ext.commands.errors.NotOwner):
        await ctx.send("You are not the owner of this bot so you can't use this command")
        return
    if isinstance(error, commands.MemberNotFound):
        await ctx.send("That member doesn't exist.")
        return

    if isinstance(error, discord.Forbidden):
        await ctx.send("I can't do this. I'm forbidden to do this.")

    if isinstance(error, discord.NotFound):
        await ctx.send("Couldn't find that sorry")
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