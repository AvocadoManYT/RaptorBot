import discord
import random
import asyncio
from games import wumpas as wumpus, minesweeper
import requests
import html
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




class Games(commands.Cog):
    """ Category for game commands """

    
    def __init__(self, client):
        self.client = client
        self.ttt_games = {}

    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Games are loaded")
    # events
    @commands.command(name='survival')
    async def _wumpus(self, ctx):
        """Play a survival game, try to find the dragon without dying!"""
        await wumpus.play(self.client, ctx)

    @commands.command(name='minesweeper', aliases=['ms'])
    async def _minesweeper(self, ctx, columns = None, rows = None, bombs = None):
        """Play Minesweeper"""
        await minesweeper.play(ctx, columns, rows, bombs)



    @commands.command(name="guess", help="guessing game")
    async def guess(self,ctx):
        lives=3
        number=randint(1,10)
        await ctx.send("Guess the number from `1 to 10` :zany_face:")
        await ctx.send("Enter the guess only ex: `1`")
        await ctx.send("BTW: You only have `30` seconds to guess so answer quickly!")

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
    async def rockpaperscissors(self, ctx, guess):
        r = ['rock', 'paper', 'scissors']
        p = random.choice(r)
        await ctx.send(f"I choose {p}")
        if guess == 'rock' and p == 'scissors':
            await ctx.send("You won!")
        elif guess == 'rock' and p == 'rock':
            await ctx.send("It's a tie!")
        elif guess == 'rock' and p == 'paper':
            await ctx.send("I won!")
        elif guess == 'paper' and p == 'rock':
            await ctx.send("You won")
        elif guess == 'paper' and p == 'scissors':
            await ctx.send("I won!")
        elif guess == 'paper' and p == 'paper':
            await ctx.send("It\'s a tie!")
        elif guess == 'scissors' and p == 'scissors':
            await ctx.send("It's a tie!")
        elif guess == 'scissors' and p == 'rock':
            await ctx.send("I won!")
        elif guess == 'scissors' and p == 'paper':
            await ctx.send("You won!")
        else:
            await ctx.send("Guess can only be rock, paper or scissors.")

    
    

    @commands.command(name='connectfour', aliases=['c4', 'connect4'])
    async def connect4(self,ctx: commands.Context,opponent="",width=7,height=6):
        #-------------- Help section ------------------#
        if(opponent=="" or opponent.find('help')!=-1):
            em = discord.Embed()
            em.title = f'Usage: r!connect4 opponent [width] [height]'
            em.description = f'Challenges opponent to a game of connect 4. The Opponent should be @mentoned to start\nBoard is default 7x6 large if not specified, though you usually wont need any board larger than that.\nMax board volume is 95 due to character limitations'
            em.add_field(name="Example", value="r!connect4 @Username\nr!connect4 @Username 10 9", inline=False)
            em.color = 0x22BBFF
            await ctx.send(embed=em)
            return
        #----------------------------------------------#
        # Remove challenge message
        await ctx.channel.delete_messages(await self.getMessages(ctx,1))
        
        # Game init
        resized = False
        if(width*height > 95):
            width = 7
            height = 6
            resized = True
        player1 = ctx.message.mentions[0].name
        player2 = ctx.message.author.name
        s = ':black_large_square:'
        p1 = ':blue_circle:'
        p2 = ':red_circle:'
        board = []
        for column in range(height):
            rowArr = []
            for row in range(width):
                rowArr.append(s)
            board.append(rowArr)
        def getDisplay(self):
            toDisplay = ""
            for y in range(height):
                for x in range(width-1):
                    toDisplay+=board[y][x]+'|'
                toDisplay+=board[y][width-1] + '\n'
            return(toDisplay)
        
        boardMessage = None
        em = discord.Embed()
        if(player1==player2):
            em.title = f"{player2} challenged themselves to a game of Connect 4 \n(wow you're lonely)"
        else:
            em.title = f'{player2} challenged {player1} to a game of Connect 4'
        em.description = f"{self.getDisplay()}"
        em.color = 0x444444
        em.add_field(name=f"{player1}", value=f"Type a number from 1-{width} to accept and place your first piece, or type 'decline' to refuse", inline=False)
        if resized:
            em.add_field(name="Note", value=f"Original board length was too large, defaulted to 7x6", inline=False)
        await ctx.send(embed=em)
        async for x in ctx.channel.history(limit = 1):
            boardMessage = x
        badInput = 0
        turns = 1
        currentPlayer = player1
        otherPlayer = player2
        currentPlayerId=1
        while True:
            try:
                msg = await self.client.wait_for('message',check=lambda message: message.author.name == player1, timeout=30)
                if(msg.content=='decline'):
                    em = discord.Embed()
                    if(player1==player2):
                        em.title = f"{player2} challenged themselves to a game of Connect 4 (wow you're lonely)"
                    else:
                        em.title = f'{player2} challenged {player1} to a game of Connect 4'
                    em.description = f"{self.getDisplay()}"
                    em.color = 0x444444
                    em.add_field(name=f"{player1}", value="Challenge refused", inline=False)
                    await boardMessage.edit(embed=em)
                    return
                
                slot = int(msg.content)
                if(slot<1 or slot>width):
                    raise ValueError
                await ctx.channel.delete_messages(await self.getMessages(ctx,1))
                board[height-1][slot-1] = p1
                gameLoop = True
                currentPlayer = player2
                otherPlayer = player1
                turns +=1
                currentPlayerId=2
                break;
            except asyncio.exceptions.TimeoutError:
                em = discord.Embed()
                if(player1==player2):
                    em.title = f"{player2} challenged themselves to a game of Connect 4 (wow you're lonely)"
                else:
                    em.title = f'{player2} challenged {player1} to a game of Connect 4'
                em.description = f"{self.getDisplay()}"
                em.color = 0x444444
                em.add_field(name=f"{player1}", value="Game timed out", inline=False)
                await boardMessage.edit(embed=em)
                return
            except ValueError:
                em = discord.Embed()
                if(player1==player2):
                    em.title = f"{player2} challenged themselves to a game of Connect 4 (wow you're lonely)"
                else:
                    em.title = f'{player2} challenged {player1} to a game of Connect 4'
                em.description = f"{self.getDisplay()}"
                em.color = 0x444444
                em.add_field(name=f"{player1}", value=f"Enter a valid number from 1-{width}", inline=False)
                await boardMessage.edit(embed=em)
                badInput+=1
            if(badInput==3):
                em = discord.Embed()
                if(player1==player2):
                    em.title = f"{player2} challenged themselves to a game of Connect 4 (wow you're lonely)"
                else:
                    em.title = f'{player2} challenged {player1} to a game of Connect 4'
                em.description = f"{self.getDisplay()}"
                em.color = 0x444444
                em.add_field(name=f"{player1}", value="Did not enter a valid number in 3 tries. Game ended.", inline=False)
                await boardMessage.edit(embed=em)
                return
        winningComment=""
        winner=""
        while gameLoop:
            if(turns==width*height):
                winner=None
                break;
            ################################
            #check for winning combinations#
            ################################
            # Horizontal
            for y in range(height):
                for x in range(width-3):
                    if(board[y][x]==board[y][x+1] and board[y][x]==board[y][x+2] and board[y][x]==board[y][x+3] and board[y][x]!=s):
                        if(board[y][x]==p1):
                            board[y][x] = ':large_blue_diamond:'
                            board[y][x+1] = ':large_blue_diamond:'
                            board[y][x+2] = ':large_blue_diamond:'
                            board[y][x+3] = ':large_blue_diamond:'
                        elif(board[y][x]==p2):
                            board[y][x]=":diamonds:"
                            board[y][x+1]=":diamonds:"
                            board[y][x+2]=":diamonds:"
                            board[y][x+3]=":diamonds:"
                        print("winner")
                        winner=otherPlayer
                        winningComment = f"{otherPlayer} connected 4 in a horizontal row"
                        break
                if(winner!=""):
                    break
            #Vertical
            for y in range(height-3):
                for x in range(width):
                    if(board[y][x]==board[y+1][x] and board[y][x]==board[y+2][x] and board[y][x]==board[y+3][x] and board[y][x]!=s):
                        if(board[y][x]==p1):
                            board[y][x] = ':large_blue_diamond:'
                            board[y+1][x] = ':large_blue_diamond:'
                            board[y+2][x] = ':large_blue_diamond:'
                            board[y+3][x] = ':large_blue_diamond:'
                        elif(board[y][x]==p2):
                            board[y][x]=":diamonds:"
                            board[y+1][x]=":diamonds:"
                            board[y+2][x]=":diamonds:"
                            board[y+3][x]=":diamonds:"
                        winner = otherPlayer
                        winningComment = f"{otherPlayer} connected 4 in a vertical row"
                        break
                if(winner!=""):
                    break      
            # diagonal \
            for y in range(height-3):
                for x in range(width-3):
                    if(board[y][x]==board[y+1][x+1] and board[y][x]==board[y+2][x+2] and board[y][x]==board[y+3][x+3] and board[y][x]!=s):
                        if(board[y][x]==p1):
                            board[y][x] = ':large_blue_diamond:'
                            board[y+1][x+1] = ':large_blue_diamond:'
                            board[y+2][x+2] = ':large_blue_diamond:'
                            board[y+3][x+3] = ':large_blue_diamond:'
                        elif(board[y][x]==p2):
                            board[y][x]=":diamonds:"
                            board[y+1][x+1]=":diamonds:"
                            board[y+2][x+2]=":diamonds:"
                            board[y+3][x+3]=":diamonds:"
                        winner = otherPlayer
                        winningComment = f"{otherPlayer} connected 4 in a \ diagonal"
                        break
                if(winner!=""):
                    break    
            # diagonal /
            for y in range(height-3):
                for x in range(3,width):
                    if(board[y][x]==board[y+1][x-1] and board[y][x]==board[y+2][x-2] and board[y][x]==board[y+3][x-3] and board[y][x]!=s):
                        if(board[y][x]==p1):
                            board[y][x] = ':large_blue_diamond:'
                            board[y+1][x-1] = ':large_blue_diamond:'
                            board[y+2][x-2] = ':large_blue_diamond:'
                            board[y+3][x-3] = ':large_blue_diamond:'
                        elif(board[y][x]==p2):
                            board[y][x]=":diamonds:"
                            board[y+1][x-1]=":diamonds:"
                            board[y+2][x-2]=":diamonds:"
                            board[y+3][x-3]=":diamonds:"
                        winner = otherPlayer
                        winningComment = f"{otherPlayer} connected 4 in a / diagonal"
                        break
                if(winner!=""):
                    break    
            if(winner!=""):
                break
            ################################
            em = discord.Embed()
            em.title = f'Connect 4'
            em.description = f"{self.getDisplay()}"
            em.color = 0x444444
            em.add_field(name=f"Turn {turns}: {currentPlayer} turn", value=f"Enter a value from 1-{width}. You have 30 seconds to make a choice", inline=True)
            await boardMessage.edit(embed=em)
            gotValidInput = False
            badInput = 0
            while not gotValidInput:
                try:
                    msg = await self.client.wait_for('message',check=lambda message: message.author.name == currentPlayer, timeout=30)
                    await ctx.channel.delete_messages(await self.getMessages(ctx,1))
                    slot = int(msg.content)
                    if(slot<1 or slot>width):
                        raise ValueError
                    # Place piece in slot
                    for y in range(height-1,-1,-1):
                        if(board[y][slot-1]==s):
                            if(currentPlayerId == 1):
                                board[y][slot-1] = p1
                                break;
                            else:
                                board[y][slot-1] = p2
                                break;
                        elif(y==0): #if column is full
                            raise ValueError
                    # switch player
                    if(currentPlayerId == 1):
                        currentPlayer = player1
                        otherPlayer = player2
                        currentPlayerId = 2
                    else:
                        currentPlayer = player1
                        otherPlayer = player2
                        currentPlayerId = 1
                    gotValidInput=True
                    turns+=1
                    break
                except asyncio.exceptions.TimeoutError:
                    winner=otherPlayer
                    winningComment=f"{currentPlayer} took too much time"
                    gameLoop = False
                    break
                except ValueError:
                    em = discord.Embed()
                    em.title = f'Connect 4'
                    em.description = f"{self.getDisplay()}"
                    em.color = 0x444444
                    em.add_field(name=f"Turn {turns}: {currentPlayer}", value=f"Enter a valid number from 1-{width}", inline=False)
                    await boardMessage.edit(embed=em)
                    badInput+=1
                if(badInput==3):
                    winner=otherPlayer
                    winningComment=f"{currentPlayer} had too many bad inputs"
                    gameLoop = False
                    break
        if(winner==None):
            em = discord.Embed()
            em.title = f'Connect 4 - Tie, No Winners'
            em.description = f"{self.getDisplay()}"
            em.color = 0x444444
            await boardMessage.edit(embed=em)
        elif(winner==player1):
            em = discord.Embed()
            em.title = f'Connect 4 - {player1} wins!'
            em.description = f"{self.getDisplay()}"
            em.add_field(name="Reason:", value=f"{winningComment}", inline=False)
            if(player1==player2):
                em.add_field(name="Also:", value=f"They won against themself", inline=False)
            em.color = 0x444444
            await boardMessage.edit(embed=em)
        elif(winner==player2):
            em = discord.Embed()
            em.title = f'Connect 4 - {player2} wins!'
            em.description = f"{self.getDisplay()}"
            em.add_field(name="Reason:", value=f"{winningComment}", inline=False)
            if(player1==player2):
                em.add_field(name="Also:", value=f"They won against themself", inline=False)
            em.color = 0x444444
            await boardMessage.edit(embed=em)

    @commands.command(name='chess')
    async def chess(self, ctx: commands.Context,opponent=""):
        #-------------- Help section ------------------#
        if(opponent=="" or opponent.find('help')!=-1):
            em = discord.Embed()
            em.title = f'Usage: r!chess opponent'
            em.description = f'Challenges opponent to a game of chess. The Opponent should be @mentoned to start\nOpponent will make the first move, and thus be controlling the white pieces.'
            em.add_field(name="Example", value="r!chess @Username", inline=False)
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
        def getDisplay():
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
        em.description = f"{self.getDisplay()}"
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
                    em.description = f"{self.getDisplay()}"
                    em.add_field(name=f"{player1}", value="Challenge refused", inline=False)
                    await boardMessage.edit(embed=em)
                    return
                gameMsg = checkPlayerMove(msg.content,castlingDict)
                if(gameMsg[0:4]!="Turn"):
                    player1badInput+=1
                    em.description = f"{getDisplay()}"
                    em.color = 0xFF0000
                    em.add_field(name="Error", value=f"{gameMsg}", inline=False)
                    await boardMessage.edit(embed=em)
                    continue
                await ctx.channel.delete_messages(await self.getMessages(ctx,1))
                turn += 1
                movePiece(msg.content)
                em.color = 0x00FF00
                em.description = f"{self.getDisplay()}"
                em.add_field(name=f"{otherPlayer}'s turn:", value=f"{gameMsg}", inline=False)
                await boardMessage.edit(embed=em)
                gameLoop = True
                currentPlayer,otherPlayer = otherPlayer,currentPlayer
                currentPlayerId = 2 if (currentPlayerId == 1) else 1
                player1badInput = 0
                prevMove = msg.content
                break;
            except asyncio.exceptions.TimeoutError:
                em.description = f"{self.getDisplay()}"
                em.color = 0xFF0000
                em.add_field(name=f"{player1}", value="Game timed out", inline=False)
                await boardMessage.edit(embed=em)
                return
            if(player1badInput==3):
                em.description = f"{self.getDisplay()}"
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
                    em.description = f"{self.getDisplay()}"
                    em.add_field(name=f"{currentPlayer} Quits", value=f"{otherPlayer} wins!", inline=False)
                    await boardMessage.edit(embed=em)
                    return
                elif(gameMsg == "That piece can not move there"):
                    coords = msg.content.split(" ")
                    if(inCheck(parseMove(coords[0]),parseMove(coords[1]))):
                        em.color = 0xFF0000
                        em.description = f"{self.getDisplay()}"
                        em.add_field(name="Error", value=f"Can not move into check", inline=False)
                    else:
                        em.color = 0x770000
                        em.description = f"{self.getDisplay()}"
                        em.add_field(name="Invalid Move", value=f"{gameMsg}", inline=False)
                    await boardMessage.edit(embed=em)
                    continue
                elif(gameMsg[0:4]!="Turn"):
                    if(currentPlayer == player1):
                        player1badInput+=1
                    else:
                        player2badInput+=1
                    em.color = 0x770000
                    em.description = f"{self.getDisplay()}"
                    em.add_field(name="Invalid Move", value=f"{gameMsg}", inline=False)
                    await boardMessage.edit(embed=em)
                    continue
                await ctx.channel.delete_messages(await self.getMessages(ctx,1))
                turn += 1
                movePiece(msg.content)
                em.description = f"{self.getDisplay()}"
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
                em.description = f"{self.getDisplay()}"
                em.color = 0x770000
                em.add_field(name=f"{currentPlayer} Forfeit", value="Didn't make a move within 30 seconds", inline=False)
                await boardMessage.edit(embed=em)
                return
            if(player1badInput==3):
                em.description = f"{self.getDisplay()}"
                em.color = 0x770000
                em.add_field(name=f"{player1} Forfeit", value="Did not enter a valid move in 3 tries. Game ended.", inline=False)
                await boardMessage.edit(embed=em)
                return
            if(player2badInput==3):
                em.description = f"{self.getDisplay()}"
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
       
        with open('words3.txt') as f:
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

    @commands.command(aliases = ['ttt'])
    async def tictactoe(self, ctx, *, opponent: discord.Member):
       
        if opponent.id == ctx.author.id:
            await ctx.send("You played yourself. Oh wait, you can't.")
            return
        if opponent.bot:
            await ctx.send("You played a bot. Oh wait, you can't.")
            return
        await ctx.send('Tictactoe has started. Type the number of the square you want to go in. Type "end_game" to end the game.')
        player1 = ctx.author
        player2 = opponent

        commands = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'end_game']

        def check(m):
            return m.channel == ctx.channel and (m.content in commands) and not m.author.bot

        def endgame(board):
            for k in range(3):
                if board[k][0] == board[k][1] and board[k][1] == board[k][2]:
                    if board[k][0] > 0:
                        return board[k][0]
                elif board[0][k] == board[1][k] and board[1][k] == board[2][k]:
                    if board[0][k] > 0:
                        return board[0][k]
            if (board[0][0] == board[1][1] and board[1][1] == board[2][2]) or (board[0][2] == board[1][1] and board[1][1] == board[2][0]):
                if board[1][1] > 0:
                    return board[1][1]
            counter = 0
            for l in range(3):
                for m in range(3):
                    if board[l][m] == 0:
                        counter += 1
            if counter == 0:
                return 3
            else:
                return 0

        board = [[0] * 3 for n in range(3)]
        end = False
        player = 1
        while not end:
            out = '```'
            for i in range(3):
                for j in range(3):
                    out += ' '
                    if board[i][j] == 0:
                        out += str(i * 3 + j + 1)
                    elif board[i][j] == 1:
                        out += 'X'
                    elif board[i][j] == 2:
                        out += 'O'
                    out += ' '
                    if j != 2:
                        out += '|'
                out += '\n'
                if i != 2:
                    out += '---+---+---\n'
            out += '```'
            await ctx.send(out)
            result = endgame(board)
            if result != 0:
                if result == 1:
                    await ctx.send(f'{player1.display_name} wins!')
                    return
                elif result == 2:
                    await ctx.send(f'{player2.display_name} wins!')
                    return
                else:
                    await ctx.send('Tie!')

                    return
            if player == 1:
                await ctx.send("{0}'s turn".format(player1.display_name))
            else:
                await ctx.send("{0}'s turn".format(player2.display_name))
            valid = False
            while not valid:
                try:
                    msg = await self.client.wait_for('message', timeout = 300.0, check = check)
                except asyncio.TimeoutError:
                    await ctx.send('Game timed out.')
                    return
                if (player == 1 and msg.author == player1) or (player == 2 and msg.author == player2):
                    if msg.content == 'end_game':
                        await ctx.send('Game ended.')
                        return
                    input = int(msg.content)
                    a = int((input - 1) / 3)
                    b = int((input - 1) % 3)
                    if board[a][b] == 0:
                        board[a][b] = player
                        player = 3 - player
                        valid = True
	
    @tictactoe.error
    async def tictactoe_error(self, ctx, error):
        print(error)
        await ctx.send('Please follow format: `r!tictactoe {opponent}`')

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
        input = ''
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