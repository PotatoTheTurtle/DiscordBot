from discord.ext import commands
from commands import basewrapper
import asyncio
import requests

class Misc(object):
    def __init__(self, client: commands.Bot):
        self.client = client

    def steamdata(self, steam_comunity_id):
        url = r"https://api.steamid.uk/request.php"
        steam_id = basewrapper.Base().get_config_vars("steamid")
        payload = {"api": steam_id, "player": steam_comunity_id, "request": 36, "format": "json"}

        r = requests.get(url, params=payload)
        steamdata = r.json()
        return steamdata

    def steamcommuinityid(self, name):
        steam_api = basewrapper.Base().get_config_vars("steamapi")
        url = r"http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/"
        payload = {"key": steam_api, "vanityurl": name}

        r = requests.get(url, params=payload)
        steam_comunity_id = r.json()["response"]["steamid"]
        basewrapper.Base().info_logger(steam_comunity_id)
        return steam_comunity_id

    def value_converter_decorator(self, value, true, false):
        if value == 0:
            return false
        return true

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
        asyncio.sleep(2.3)
        await self.client.delete_message(msg)
        basewrapper.Base().info_logger(f"Cleared {number - 1} messages")

    @commands.command(pass_context=True)
    async def steam(self, ctx: commands.Context, *, name):
        try:
            steam_community_id = self.steamcommuinityid(name)
            steamdata = self.steamdata(steam_community_id)

            basewrapper.Base().info_logger(f"Searched for {name} steam info.")
            await self.client.say(f"{ctx.message.author.mention} Steam info for {name}: \n"
                                  f"```Steam playername: {steamdata['profile']['playername']} \n"
                                  f"Steam Profile detailed: {steamdata['profile']['steamidurl']} \n"
                                  f"Steam Profile: https://steamcommunity.com/id/{name} \n"
                                  f"SteamID: {steamdata['profile']['steamid']} \n"
                                  f"SteamID3: {steamdata['profile']['steam3']} \n"
                                  f"Bans: Vac Ban {self.value_converter_decorator(steamdata['profile_status']['vac'], 'Yes', 'No')} - Trade Ban {self.value_converter_decorator(steamdata['profile_status']['tradeban'], 'Yes', 'No')} - Community Ban {self.value_converter_decorator(steamdata['profile_status']['communityban'], 'Yes', 'No')}```")

        except Exception as e:
            await self.client.say(f"{ctx.message.author.mention} No account found!")
            basewrapper.Base().info_logger(f"Error found, possibly no account found:  {e}")

    @commands.command(pass_context=True)
    async def suggestion(self, ctx: commands.Context, *, suggestion: str):
        text_file = basewrapper.Base().get_config_vars("TEXT_FILE")
        try:
            with open(text_file, "a") as f:
                f.write(f"{ctx.message.author.mention} - {suggestion} \n")
                f.close()
                await self.client.say(f"{ctx.message.author.mention} Thanks for the suggestion! :3")
        except Exception as e:
            await self.client.say(f"{ctx.message.author.mention} Problem occured while adding suggestion, please try again later.")


    @commands.command(pass_context=True)
    @commands.has_role("root")
    async def setrole(self, ctx: commands.Context, name, role: str):
        await self.client.add_roles(name, role)

    @commands.command(pass_context=True)
    async def poll(self, ctx: commands.Context, name, amount: int):

        return



def setup(client: commands.Bot):
    client.add_cog(Misc(client))
