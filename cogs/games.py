import discord
import random
import asyncio
from games import wumpas as wumpus, minesweeper
import requests
import html
import re
from discord.ext import commands
from random import randint


smoother = True
player1 = ""
player2 = ""
turn = ""
gameOver = True
active_games = {}
board = []
games = {}

winningConditions = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
]


class Board:
    def __init__(self, player1, player2):
        # Our board just needs to be a 3x3 grid. To keep formatting nice, each one is going to be a space to start
        self.board = [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]

        # Randomize who goes first when the board is created
        if random.SystemRandom().randint(0, 1):
            self.challengers = {"x": player1, "o": player2}
        else:
            self.challengers = {"x": player2, "o": player1}

        # X's always go first
        self.X_turn = True

    def full(self):
        # For this check we just need to see if there is a space anywhere, if there is then we're not full
        for row in self.board:
            if " " in row:
                return False
        return True

    def can_play(self, player):
        # Simple check to see if the player is the one that's up
        if self.X_turn:
            return player == self.challengers["x"]
        else:
            return player == self.challengers["o"]

    def update(self, x, y):
        # If it's x's turn, we place an x, otherwise place an o
        letter = "x" if self.X_turn else "o"
        # Make sure the place we're trying to update is blank, we can't override something
        if self.board[x][y] == " ":
            self.board[x][y] = letter
        else:
            return False
        # If we were succesful in placing the piece, we need to switch whose turn it is
        self.X_turn = not self.X_turn
        return True

    def check(self):
        # Checking all possiblities will be fun...
        # First base off the top-left corner, see if any possiblities with that match
        # We need to also make sure that the place is not blank, so that 3 in a row that are blank doesn't cause a 'win'
        # Top-left, top-middle, top right
        if (
            self.board[0][0] == self.board[0][1]
            and self.board[0][0] == self.board[0][2]
            and self.board[0][0] != " "
        ):
            return self.challengers[self.board[0][0]]
        # Top-left, middle-left, bottom-left
        if (
            self.board[0][0] == self.board[1][0]
            and self.board[0][0] == self.board[2][0]
            and self.board[0][0] != " "
        ):
            return self.challengers[self.board[0][0]]
        # Top-left, middle, bottom-right
        if (
            self.board[0][0] == self.board[1][1]
            and self.board[0][0] == self.board[2][2]
            and self.board[0][0] != " "
        ):
            return self.challengers[self.board[0][0]]

        # Next check the top-right corner, not re-checking the last possiblity that included it
        # Top-right, middle-right, bottom-right
        if (
            self.board[0][2] == self.board[1][2]
            and self.board[0][2] == self.board[2][2]
            and self.board[0][2] != " "
        ):
            return self.challengers[self.board[0][2]]
        # Top-right, middle, bottom-left
        if (
            self.board[0][2] == self.board[1][1]
            and self.board[0][2] == self.board[2][0]
            and self.board[0][2] != " "
        ):
            return self.challengers[self.board[0][2]]

        # Next up, bottom-right corner, only one possiblity to check here, other two have been checked
        # Bottom-right, bottom-middle, bottom-left
        if (
            self.board[2][2] == self.board[2][1]
            and self.board[2][2] == self.board[2][0]
            and self.board[2][2] != " "
        ):
            return self.challengers[self.board[2][2]]

        # No need to check the bottom-left, all posiblities have been checked now
        # Base things off the middle now, as we only need the two 'middle' possiblites that aren't diagonal
        # Top-middle, middle, bottom-middle
        if (
            self.board[1][1] == self.board[0][1]
            and self.board[1][1] == self.board[2][1]
            and self.board[1][1] != " "
        ):
            return self.challengers[self.board[1][1]]
        # Left-middle, middle, right-middle
        if (
            self.board[1][1] == self.board[1][0]
            and self.board[1][1] == self.board[1][2]
            and self.board[1][1] != " "
        ):
            return self.challengers[self.board[1][1]]

        # Otherwise nothing has been found, return None
        return None

    def __str__(self):
        # Simple formatting here when you look at it, enough spaces to even out where everything is
        # Place whatever is at the grid in place, whether it's x, o, or blank
        _board = " {}  |  {}  |  {}\n".format(
            self.board[0][0], self.board[0][1], self.board[0][2]
        )
        _board += "———————————————\n"
        _board += " {}  |  {}  |  {}\n".format(
            self.board[1][0], self.board[1][1], self.board[1][2]
        )
        _board += "———————————————\n"
        _board += " {}  |  {}  |  {}\n".format(
            self.board[2][0], self.board[2][1], self.board[2][2]
        )
        return "```\n{}```".format(_board)


class Games(commands.Cog):
    """ Category for game commands """
    def get_embed(self, _title, _description, _color):
        return discord.Embed(title=_title, description=_description, color=_color)
    
    def __init__(self, client):
        self.client = client
        self.bot = client
        self.ttt_games = {}

    
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Games are loaded")

    
    # events
    global i
    i = 0

   

    @commands.command(aliases=['russianr', 'roulette'])
    async def russianroulette(self, ctx):
        user = ctx.message.author.mention
        global i
        chance = 6 - i
        num = random.randint(1, chance)

        if i == 0:
            embed=discord.Embed(description="Reloads Revolver...", color=ctx.author.color)
            await ctx.send(embed=embed)
            await asyncio.sleep(2)
            embed=discord.Embed(description="Spins Chamber...", color=ctx.author.color)
            await ctx.send(embed=embed)
        else:
            embed=discord.Embed(description="Already Loaded...",    color=ctx.author.color)
            await ctx.send(embed=embed)

        await asyncio.sleep(2)
        embed=discord.Embed(description="Pulls Trigger...",     color=ctx.author.color)
        await ctx.send(embed=embed)
        await asyncio.sleep(2)

        if num == 1:
            embed=discord.Embed(description="Revolver Fires!  🔥🔫", color=16711680)
            await ctx.send(embed=embed)
            await asyncio.sleep(2)
            embed=discord.Embed(description="You Died " + user + "! ⚰️", color=16711680)
            await ctx.send(embed=embed)
            i = 0
        else:
            embed=discord.Embed(description="Revolver Clicks!  🔫", color=65280)
            await ctx.send(embed=embed)
            await asyncio.sleep(2)
            embed=discord.Embed(description="You Survived " + user + "! 😀", color=65280)
            await ctx.send(embed=embed)
            i += 1


    @commands.command(aliases=['gletter', 'guessl', 'gl'])
    async def guessletter(self, ctx, amount_of_lives:int=10):
        lives = 0
        letter = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        if amount_of_lives > 20:
            return await ctx.send("Amount of lives has to be less than 20!")
        if amount_of_lives < 5:
            def check(m):
                return m.author == ctx.author and m.channel == ctx.channel
            await ctx.send("Are you sure that you want less than 5 tries? Even the developer takes like 10 to 15 tries. (y/n)")
            try:
                messge = await self.client.wait_for("message", check=check, timeout=30)
                if messge.content=="y":
                    await ctx.send("Ok then... your choice")
                    lives = amount_of_lives
                    
                else:
                    return await ctx.send("Thank you for understanding :)")
            except asyncio.TimeoutError:
                return await ctx.send("Timeout...try again")
        else:
            lives = amount_of_lives
        await ctx.send("I'm thinking of a letter. Try to guess it!")
        number=random.choice(letter)
        print(number)
        await ctx.send("Enter the guess as a lowercase ex: `s`")
        await ctx.send(f"You only have `{lives}` guesses!")
        await ctx.send("Also: You only have `30` seconds to guess so answer quickly!")
        

        while lives !=-1:

            if lives==0:
                lives=lives-1
                await ctx.send(f"Game Over!!! The letter was `{number}`")
                break

            def checka(m):
                return m.author == ctx.author
            try:
                guess=await self.client.wait_for("message",timeout=30, check = checka)
            except asyncio.TimeoutError:
                await ctx.send("Timeout")

            if not guess.author.bot:
                if guess.content!=number:
                    lives=lives-1
                    await ctx.send(f"Your guess is **NOT RIGHT** , you have `{lives}` attempts left")
                else:
                    await ctx.send("Your guess is ***Correct*** :exploding_head: :exploding_head: :exploding_head: ")
                    break
        
    @commands.command(aliases=['fi'])
    async def findimposter(self, ctx):
        """Impostors can sabotage the reactor, 
        which gives Crewmates 30–45 seconds to resolve the sabotage. 
        If it is not resolved in the allotted time, The Impostor(s) will win."""


        # determining
        embed1 = discord.Embed(title = "Who's the imposter?" , description = "Find out who the imposter is, before the reactor breaks down!" , color=000000)
        
        # fields
        embed1.add_field(name = 'Purple' , value= ' <:AmongUsPurple:838846127691661316>' , inline=False)
        embed1.add_field(name = 'Yellow' , value= '<:AmongUsYellow:838846127565438976>' , inline=False)
        embed1.add_field(name = 'Cyan' , value= '<:AmongUsCyan:838846127667281960>' , inline=False)
        embed1.add_field(name = 'White' , value= '<:AmongUsWhite:838846127830204476>' , inline=False)
        
        # sending the message
        msg = await ctx.send(embed=embed1)
        
        # emojis
        emojis = {
            'purple': '<:AmongUsPurple:838846127691661316>',
            'yellow': '<:AmongUsYellow:838846127565438976>',
            'cyan': '<:AmongUsCyan:838846127667281960>',
            'white': '<:AmongUsWhite:838846127830204476>'
        }
        
        # who is the imposter?
        imposter = random.choice(list(emojis.items()))
        imposter = imposter[0]
        
        # for testing...
        
        # adding choices
        for emoji in emojis.values():
            await msg.add_reaction(emoji)
        
        # a simple check, whether reacted emoji is in given choises.
        def check(reaction, user):
            self.reacted = reaction.emoji
            return user == ctx.author and str(reaction.emoji) in emojis.values()

        # waiting for the reaction to proceed
        try: 
            reaction, user = await self.bot.wait_for('reaction_add', timeout=30.0, check=check)
        
        except TimeoutError:
            # reactor meltdown - defeat
            description = "Reactor Meltdown.{0} was the imposter...".format(imposter)
            embed = self.get_embed("Defeat", description, discord.Color.red())
            await ctx.send(embed=embed)
        else:
            # victory
            if str(self.reacted) == emojis[imposter]:
                description = "**{0}** was the imposter!".format(imposter)
                embed = self.get_embed("Victory", description, discord.Color.blue())
                await ctx.send(embed=embed)

            # defeat
            else:
                for key, value in emojis.items(): 
                    if value == str(self.reacted):
                        description = f"**{key}** was not the imposter...**{imposter}** was."
                        embed = self.get_embed("Defeat", description, discord.Color.red())
                        await ctx.send(embed=embed)
                        break

    @commands.command(name='survival')
    async def _wumpus(self, ctx):
        """Play a survival game, try to find the dragon without dying!"""
        await wumpus.play(self.client, ctx)

    @commands.command(name='minesweeper', aliases=['ms'])
    async def _minesweeper(self, ctx, columns = None, rows = None, bombs = None):
        """Play Minesweeper"""
        await minesweeper.play(ctx, columns, rows, bombs)



    @commands.command(name="guessnunber", aliases=['guessn', 'gnumber', 'gn'])
    async def guess(self,ctx, num1:int=1, num2:int=30):
        lives=3
        number=randint(num1,num2)
        await ctx.send(f"Guess the number from `{num1} to {num2}` :zany_face:")
        await ctx.send("Enter the guess only ex: `1`")
        await ctx.send("Also: You only have `30` seconds to guess so answer quickly!")

        while lives !=-1:

            if lives==0:
                lives=lives-1
                await ctx.send(f"Game Over!!! The number was {number}")
                break

            def check(m):
                return m.author == ctx.author
            try:
                guess=await self.client.wait_for("message",timeout=30, check = check)
            except asyncio.TimeoutError:
                await ctx.send("Timeout")

            if int(guess.content)>number:
                lives=lives-1
                await ctx.send(f"Your guess is **TOO BIG** , you have `{lives}` attempts left")
            elif int(guess.content)<number:
                lives=lives-1
                await ctx.send(f"Your guess is **TOO SMALL** ,  you have `{lives}` attempts left")
            elif int(guess.content)==number:
                await ctx.send("Your guess is ***Correct*** :exploding_head: :exploding_head: :exploding_head: ")
                break

    @commands.command(aliases=['coin', 'flip'])
    async def coinflip(self, ctx):
        side = ['heads', 'talis']
        ran = random.choice(side)

        await ctx.send(f" <:Coin:841814443997921350> I choose {ran}.")

    @commands.command(aliases=['rps'])
    async def rockpaperscissors(self, ctx):

      buttons=["🪨", "🧾", "✂️"]
      embed=discord.Embed(title="Rock Paper Scissors!", description="Choose `Rock`, `Paper` Or `Scissors` For Your Answer!", color=ctx.author.color)
      embed.set_footer(text="Command Requested By {}".format(ctx.message.author.name), icon_url=ctx.message.author.avatar_url)
      sent=await ctx.send(embed=embed)

      for button in buttons:
         await sent.add_reaction(button)

      while True:
        try:
            reaction, user = await self.client.wait_for("reaction_add", check=lambda reaction, user: user == ctx.author and reaction.emoji in buttons, timeout=30.0)

        except asyncio.TimeoutError:
            await sent.delete()
            break

        else:
          bot_rps="rps"
          rps_random=random.choice(bot_rps)
          
          if rps_random == "r":
            if reaction.emoji == "🪨":
              embed=discord.Embed(title="It's A Tie!", description="Both Players Chose Rock! It's A Tie!", color=16776960)
              await ctx.send(embed=embed)
              break
            
            elif reaction.emoji == "🧾":
              embed=discord.Embed(title="You Win!", description="You Chose Paper & I Chose Rock! You Win!", color=65280)
              await ctx.send(embed=embed)
              break
            
            elif reaction.emoji == "✂️":
              embed=discord.Embed(title="You Lose!", description="You Chose Scissors & I Chose Rock", color=16711680)
              await ctx.send(embed=embed)
              break
          
          elif rps_random == "p":
            if reaction.emoji == "🪨":
              embed=discord.Embed(title="You Lose!", description="You Chose Rock & I Chose Paper! You Lose!", color=16711680)
              await ctx.send(embed=embed)
              break
            
            elif reaction.emoji == "🧾":
              embed=discord.Embed(title="It's A Tie!", description="Both Players Chose Paper! It's A Tie!", color=16776960)
              await ctx.send(embed=embed)
              break
            
            elif reaction.emoji == "✂️":
              embed=discord.Embed(title="You Win!", description="You Chose Scissors & I Chose Paper! You Win!", color=65280)
              await ctx.send(embed=embed)
              break
          
          elif rps_random == "s":
            if reaction.emoji == "🪨":
              embed=discord.Embed(title="You Win!", description="You Chose Rock & I Chose Scissors! You Win!", color=65280)
              await ctx.send(embed=embed)
              break
            
            elif reaction.emoji == "🧾":
              embed=discord.Embed(title="You Lose!", description="You Chose Paper & I Chose Scissors! You Lose!", color=16711680)
              await ctx.send(embed=embed)
              break
            
            elif reaction.emoji == "✂️":
              embed=discord.Embed(title="It's A Tie!", description="Both Players Chose Scissors! It's A Tie!", color=16776960)
              await ctx.send(embed=embed)
              break

    
    

    

    @commands.command(name='chess')
    async def chess(self, ctx: commands.Context,opponent=""):
        #-------------- Help section ------------------#
        if(opponent=="" or opponent.find('help')!=-1):
            em = discord.Embed()
            em.title = f'Usage: rap chess opponent'
            em.description = f'Challenges opponent to a game of chess. The Opponent should be @mentoned to start\nOpponent will make the first move, and thus be controlling the white pieces.'
            em.add_field(name="Example", value="rap chess @Username", inline=False)
            em.color = 0x22BBFF
            await ctx.send(embed=em)
            return
        #----------------------------------------------#
        # Remove challenge message
        await ctx.channel.delete_messages(await self.getMessages(ctx,1))
        # Game init
        pawnwhite = "♙" 
        knightwhite = "♞"
        bishopwhite = "♝"
        rookwhite = "♜"
        queenwhite = "♛"
        kingwhite = "♚"
        whitepieces = (pawnwhite,knightwhite,bishopwhite,rookwhite,queenwhite,kingwhite)
        pawnblack = "♟︎"
        knightblack = "♘"
        bishopblack = "♗"
        rookblack = "♖"
        queenblack = "♕"
        kingblack = "♔"
        blackpieces = (pawnblack,knightblack,bishopblack,rookblack,queenblack,kingblack)
        space = " "

        board = [[rookwhite,knightwhite,bishopwhite,queenwhite,kingwhite,bishopwhite,knightwhite,rookwhite],
                 [pawnwhite,pawnwhite,pawnwhite,pawnwhite,pawnwhite,pawnwhite,pawnwhite,pawnwhite],
                 ['','','','','','','',''],
                 ['','','','','','','',''],
                 ['','','','','','','',''],
                 ['','','','','','','',''],
                 [pawnblack,pawnblack,pawnblack,pawnblack,pawnblack,pawnblack,pawnblack,pawnblack],
                 [rookblack,knightblack,bishopblack,queenblack,kingblack,bishopblack,knightblack,rookblack],
        ]

        # Game variables
        player1 = ctx.message.mentions[0].name
        player2 = ctx.message.author.name
        currentPlayer = player1
        otherPlayer = player2
        player1badInput = 0
        player2badInput = 0
        currentPlayerId=1
        prevMove = ""
        turn = 0
        #Castling check
        castlingDict = {
            "isWhiteKingMove": False,
            "isWhiteRookMoveL": False,
            "isWhiteRookMoveR": False,
            "isBlackKingMove": False,
            "isBlackRookMoveL": False,
            "isBlackRookMoveR": False,
        }
        
        #Bunch of helper functions
        def etDisplay(self):
            toDisplay = ""
            for y in range(0,8):
                toDisplay+=(f'{y+1} |')
                for x in range(8):
                    if(board[y][x]==''):
                        toDisplay+=space+'|'
                    else:
                        toDisplay+=board[y][x]+'|'
                toDisplay+='\n'
            toDisplay+="  A | B | C | D | E | F | G | H |"
            return(toDisplay)

        def parseMove(msg: str):
            msg = msg.lower()
            try:
                if (msg[0].isalpha() and msg[1].isdigit()):
                    x = ord(msg[0])-97
                    y = int(msg[1])-1
                    if(x < 8 and y < 8 and x >= 0 and y >= 0):
                        return ((y,x))
                else:
                    raise ValueError
            except:
                pass
            return ((None,None))

        def validateMove(src: tuple, dst: tuple, castlingDict: dict):
            piece = board[src[0]][src[1]]
            dx = dst[1]-src[1]
            dy = dst[0]-src[0]
            #check if the shape/direction of travel is valid
            if(piece == pawnwhite):
                if(dx==0):
                    if(dy==1): #can move down 1 if spot above is empty
                        return (board[dst[0]][dst[1]]=="" and not inCheck(src,dst))
                    elif(dy==2): #double move if space between is empty and destination is empty
                        return(emptySpaceBetween(src,dst) and board[dst[0]][dst[1]]=="" and not inCheck(src,dst))
                    return False
                #if moving diagonally
                elif(abs(dx)==1 and dy==1):
                    #en passant at right spot, to an empty space, and passing an opponent pawn
                    if(dst[0]==5 and board[dst[0]][dst[1]]=="" and board[dst[0]-1][dst[1]]==pawnblack):
                        #check if pervious move before was a double move
                        prevMoveCoordsSrc = parseMove(prevMove.split(" ")[0])
                        prevMoveCoordsDst = parseMove(prevMove.split(" ")[1])
                        #if x move is 0, y move is 2, and prevMoveCoordsDst x is dst x 
                        if(abs(prevMoveCoordsSrc[0]-prevMoveCoordsDst[0])==2 and prevMoveCoordsSrc[1]-prevMoveCoordsDst[1]==0 and prevMoveCoordsDst[1] == dst[1] and not inCheck(src,dst)):
                            board[prevMoveCoordsDst[0]][prevMoveCoordsDst[1]] = ""
                            return True
                        return False
                    return (isOpponentPiece(src,dst) and not inCheck(src,dst))
                return False

            elif(piece == pawnblack):
                if(dx==0):
                    if(dy==-1): #can move up 1 if spot above is empty
                        return (board[dst[0]][dst[1]]=="" and not inCheck(src,dst))
                    elif(dy==-2): #double move if space between is empty and destination is empty
                        return(emptySpaceBetween(src,dst) and board[dst[0]][dst[1]]=="" and not inCheck(src,dst))
                    return False
                #if moving diagonally
                elif(abs(dx)==1 and dy==-1):
                    #en passant at right spot, to an empty space, and passing an opponent pawn
                    if(dst[0]==2 and board[dst[0]][dst[1]]=="" and board[dst[0]+1][dst[1]]==pawnwhite):
                        #check if pervious move before was a double move
                        prevMoveCoordsSrc = parseMove(prevMove.split(" ")[0])
                        prevMoveCoordsDst = parseMove(prevMove.split(" ")[1])
                        #if x move is 0, y move is 2, and prevMoveCoordsDst x is dst x 
                        if (abs(prevMoveCoordsSrc[0]-prevMoveCoordsDst[0])==2 and prevMoveCoordsSrc[1]-prevMoveCoordsDst[1]==0 and prevMoveCoordsDst[1] == dst[1] and not inCheck(src,dst)):
                            board[prevMoveCoordsDst[0]][prevMoveCoordsDst[1]] = ""
                            return True
                        return False
                    return(isOpponentPiece(src,dst) and not inCheck(src,dst))
                return False

            elif(piece == rookwhite or piece == rookblack):
                if((dy==0 and dx!=0) or (dy!=0 and dx==0)):
                    if(emptySpaceBetween(src,dst) and (board[dst[0]][dst[1]]=="" or isOpponentPiece(src,dst)) and not inCheck(src,dst)):
                        if(src[0]==0 and src[1]==0):
                            castlingDict["isWhiteRookMoveL"] = True
                        elif(src[0]==0 and src[1]==7):
                            castlingDict["isWhiteRookMoveR"] = True
                        elif(src[0]==7 and src[1]==0):
                            castlingDict["isBlackRookMoveL"] = True
                        elif(src[0]==7 and src[1]==7):
                            castlingDict["isBlackRookMoveR"] = True
                        return True
                    return False

            elif(piece == knightblack or piece == knightwhite):
                return (
                        (   #L-moves
                            (abs(dy)==1 and abs(dx)==2) 
                            or 
                            (abs(dy)==2 and abs(dx)==1)
                        ) 
                        and #destination is a capture or empty
                        (   board[dst[0]][dst[1]]=="" or isOpponentPiece(src,dst)  )
                        and
                            not inCheck(src,dst)
                       )

            elif(piece == bishopwhite or piece == bishopblack):
                if(abs(dy)==abs(dx)):
                    return(emptySpaceBetween(src,dst) and (board[dst[0]][dst[1]]=="" or isOpponentPiece(src,dst)) and not inCheck(src,dst))
                return False

            elif(piece == queenblack or piece == queenwhite):
                if( (dy==0 and dx!=0) or #horizontal
                    (dy!=0 and dx==0) or #vertucak
                    (abs(dy)==abs(dx))): #diagonal
                    return(emptySpaceBetween(src,dst) and (board[dst[0]][dst[1]]=="" or isOpponentPiece(src,dst)) and not inCheck(src,dst))
                return False

            elif(piece == kingblack or piece == kingwhite):
                if(abs(dx)<=1 and abs(dy)<=1 and not inCheck(src,dst)):
                    if(src[0]==7 and src[1] == 4):
                        castlingDict["isBlackKingMove"] = True
                    elif(src[0]==0 and src[1] == 4):
                        castlingDict["isWhiteKingMove"] = True
                    return (board[dst[0]][dst[1]]=="" or isOpponentPiece(src,dst) and not inCheck(src,dst))
                elif(abs(dx)>1 and dy==0 and not inCheck(src,dst)):
                    #possible castling
                    #move the rook as well since we are only moving the king
                    if(src[0]==0 and src[1]==4 and dx==-3 and not castlingDict["isWhiteRookMoveL"] and not castlingDict["isWhiteKingMove"] and board[0][0]==rookwhite):
                        board[0][0] = ""
                        board[0][2] = rookwhite
                        return True
                    elif (src[0]==0 and src[1]==4 and dx==2 and not castlingDict["isWhiteRookMoveR"] and not castlingDict["isWhiteKingMove"] and board[0][7]==rookwhite):
                        board[0][7] = ""
                        board[0][5] = rookwhite
                        return True
                    elif(src[0]==7 and src[1]==4 and dx==-3 and not castlingDict["isBlackRookMoveL"] and not castlingDict["isBlackKingMove"] and board[7][0]==rookblack):
                        board[7][0] = ""
                        board[7][2] = rookblack
                        return True
                    elif(src[0]==7 and src[1]==4 and dx==2 and not castlingDict["isBlackRookMoveR"] and not castlingDict["isBlackKingMove"] and board[7][7]==rookblack):
                        board[7][7] = ""
                        board[7][5] = rookblack
                        return True
                    return False

        def emptySpaceBetween(src: tuple, dst: tuple):
            dx = dst[1]-src[1]
            dy = dst[0]-src[0]
            dxDir = 1 if (dx > 0) else -1
            dyDir = 1 if (dy > 0) else -1
            if(dy==0 and dx != 0):
                #move from source x to destination x, ignoring itself (hence the src[1] +- 1)
                for x in range(src[1]+dxDir,dst[1],dxDir):
                    if(board[src[0]][x] != ""): 
                        return False #if piece between src and dst, return false
                return True
            elif(dx==0 and dy != 0):
                #move from source x to destination x, ignoring itself (hence the src[1] +- 1)
                for y in range(src[0]+dyDir,dst[0],dyDir):
                    if(board[y][src[1]] != ""): 
                        return False #if piece between src and dst, return false
                return True
            elif(abs(dy)==abs(dx)):
                for i in range (1,abs(dx)):
                    if(board[src[0]+i*dyDir][src[1]+i*dxDir] != ""):
                        return False
                return True
            return False

        def isOpponentPiece(src: tuple, dst: tuple):
            if(board[src[0]][src[1]] in whitepieces):
                return (board[dst[0]][dst[1]] in blackpieces)
            elif (board[src[0]][src[1]] in blackpieces):
                return (board[dst[0]][dst[1]] in whitepieces)
            return False

        def movePiece(msg: str):
            src = parseMove(msg.split(" ")[0])
            dst = parseMove(msg.split(" ")[1])
            board[dst[0]][dst[1]] = board[src[0]][src[1]]
            board[src[0]][src[1]] = ""

        def checkPlayerMove(msg: str, castlingDict: dict):
            coords = msg.split(" ")
            if(len(coords) != 2):
                return "Please give 2 coordinates separated by spaces. Ex: a2 a4"
            src = parseMove(coords[0])
            dst = parseMove(coords[1])
            if(src[0]==None):
                return "The first coordinate entered is in an invalid format (a-h)(1-8). Ex: A5 or a5"
            if(dst[0]==None):
                return "The second coordinate entered is in an invalid format (a-h)(1-8). Ex: A5 or a5"
            if((currentPlayerId == 2 and board[src[0]][src[1]] in whitepieces) or (currentPlayerId == 1 and board[src[0]][src[1]] in blackpieces)):
                return "You can not move your opponent's pieces"
            if(validateMove(src,dst,castlingDict)):
                return f"Turn {turn}: {currentPlayer} moved from {coords[0].upper()} to {coords[1].upper()}\n{otherPlayer}, Type two coordinates to move"
            if(board[src[0]][src[1]] == ""):
                return ("You did not select a valid piece")
            return "That piece can not move there"
       
        def inCheck(src: tuple, dst: tuple, player=None):
            if(player==None): #check player dependinbg on src piece
                pass
            elif (player == player1): #if player is defined, check if white is in check
                pass
            elif (player == player2): #if player is defined, check if black is in check
                pass
            return False #placeholder
        ### Send Message
        boardMessage = None #the message so that it can be deleted and altered when a move is made
        # Create Message
        em = discord.Embed()
        em.title = f'{player2} challenged {player1} to a game of chess'
        em.description = f"{self.etDisplay()}"
        em.color = 0x444444
        em.add_field(name=f"{player1}", value=f"Type two coordinates (piece -> destination), or type 'decline' to refuse\nYou are playing white", inline=False)
        em.add_field(name="Example", value="a2 a3", inline=False)
        await ctx.send(embed=em)
        # Add message to edit later
        async for x in ctx.channel.history(limit = 1):
            boardMessage = x

        for x in range(4):
            try:
                em = discord.Embed()
                em.title = f'{player2} challenged {player1} to a game of chess'
                msg = await self.client.wait_for('message',check=lambda message: message.author.name == player1, timeout=30)
                if(msg.content=='decline'):
                    em.description = f"{self.etDisplay()}"
                    em.add_field(name=f"{player1}", value="Challenge refused", inline=False)
                    await boardMessage.edit(embed=em)
                    return
                gameMsg = checkPlayerMove(msg.content,castlingDict)
                if(gameMsg[0:4]!="Turn"):
                    player1badInput+=1
                    em.description = f"{self.etDisplay()}"
                    em.color = 0xFF0000
                    em.add_field(name="Error", value=f"{gameMsg}", inline=False)
                    await boardMessage.edit(embed=em)
                    continue
                await ctx.channel.delete_messages(await self.getMessages(ctx,1))
                turn += 1
                movePiece(msg.content)
                em.color = 0x00FF00
                em.description = f"{self.etDisplay()}"
                em.add_field(name=f"{otherPlayer}'s turn:", value=f"{gameMsg}", inline=False)
                await boardMessage.edit(embed=em)
                gameLoop = True
                currentPlayer,otherPlayer = otherPlayer,currentPlayer
                currentPlayerId = 2 if (currentPlayerId == 1) else 1
                player1badInput = 0
                prevMove = msg.content
                break;
            except asyncio.exceptions.TimeoutError:
                em.description = f"{self.etDisplay()}"
                em.color = 0xFF0000
                em.add_field(name=f"{player1}", value="Game timed out", inline=False)
                await boardMessage.edit(embed=em)
                return
            if(player1badInput==3):
                em.description = f"{self.etDisplay()}"
                em.color = 0xFF0000
                em.add_field(name=f"{player1}", value="Did not enter a valid move in 3 tries. Game ended.", inline=False)
                await boardMessage.edit(embed=em)
                return
        #Main game loop
        while gameLoop:
            try:
                em = discord.Embed()
                em.title = f'Chess match between {player2} and {player1}'
                em.add_field(name="Moves:", value=f"Type the 2 coordinates for the piece you want to move and the spot to move to, or type 'quit' to stop the game.", inline=False)
                msg = await self.client.wait_for('message',check=lambda message: message.author.name == currentPlayer, timeout=30)
                gameMsg = checkPlayerMove(msg.content,castlingDict)
                if(msg.content[0:4]=="quit"):
                    em.color = 0x770000
                    em.description = f"{self.etDisplay()}"
                    em.add_field(name=f"{currentPlayer} Quits", value=f"{otherPlayer} wins!", inline=False)
                    await boardMessage.edit(embed=em)
                    return
                elif(gameMsg == "That piece can not move there"):
                    coords = msg.content.split(" ")
                    if(inCheck(parseMove(coords[0]),parseMove(coords[1]))):
                        em.color = 0xFF0000
                        em.description = f"{self.etDisplay()}"
                        em.add_field(name="Error", value=f"Can not move into check", inline=False)
                    else:
                        em.color = 0x770000
                        em.description = f"{self.etDisplay()}"
                        em.add_field(name="Invalid Move", value=f"{gameMsg}", inline=False)
                    await boardMessage.edit(embed=em)
                    continue
                elif(gameMsg[0:4]!="Turn"):
                    if(currentPlayer == player1):
                        player1badInput+=1
                    else:
                        player2badInput+=1
                    em.color = 0x770000
                    em.description = f"{self.etDisplay()}"
                    em.add_field(name="Invalid Move", value=f"{gameMsg}", inline=False)
                    await boardMessage.edit(embed=em)
                    continue
                await ctx.channel.delete_messages(await self.getMessages(ctx,1))
                turn += 1
                movePiece(msg.content)
                em.description = f"{self.etDisplay()}"
                em.color = 0x00FF00
                em.add_field(name=f"{otherPlayer}'s turn:", value=f"{gameMsg}", inline=False)
                if(currentPlayerId == 1):
                    player1badInput = 0
                elif(currentPlayerId == 2):
                    player2badInput = 0
                currentPlayer,otherPlayer = otherPlayer,currentPlayer
                currentPlayerId = 2 if (currentPlayerId == 1) else 1
                prevMove = msg.content
                await boardMessage.edit(embed=em)
            except asyncio.exceptions.TimeoutError:
                em.description = f"{self.etDisplay()}"
                em.color = 0x770000
                em.add_field(name=f"{currentPlayer} Forfeit", value="Didn't make a move within 30 seconds", inline=False)
                await boardMessage.edit(embed=em)
                return
            if(player1badInput==3):
                em.description = f"{self.etDisplay()}"
                em.color = 0x770000
                em.add_field(name=f"{player1} Forfeit", value="Did not enter a valid move in 3 tries. Game ended.", inline=False)
                await boardMessage.edit(embed=em)
                return
            if(player2badInput==3):
                em.description = f"{self.etDisplay()}"
                em.color = 0x770000
                em.add_field(name=f"{player2} Forfeit", value="Did not enter a valid move in 3 tries. Game ended.", inline=False)
                await boardMessage.edit(embed=em)
                return

       #ToDO
       #Finish castling (move the rook)
       #check

    @commands.command(aliases = ['t'])
    @commands.cooldown(3, 30, commands.BucketType.channel)

    async def trivia(self, ctx):
        data = requests.get(f'https://opentdb.com/api.php?amount=1').json()
        results = data['results'][0]
        embed = discord.Embed(
            title = ":question:  Trivia",
            description = f"Category: {results['category']} | Difficulty: {results['difficulty'].capitalize()}",
            color = ctx.author.color
        )
        embed2 = embed
        def decode(answers):
            new = []
            for i in answers:
                new.append(html.unescape(i))
            return new
        if results['type'] == 'boolean':
            if results['correct_answer'] == "False":
                answers = results['incorrect_answers'] + [results['correct_answer']]
            else:
                answers = [results['correct_answer']] + results['incorrect_answers']
            answers = decode(answers)
            embed.add_field(name = html.unescape(results['question']), value = f"True or False")
            available_commands = ['true', 'false', 't', 'f']
        else:
            pos = random.randint(0, 3)
            if pos == 3:
                answers = results['incorrect_answers'] + [results['correct_answer']]
            else:
                answers = results['incorrect_answers'][0:pos] + [results['correct_answer']] + results['incorrect_answers'][pos:]
            answers = decode(answers)
            embed.add_field(name = html.unescape(results['question']), value = f"A) {answers[0]}\nB) {answers[1]}\nC) {answers[2]}\nD) {answers[3]}")
            available_commands = ['a', 'b', 'c', 'd'] + [x.lower() for x in answers]
        question = await ctx.send(embed = embed)
        correct_answer = html.unescape(results['correct_answer'])
        def check(m):
            return m.channel == ctx.channel and m.content.lower() in available_commands and not m.author.bot
        try:
            msg = await self.client.wait_for('message', timeout = 30.0, check = check)
        except asyncio.TimeoutError:
            return
        correct = False
        if results['type'] == 'boolean':
            if msg.content.lower() == correct_answer.lower() or msg.content.lower() == correct_answer.lower()[0]:
                correct = True
            answer_string = f"The answer was **{correct_answer}**"
        else:
            letters = ['a', 'b', 'c', 'd']
            if msg.content.lower() == correct_answer.lower() or msg.content.lower() == letters[pos]:
                correct = True
            answer_string = f"The answer was **{letters[pos].upper()}) {correct_answer}**"
        if correct:
            name = ":white_check_mark:  Correct"
        else:
            name = ":x:  Incorrect"
        embed2.clear_fields()
        embed2.add_field(name = name, value = answer_string)
        await question.edit(embed = embed2)

    @trivia.error
    async def trivia_error(self, ctx, error):
        await ctx.send(error)

    #@commands.max_concurrency(1, commands.BucketType.channel, wait = False)
    @commands.command(aliases = ['hang', 'hm'])
    async def hangman(self, ctx):
       
        with open('txt/words.txt') as f:
            word = random.choice(f.readlines()).rstrip("\n")
        hang = [
            "**```    ____",
            "   |    |",
            "   |    ",
            "   |   ",
            "   |    ",
            "   |   ",
            "___|__________```**"
        ]
        empty = '\n'.join(hang)
        man = [['@', 2], [' |', 3], ['\\', 3, 7], ['/', 3], ['|', 4], ['/', 5], [' \\', 5]]
        string = [':blue_square:' for i in word]
        embed = discord.Embed(
            title = "Hangman",
            color = ctx.author.color,
            description = f"Type a letter in chat to guess.\n\n**{' '.join(string)}**\n\n{empty}",
        )
        incorrect = 0
        original = await ctx.send(embed = embed)
        guessed = []
        incorrect_guessed = []
        already_guessed = None
        def check(m):
            return m.channel == ctx.channel and m.content.isalpha() and len(m.content) == 1 and m.author == ctx.author
        while incorrect < len(man) and ':blue_square:' in string:
            try:
                msg = await self.client.wait_for('message', timeout = 120.0, check = check)
                letter = msg.content.lower()
            except asyncio.TimeoutError:
                await ctx.send("Game timed out.")
                return
            if already_guessed:
                await already_guessed.delete()
                already_guessed = None
            if letter in guessed:
                already_guessed = await ctx.send("You have already guessed that letter.")
                await msg.delete()
                continue
            guessed += letter
            if letter not in word:
                incorrect_guessed += letter
                if embed.fields:
                    embed.set_field_at(0, name = "Incorrect letters:", value = ', '.join(incorrect_guessed))
                else:
                    embed.add_field(name = "Incorrect letters:", value = ', '.join(incorrect_guessed))
                part = man[incorrect]
                if len(part) > 2:
                    hang[part[1]] = hang[part[1]][0:part[2]] + part[0] + hang[part[1]][part[2] + 1:]
                else:
                    hang[part[1]] += part[0]
                incorrect += 1
            else:
                for j in range(len(word)):
                    if letter  == word[j]:
                        string[j] = word[j]
            new = '\n'.join(hang)
            if ':blue_square:' not in string:
                embed.description = f"You guessed the word!\n\n**{' '.join(string)}**\n\n{new}"
            elif incorrect == len(man):
                embed.description = f"You've been hanged! The word was \n\n**{' '.join([k for k in word])}**\n\n{new}"
            else:
                embed.description = f"Type a letter in chat to guess.\n\n**{' '.join(string)}**\n\n{new}"
            await msg.delete()
            await original.edit(embed = embed)

    @hangman.error
    async def hangman_error(self, ctx, error):
        await ctx.send(error)


    boards = {}

    def create(self, server_id, player1, player2):
        self.boards[server_id] = Board(player1, player2)

        # Return whoever is x's so that we know who is going first
        return self.boards[server_id].challengers["x"]

    @commands.group(aliases=["tic", "tac", "toe", "ttt"], invoke_without_command=True)
    @commands.guild_only()
    async def tictactoe(self, ctx):
        em =discord.Embed(title = "Tictactoe!", description = f"Use `{ctx.prefix}help ttt` for more info!")
        em.set_thumbnail(url="https://image.flaticon.com/icons/png/512/566/566294.png")
        await ctx.send(embed=em)

    @tictactoe.command(name="place", aliases=["plc"])
    @commands.guild_only()
    async def place(self, ctx, *, option: str=None):
        f"""Updates the current server's tic-tac-toe board
        You obviously need to be one of the players to use this
        It also needs to be your turn
        Provide top, left, bottom, right, middle as you want to mark where to play on the board
        EXAMPLE: rap tictactoe place middle top
        RESULT: Your piece is placed in the very top space, in the middle"""
        player = ctx.message.author
        board = self.boards.get(ctx.message.guild.id)
        # Need to make sure the board exists before allowing someone to play
        if not board:
            await ctx.send("There are currently no Tic-Tac-Toe games setup!")
            return
        # Now just make sure the person can play, this will fail if o's are up and x tries to play
        # Or if someone else entirely tries to play
        if not board.can_play(player):
            await ctx.send("You cannot play right now!")
            return

        # Search for the positions in the option given, the actual match doesn't matter, just need to check if it exists
        top = re.search("top", option)
        middle = re.search("middle", option)
        bottom = re.search("bottom", option)
        left = re.search("left", option)
        right = re.search("right", option)

        # Just a bit of logic to ensure nothing that doesn't make sense is given
        if top and bottom:
            await ctx.send("That is not a valid location! Use some logic, come on!")
            return
        if left and right:
            await ctx.send("That is not a valid location! Use some logic, come on!")
            return
        # Make sure at least something was given
        if not top and not bottom and not left and not right and not middle:
            await ctx.send("Please provide a valid location to play!")
            return

        x = 0
        y = 0
        # Simple assignments
        if top:
            x = 0
        if bottom:
            x = 2
        if left:
            y = 0
        if right:
            y = 2
        # If middle was given and nothing else, we need the exact middle
        if middle and not (top or bottom or left or right):
            x = 1
            y = 1
        # If just top or bottom was given, we assume this means top-middle or bottom-middle
        # We don't need to do anything fancy with top/bottom as it's already assigned, just assign middle
        if (top or bottom) and not (left or right):
            y = 1
        # If just left or right was given, we assume this means left-middle or right-middle
        # We don't need to do anything fancy with left/right as it's already assigned, just assign middle
        elif (left or right) and not (top or bottom):
            x = 1

        # If all checks have been made, x and y should now be defined
        # Correctly based on the matches, and we can go ahead and update the board
        # We've already checked if the author can play, so there's no need to make any additional checks here
        # board.update will handle which letter is placed
        # If it returns false however, then someone has already played in that spot and nothing was updated
        if not board.update(x, y):
            await ctx.send("Someone has already played there!")
            return
        # Next check if there's a winner
        winner = board.check()
        if winner:
            # Get the loser based on whether or not the winner is x's
            # If the winner is x's, the loser is o's...obviously, and vice-versa
            loser = (
                board.challengers["x"]
                if board.challengers["x"] != winner
                else board.challengers["o"]
            )
            await ctx.send(
                "{} has won this game of TicTacToe, better luck next time {}".format(
                    winner.display_name, loser.display_name
                )
            )
            # Handle updating ratings based on the winner and loser
           
            # This game has ended, delete it so another one can be made
            try:
                del self.boards[ctx.message.guild.id]
            except KeyError:
                pass
        else:
            # If no one has won, make sure the game is not full. If it has, delete the board and say it was a tie
            if board.full():
                await ctx.send("This game has ended in a tie!")
                try:
                    del self.boards[ctx.message.guild.id]
                except KeyError:
                    pass
            # If no one has won, and the game has not ended in a tie, print the new updated board
            else:
                player_turn = (
                    board.challengers.get("x")
                    if board.X_turn
                    else board.challengers.get("o")
                )
                fmt = str(board) + "\n{} It is now your turn to play!".format(
                    player_turn.display_name
                )
                await ctx.send(fmt)

    @tictactoe.command(name="start", aliases=["challenge", "create"])
    @commands.guild_only()
    async def start_game(self, ctx, player2: discord.Member):
        f"""Starts a game of tictactoe with another player
        EXAMPLE: rap tictactoe start @OtherPerson
        RESULT: A new game of tictactoe"""
        player1 = ctx.message.author
        # For simplicities sake, only allow one game on a server at a time.
        # Things can easily get confusing (on the server's end) if we allow more than one
        if self.boards.get(ctx.message.guild.id) is not None:
            await ctx.send(
                "Sorry but only one Tic-Tac-Toe game can be running per server!"
            )
            return
        # Make sure we're not being challenged, I always win anyway
        if player2 == ctx.message.guild.me:
            await ctx.send(
                "You want to play? Alright lets play.\n\nI win, so quick you didn't even notice it."
            )
            return
        if player2 == player1:
            await ctx.send(
                "You can't play yourself, I won't allow it. Go find some friends"
            )
            return

        # Create the board and return who has been decided to go first
        x_player = self.create(ctx.message.guild.id, player1, player2)
        fmt = "A tictactoe game has just started between {} and {}\n".format(
            player1.display_name, player2.display_name
        )
        # Print the board too just because
        fmt += str(self.boards[ctx.message.guild.id])

        # We don't need to do anything weird with assigning x_player to something
        # it is already a member object, just use it
        fmt += (
            "I have decided at random, and {} is going to be x's this game. It is your turn first! "
            "Use the {}tictactoe command, and a position, to choose where you want to play".format(
                x_player.display_name, ctx.prefix
            )
        )
        await ctx.send(fmt)

    @tictactoe.command(name="delete", aliases=["stop", "remove", "end"])
    @commands.guild_only()
    async def stop_game(self, ctx):
        f"""Force stops a game of tictactoe
        This should realistically only be used in a situation like one player leaves
        Hopefully a moderator will not abuse it, but there's not much we can do to avoid that
        EXAMPLE: rap tictactoe stop
        RESULT: No more tictactoe!"""
        if self.boards.get(ctx.message.guild.id) is None:
            await ctx.send("There are no tictactoe games running on this server!")
            return

        del self.boards[ctx.message.guild.id]
        await ctx.send(
            "I have just stopped the game of TicTacToe, a new should be able to be started now!"
        )


    @commands.command(aliases = ['2048', 'twenty48'])
    @commands.max_concurrency(1, commands.BucketType.channel, wait = False)
    async def twentyfortyeight(self, ctx):

        available_commands = ['w', 'a', 's', 'd', 'end_game']
        await ctx.send('2048 has started. Use WASD keys to move. Type "end_game" to end the game.')
        
        def moveNumbers(input, board):
            up = False
            down = False
            left = False
            right = False
            alreadyMoved = [[False] * 4 for n in range(4)]
            if input == 'w':
                up = True
            elif input == 's':
                down = True
            elif input == 'a':
                left = True
            else:
                right = True
            for k in range(4):
                for l in range(4):
                    stop = False
                    limit = 0
                    if down or right:
                        limit = 3
                    a = 0
                    b = 0
                    if up:
                        a = l
                        b = k
                    elif down:
                        a = 3 - l
                        b = k
                    elif left:
                        a = k
                        b = l
                    else:
                        a = k
                        b = 3 - l
                    while not stop:
                        if up or down:
                            c = a - 1
                            if down:
                                c = a + 1
                            if a == limit:
                                stop = True
                            else:
                                if board[c][b] == 0:
                                    board[c][b] = board[a][b]
                                    board[a][b] = 0
                                    a = c
                                elif board[c][b] == board[a][b] and alreadyMoved[c][b] != True:
                                    board[c][b] = board[c][b] * 2
                                    board[a][b] = 0
                                    alreadyMoved[c][b] = True
                                    stop = True
                                else:
                                    stop = True
                        else:
                            c = b - 1
                            if right:
                                c = b + 1
                            if b == limit:
                                stop = True
                            else:
                                if board[a][c] == 0:
                                    board[a][c] = board[a][b]
                                    board[a][b] = 0
                                    b = c
                                elif board[a][c] == board[a][b] and alreadyMoved[a][c] != True:
                                    board[a][c] = board[a][c] * 2
                                    board[a][b] = 0
                                    alreadyMoved[a][c] = True
                                    stop = True
                                else:
                                    stop = True
        
        end = False
        win = False
        start = True
        board = [[0] * 4 for n in range(4)]
        empty2 = 0
        empty = 0
        emptyX = []
        emptyY = []
        counter = 0
        while not end:
            canMove = False
            empty2 = 0
            if start:
                randX = random.randint(0, 3)
                randY = random.randint(0, 3)
                board[randX][randY] = 2
            out = '``` -------------------\n'
            for i in range(4):
                for j in range(4):
                    if i == 0:
                        if j == 0:
                            if board[i][j] == board[i + 1][j] or board[i][j] == board[i][j + 1]:
                                canMove = True
                        elif j == 3:
                            if board[i][j] == board[i + 1][j] or board[i][j] == board[i][j - 1]:
                                    canMove = True
                        else:
                            if board[i][j] == board[i + 1][j] or board[i][j] == board[i][j + 1] or board[i][j] == board[i][j - 1]:
                                    canMove = True
                    elif i == 3:
                        if j == 0:
                            if board[i][j] == board[i - 1][j] or board[i][j] == board[i][j + 1]:
                                canMove = True
                        elif j == 3:
                            if board[i][j] == board[i - 1][j] or board[i][j] == board[i][j - 1]:
                                canMove = True
                        else:
                            if board[i][j] == board[i][j + 1] or board[i][j] == board[i - 1][j] or board[i][j] == board[i][j - 1]:
                                canMove = True
                    else:
                        if j == 0:
                            if board[i][j] == board[i - 1][j] or board[i][j] == board[i][j + 1] or board[i][j] == board[i + 1][j]:
                                canMove = True
                        elif j == 3:
                            if board[i][j] == board[i - 1][j] or board[i][j] == board[i][j - 1] or board[i][j] == board[i + 1][j]:
                                canMove = True
                        else:
                            if board[i][j] == board[i][j + 1] or board[i][j] == board[i - 1][j] or board[i][j] == board[i][j - 1] or board[i][j] == board[i + 1][j]:
                                canMove = True
                    if board[i][j] == 2048:
                        win = True
                    if board[i][j] == 0:
                        empty2 += 1
                        out += '|    '
                    elif board[i][j] > 0 and board[i][j] < 10:
                        out += '|  ' + str(board[i][j]) + ' '
                    elif board[i][j] >= 10 and board[i][j] < 100:
                        out += '| ' + str(board[i][j]) + ' '
                    elif board[i][j] >= 100 and board[i][j] < 1000:
                        out += '| ' + str(board[i][j])
                    elif board[i][j] >= 1000 and board[i][j] < 10000:
                        out += '|' + str(board[i][j])
                out += '|\n'
                if i != 3:
                    out += '|----+----+----+----|\n'
            out += ' -------------------```'
            if start:
                msg2 = await ctx.send(out)
            else:
                await msg2.edit(content = out)
            if win:
                await ctx.send('You won!')

                return
            elif empty2 == 0 and not canMove:

                return
            valid = False
            while not valid:
                try:
                    msg = await self.client.wait_for('message', timeout = 300.0)
                except asyncio.TimeoutError:
                    await ctx.send('Game timed out.')
                    return
                if msg.channel == ctx.channel and msg.author == ctx.author:
                    if msg.content in available_commands:
                        content = msg.content
                        if content == 'end_game':
                            await ctx.send('Game ended.')
                            return
                        valid = True
                    await msg.delete()
            board2 = [row[:] for row in board]
            moveNumbers(content, board)
            for k in range(4):
                for l in range(4):
                    if board[k][l] == 0:
                        empty += 1
                        emptyX.append(k)
                        emptyY.append(l)

            if board != board2 and empty != 0:
                pos = random.randint(0, empty - 1)
                board[emptyX[pos]][emptyY[pos]] = 2 + (random.randint(0, 1) * 2)
                counter += 1
            empty = 0
            emptyX = []
            emptyY = []
            start = False

    @twentyfortyeight.error
    async def twentyfortyeight_error(self, ctx, error):
        await ctx.send(error)




    async def getMessages(self,ctx: commands.Context,number: int=1):
        if(number==0):
            return([])
        toDelete = []
        async for x in ctx.channel.history(limit = number):
            toDelete.append(x)
        return(toDelete)



	
def setup(client):
    client.add_cog(Games(client))