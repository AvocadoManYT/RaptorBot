import discord
import random
import base91
import numpy as np
import asyncio
from discord.ext import commands
from random import randint
from hangman.controller import HangmanGame

smoother = True

player1 = ""
player2 = ""
turn = ""
gameOver = True

board = []

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

numbers = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]

def checkWinner(self, winningConditions, mark):
        global gameOver
        for condition in winningConditions:
            if board[condition[0]] == mark and board[condition[1]] == mark and board[condition[2]] == mark:
                gameOver = True




class Games(commands.Cog):
    """ Category for game commands """

    
    def __init__(self, client):
        self.client = client
        self.ttt_games = {}

    # events

    def array_to_string(self, array_in, user):
        string = ""
        string2 = ""
        rows = array_in.shape[0]
        cols = array_in.shape[1]

        for x in range(0, rows):
            for y in range(0, cols):
                string += str(array_in[x][y]).replace(".0", "")
                for i in range(0, len(str(np.amax(array_in)).replace(".0", "")) - len(
                        str(array_in[x][y]).replace(".0", ""))):
                    string2 += ":new_moon:"
                for char in str(array_in[x][y]).replace(".0", ""):
                    if char == "0" and str(array_in[x][y]).replace(".0", "") == "0":
                        string2 += ":new_moon:"
                    else:
                        string2 += ":" + numbers[int(char)] + ":"
                if y != 3:
                    string += ","
                    if len(str(np.amax(array_in)).replace(".0", "")) > 1:
                        string2 += ":tm:"
                    else:
                        string2 += "   "
            if x != 3:
                string += "|"
                string2 += "\n"
                for i in range(0, len(str(np.amax(array_in)).replace(".0", ""))):
                    string2 += "\n"

        # Adds user id so the next action can tell who the game belongs to
        string += "[]%s" % user

        # Returns string2 as well which is the emoji-fied version of the game board
        return string, string2


    def string_to_array(self, string):
        # Turn the string from the footer back into a numpy array that can be acted upon
        output = np.zeros((4, 4))
        x_num = 0
        y_num = 0
        for x in string.split("[]")[0].split("|"):
            for y in x.split(","):
                output[x_num][y_num] = y
                y_num += 1
            y_num = 0
            x_num += 1
        user = string.split("[]")[1]

        # Returns output array and original game user
        return output, user


    async def delete_game(self, reaction):
        await reaction.message.edit(content="*Game removed*", embed=None)
        for emoji in ['⬆', '⬇', '⬅', '➡']:
            await reaction.message.remove_reaction(emoji=emoji, member=self.client.user)
        await reaction.message.remove_reaction(emoji=reaction, member=self.client.user)


    def check_valid(self, output2):
        # Check for valid moves
        rows = output2.shape[0]
        cols = output2.shape[1]
        found = False
        original = output2

        for j in range(0, 4):
            output2 = np.zeros(shape=(4, 4))
            output = original
            output = np.rot90(output, j)
            # Move everything to the left 4 times to be sure to get everything
            for i in range(0, 3):
                output2 = np.zeros(shape=(4, 4))
                for x in range(0, cols):
                    for y in range(0, rows):
                        if y != 0:
                            if output[x][y - 1] == 0:
                                output2[x][y - 1] = output[x][y]
                            else:
                                output2[x][y] = output[x][y]
                        else:
                            output2[x][y] = output[x][y]
                output = output2

            # Combine adjacent equal tiles
            output3 = np.zeros(shape=(4, 4))
            for x in range(0, cols):
                for y in range(0, rows):
                    if y != 0:
                        if output2[x][y - 1] == output2[x][y]:
                            output3[x][y - 1] = output2[x][y] * 2
                        else:
                            output3[x][y] = output2[x][y]
                    else:
                        output3[x][y] = output2[x][y]

            output = output3

            # Move over two more times
            for i in range(0, 1):
                output3 = np.zeros(shape=(4, 4))
                for x in range(0, cols):
                    for y in range(0, rows):
                        if y != 0:
                            if output[x][y - 1] == 0:
                                output3[x][y - 1] = output[x][y]
                            else:
                                output3[x][y] = output[x][y]
                        else:
                            output3[x][y] = output[x][y]
                output = output3

            output2 = output3
            output2 = np.rot90(output2, 4-j)

            if np.array_equal(original, output2) is False:
                found = True

        if found is True:
            return True
        else:
            return False


    @commands.Cog.listener()
    async def on_ready(self):
        print('game cog is ready.')

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        # Stop the bot from going when it adds its own reactions
        if user == self.client.user:
            return

        # Just to show in the console which reaction is being sent

        # If the message that was reacted on was one sent by the bot, guaranteeing it's a game
        if reaction.message.author == self.client.user:
            # Game is over and anyone can delete the game board and reactions by reacting the X emoji
            if reaction.emoji == '🇽' and base91.decode(reaction.message.embeds[0].footer.text).decode("utf-8") == "Game over!":
                await self.delete_game(reaction)
            else:
                # decode footer from base91
                footer = base91.decode(reaction.message.embeds[0].footer.text).decode("utf-8")
                output, user2 = self.string_to_array(footer)

                # if the user is the same one that started the game
                if user2 == user.mention:
                    original = output

                    rows = output.shape[0]
                    cols = output.shape[1]
                    output2 = np.zeros(shape=(4, 4))

                    if reaction.emoji == '🇽':
                        # Game is still going and original user can decide to delete game
                        await self.delete_game(reaction)
                        await reaction.message.remove_reaction(emoji=reaction, member=user)
                        return
                    # Rotate arrays to all be facing to the left to make actions on them easier
                    elif reaction.emoji == '⬅':
                        output = np.rot90(output, 0)
                    elif reaction.emoji == '➡':
                        output = np.rot90(output, 2)
                    elif reaction.emoji == '⬆':
                        output = np.rot90(output, 1)
                    elif reaction.emoji == '⬇':
                        output = np.rot90(output, 3)
                    else:
                        await reaction.message.remove_reaction(emoji=reaction, member=user)
                        return

                    # Move everything to the left 4 times to be sure to get everything
                    for i in range(0, 3):
                        output2 = np.zeros(shape=(4, 4))
                        for x in range(0, cols):
                            for y in range(0, rows):
                                if y != 0:
                                    if output[x][y-1] == 0:
                                        output2[x][y-1] = output[x][y]
                                    else:
                                        output2[x][y] = output[x][y]
                                else:
                                    output2[x][y] = output[x][y]
                        output = output2

                    # Combine adjacent equal tiles
                    output3 = np.zeros(shape=(4, 4))
                    for x in range(0, cols):
                        for y in range(0, rows):
                            if y != 0:
                                if output2[x][y - 1] == output2[x][y]:
                                    output3[x][y - 1] = output2[x][y]*2
                                    output2[x][y] = 0
                                else:
                                    output3[x][y] = output2[x][y]
                            else:
                                output3[x][y] = output2[x][y]

                    output = output3

                    # Move over two more times and check if the board has a 2048 in it or if it's completely full
                    found_win = False
                    found_end = True
                    for i in range(0, 1):
                        output3 = np.zeros(shape=(4, 4))
                        for x in range(0, cols):
                            for y in range(0, rows):
                                if y != 0:
                                    if output[x][y-1] == 0:
                                        output3[x][y-1] = output[x][y]
                                    else:
                                        output3[x][y] = output[x][y]
                                else:
                                    output3[x][y] = output[x][y]
                                if output3[x][y] == 2048:
                                    found_win = True
                                if output3[x][y] == 0:
                                    found_end = False
                        output = output3

                    output2 = output3

                    e = discord.Embed(title="%s's Game!" % user)

                    # Undo the rotations from before
                    if reaction.emoji == '⬅':
                        output2 = np.rot90(output2, 0)
                    if reaction.emoji == '➡':
                        output2 = np.rot90(output2, 2)
                    if reaction.emoji == '⬆':
                        output2 = np.rot90(output2, 3)
                    if reaction.emoji == '⬇':
                        output2 = np.rot90(output2, 1)

                    # If there's a 2048 on the board, the player won! Add the win gif
                    if found_win is True:
                        e = discord.Embed()
                        e.add_field(name="%s got the 2048 tile!" % user, value="You did it!!")
                        e.set_image(url="https://media1.giphy.com/media/l2SpR4slaePsGG49O/giphy.gif")
                        e.set_footer(text=base91.encode(b"Game over!"))
                        await reaction.message.edit(embed=e)
                        for emoji in ['⬆', '⬇', '⬅', '➡']:
                            await reaction.message.remove_reaction(emoji=emoji, member=self.client.user)
                        await reaction.message.add_reaction('🇽')
                    # If the array changed from how it was before and if there are any empty spaces on the board, add a random tile
                    elif np.array_equal(output2, original) is False and found_end is False:
                        if smoother == False:
                            found = False
                            while found is not True:
                                first_2 = randint(0, 3)
                                second_2 = randint(0, 3)
                                if output2[first_2][second_2] == 0:
                                    found = True
                                    output2[first_2][second_2] = randint(1, 2) * 2

                        string, string2 = self.array_to_string(output2, user.mention)



                        e.add_field(name="Try to get the 2048 tile!", value=string2)
                        e.set_footer(text=base91.encode(bytes(string, 'utf-8')))
                        await reaction.message.edit(embed=e)

                        # Check if there are valid moves and if not, end the game
                        if self.check_valid(output2) is False:

                            # If there are no 0's, check if there are any valid moves. If there aren't, say the game is over.
                            e = discord.Embed()
                            e.add_field(name="%s is unable to make any more moves." % user, value=":cry:")
                            e.set_image(url="https://media2.giphy.com/media/joNVQCtuecqHK/giphy.gif")
                            e.set_footer(text=base91.encode(b"Game over!"))
                            await reaction.message.edit(embed=e)
                            for emoji in ['⬆', '⬇', '⬅', '➡']:
                                await reaction.message.remove_reaction(emoji=emoji, member=self.client.user)
                            await reaction.message.add_reaction('🇽')

                        if smoother == True:
                            found = False
                            while found is not True:
                                first_2 = randint(0, 3)
                                second_2 = randint(0, 3)
                                if output2[first_2][second_2] != 0:
                                    None
                                else:
                                    found = True
                                    output2[first_2][second_2] = randint(1, 2) * 2

                            string, string2 = self.array_to_string(output2, user.mention)
                            e = discord.Embed()
                            e.add_field(name="Try to get the 2048 tile!", value=string2)
                            e.set_footer(text=base91.encode(bytes(string, 'utf-8')))
                            await reaction.message.edit(embed=e)
                    elif self.check_valid(output2) is False:

                        # If there are no 0's, check if there are any valid moves. If there aren't, say the game is over.
                        e = discord.Embed()
                        e.add_field(name="%s is unable to make any more moves." % user, value=":cry:")
                        e.set_image(url="https://media2.giphy.com/media/joNVQCtuecqHK/giphy.gif")
                        e.set_footer(text=base91.encode(b"Game over!"))
                        await reaction.message.edit(embed=e)
                        for emoji in ['⬆', '⬇', '⬅', '➡']:
                            await reaction.message.remove_reaction(emoji=emoji, member=self.client.user)
                        await reaction.message.add_reaction('🇽')
                    else:

                        # They made a valid move, but it didn't change anything, so don't add a new tile
                        string, string2 = self.array_to_string(output2, user.mention)



                        e.add_field(name="Try to get the 2048 tile!", value=string2)
                        e.set_footer(text=base91.encode(bytes(string, 'utf-8')))
                        await reaction.message.edit(embed=e)

            # Remove reaction
            await reaction.message.remove_reaction(emoji=reaction, member=user)

    players = {}
    
    # TicTacToe COMMAND
    
    @commands.command(aliases=['ttt'])
    async def tictactoe(self, ctx, player: discord.Member):
        global count
        global player1
        global player2
        global turn
        global gameOver

        if player == ctx.author:
            await ctx.send("You can\'t play with yourself!")
            return
        if player == ctx.bot:
            await ctx.send("You can\'t play with a bot!")
        if gameOver:
            global board
            board = [":white_large_square:", ":white_large_square:", ":white_large_square:",
                    ":white_large_square:", ":white_large_square:", ":white_large_square:",
                    ":white_large_square:", ":white_large_square:", ":white_large_square:"]
            turn = ""
            gameOver = False
            count = 0

            player1 = ctx.author
            player2 = player

            # print the board
            line = ""
            for x in range(len(board)):
                if x == 2 or x == 5 or x == 8:
                    line += " " + board[x]
                    await ctx.send(line)
                    line = ""
                else:
                    line += " " + board[x]

            # determine who goes first
            num = random.randint(1, 2)
            if num == 1:
                turn = player1
                await ctx.send("It is <@" + str(player1.id) + ">'s turn.")
            elif num == 2:
                turn = player2
                await ctx.send("It is <@" + str(player2.id) + ">'s turn.")
        else:
            await ctx.send("A game is already in progress! Finish it before starting a new one.")

    @commands.command(aliases=['place'])
    async def tttplace(self, ctx, pos: int):
        global turn
        global player1
        global player2
        global board
        global count
        global gameOver


        
        if not gameOver:
            mark = ""
            if turn == ctx.author:
                if turn == player1:
                    mark = ":regional_indicator_x:"
                elif turn == player2:
                    mark = ":o2:"
                if 0 < pos < 10 and board[pos - 1] == ":white_large_square:" :
                    board[pos - 1] = mark
                    count += 1

                    # print the board
                    line = ""
                    for x in range(len(board)):
                        if x == 2 or x == 5 or x == 8:
                            line += " " + board[x]
                            await ctx.send(line)
                            line = ""
                        else:
                            line += " " + board[x]

                    checkWinner(winningConditions, mark)
                    if gameOver == True:
                        await ctx.send(mark + " wins!")
                    elif count >= 9:
                        gameOver = True
                        await ctx.send("It's a tie!")

                    # switch turns
                    if turn == player1:
                        turn = player2
                    elif turn == player2:
                        turn = player1
                else:
                    await ctx.send("Be sure to choose an integer between 1 and 9 (inclusive) and an unmarked tile.")
            else:
                await ctx.send("It is not your turn.")
        else:
            await ctx.send("Please start a new game using the r!tictactoe command.")


    

    @tictactoe.error
    async def tictactoe_error(ctx, error):
        print(error)
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please mention 2 players for this command.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Please make sure to mention/ping players (ie. <@688534433879556134>).")

    @tttplace.error
    async def place_error(ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please enter a position you would like to mark.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Please make sure to enter an integer.")
            

    @commands.command(aliases=['end'])
    async def tttend(self, ctx):
        try:
            # We need to declare them as global first
            global count
            global player1
            global player2
            global turn
            global gameOver
            
            # Assign their initial value
            count = 0
            player1 = ""
            player2 = ""
            turn = ""
            gameOver = True

            # Now print your message or whatever you want
            myEmbed = discord.Embed(title= "Reseted",description="To start a new game, use the  r!ttt command!",color=0x2ecc71)
            await ctx.send(embed=myEmbed)
        except:
            await ctx.send("You\'re not in a game ;-;") 



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
            await ctx.send("It\'s a tie!")
        elif guess == 'rock' and p == 'paper':
            await ctx.send("I won!")
        elif guess == 'paper' and p == 'rock':
            await ctx.send("You won")
        elif guess == 'paper' and p == 'scissors':
            await ctx.send("I won!")
        elif guess == 'paper' and p == 'paper':
            await ctx.send("It\'s a tie!")
        elif guess == 'scissors' and p == 'scissors':
            await ctx.send("It\'s a tie!")
        elif guess == 'scissors' and p == 'rock':
            await ctx.send("I won!")
        elif guess == 'scissors' and p == 'paper':
            await ctx.send("You won!")
        else:
            await ctx.send("Guess can only be rock, paper or scissors.")

    
    @commands.command(aliases=['hm'])
    async def hangman(self, ctx, guess:str=None):
        

        if guess == None:
            await ctx.send("How about add a letter after `r!hangman` next time?")
            return
        else:
            player_id = ctx.author.id
            hangman_instance = HangmanGame()
            game_over, won = hangman_instance.run(player_id, guess)
            if game_over:
                game_over_message = ":/ You did not win."
                if won:
                    game_over_message = "Congrats you won!"

                game_over_message = game_over_message + \
                    " The word was %s" % hangman_instance.get_secret_word()

                await hangman_instance.reset(player_id)
                await ctx.send(game_over_message)

            else:
                await ctx.send("Progress: %s" % hangman_instance.get_progress_string())
                await ctx.send("Guess so far: %s" % hangman_instance.get_guess_string())

    
    @commands.command(name = "2048")
    async def twenty48(self, ctx):
        # To show who's game it is (no one else can play the game than this person)
        message = ctx
        e = discord.Embed(title="%s's Game!" % message.author)

        # Generate Random Game Board
        start_array = np.zeros(shape=(4, 4))

        first = randint(0, 3)
        second = randint(0, 3)
        start_array[first][second] = randint(1, 2) * 2

        found = False
        while found is not True:
            first_2 = randint(0, 3)
            second_2 = randint(0, 3)
            if first_2 == first and second_2 == second:
                None
            else:
                found = True
                start_array[first_2][second_2] = randint(1, 2) * 2

        #start_array[randint(0, 3)][randint(0, 3)] = randint(1, 90) * 2

        string, string2 = self.array_to_string(start_array, message.author.mention)

        e.add_field(name="Try to get the 2048 tile!", value=string2)    
        e.set_footer(text=base91.encode(bytes(string, 'utf-8')))

        new_msg = await message.channel.send(embed=e)
        # Add control reactions
        for emoji in ['⬆', '⬅', '➡', '⬇']:
            await new_msg.add_reaction(emoji)

	
def setup(client):
    client.add_cog(Games(client))