from discord.ext import commands
from commands import basewrapper
import time


class Misc(object):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command(pass_context=True)
    async def ping(self, ctx: commands.Context):
        basewrapper.Base().info_logger(f"{ctx.message.author} - Ping!")
        await self.client.say(f"{ctx.message.author.mention} Pong!")

    @commands.command(pass_context=True)
    async def clear(self, ctx: commands.Context, *, number):
        number = int(number) + 2  # Converting the amount of messages to delete to an integer
        messages = []
        async for x in self.client.logs_from(ctx.message.channel, limit=number):
            messages.append(x)

        loading = await self.client.say(f"<a:loadring:550693379567255552> Deleting {number - 2} messages.")

        for x in messages:
            await self.client.delete_message(x)

        await self.client.delete_message(loading)

        msg = await self.client.say(f":white_check_mark: {number -2} messages removed.")
        time.sleep(2.3)
        await self.client.delete_message(msg)
        basewrapper.Base().info_logger(f"Cleared {number - 2} messages")



def setup(client: commands.Bot):
    client.add_cog(Misc(client))
