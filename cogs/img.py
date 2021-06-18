import discord
import asyncio
import json
import aiohttp
import datetime
import random
import io
import requests
import numpy as np
import cv2 as cv
from datetime import datetime
from discord.ext import commands
import PIL
from PIL import Image, ImageFont, ImageDraw, ImageFilter
from io import BytesIO
err_color = discord.Color.red()
color = 0x0da2ff

class Images(commands.Cog):
    """ Category for image commands """

    def __init__(self, client):
        self.client = client
        self.ses = aiohttp.ClientSession()
        

    # events
    @commands.Cog.listener()
    async def on_ready(self):
        print('Img cog is ready.')

    # commands
    

    @commands.command()
    async def wanted(self, ctx, user : discord.Member = None):
        if user == None:
            user = ctx.author

        wanted = Image.open("images/Wanted.jpeg")
        
        asset = user.avatar_url_as(size = 128)

        data = BytesIO(await asset.read())

        pfp = Image.open(data)
        pfp = pfp.resize((106,106))

        wanted.paste(pfp, (41,85))

        wanted.save("images/profile.jpg")
        await ctx.send(file = discord.File("images/profile.jpg"))

    @commands.command()
    async def amogus(self, ctx, user : discord.Member = None):
        if user == None:
            user = ctx.author

        wanted = Image.open("images/amogu.png")
        
        asset = user.avatar_url_as(size = 128)

        data = BytesIO(await asset.read())

        pfp = Image.open(data)
        pfp = pfp.resize((48,48))

        wanted.paste(pfp, (246, 310))

        wanted.save("images/amog.png")
        await ctx.send(file = discord.File("images/amog.png"))

    @commands.command()
    async def rip(self, ctx, member:discord.Member=None):
        if member == None:
            member = ctx.author
        rip = Image.open('images/RIP.jpg')

        asset = member.avatar_url_as(size=128)

        data = BytesIO(await asset.read())

        pfp = Image.open(data)

        pfp = pfp.resize((87, 87))

        rip.paste(pfp, (57, 124))

        rip.save('images/prip.jpg')

        await ctx.send(file = discord.File('images/prip.jpg'))


    
    @commands.command()
    async def naruto(self, ctx, user: discord.Member = None):
        if not user:
            user = ctx.author

        naruto = Image.open("images/Naruto.png")

        asset = user.avatar_url_as(size=128)
        data = BytesIO(await asset.read())
        pfp = Image.open(data)

        pfp = pfp.resize((97, 97))
        naruto.paste(pfp, (418, 120))

        naruto.save("images/n.png")

        await ctx.send(file=discord.File("images/n.png"))

    @commands.command()
    async def amongus(self, ctx, user: discord.Member = None):
        if not user:
            user = ctx.author

        naruto = Image.open("images/Amongus.jpeg")

        asset = user.avatar_url_as(size=128)
        data = BytesIO(await asset.read())
        pfp = Image.open(data)

        pfp = pfp.resize((108, 108))
        naruto.paste(pfp, (87, 25))

        naruto.save("images/au.jpeg")

        await ctx.send(file=discord.File("images/au.jpeg"))

    @commands.command()
    async def text(self, ctx, *, text = "No text entered"):

        img = Image.open("images/White.jpeg")

        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("JosefinSans-Regular.ttf", 24)

        draw.text((100,100), text, (0,17,0), font = font)

        img.save("images/text.jpeg")

        await ctx.send(file = discord.File("images/text.jpeg"))


    @commands.command(aliases=['trigger', 'trg'])
    async def triggered(self, ctx, member: discord.Member=None):
        if not member: # if no member is mentioned
            member = ctx.author # the user who ran the command will be the member
            
        async with aiohttp.ClientSession() as wastedSession:
            async with wastedSession.get(f'https://some-random-api.ml/canvas/triggered?avatar={member.avatar_url_as(format="png", size=1024)}') as wastedImage: # get users avatar as png with 1024 size
                imageData = BytesIO(await wastedImage.read()) # read the image/bytes
            
                
                await ctx.send(file=discord.File(imageData, 'triggered.gif')) # sending the file

    @commands.command()
    async def wasted(self, ctx, member: discord.Member=None):
        if not member: # if no member is mentioned
            member = ctx.author # the user who ran the command will be the member
            
        async with aiohttp.ClientSession() as wastedSession:
            async with wastedSession.get(f'https://some-random-api.ml/canvas/wasted?avatar={member.avatar_url_as(format="png", size=1024)}') as wastedImage: # get users avatar as png with 1024 size
                imageData = BytesIO(await wastedImage.read()) # read the image/bytes
            
                
                await ctx.send(file=discord.File(imageData, 'wasted.png')) # sending the file

    @commands.command(aliases=['redpanda', 'redpandaimg'])
    async def redpandaimage(self, ctx):
        async with aiohttp.ClientSession() as ses:
            async with ses.get('https://some-random-api.ml/img/red_panda') as f:
                if f.status in range(200, 299):
                    dat = await f.json()
                    img = dat['link']
                    em = discord.Embed(
                        title='Red Panda',
                        color = ctx.author.color
                    )
                    em.set_image(url=f'{img}')
                    await ctx.send(embed=em)
                    await ses.close()
                else:
                    await ctx.reply("Error when trying to get a red panda image.")
                    await ses.close()
    
    @commands.command(aliases=['pikachu', 'pikachuimg', 'pika', 'pikaimg', 'pikaimage'])
    async def pikachuimage(self, ctx):
        async with aiohttp.ClientSession() as ses:
            async with ses.get('https://some-random-api.ml/img/pikachu') as f:
                if f.status in range(200, 299):
                    dat = await f.json()
                    img = dat['link']
                    em = discord.Embed(
                        title='Pikachu Image',
                        color = ctx.author.color
                    )
                    em.set_image(url=f'{img}')
                    await ctx.send(embed=em)
                    await ses.close()
                else:
                    await ctx.reply("Error when trying to get a pikachu image.")
                    await ses.close()



    @commands.command()
    async def glass(self, ctx, member: discord.Member=None):
        if not member: # if no member is mentioned
            member = ctx.author # the user who ran the command will be the member
            
        async with aiohttp.ClientSession() as wastedSession:
            async with wastedSession.get(f'https://some-random-api.ml/canvas/glass?avatar={member.avatar_url_as(format="png", size=1024)}') as wastedImage: # get users avatar as png with 1024 size
                imageData = BytesIO(await wastedImage.read()) # read the image/bytes
            
                
                await ctx.send(file=discord.File(imageData, 'glass.png')) # sending the file
    
    @commands.command()
    async def rainbow(self, ctx, member: discord.Member=None):
        if not member: # if no member is mentioned
            member = ctx.author # the user who ran the command will be the member
            
        async with aiohttp.ClientSession() as wastedSession:
            async with wastedSession.get(f'https://some-random-api.ml/canvas/gay?avatar={member.avatar_url_as(format="png", size=1024)}') as wastedImage: # get users avatar as png with 1024 size
                imageData = BytesIO(await wastedImage.read()) # read the image/bytes
            
                
                await ctx.send(file=discord.File(imageData, 'rainbow.png')) # sending the 
    
    

    @commands.command()
    async def invert(self, ctx, member: discord.Member=None):
        if not member: # if no member is mentioned
            member = ctx.author # the user who ran the command will be the member
            
        async with aiohttp.ClientSession() as wastedSession:
            async with wastedSession.get(f'https://some-random-api.ml/canvas/invert?avatar={member.avatar_url_as(format="png", size=1024)}') as wastedImage: # get users avatar as png with 1024 size
                imageData = BytesIO(await wastedImage.read()) # read the image/bytes
            
                
                await ctx.send(file=discord.File(imageData, 'inverted.png')) # sending the 

    
    
    @commands.command()
    async def blue(self, ctx, member: discord.Member=None):
        if not member: # if no member is mentioned
            member = ctx.author # the user who ran the command will be the member
            
        async with aiohttp.ClientSession() as wastedSession:
            async with wastedSession.get(f'https://some-random-api.ml/canvas/blue?avatar={member.avatar_url_as(format="png", size=1024)}') as wastedImage: # get users avatar as png with 1024 size
                imageData = BytesIO(await wastedImage.read()) # read the image/bytes
            
                
                await ctx.send(file=discord.File(imageData, 'blue.png')) # sending the 

    @commands.command()
    async def green(self, ctx, member: discord.Member=None):
        if not member: # if no member is mentioned
            member = ctx.author # the user who ran the command will be the member
            
        async with aiohttp.ClientSession() as wastedSession:
            async with wastedSession.get(f'https://some-random-api.ml/canvas/green?avatar={member.avatar_url_as(format="png", size=1024)}') as wastedImage: # get users avatar as png with 1024 size
                imageData = BytesIO(await wastedImage.read()) # read the image/bytes
            
                
                await ctx.send(file=discord.File(imageData, 'green.png')) # sending the 

    @commands.command()
    async def red(self, ctx, member: discord.Member=None):
        if not member: # if no member is mentioned
            member = ctx.author # the user who ran the command will be the member
            
        async with aiohttp.ClientSession() as wastedSession:
            async with wastedSession.get(f'https://some-random-api.ml/canvas/red?avatar={member.avatar_url_as(format="png", size=1024)}') as wastedImage: # get users avatar as png with 1024 size
                imageData = BytesIO(await wastedImage.read()) # read the image/bytes
            
                
                await ctx.send(file=discord.File(imageData, 'red.png')) # sending the 

    @commands.command()
    async def sepia(self, ctx, member: discord.Member=None):
        if not member: # if no member is mentioned
            member = ctx.author # the user who ran the command will be the member
            
        async with aiohttp.ClientSession() as wastedSession:
            async with wastedSession.get(f'https://some-random-api.ml/canvas/sepia?avatar={member.avatar_url_as(format="png", size=1024)}') as wastedImage: # get users avatar as png with 1024 size
                imageData = BytesIO(await wastedImage.read()) # read the image/bytes
            
                
                await ctx.send(file=discord.File(imageData, 'sepia.png')) # sending the 

    @commands.command(aliases=['baw'])
    async def blackwhite(self, ctx, member: discord.Member=None):
        if not member: # if no member is mentioned
            member = ctx.author # the user who ran the command will be the member
            
        async with aiohttp.ClientSession() as wastedSession:
            async with wastedSession.get(f'https://some-random-api.ml/canvas/threshold?avatar={member.avatar_url_as(format="png", size=1024)}') as wastedImage: # get users avatar as png with 1024 size
                imageData = BytesIO(await wastedImage.read()) # read the image/bytes
            
                
                await ctx.send(file=discord.File(imageData, 'baw.png')) # sending the 

    @commands.command(aliases=['bright'])
    async def brightness(self, ctx, member: discord.Member=None):
        if not member: # if no member is mentioned
            member = ctx.author # the user who ran the command will be the member
            
        async with aiohttp.ClientSession() as wastedSession:
            async with wastedSession.get(f'https://some-random-api.ml/canvas/brightness?avatar={member.avatar_url_as(format="png", size=1024)}') as wastedImage: # get users avatar as png with 1024 size
                imageData = BytesIO(await wastedImage.read()) # read the image/bytes
            
                
                await ctx.send(file=discord.File(imageData, 'bright.png')) # sending the 

    


    @commands.command()
    async def tweet(self, ctx, *, msg="No text entered"):
        async with aiohttp.ClientSession() as ses:
            async with ses.get(f"https://nekobot.xyz/api/imagegen?type=tweet&username={ctx.author.name}&text={msg}") as f:
                if f.status in range(200, 299):
                    dat = await f.json()
                    img = dat['message']
                    em = discord.Embed(
                        title='Tweeted!',
                        color = ctx.author.color
                    )
                    em.set_image(url=f'{img}')
                    await ctx.send(embed=em)
                    await ses.close()
                else:
                    await ctx.reply("Error when trying to tweet.")
                    await ses.close()

    @commands.command()
    async def magik(self, ctx, member:discord.Member=None):
        if member == None:
            member = ctx.author
        async with aiohttp.ClientSession() as ses:
            async with ses.get(f"https://nekobot.xyz/api/imagegen?type=magik&image={member.avatar_url}") as f:
                if f.status in range(200, 299):
                    dat = await f.json()
                    img = dat['message']
                    em = discord.Embed(
                        title='Magikified!',
                        color = ctx.author.color
                    )
                    em.set_image(url=f'{img}')
                    await ctx.send(embed=em)
                    await ses.close()
                else:
                    await ctx.reply("Error when trying to magikify.")
                    await ses.close()

    @commands.command()
    async def iphonex(self, ctx, member:discord.Member=None):
        if member == None:
            member = ctx.author
        async with aiohttp.ClientSession() as ses:
            async with ses.get(f"https://nekobot.xyz/api/imagegen?type=iphonex&url={member.avatar_url}") as f:
                if f.status in range(200, 299):
                    dat = await f.json()
                    img = dat['message']
                    em = discord.Embed(
                        title='Iphonexed!',
                        color = ctx.author.color
                    )
                    em.set_image(url=f'{img}')
                    await ctx.send(embed=em)
                    await ses.close()
                else:
                    await ctx.reply("Error when trying to iphonex.")
                    await ses.close()

    @commands.command()
    async def threats(self, ctx, member:discord.Member=None):
        if member == None:
            member = ctx.author
        async with aiohttp.ClientSession() as ses:
            async with ses.get(f"https://nekobot.xyz/api/imagegen?type=threats&url={member.avatar_url}") as f:
                if f.status in range(200, 299):
                    dat = await f.json()
                    img = dat['message']
                    em = discord.Embed(
                        title='Done!',
                        color = ctx.author.color
                    )
                    em.set_image(url=f'{img}')
                    await ctx.send(embed=em)
                    await ses.close()
                else:
                    await ctx.reply("Error when trying to threat.")
                    await ses.close()
    
    @commands.command()
    async def baguette(self, ctx, member:discord.Member=None):
        if member == None:
            member = ctx.author
        async with aiohttp.ClientSession() as ses:
            async with ses.get(f"https://nekobot.xyz/api/imagegen?type=baguette&url={member.avatar_url}") as f:
                if f.status in range(200, 299):
                    dat = await f.json()
                    img = dat['message']
                    em = discord.Embed(
                        title='Baguetted!',
                        color = ctx.author.color
                    )
                    em.set_image(url=f'{img}')
                    await ctx.send(embed=em)
                    await ses.close()
                else:
                    await ctx.reply("Error when trying to baguette.")
                    await ses.close()

    @commands.command()
    async def clyde(self, ctx, *, text="No text entered"):

        async with aiohttp.ClientSession() as ses:
            async with ses.get(f"https://nekobot.xyz/api/imagegen?type=clyde&text={text}") as f:
                if f.status in range(200, 299):
                    dat = await f.json()
                    img = dat['message']
                    em = discord.Embed(
                        title='Clyded!',
                        color = ctx.author.color
                    )
                    em.set_image(url=f'{img}')
                    await ctx.send(embed=em)
                    await ses.close()
                else:
                    await ctx.reply("Error when trying to clyde.")
                    await ses.close()


    @commands.command()
    async def captcha(self, ctx, member:discord.Member=None):
        if member == None:
            member = ctx.author
        async with aiohttp.ClientSession() as ses:
            async with ses.get(f"https://nekobot.xyz/api/imagegen?type=captcha&url={member.avatar_url}&username={member.name}") as f:
                if f.status in range(200, 299):
                    dat = await f.json()
                    img = dat['message']
                    em = discord.Embed(
                        title='Captcha!',
                        color = ctx.author.color
                    )
                    em.set_image(url=f'{img}')
                    await ctx.send(embed=em)
                    await ses.close()
                else:
                    await ctx.reply("Error when trying to captcha.")
                    await ses.close()

    @commands.command()
    async def blurpify(self, ctx, member:discord.Member=None):
        if member == None:
            member = ctx.author
        async with aiohttp.ClientSession() as ses:
            async with ses.get(f"https://nekobot.xyz/api/imagegen?type=blurpify&image={member.avatar_url}") as f:
                if f.status in range(200, 299):
                    dat = await f.json()
                    img = dat['message']
                    em = discord.Embed(
                        title='Blurpified!',
                        color = ctx.author.color
                    )
                    em.set_image(url=f'{img}')
                    await ctx.send(embed=em)
                    await ses.close()
                else:
                    await ctx.reply("Error when trying to blurpify.")
                    await ses.close()

    @commands.command(aliases=['fry'])
    async def deepfry(self, ctx, member:discord.Member=None):
        if member == None:
            member = ctx.author
        async with aiohttp.ClientSession() as ses:
            async with ses.get(f"https://nekobot.xyz/api/imagegen?type=deepfry&image={member.avatar_url}") as f:
                if f.status in range(200, 299):
                    dat = await f.json()
                    img = dat['message']
                    em = discord.Embed(
                        title='Deep Fryed!',
                        color = ctx.author.color
                    )
                    em.set_image(url=f'{img}')
                    await ctx.send(embed=em)
                    await ses.close()
                else:
                    await ctx.reply("Error when trying to deep fry.")
                    await ses.close()
    
    @commands.command()
    async def trap(self, ctx, member:discord.Member=None):
        if member == None:
            member = ctx.author
        async with aiohttp.ClientSession() as ses:
            async with ses.get(f"https://nekobot.xyz/api/imagegen?type=trap&name={member.name}&author={ctx.author.name}&image={member.avatar_url}") as f:
                if f.status in range(200, 299):
                    dat = await f.json()
                    img = dat['message']
                    em = discord.Embed(
                        title='Trapped!',
                        color = ctx.author.color
                    )
                    em.set_image(url=f'{img}')
                    await ctx.send(embed=em)
                    await ses.close()
                else:
                    await ctx.reply(f"Error when trying to trap {member.name}.")
                    await ses.close()


    @commands.command(aliases=['trumpt'])
    async def trumptweet(self, ctx, *, msg="No text entered"):
        async with aiohttp.ClientSession() as ses:
            async with ses.get(f"https://nekobot.xyz/api/imagegen?type=trumptweet&text={msg}") as f:
                if f.status in range(200, 299):
                    dat = await f.json()
                    img = dat['message']
                    em = discord.Embed(
                        title='Tweeted!',
                        color = ctx.author.color
                    )
                    em.set_image(url=f'{img}')
                    await ctx.send(embed=em)
                    await ses.close()
                else:
                    await ctx.reply("Error when trying to tweet.")
                    await ses.close()

    @commands.command(aliases=['www'])
    async def whowouldwin(self, ctx, member:discord.Member):
        async with aiohttp.ClientSession() as ses:
            async with ses.get(f"https://nekobot.xyz/api/imagegen?type=whowouldwin&user1={ctx.author.avatar_url}&user2={member.avatar_url}") as f:
                if f.status in range(200, 299):
                    dat = await f.json()
                    img = dat['message']
                    em = discord.Embed(
                        title='Who Would Win?',
                        color = ctx.author.color
                    )
                    em.set_image(url=f'{img}')
                    await ctx.send(embed=em)
                    await ses.close()
                else:
                    await ctx.reply("Error when trying to see who would win.")
                    await ses.close()

    @commands.command(aliases=['cmm'])
    async def changemymind(self, ctx, *, msg="No text entered"):
        async with aiohttp.ClientSession() as ses:
            async with ses.get(f"https://nekobot.xyz/api/imagegen?type=changemymind&text={msg}") as f:
                if f.status in range(200, 299):
                    dat = await f.json()
                    img = dat['message']
                    em = discord.Embed(
                        title='Done!',
                        color = ctx.author.color
                    )
                    em.set_image(url=f'{img}')
                    await ctx.send(embed=em)
                    await ses.close()
                else:
                    await ctx.reply("Error when trying to change my mind.")
                    await ses.close()

    @commands.command()
    async def kannagen(self, ctx, *, text = "No text entered"):
        async with aiohttp.ClientSession() as ses:
            async with ses.get(f"https://nekobot.xyz/api/imagegen?type=kannagen&text={text}") as f:
                if f.status in range(200, 299):
                    dat = await f.json()
                    img = dat['message']
                    em = discord.Embed(
                        title='Kannagened!',
                        color = ctx.author.color
                    )
                    em.set_image(url=f'{img}')
                    await ctx.send(embed=em)
                    await ses.close()
                else:
                    await ctx.reply("Error when trying to kannagen.")
                    await ses.close()

    @commands.command()
    async def km(self, ctx, member:discord.Member=None):
        if member == None:
            member = ctx.author
        async with aiohttp.ClientSession() as ses:
            async with ses.get(f"https://nekobot.xyz/api/imagegen?type=kms&url={member.avatar_url}") as f:
                if f.status in range(200, 299):
                    dat = await f.json()
                    img = dat['message']
                    em = discord.Embed(
                        title='Kmed!',
                        color = ctx.author.color
                    )
                    em.set_image(url=f'{img}')
                    await ctx.send(embed=em)
                    await ses.close()
                else:
                    await ctx.reply("Error when trying to km.")
                    await ses.close()

    @commands.command()
    async def awooify(self, ctx, member:discord.Member=None):
        if member == None:
            member = ctx.author
        async with aiohttp.ClientSession() as ses:
            async with ses.get(f"https://nekobot.xyz/api/imagegen?type=awooify&url={member.avatar_url}") as f:
                if f.status in range(200, 299):
                    dat = await f.json()
                    img = dat['message']
                    em = discord.Embed(
                        title='Awoofied!',
                        color = ctx.author.color
                    )
                    em.set_image(url=f'{img}')
                    await ctx.send(embed=em)
                    await ses.close()
                else:
                    await ctx.reply("Error when trying to awooify.")
                    await ses.close()

    @commands.command()
    async def kidnap(self, ctx, member:discord.Member):
        async with aiohttp.ClientSession() as ses:
            async with ses.get(f"https://nekobot.xyz/api/imagegen?type=kidnap&image={member.avatar_url}") as f:
                if f.status in range(200, 299):
                    dat = await f.json()
                    img = dat['message']
                    em = discord.Embed(
                        title='Kidnapped!',
                        color = ctx.author.color
                    )
                    em.set_image(url=f'{img}')
                    await ctx.send(embed=em)
                    await ses.close()
                else:
                    await ctx.reply(f"Error when trying to kidnap {member.name}.")
                    await ses.close()

    

    @commands.command()
    async def stickbug(self, ctx, member:discord.Member=None):
        if member == None:
            member = ctx.author
        async with aiohttp.ClientSession() as ses:
            async with ses.get(f"https://nekobot.xyz/api/imagegen?type=stickbug&url={member.avatar_url}") as f:
                if f.status in range(200, 299):
                    dat = await f.json()
                    img = dat['message']
                    em = discord.Embed(
                        title='Stuckbugged!',
                        color = ctx.author.color
                    )
                    em.set_image(url=f'{img}')
                    await ctx.send(embed=em)
                    await ses.close()
                else:
                    await ctx.reply("Error when trying to stickbug.")
                    await ses.close()

    @commands.command()
    async def food(self, ctx):
        async with aiohttp.ClientSession() as ses:
            async with ses.get(f"https://nekobot.xyz/api/image?type=food") as f:
                if f.status in range(200, 299):
                    dat = await f.json()
                    img = dat['message']
                    color = dat['color']
                    em = discord.Embed(
                        title='Food Photo!',
                        color = color
                    )
                    em.set_image(url=f'{img}')
                    await ctx.send(embed=em)
                    await ses.close()
                else:
                    await ctx.reply("Error when trying to find a food photo.")
                    await ses.close()


    @commands.command()
    async def coffee(self, ctx):
        async with aiohttp.ClientSession() as ses:
            async with ses.get(f"https://nekobot.xyz/api/image?type=coffee") as f:
                if f.status in range(200, 299):
                    dat = await f.json()
                    img = dat['message']
                    color = dat['color']
                    em = discord.Embed(
                        title='Coffee Photo!',
                        color = color
                    )
                    em.set_image(url=f'{img}')
                    await ctx.send(embed=em)
                    await ses.close()
                else:
                    await ctx.reply("Error when trying to find a coffee photo.")
                    await ses.close()

    @commands.command(aliases=['ytc', 'ytcomment'])
    async def youtubecomment(self, ctx, text = "No text entered."):
            
        async with aiohttp.ClientSession() as wastedSession:
            async with wastedSession.get(f'https://some-random-api.ml/canvas/youtube-comment?avatar={ctx.author.avatar_url_as(format="png", size=1024)}&username={ctx.author.display_name}&comment={text}') as wastedImage: # get users avatar as png with 1024 size
                imageData = io.BytesIO(await wastedImage.read()) # read the image/bytes
                
                await wastedSession.close() # closing the session and;
                
                await ctx.reply(file=discord.File(imageData, 'ytcomment.png')) # sending the file

def setup(client):
    client.add_cog(Images(client))

