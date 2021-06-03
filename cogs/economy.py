import discord
import json
import random
from discord.ext import commands

class Economy(commands.Cog):
    """ Category for ecomony commands """

    def __init__(self, client):
        self.client = client

    # events
    @commands.Cog.listener()
    async def on_ready(self):
        print('Economy cog is ready.')

    
    
    # commands
    @commands.command(aliases=['bal'])
    async def balance(self, ctx, member : discord.Member = None):
        if member is None:
            member = ctx.author
        await self.open_account(member)

        open_account = self.open_account
        update_bank = self.update_bank
        get_bank_data = self.get_bank_data

        user =  member

        users = await self.get_bank_data()

        wallet_amt = users[str(user.id)]["wallet"]

        bank_amt = users[str(user.id)]["bank"]

        net_worth = bank_amt + wallet_amt

        balance = discord.Embed(title = f"{member.name}'s balance" , color = discord.Colour.blue())
        balance.add_field(name = "Wallet Balance :dollar:", value = f"△ {wallet_amt}")
        balance.add_field(name = "Bank Balance :bank:", value = f"△ {bank_amt}", inline = False)
        balance.add_field(name = "Net Worth :moneybag:", value = f"△ {net_worth}", inline = False)
        balance.set_thumbnail(url = member.avatar_url)
        balance.set_footer(text = f"Requested By {ctx.author}", icon_url = ctx.author.avatar_url)
        await ctx.send(embed = balance)

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def beg(self, ctx):
        open_account = self.open_account
        update_bank = self.update_bank
        get_bank_data = self.get_bank_data
        
        await open_account(ctx.author)
        user = ctx.author
        users = await get_bank_data()

        
        earnings = random.randrange(2002)

        await ctx.send(f"Someone just gave you △ {earnings}!")
        
        
        users[str(user.id)]["wallet"] += earnings

        with open("mainbank.json", "w") as f:
            json.dump(users,f)

    @commands.command(aliases=['gamble'])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def bet(self, ctx, amount:int=None):
        open_account = self.open_account
        update_bank = self.update_bank
        get_bank_data = self.get_bank_data
        
        if amount == None:
            await ctx.send("Please enter an amount.")
            return

        bal = await update_bank(ctx.author)
        if amount == "max":
            amount = bal[1]

        if amount == "all":
            amount = bal[1]

        amount = int(amount)
        if amount>bal[1]:
            await ctx.send("Far out! You don't have that much money!")
            return
        
        if amount<0:
            await ctx.send("Amount must be positive. ;-;")
            return
        
        await open_account(ctx.author)
        user = ctx.author
        users = await get_bank_data()

        r = random.randint(1, 12)
        p = random.randint(1, 12)

        
        color = ctx.author.color
        f = ""
        
        if r > p:
            f = f"You won! You got △ {amount*2}"
            users[str(user.id)]["wallet"] += amount*2
            color = discord.Colour.green()
        else:
            f = f"I won! You lost △ {amount}."
            users[str(user.id)]["wallet"] -= amount
            color = discord.Colour.red()

        embed = discord.Embed(
            title = "Betted!",
            color = color
        )
        embed.add_field(name = "You rolled:", value = r)
        embed.add_field(name = "I rolled:", value = p, inline = True)
        embed.add_field(name = f, value = "GG", inline = False)
        
        

        await ctx.send(embed = embed )
        
        

        with open("mainbank.json", "w") as f:
            json.dump(users,f)


    @commands.command()
    @commands.cooldown(1, 35, commands.BucketType.user)
    async def work(self, ctx):
        open_account = self.open_account
        update_bank = self.update_bank
        get_bank_data = self.get_bank_data
        
        await open_account(ctx.author)
        user = ctx.author
        users = await get_bank_data()

        
        earnings = random.randrange(2000, 15000)

        work_pl = ['Target', 'Walmart', 'Costco', 'CVS', 'Amazon', 'Apple', 'Google', 'Intel', 'Sumsung']
        num = ['2','3','4','5']
        
        wr_hr = random.choice(num)


        await ctx.send(f"You worked at {random.choice(work_pl)} for {wr_hr} hours, earning △ {earnings}!")
        
        
        users[str(user.id)]["wallet"] += earnings

        with open("mainbank.json", "w") as f:
            json.dump(users,f)


    @commands.command(aliases=["i"], help="This let\'s me, as in the owner, add money to people.")
    @commands.is_owner()
    async def inject(self, ctx, coins:int=0, member:discord.Member=None):
        """ This let\'s me, as in the owner, add money to people. """
        if ctx.author.id == 801234598334955530:

            if coins == 0:
                await ctx.send("Please enter a number of coins to inject!")
                return
            elif coins < 0:
                await ctx.send("Number cannot be negative!")
                return
            elif coins > 99999:
                await ctx.send("Number too big lmao")
                return
            else:
                if member == None:
                    await self.update_bank(ctx.author,coins)
                    name = ctx.author.name
                else:
                    await self.update_bank(member,coins)
                    await ctx.send("Injection Complete")
        else:
            await ctx.send("You're not the owner or me :/")

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def search(self, ctx):
        open_account = self.open_account
        update_bank = self.update_bank
        get_bank_data = self.get_bank_data
        
        await open_account(ctx.author)
        user = ctx.author
        users = await get_bank_data()

        
        earnings = random.randrange(1502)
        place = ["the bank", "the shop", "Discord", "YouTube", "Twitter", "Instagram", "your dms", "my code", "the internet", "Google", "Bing", "Yahoo"]
        
        await ctx.send(f"You searched {random.choice(place)} and found △ {earnings}!")
        
        
        users[str(user.id)]["wallet"] += earnings

        with open("mainbank.json", "w") as f:
            json.dump(users,f)
        

    @commands.command(aliases=['with'])
    @commands.cooldown(1,5, commands.BucketType.user)
    async def withdraw(self, ctx, amount = None):
        open_account = self.open_account
        update_bank = self.update_bank
        
        await open_account(ctx.author)

        if amount == None:
            await ctx.send("Please enter an amount.")
            return

        bal = await update_bank(ctx.author)
        if amount == "max":
            amount = bal[1]

        amount = int(amount)
        if amount>bal[1]:
            await ctx.send("Far out! You don't have that much money!")
            return
        
        if amount<0:
            await ctx.send("Amount must be positive. ;-;")
            return

        await update_bank(ctx.author, amount)
        await update_bank(ctx.author, -1*amount, "bank")

        await ctx.send(f"You withdrew △ {amount}!")

    @commands.command(aliases=['dep'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def deposit(self, ctx, amount = None):
        open_account = self.open_account
        update_bank = self.update_bank
        
        await open_account(ctx.author)

        if amount == None:
            await ctx.send("Please enter an amount.")
            return

        bal = await update_bank(ctx.author)
        if amount == "max":
            amount = bal[0]

        amount = int(amount)
        if amount>bal[0]:
            await ctx.send("Far out! You don't have that much money!")
            return

        if amount<0:
            await ctx.send("Amount must be positive. ;-;")
            return

        await update_bank(ctx.author, -1*amount)
        await update_bank(ctx.author, amount, "bank")

        await ctx.send(f"You deposited △ {amount}!")

    @commands.command(aliases=['send'])
    async def share(self, ctx,member : discord.Member, amount = None):
        open_account = self.open_account
        update_bank = self.update_bank

        
        await open_account(ctx.author)
        await open_account(member)

        if amount == None:
            await ctx.send("Please enter an amount.")
            return

        bal = await update_bank(ctx.author)
        if amount == "max":
            amount = bal[1]

        amount = int(amount)
        if amount>bal[1]:
            await ctx.send("Far out! You don't have that much money!")
            return

        if amount<0:
            await ctx.send("Amount must be positive. ;-;")
            return

        await update_bank(ctx.author, -1*amount,"wallet")
        await update_bank(member, amount)

        await ctx.send(f"You gave △ {amount} to {member}!")

    
    @commands.command()
    @commands.cooldown(rate=1, per=15, type=commands.BucketType.user)
    async def slots(self, ctx, amount):
        """ Roll the slot machine """
        emojis = "🍎🍊🍐🍋🍉🍇🍓🍒"
        a = random.choice(emojis)
        b = random.choice(emojis)
        c = random.choice(emojis)

        open_account = self.open_account
        update_bank = self.update_bank
        get_bank_data = self.get_bank_data
        
        await open_account(ctx.author)

        if amount == None:
            await ctx.send("Please enter an amount.")
            return

        bal = await update_bank(ctx.author)
        if amount == "max":
            amount = 25000

        amount = int(amount)
        if amount>bal[0]:
            await ctx.send("Far out! You don't have that much money!")
            return

        if amount<0:
            await ctx.send("Amount must be positive. ;-;")
            return

        slotmachine = f"**[ {a} {b} {c} ]\n{ctx.author.name}**,"

        if (a == b == c):
            await ctx.send(f"{slotmachine} All matching, you won {amount*4}! 🎉")
            await update_bank(ctx.author, 4*amount)
        elif (a == b) or (a == c) or (b == c):
            await ctx.send(f"{slotmachine} 2 in a row, you won {amount*2}!🎉")
            await update_bank(ctx.author, 2*amount)
        else:
            await ctx.send(f"{slotmachine} No match, you lost {amount}. 😢")
            await update_bank(ctx.author, -1*amount)

    @commands.command()
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def dice(self, ctx, amount = None):
        open_account = self.open_account
        update_bank = self.update_bank
        get_bank_data = self.get_bank_data
        
        await open_account(ctx.author)

        if amount == None:
            await ctx.send("Please enter an amount.")
            return

        bal = await update_bank(ctx.author)
        if amount == "max":
            amount = 25000

        amount = int(amount)
        if amount>bal[0]:
            await ctx.send("Far out! You don't have that much money!")
            return

        if amount<0:
            await ctx.send("Amount must be positive. ;-;")
            return

        final = []
        for i in range(3):
            a = random.choice(["<:YellowDice:836717543095664660>", "<:RedDice:836718117375049728>", "<:BlueDice:836718117031772202>"])

            final.append(a)

        await ctx.send(str(final))

        if final[0] == final[1] or final[0] == final[2] or final[2] == final[1]:
            await update_bank(ctx.author, 2*amount)
            await ctx.send(f"You won △ {2*amount}")
        else:
            await update_bank(ctx.author, -1*amount)
            await ctx.send(f"You lost △ {amount}. Oof.")


    @commands.command()
    @commands.cooldown(1, 120, commands.BucketType.user)
    async def rob(self, ctx,member : discord.Member):
        await ctx.reply("**Sike. You think I'm gonna add a rob command after seeing what Dank Memer rob does to people? Nope**")

    async def open_account(self, user):
        with open("mainbank.json", "r") as f:
            
            users = await self.get_bank_data()

        if str(user.id) in users:
            return False
        else:
            users[str(user.id)] = {}
            users[str(user.id)]["wallet"] = 0
            users[str(user.id)]["bank"] = 0

            with open("mainbank.json", "w") as f:
                json.dump(users,f)
            return True

    mainshop = [{"name":"CellPhone","price":5000,"description":"Tools"},
                {"name":"Radar","price":10000,"description":"Tools"},
                {"name":"DinoCatcher","price":25000,"description":"Tools"},
                {"name":"DinoScouterRV","price":50000,"description":"Tools"},
                {"name":"BabyDinoEgg","price":75000,"description":"Eggs"},
                {"name":"SpinosaurusEgg","price":100000,"description":"Eggs"},
                {"name":"UltrasaurusEgg","price":250000,"description":"Eggs"},
                {"name":"Gigantosarus","price":500000,"description":"Eggs"},
                {"name":"TyranasaurusRexEgg","price":1000000,"description":"Eggs"},
                {"name":"VelociraptorEgg","price":2500000,"description":"Eggs"},
                {"name":"HolyRaptorEgg","price":5000000,"description":"Eggs"}]

    @commands.command()
    async def shop(self, ctx, item = None):
        if item == None:
            em = discord.Embed(title = "Shop", color = discord.Colour.blue())

            for item in self.mainshop:
                name = item["name"]
                price = item["price"]
                desc = item["description"]
                em.add_field(name = f"{name}", value = f"△ {price} | {desc}")
                

            await ctx.send(embed = em)
        elif item == item["name"]:
                for item in self.mainshop:
                    name = item["name"]
                    price = item["price"]
                    desc = item["description"]
                emItem = discord.embed(title = f"{name}", description = f"{price}", color = discord.Colour.blue())
                emItem.add_field(name = f"{desc}")

                await ctx.send(embed = emItem)



    @commands.command()
    async def buy(self, ctx, item, amount = 1):
        open_account = self.open_account
        update_bank = self.update_bank
        get_bank_data = self.get_bank_data
        
        await open_account(ctx.author)

        res = await self.buy_this(ctx.author,item,amount)

        if not res[0]:
            if res[1]==1:
                await ctx.send("That Object isn't there!")
                return
            if res[1]==2:
                await ctx.send(f"You don't have enough money in your wallet to buy {amount} {item}")
                return


        await ctx.send(f"You just bought {amount} {item}")


    @commands.command(aliases=['inv'])
    async def inventory(self, ctx, member:discord.Member=None):
        open_account = self.open_account
        update_bank = self.update_bank
        get_bank_data = self.get_bank_data
        
        if member == None:
            member = ctx.author
        await open_account(ctx.author)
        user = ctx.author
        users = await self.get_bank_data()

        try:
            bag = users[str(user.id)]["bag"]
        except:
            bag = []


        em = discord.Embed(title = "Inv", color = discord.Colour.blue())
        for item in bag:
            name = item["item"]
            amount = item["amount"]
            if amount!=0:
                em.add_field(name=name, value=amount)
        

        await ctx.send(embed = em)  
    

    async def buy_this(self, user,item_name,amount):
        open_account = self.open_account
        update_bank = self.update_bank
        get_bank_data = self.get_bank_data
        
        item_name = item_name.lower()
        name_ = None
        for item in self.mainshop:
            name = item["name"].lower()
            if name == item_name:
                name_ = name
                price = item["price"]
                break

        if name_ == None:
            return [False,1]

        cost = price*amount

        users = await get_bank_data()

        bal = await update_bank(user)

        if bal[0]<cost:
            return [False,2]


        try:
            index = 0
            t = None
            for thing in users[str(user.id)]["bag"]:
                n = thing["item"]
                if n == item_name:
                    old_amt = thing["amount"]
                    new_amt = old_amt + amount
                    users[str(user.id)]["bag"][index]["amount"] = new_amt
                    t = 1
                    break
                index+=1 
            if t == None:
                obj = {"item":item_name , "amount" : amount}
                users[str(user.id)]["bag"].append(obj)
        except:
            obj = {"item":item_name , "amount" : amount}
            users[str(user.id)]["bag"] = [obj]        

        with open("mainbank.json","w") as f:
            json.dump(users,f)

        await update_bank(user,cost*-1,"wallet")

        return [True,"Worked"] 

    @commands.command()
    async def sell(self, ctx,item,amount = 1):
        open_account = self.open_account
        update_bank = self.update_bank
        get_bank_data = self.get_bank_data
        
        await open_account(ctx.author)

        res = await self.sell_this(ctx.author,item,amount)

        if not res[0]:
            if res[1]==1:
                await ctx.send("That Object isn't there!")
                return
            if res[1]==2:
                await ctx.send(f"You don't have {amount} {item} in your bag.")
                return
            if res[1]==3:
                await ctx.send(f"You don't have {item} in your bag.")
                return

        await ctx.send(f"You just sold {amount} {item}.")

    @commands.command(aliases = ["lb"])
    async def leaderboard(self, ctx, x = 5):
        open_account = self.open_account
        update_bank = self.update_bank
        get_bank_data = self.get_bank_data
        
        users = await get_bank_data()
        leader_board = {}
        total = []
        for user in users:
            name = int(user)
            total_amount = users[user]["wallet"] + users[user]["bank"]
            leader_board[total_amount] = name
            total.append(total_amount)

        total = sorted(total,reverse=True)    

        try:
            em = discord.Embed(title = f"Top {x} Richest People" , description = "This is decided on the basis of raw money in the bank and wallet",color = discord.Color.dark_green())
            index = 1
            for amt in total:
                id_ = leader_board[amt]
                member = self.client.get_user(id_)
                name = member.name
                em.add_field(name = f"{index}. {name}" , value = f"{amt}",  inline = False)
                if index == x:
                    break
                else:
                    index += 1

            await ctx.send(embed = em)
        except:
            await ctx.send(f"{x} people havn\'t used my economy :\ ")

    async def sell_this(self, user,item_name,amount,price = None):
        item_name = item_name.lower()
        name_ = None
        for item in self.mainshop:
            name = item["name"].lower()
            if name == item_name:
                name_ = name
                if price==None:
                    price = 0.9* item["price"]
                break

        if name_ == None:
            return [False,1]

        cost = price*amount

        users = await self.get_bank_data()

        bal = await self.update_bank(user)


        try:
            index = 0
            t = None
            for thing in users[str(user.id)]["bag"]:
                n = thing["item"]
                if n == item_name:
                    old_amt = thing["amount"]
                    new_amt = old_amt - amount
                    if new_amt < 0:
                        return [False,2]
                    users[str(user.id)]["bag"][index]["amount"] = new_amt
                    t = 1
                    break
                index+=1 
            if t == None:
                return [False,3]
        except:
            return [False,3]    

        with open("mainbank.json","w") as f:
            json.dump(users,f)

        await self.update_bank(user,cost,"wallet")

        return [True,"Worked"]


    async def get_bank_data(self):
        with open("mainbank.json", "r") as f:
            users = json.load(f)
            
            return users

    async def update_bank(self, user,change = 0,mode = "wallet"):
        users = await self.get_bank_data()

        users[str(user.id)][mode] += change

        with open("mainbank.json", "w") as f:
                json.dump(users,f)
            
        bal = [users[str(user.id)]["wallet"],users[str(user.id)]["bank"]]
        return bal


def setup(client):
    client.add_cog(Economy(client))