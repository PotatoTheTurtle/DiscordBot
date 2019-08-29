from discord.ext import commands
import discord
from commands import basewrapper
import asyncio
import requests

import valve.source
import valve.source.a2s
import valve.source.master_server

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
    async def steam(self, ctx: commands.Context, *, url):
        try:
            name = url.content[30:]
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
        try:
            basewrapper.Database().write_suggestion(f"{ctx.message.author}: {suggestion}")
            await self.client.say(f"{ctx.message.author.mention} Thanks for the suggestion! :3")
        except Exception as e:
            basewrapper.Base().info_logger(f"Error: {e}")
            await self.client.say(f"{ctx.message.author.mention} Problem occured while adding suggestion, please try again later.")

    @commands.command(pass_context=True)
    async def server(self, ctx: commands.Context):
        """
        :return: max 2000 characters for an embedded message (that is kinda gay and fagish)
        """
        ip = basewrapper.Base().get_config_vars("GMOD_ADDRESS")
        port = basewrapper.Base().get_config_vars("GMOD_PORT")
        url = basewrapper.Base().get_config_vars("GMOD_URL")
        address = (ip, int(port))
        info = None
        try:
            try:
                with valve.source.a2s.ServerQuerier(address) as server:
                    info = server.info()

            except valve.source.NoResponseError:
                print("Master server request timed out!")

            embed = discord.Embed(title=f'{info.values["server_name"]}')
            embed.add_field(name='Players', value=f'{info.values["player_count"]} / {info.values["max_players"]}', inline=True)
            embed.add_field(name='Gamemode', value=f'{info.values["game"]}', inline=True)
            embed.add_field(name='Map', value=f'{info.values["map"]}', inline=True)
            embed.set_footer(text=f"Join server! {url}")
            await self.client.say(embed=embed)
        except:
            await self.client.say(f"{ctx.message.author.mention} Server either down or restarting. Please try again later.")

    @commands.command(pass_context=True)
    async def stats(self, ctx: commands.Context, *,player=None):
        data = basewrapper.Database().get_player_data()
        top = None
        array = []
        totals = {}
        if player is None:
            for k, v in data:
                totals[k] = totals.get(k, 0) + v
                top = sorted(map(list, totals.items()))

            for data in top:
                i = 0
                print(top)
                index_int = max([sublist[-1] for sublist in top])
                if data[1] != index_int:
                    return
                index = data.index(index_int)
                money, name = max([sublist[-1] for sublist in top]), max([sublist[0] for sublist in top])
                array.append([money, name])
                print(index)
                data.pop(index_int)
                if i == 0:
                    return
                i += 1

            print(array)

            embed = discord.Embed(title="Top 10 Richest people")
            embed.add_field(name="Top 1", value=f'{top[0][0]} - ${top[0][1]}', inline=False)
            embed.add_field(name="Top 2", value=f'{top[1][0]} - ${top[1][1]}', inline=False)
            embed.add_field(name="Top 3", value=f'{top[2][0]} - ${top[2][1]}', inline=False)
            embed.add_field(name="Top 4", value=f'{top[3][0]} - ${top[3][1]}', inline=False)
            embed.add_field(name="Top 5", value=f'{top[4][0]} - ${top[4][1]}', inline=False)
            embed.add_field(name="Top 6", value=f'{top[5][0]} - ${top[5][1]}', inline=False)
            embed.add_field(name="Top 7", value=f'{top[6][0]} - ${top[6][1]}', inline=False)
            embed.add_field(name="Top 8", value=f'{top[7][0]} - ${top[7][1]}', inline=False)
            embed.add_field(name="Top 9", value=f'{top[8][0]} - ${top[8][1]}', inline=False)
            embed.add_field(name="Top 10", value=f'{top[9][0]} - ${top[9][1]}', inline=False)
            await self.client.say(embed=embed)
            return
        try:
            for info in data:
                name = info[0]
                if name == player:
                    money = info[1]
                    await self.client.say(f"{ctx.message.author.mention} Stats for {name}: Balance ${money}")
                    return
                else:
                    continue
            raise Exception

        except:
            await self.client.say(
                f"{ctx.message.author.mention} Player not found. Use rp name example: 'Ivan Rockford'")

    @commands.command(pass_context=True)
    async def workshop(self, ctx: commands.Context):
        await self.client.say(f"{ctx.message.author.mention} https://steamcommunity.com/sharedfiles/filedetails/?id=1549043958")


    @commands.command(pass_context=True)
    async def help(self, ctx: commands.Context):
        await self.client.say(
            f"{ctx.message.author.mention} List of the commands:\n"
            f"```"
            f"Command                      |Description                                   \n"
            f"Chatbot:                     |                                              \n"
            f"  @TurtleBot <message>       | Talk to chatbot                              \n"
            f"                             |\n"
            f"Reddit:                      |                                              \n"
            f"  -reddit <subreddit>        | Get random post from requested subreddit     \n"
            f"                             |\n"
            f"Misc:                        |                                              \n"
            f"  -ping                      |Pings the bot to see if its alive             \n"
            f"  -help                      |Lists you the commands                        \n"
            f"  -suggestion <text>         |Sends a suggestion to the developer!          \n"
            f"  -steam <steam_url>         |Provides steam information                    \n"
            f"  -clear <amount of msg>     |Use mega fancy message clear function         \n"
            f"                             |\n"
            f"Spotify:                     |                                              \n"
            f"  -setplaylist <playlistid>  |Last letters\digits in spotify playlist url   \n"
            f"  -playlist <Discord#6969>   |View selected users playlist id               \n"
            f"  -rngplaylist <Discord#6969>|Get random preview from selected user playlist\n"
            f"\n"
            f"For bugs/info contact PotatoTurtle#1337\n"
            f"GitHub: https://github.com/PotatoTheTurtle```")


    @commands.command(pass_context=True)
    @commands.has_role("root")
    async def setrole(self, ctx: commands.Context, rolename: str):
        member = ctx.message.author
        role = discord.utils.get(member.server.roles, name=rolename)
        await self.client.add_roles(member, role)

    @commands.command(pass_context=True)
    async def poll(self, ctx: commands.Context, title: str, *, questions: str):
        options = questions.split(',')
        embed = discord.Embed(title=title)
        for option in options:
            embed.add_field(name='Vote:', value=f'{option}')
        await self.client.say(embed=embed)
        return

    @commands.command(pass_context=True)
    @commands.has_role("root")
    async def bug(self, ctx: commands.Context, ):


        return

def setup(client: commands.Bot):
    client.add_cog(Misc(client))
