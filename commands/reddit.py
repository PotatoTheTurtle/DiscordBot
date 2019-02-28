from discord.ext import commands
import praw
import random
from commands import basewrapper


class Memes(object):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.c_reddit = praw.Reddit(client_id=basewrapper.Base().get_token("REDDIT", "client_id"),
                             client_secret=basewrapper.Base().get_token("REDDIT", "client_secret"),
                             password=basewrapper.Base().get_token("REDDIT", "password"),
                             user_agent=basewrapper.Base().get_token("REDDIT", "user_agent"),
                             username=basewrapper.Base().get_token("REDDIT", "username"))


    @commands.command(pass_context=True)
    async def reddit(self, ctx: commands.Context, *, subreddit: str):
        reddit_posts = []
        for post in self.c_reddit.subreddit(subreddit).hot(limit=45):
            if post.url.__contains__(".png" or ".jpg" or ".gifv" or ".gif"):
                reddit_posts.append(post.url)

        basewrapper.Base().info_logger(f"Get Reddit post: {subreddit}")
        await self.client.say(f"{ctx.message.author.mention} Random post from r/{subreddit}: {random.choice(reddit_posts)}")


def setup(client: commands.Bot):
    client.add_cog(Memes(client))
