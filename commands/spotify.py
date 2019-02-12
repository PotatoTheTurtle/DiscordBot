from discord.ext import commands
from commands import basewrapper
import json

JSON_FILE = r"D:\__GIT\DiscordBot\data\playlist.json"
#JSON_FILE = "C:\\Users\\turbiv\\PycharmProjects\\DiscordBot\\data\\playlist.json"

class Spotify(object):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command(pass_context=True)
    async def setplaylist(self, ctx: commands.Context, *, msg: str):
        data = {f"{ctx.message.author}": {"name": f"{ctx.message.author}", "playlist_link": f"{msg}"}}
        jsonfile = open(JSON_FILE, "r")
        jl = json.load(jsonfile)
        jsonfile.close()

        print(jl)
        for j in jl:
            print(j)
            if j[ctx.message.author]["name"] == ctx.message.author:
                basewrapper.Base().warning_logger(f"User data already exists: {j}")
                j[ctx.message.author]["playlist_link"] = msg

        jl.append(data)

        jsonfile = open(JSON_FILE, "w+")
        jsonfile.write(json.dumps(jl))
        jsonfile.close()
        basewrapper.Base().info_logger(f"{self.client.user.id} - Playlist set!")
        await self.client.say(f"{ctx.message.author.mention} Playlist set!")

    @commands.command(pass_context=True)
    async def playlist(self, ctx: commands.Context, *, msg: str):
        jsonfile = open(JSON_FILE, "r")
        jl = json.load(jsonfile)
        jsonfile.close()

        for data in jl:
            if data == ctx.message.author:
                playlist = jl[ctx.message.author]["playlist_link"]
                await self.client.say(f"{ctx.message.author.mention} Playlist: {playlist}")


        await self.client.say(f"{ctx.message.author.mention} No playlist was found!")


    @commands.command(pass_context=True)
    async def reset(self, ctx: commands.Context):
        with open(JSON_FILE, 'wb') as fp:
            data = []
            json.dump(data, fp)

        await self.client.say(f"{ctx.message.author.mention} Empty!")

def setup(client: commands.Bot):
    client.add_cog(Spotify(client))
