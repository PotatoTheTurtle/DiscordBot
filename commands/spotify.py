from discord.ext import commands
from commands import basewrapper
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json
import random

#JSON_FILE = r"D:\__GIT\DiscordBot\data\playlist.json"
JSON_FILE = "C:\\Users\\turbiv\\PycharmProjects\\DiscordBot\\data\\playlist.json"
client_secret = basewrapper.Base().get_token("SPOTIFY", "client_secret")
client_id = basewrapper.Base().get_token("SPOTIFY", "client_id")



class Spotify(object):
    def __init__(self, client: commands.Bot):
        self.client = client

    def spotify_playlists(self, name):
        client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
        sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
        user = 'spotify'
        playlist_id = self.get_playlist_id(name, JSON_FILE, "r")
        playlists = sp.user_playlist_tracks(user, playlist_id=playlist_id)
        return playlists

    def spotify_playlist_random_song(self, name):
        playlists = self.spotify_playlists(name)

        songs = {}
        for song in playlists["tracks"]["items"]:
            try:
                songs[song["track"]["name"]] = song["track"]["external_urls"]["spotify"]
            except KeyError:
                print("Looks like custom song aka empty url: %s" % song["track"])

        random_song, random_url = random.choice(list(songs.items()))
        return random_song, random_url

    def get_playlist_id(self, name, jsonfile, char):
        jl = basewrapper.Json().json_load(jsonfile, char)
        for data in jl:
            if data[name]["name"] == name:
                playlist = data[name]["playlist_link"]
                return playlist

    @commands.command(pass_context=True)
    async def setplaylist(self, ctx: commands.Context, *, msg: str):
        """
            Set your playlist ID
        """

        data = basewrapper.Base().jsondata(ctx.message.author, msg)
        jl = basewrapper.Json().json_load(JSON_FILE, "r")

        for j in jl:
            author = str(ctx.message.author)
            if j[author]["name"] == author:
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
            Get a random song from your playlist
        """
        jl = basewrapper.Json().json_load(JSON_FILE, "r")

        for data in jl:
            if data[msg]["name"] != msg:
                await self.client.say(f"{ctx.message.author.mention} No playlist was found!")
                return

        author = str(ctx.message.author)
        song, url = self.spotify_playlist_random_song(author)
        await self.client.say(f"{ctx.message.author.mention} Random song from {msg}: {song}\n"
                              f"{url}")


    @commands.command(pass_context=True)
    async def playlist(self, ctx: commands.Context, *, msg: str):
        """
            Print playlist ID
        """
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
