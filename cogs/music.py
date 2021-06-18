import discord
from discord.ext import commands
import DiscordUtils
import aiohttp
import datetime
from datetime import datetime
music = DiscordUtils.Music()

class Music(commands.Cog):
    """ Category for music commands """

    def __init__(self, client):
        self.client = client

    # events
    @commands.Cog.listener()
    async def on_ready(self):
        print('Music cog is ready.')
    #COMMAND

    @commands.command()
    async def join(self, ctx):
        try:
            await ctx.author.voice.channel.connect() #Joins author's voice channel
        except:
            await ctx.send("You have not joined a voice channel.")

    @commands.command()
    async def leave(self, ctx):
        await ctx.voice_client.disconnect()

    @commands.command()
    async def play(self, ctx, *, url):
        player = music.get_player(guild_id=ctx.guild.id)
        if not player:
            player = music.create_player(ctx, ffmpeg_error_betterfix=True)
        if not ctx.voice_client.is_playing():
            await player.queue(url, search=True)
            song = await player.play()
            await ctx.send(f"Playing {song.name}")
        else:
            song = await player.queue(url, search=True)
            await ctx.send(f"Queued {song.name}")

    @commands.command()
    async def pause(self, ctx):
        player = music.get_player(guild_id=ctx.guild.id)
        song = await player.pause()
        await ctx.send(f"Paused {song.name}")

    @commands.command()
    async def resume(self, ctx):
        player = music.get_player(guild_id=ctx.guild.id)
        song = await player.resume()
        await ctx.send(f"Resumed {song.name}")

    @commands.command()
    async def stop(self, ctx):
        player = music.get_player(guild_id=ctx.guild.id)
        await player.stop()
        await ctx.send("Stopped")

    @commands.command()
    async def loop(self, ctx):
        player = music.get_player(guild_id=ctx.guild.id)
        song = await player.toggle_song_loop()
        if song.is_looping:
            await ctx.send(f"Enabled loop for {song.name}")
        else:
            await ctx.send(f"Disabled loop for {song.name}")

    @commands.command()
    async def queue(self, ctx):
        player = music.get_player(guild_id=ctx.guild.id)
        embed = discord.Embed(title = "Queue!", description = "")
        try:
            embed.description += {" \n".join([song.name for song in player.current_queue()])}
        except:
            return await ctx.send("There are no songs in queue")
        await ctx.send("The songs are separated by commas")
        await ctx.send(embed = embed)

    @commands.command(aliases=['np'])
    async def nowplaying(self, ctx):
        player = music.get_player(guild_id=ctx.guild.id)
        song = player.now_playing()
        await ctx.send(song.name)

    @commands.command()
    async def skip(self, ctx):
        player = music.get_player(guild_id=ctx.guild.id)
        data = await player.skip(force=True)
        if len(data) == 2:
            await ctx.send(f"Skipped from {data[0].name} to {data[1].name}")
        else:
            await ctx.send(f"Skipped {data[0].name}")

    @commands.command()
    async def volume(self, ctx, vol):
        player = music.get_player(guild_id=ctx.guild.id)
        song, volume = await player.change_volume(float(vol) / 100) # volume should be a float between 0 to 1
        await ctx.send(f"Changed volume for {song.name} to {volume*100}%")

    @commands.command()
    async def remove(self, ctx, index):
        player = music.get_player(guild_id=ctx.guild.id)
        song = await player.remove_from_queue(int(index))
        await ctx.send(f"Removed {song.name} from queue")
    
    @commands.command(aliases=['lyrc']) # adding a aliase to the command so we can use !lyrc or !lyrics
    async def lyrics(self, ctx, *, search=None):
        """A command to find lyrics easily!"""
        
        if not search: # if user hasnt typed anything, throw a error
            embed = discord.Embed(title="No search argument!", description="You havent entered anything, so i couldnt find lyrics!")
            await ctx.reply(embed=embed)
            
            # ctx.reply is available only on discord.py 1.6.0!
            
        song = search.replace(' ', '%20') # replace spaces with "%20"
        
        async with aiohttp.ClientSession() as lyricsSession: # define session
            async with lyricsSession.get(f'https://some-random-api.ml/lyrics?title={song}') as jsondata: # define json data
                if not (300 > jsondata.status >= 200):
                    await ctx.send(f'Recieved Poor Status code of {jsondata.status}.')
                else:
                    lyricsData = await jsondata.json() # load json data
            songLyrics = lyricsData['lyrics'] # the lyrics
            songArtist = lyricsData['author'] # the authors name
            songTitle = lyricsData['title'] # the songs title
            
            try:
                for chunk in [songLyrics[i:i+2000] for i in range(0, len(songLyrics), 2000)]: # if the lyrics extend the discord character limit (2000): split the embed
                    embed = discord.Embed(title=f'{songTitle} by {songArtist}', description=chunk, color=discord.Color.blurple())
                    embed.timestamp = datetime.utcnow()
                    
                    await lyricsSession.close() # closing the session
                    
                    await ctx.reply(embed=embed)
                    
            except discord.HTTPException:
                embed = discord.Embed(title=f'{songTitle} by {songArtist}', description=chunk, color=discord.Color.blurple())
                embed.timestamp = datetime.utcnow()
                
                await lyricsSession.close() # closing the session
                
                await ctx.reply(embed=embed)

def setup(client):
    client.add_cog(Music(client))