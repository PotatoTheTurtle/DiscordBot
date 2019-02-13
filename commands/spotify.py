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

    def spotify_playlist_content(self, name):
        client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
        sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
        user = 'spotify'
        playlist_id = self.get_playlist_id(name, JSON_FILE, "r")
        playlists = sp.user_playlist_tracks(user, playlist_id=playlist_id)
        songs = []
        for song in playlists["tracks"]["items"]:
            songs.append(song["track"]["name"])
            return songs

    def get_playlist_id(self, name, jsonfile, char):
        jl = basewrapper.Json().json_load(jsonfile, char)
        for data in jl:
            if data[name]["name"] == name:
                playlist = data[name]["playlist_link"]
                return playlist

    @commands.command(pass_context=True)
    async def setplaylist(self, ctx: commands.Context, *, msg: str):
        """
        Writes playlist ID to playlist.json
        :param msg: playlist ID
        :return: write playlist_id to json
        """

        data = basewrapper.Base().jsondata(ctx.message.author, msg)
        jl = basewrapper.Json().json_load(JSON_FILE, "r")

        for j in jl:
            author = str(ctx.message.author)
            if j[author]["name"] == author:
                print("xxy")
                basewrapper.Base().warning_logger(f"User data already exists: {j}")
                j[author]["playlist_link"] = msg
                basewrapper.Base().info_logger(f"{self.client.user.id} - Playlist set!")
                await self.client.say(f"{ctx.message.author.mention} Playlist set!")
                return

        jl.append(data)

        print(jl)
        basewrapper.Json().json_write(JSON_FILE, "w+", jl)
        basewrapper.Base().info_logger(f"{self.client.user.id} - Playlist set!")
        await self.client.say(f"{ctx.message.author.mention} Playlist set!")

    @commands.command(pass_context=True)
    async def rngplaylist(self, ctx: commands.Context, *, msg: str):
        """
        :return Get random song from users set playlist (Spotify)
        TODO FIX RANDOM - RANDOM IN BASE WRAPPER
        """
        jl = basewrapper.Json().json_load(JSON_FILE, "r")

        for data in jl:
            if data[msg]["name"] != msg:
                await self.client.say(f"{ctx.message.author.mention} No playlist was found!")
                return

        author = str(ctx.message.author)
        await self.client.say(f"{ctx.message.author.mention} Random song from {msg}: "
                              f"{basewrapper.Base().randomizer(self.spotify_playlist_content(author))}")


    @commands.command(pass_context=True)
    async def playlist(self, ctx: commands.Context, *, msg: str):
        jl = basewrapper.Json().json_load(JSON_FILE, "r")
        for data in jl:
            if data[msg]["name"] == msg:
                playlist = data[msg]["playlist_link"]
                await self.client.say(f"{ctx.message.author.mention} Playlist id: {playlist}")
                return
        await self.client.say(f"{ctx.message.author.mention} No playlist was found!")


    @commands.command(pass_context=True)
    async def reset(self, ctx: commands.Context):
        with open(JSON_FILE, 'w') as fp:
            data = []
            json.dump(data, fp)

        await self.client.say(f"{ctx.message.author.mention} Empty!")

def setup(client: commands.Bot):
    client.add_cog(Spotify(client))
