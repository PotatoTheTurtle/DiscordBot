from discord.ext import commands
import praw
import random
from commands import basewrapper


class Reddit(object):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.reddit = praw.Reddit(client_id='BAGbQmlllg3abA',
                             client_secret='wl8mQD6zrevyqzb6pabGOPyXSDE',
                             password='ivan123.',
                             user_agent='discord bot by PotatoTurtle#1337',
                             username='turtlebot_discord')


    @commands.command(pass_context=True)
    async def meme(self, ctx: commands.Context, *, subreddit: str):
        reddit_posts = []
        for post in self.reddit.subreddit(subreddit).hot(limit=45):
            if post.url.__contains__(".png" or ".jpg"):
                reddit_posts.append(post.url)

        print(reddit_posts)
        await self.client.say(f"{ctx.message.author.mention} Random post from r/{subreddit}: {random.choice(reddit_posts)}")


def setup(client: commands.Bot):
    client.add_cog(Reddit(client))
