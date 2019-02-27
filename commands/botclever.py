import discord
from discord.ext import commands
from cleverwrap import CleverWrap
import requests


def setup(client: commands.Bot):
    client.add_cog(Clever(client))


class Clever(object):
    def __init__(self, client: commands.Bot):
        self.clever = CleverWrap("CC8sl6pv19pwWpQhE1wk-1edDPw")
        self.client = client
        client.clever_response = self.clever_response

    async def clever_response(self, message):
        response = self.clever.say(message)
        msg = response
        self.clever.reset()
        return msg


    @commands.command(pass_context=True)
    async def clever_convo(self, ctx: commands.Context, *, message: str):
        #self.clever.conversation()
        data = {
                "user": "PfIGLHA3k5dCcmd3",
                "key": "N3BYYM9xcW547KC7dz7uvXGsR2JuZPps",
                "nick": "ivan.turbin",
                "text": message
                }
        r = requests.post(r"https://cleverbot.io/1.0/ask", data)
        print(r.json())


    @commands.command(pass_context=True)
    async def clever(self, ctx: commands.Context, *, message: str):
        await self.client.send_typing(ctx.message.channel)
        response = await self.clever_response(message)
        await self.client.say(f"{ctx.message.author.mention} {response}")

    @commands.command(pass_context=True)
    async def convo(self, ctx: commands.Context, *, msg: str):
        await self.client.send_typing(ctx.message.channel)
        response = await self.clever_response(message)
        await self.client.say(f"{ctx.message.author.mention} {response}")

