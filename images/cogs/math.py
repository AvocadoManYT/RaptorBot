from asyncio import sleep
import discord
from discord.ext import commands
import random
import math

class Math(commands.Cog):
    """ Category for math commands """

    def __init__(self, client):
        self.client = client

    # events
    @commands.Cog.listener()
    async def on_ready(self):
        print('Math cog is ready.')

    # commands

    def madd(self, n: float, n2: float):
        return n + n2

    def msub(self, n: float, n2: float):
        return n - n2

    def mrando(self, n: int, n2: int):
        return random.randint(n, n2)

    def mdiv(self, n: float, n2: float):
        return n / n2
    

    def msqrt(self, n: float):
        return math.sqrt(n)

    def mmult(self, n: float, n2: float):
        return n * n2

    @commands.command()
    async def add(self, ctx, num1: float, num2: float):
        try:
            result = self.madd(num1, num2)
            await ctx.send(result)

        except:
            pass

    @commands.command(aliases=['sub'])
    async def subtract(self, ctx, num1: float, num2: float):
        try:
            result = self.msub(num1, num2)
            await ctx.send(result)

        except:
            pass

    @commands.command()
    async def rando(self, ctx, num1: int, num2: int):
        try:
            result = self.mrando(num1, num2)
            await ctx.send(result)

        except:
            pass

    @commands.command(aliases=['div'])
    async def division(self, ctx, num1: float, num2: float):
        try:
            result = self.mdiv(num1, num2)
            await ctx.send(result)

        except:
            pass

    @commands.command(aliases=['multi'])
    async def multiply(self, ctx, num1: float, num2: float):
        try:
            result = self.mmult(num1, num2)
            await ctx.send(result)

        except:
            pass

    @commands.command(aliases=['sqrt'])
    async def squareroot(self, ctx, num: float):
        try:
            result = self.msqrt(num)
            await ctx.send(result)

        except:
            pass



def setup(client):
    client.add_cog(Math(client))