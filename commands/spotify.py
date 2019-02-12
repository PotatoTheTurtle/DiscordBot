from discord.ext import commands
from commands import basewrapper
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json

JSON_FILE = r"D:\__GIT\DiscordBot\data\playlist.json"
#JSON_FILE = "C:\\Users\\turbiv\\PycharmProjects\\DiscordBot\\data\\playlist.json"
client_secret = "4bd50f140f3349cfac0ef875ab10718e"
client_id = "fb551e5fad8f4f8ab9c838fa552d9a70"



class Spotify(object):
    def __init__(self, client: commands.Bot):
        self.client = client

    def spotify_playlist_content(self):
        client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
        sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
        user = 'spotify'

        playlists = sp.user_playlist_tracks(user, playlist_id=playlist_link)
        for song in playlists["tracks"]["items"]:
            print(song["track"]["name"])

    @commands.command(pass_context=True)
    async def setplaylist(self, ctx: commands.Context, *, msg: str):
        """
        Writes playlist ID to playlist.json
        :param msg: playlist ID
        :return: write playlist_id to json
        """
        data = {f"{ctx.message.author}": {"name": f"{ctx.message.author}", "playlist_link": f"{msg}"}}
        jsonfile = open(JSON_FILE, "r")
        jl = json.load(jsonfile)
        jsonfile.close()

        for j in jl:
            author = str(ctx.message.author)
            if j[author]["name"] == author:
                basewrapper.Base().warning_logger(f"User data already exists: {j}")
                j[author]["playlist_link"] = msg
            else:
                jl.append(data)

        jsonfile = open(JSON_FILE, "w+")
        jsonfile.write(json.dumps(jl))
        jsonfile.close()
        basewrapper.Base().info_logger(f"{self.client.user.id} - Playlist set!")
        await self.client.say(f"{ctx.message.author.mention} Playlist set!")

    @commands.command(pass_context=True)
    async def rngplaylist(self, ctx: commands.Context, *, msg: str):
        """
        :return Get random song from users set playlist (Spotify)
        """
        jsonfile = open(JSON_FILE, "r")
        jl = json.load(jsonfile)
        jsonfile.close()

        playlist_link = None

        for data in jl:
            if data[msg]["name"] == msg:
                playlist_link = data[msg]["playlist_link"]
            else:
                await self.client.say(f"{ctx.message.author.mention} No playlist was found!")
                return

        self.spotify_playlist_content()

    @commands.command(pass_context=True)
    async def playlist(self, ctx: commands.Context, *, msg: str):
        jsonfile = open(JSON_FILE, "r")
        jl = json.load(jsonfile)
        jsonfile.close()

        for data in jl:
            if data[msg]["name"] == msg:
                playlist = data[msg]["playlist_link"]
                await self.client.say(f"{ctx.message.author.mention} Playlist: {playlist}")
                return
        await self.client.say(f"{ctx.message.author.mention} No playlist was found!")


    @commands.command(pass_context=True)
    async def reset(self, ctx: commands.Context):
        with open(JSON_FILE, 'wb') as fp:
            data = []
            json.dump(data, fp)

        await self.client.say(f"{ctx.message.author.mention} Empty!")

def setup(client: commands.Bot):
    client.add_cog(Spotify(client))
