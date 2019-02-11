from discord.ext import commands


class Misc(object):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command(pass_context=True)
    async def ping(self, ctx: commands.Context):
        await self.client.say(f"{ctx.message.author.mention} Pong!")


def setup(client: commands.Bot):
    client.add_cog(Misc(client))
