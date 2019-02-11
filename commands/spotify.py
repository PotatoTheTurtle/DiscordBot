from discord.ext import commands
import pickle
import json

PICKLE_FILE = "C:\\Users\\turbiv\\PycharmProjects\\DiscordBot\\data\\pickledata.p"
JSON_FILE = "C:\\Users\\turbiv\\PycharmProjects\\DiscordBot\\data\\playlist.json"
data_list = []

class Spotify(object):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command(pass_context=True)
    async def setplaylist(self, ctx: commands.Context, *, msg: str):
        data = {f"{ctx.message.author}": {"name": f"{ctx.message.author}", "playlist_link": f"{msg}"}}
        jsonFile = open(JSON_FILE, "r")
        jl = json.load(jsonFile)
        jsonFile.close()

        jl.append(data)

        jsonFile  = open(JSON_FILE, "w+")
        jsonFile.write(json.dumps(jl))
        jsonFile.close()


        await self.client.say(f"{ctx.message.author.mention} Playlist set!")

    @commands.command(pass_context=True)
    async def loadplaylist(self, ctx: commands.Context):
        with open(PICKLE_FILE, 'rb') as fp:
            pickle_load = pickle.load(fp)
            print(pickle_load)
            fp.close()

        await self.client.say(f"{ctx.message.author.mention} Playlist loaded!")

    @commands.command(pass_context=True)
    async def reset(self, ctx: commands.Context):
        with open(PICKLE_FILE, 'wb') as fp:
            data = []
            pickle.dump(data, fp, protocol=pickle.HIGHEST_PROTOCOL)

        await self.client.say(f"{ctx.message.author.mention} Empty!")

def setup(client: commands.Bot):
    client.add_cog(Spotify(client))
