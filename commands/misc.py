from discord.ext import commands
from commands import basewrapper
import time
import requests
import json

class Misc(object):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command(pass_context=True)
    async def ping(self, ctx: commands.Context):
        basewrapper.Base().info_logger(f"{ctx.message.author} - Ping!")
        await self.client.say(f"{ctx.message.author.mention} Pong!")

    @commands.command(pass_context=True)
    async def clear(self, ctx: commands.Context, *, number):
        number = int(number) + 1  # Converting the amount of messages to delete to an integer
        messages = []
        async for x in self.client.logs_from(ctx.message.channel, limit=number):
            messages.append(x)

        msg = await self.client.say(f"<a:loadring:550693379567255552> Deleting {number - 1} messages.")

        for x in messages:
            await self.client.delete_message(x)

        await self.client.edit_message(msg, f":white_check_mark: {number -1} messages removed.")
        time.sleep(2.3)
        await self.client.delete_message(msg)
        basewrapper.Base().info_logger(f"Cleared {number - 1} messages")

    @commands.command(pass_context=True)
    async def steam(self, ctx: commands.Context, *, name):
        try:
            steam_api = basewrapper.Base().get_config_vars("steamapi")
            url = r"http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/"
            payload = {"key": steam_api, "vanityurl": name}

            r = requests.get(url, params=payload)
            steam_comunity_id = r.json()["response"]["steamid"]
            basewrapper.Base().info_logger(steam_comunity_id)

            #Get steam id through community ID obtained above

            print(steam_comunity_id)

            url = r"https://api.steamid.uk/request.php"
            steam_id = basewrapper.Base().get_config_vars("steamid")
            payload = {"api": steam_id, "player": steam_comunity_id, "request": 36, "format": "json"}

            r = requests.get(url, params=payload)
            steamdata = r.json()

            basewrapper.Base().info_logger(f"Searched for {name} steamid: {steamdata}")
            await self.client.say(f"{ctx.message.author.mention} Steam info for {name}: \n"
                                  f"```Steam playername: {steamdata['profile']['playername']} \n"
                                  f"Steam Profile detailed: {steamdata['profile']['steamidurl']} \n"
                                  f"Steam Profile: https://steamcommunity.com/id/{name} \n"
                                  f"SteamID: {steamdata['profile']['steamid']} \n"
                                  f"SteamID3: {steamdata['profile']['steam3']} \n"
                                  f"Bans - Vac {steamdata['profile_status']['vac']} - Trade {steamdata['profile_status']['tradeban']} - Community Ban {steamdata['profile_status']['communityban']}```")

        except Exception as e:
            await self.client.say(f"{ctx.message.author.mention} No account found!")
            basewrapper.Base().info_logger(f"Error found, possibly no account found:  {e}")

    @commands.command(pass_context=True)
    @commands.has_role("root")
    async def setrole(self, ctx: commands.Context, name, role: str):
        await self.client.add_roles(name, role)

    @commands.command(pass_context=True)
    async def poll(self, ctx: commands.Context, name, amount: int):

        return



def setup(client: commands.Bot):
    client.add_cog(Misc(client))
