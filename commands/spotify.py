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
        try:
            jsonFile = open(JSON_FILE, "r")
            jl = json.load(jsonFile)
            jsonFile.close()

            jl.append(data)

            jsonFile  = open(JSON_FILE, "w+")
            jsonFile.write(json.dumps(jl))
            jsonFile.close()
            basewrapper.Base().info_logger(f"{self.client.user.id} - Playlist set!")
        except Exception as error:
            basewrapper.Base().error_logger(f"{self.client.user.id} - JSON APPEND ERROR! ERROR: {error}")
        await self.client.say(f"{ctx.message.author.mention} Playlist set!")


    @commands.command(pass_context=True)
    async def reset(self, ctx: commands.Context):
        with open(JSON_FILE, 'wb') as fp:
            data = []
            json.dump(data, fp)

        await self.client.say(f"{ctx.message.author.mention} Empty!")

def setup(client: commands.Bot):
    client.add_cog(Spotify(client))
