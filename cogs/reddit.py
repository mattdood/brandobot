import praw
import settings
from datetime import datetime
from cogs.utils.helpers import Helpers
import discord
from discord.ext import commands

class RedditCog(commands.Cog):
    """Reddit functionality.

    This cog is used to provide Reddit functionality.

    The `ctx` argument is treated as `self` for commands and is omitted from documentation.
    """

    reddit = praw.Reddit(
        client_id=settings.REDDIT_CLIENT_ID,
        client_secret=settings.REDDIT_CLIENT_SECRET,
        username=settings.REDDIT_USERNAME,
        password=settings.REDDIT_PASSWORD,
        user_agent=settings.REDDIT_USER_AGENT
    )

    def __init__(self, bot):
        """Reddit Authentication and bot extension.
        
        Inherits the bot instance and provides API extension with Reddit.

        Attributes:
            bot: BrandoBot (class `BrandoBot`)
                Instance of the BrandoBot client.
            reddit: praw.Reddit (class `Reddit`)
                Instance of PRAW Reddit API.
        """
        self.bot = bot
        self.reddit = RedditCog.reddit

    @commands.command()
    async def random_sub(self, ctx):
        """Hot posts from a random subreddit.

        Gets hot posts from random subreddit.

        Returns:
            message (class Embed): A series of embedded messages with `Submission` content.
        """
        random_sub = self.reddit.random_subreddit()
        content = random_sub.hot(limit=5)
        posts = RedditCog._structure_posts(content)
                
        for x in posts:
            await ctx.send(f'{x}')

    @commands.command()
    async def pm_random_sub(self, ctx):
        """PM hot posts from a random subreddit.

        Gets hot posts from random subreddit as a Discord DM.

        Returns:
            message (class Embed): A series of embedded messages with `Submission` content.
        """
        random_sub = self.reddit.random_subreddit()
        content = random_sub.hot(limit=5)
        posts = RedditCog._structure_posts(content)
                
        for x in posts:
            await ctx.author.send(f'{x}')

    @commands.command()
    async def hot_posts(self, ctx, sub: str, count: int = 5):
        """Hot posts from a subreddit.

        Gets hot posts from a sub of your choice. Must provide `count`
        in a int format.

        Parameters:
            sub (str): The subreddit name as a string, without the 'r/'
            count (str): Default `5` posts.
        Returns:
            message (class Embed): A series of embedded messages with `Submission` content.
        """
        subreddit = self.reddit.subreddit(sub)        
        content = subreddit.hot(limit=count)
        posts = RedditCog._structure_posts(content)

        for x in posts:
            await ctx.send(f'{x}')

    @commands.command()
    async def pm_hot_posts(self, ctx, sub: str, count: int = 5):
        """PM hot posts from a subreddit.

        Gets hot posts from a sub of your choice and DMs them to you. 
        Must provide `count` in a int format.

        Parameters:
            sub (str): The subreddit name as a string, without the 'r/'
            count (str): Default `5` posts.
        Returns:
            message (class Embed): A series of embedded messages with `Submission` content.
        """
        subreddit = self.reddit.subreddit(sub)        
        content = subreddit.hot(limit=count)
        posts = RedditCog._structure_posts(content)

        for x in posts:
            await ctx.author.send(f'{x}')

    @commands.command()
    async def top_posts(self, ctx, sub: str, timeframe: str = 'hour'):
        """Top posts from a subreddit.

        Gets top post from a sub of your choice. Must provide `timeframe`
        in a string format.

        Parameters:
            sub (str): The subreddit name as a string, without the 'r/'
            timeframe (str): Default `hour`, other acceptable options are below.
        Returns:
            message (class Embed): A series of embedded messages with `Submission` content.
        """
        subreddit = self.reddit.subreddit(sub)
        content = subreddit.top(timeframe)
        posts = RedditCog._structure_posts(content)

        for x in posts:
            await ctx.send(embed=x)

    @commands.command()
    async def pm_top_posts(self, ctx, sub: str, timeframe: str = 'hour'):
        """PM top posts from a subreddit.

        Gets top post from a sub of your choice and sends them in a DM.
        Must provide `timeframe` in a string format.

        Parameters:
            sub (str): The subreddit name as a string, without the 'r/'
            timeframe (str): Default `hour`, other acceptable options are below.
        Returns:
            message (class Embed): A series of embedded messages with `Submission` content.
        """
        subreddit = self.reddit.subreddit(sub)
        content = subreddit.top(timeframe)
        posts = RedditCog._structure_posts(content)

        for x in posts:
            await ctx.author.send(embed=x)

    @staticmethod
    def _structure_posts(content):
        posts = []
        for x in content:
            posts.append({
                'title': '[' + x.title + '](' + x.url + ')',
                # 'score': str(x.score),
                # 'id': str(x.id),
                # 'url': '<' + x.url + '>'
            })
        return posts
