import discord
from discord.ext import commands
from cleverwrap import CleverWrap


def setup(client: commands.Bot):
    client.add_cog(Clever(client))


class Clever(object):
    def __init__(self, client: commands.Bot):
        self.clever = CleverWrap()
        self.client = client
        client.clever_response = self.clever_response

    async def clever_response(self, message):
        response = self.clever.say(message)
        msg = response
        self.clever.reset()
        return msg

    @commands.command(pass_context=True)
    async def clever(self, ctx: commands.Context, *, message: str):
        await self.client.send_typing(ctx.message.channel)
        response = await self.clever_response(message)
        await self.client.say(f"{ctx.message.author.mention} {response}")
