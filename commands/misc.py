from discord.ext import commands
from commands import basewrapper


class Misc(object):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command(pass_context=True)
    async def ping(self, ctx: commands.Context):
        basewrapper.Base().info_logger(f"{ctx.message.author} - Ping!")
        await self.client.say(f"{ctx.message.author.mention} Pong!")

    @commands.command(pass_context=True)
    async def clear(self, ctx: commands.Context, *, number):
        number = int(number)  # Converting the amount of messages to delete to an integer
        counter = 0
        async for x in self.client.logs_from(ctx.message.channel, limit=number):
            if counter < number:
                await self.client.delete_message(x)
                counter += 1


def setup(client: commands.Bot):
    client.add_cog(Misc(client))
