import praw
import settings
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
    async def random_subreddit(self, ctx):
        """Discover a random sub.

        Fetch 5 of the most recent posts from a random subreddit.

        Returns:
            message (class Message): Subreddit posts and links.
        """
        random_sub = self.reddit.random_subreddit()
        
        posts = RedditCog._fetch_recent(random_sub, 5)
        posts = Helpers.break_message(posts)
                
        await ctx.send(
            f'Fetched a random subreddit: \n'
            f'{random_sub.display_name}\n'
        )
        for x in posts:
            await ctx.send(f'{x}')

    @commands.command()
    async def hot_posts(self, ctx, sub: str, count=None):
        subreddit = self.reddit.subreddit(sub).hot(limit=count)
        
        posts = RedditCog._structure_posts(subreddit)
        posts = Helpers.break_message(posts)
                
        await ctx.send(
            f'Fetched posts from: \n'
            f'{subreddit.display_name}\n'
        )
        for x in posts:
            await ctx.send(f'{x}')

    @commands.command()
    async def top_posts(self, ctx, sub: str, timeframe=None):
        subreddit = self.reddit.subreddit(sub)
        content = subreddit.top(timeframe)

        posts = RedditCog._structure_posts(content)
                
        await ctx.send(
            f'**Fetched posts from:**\n'
            f'`{subreddit.display_name}`\n'
            f'**Posts:**\n'
        )
        # TODO
        for x in posts:
            embed = discord.Embed(title=x['title'], color=0x00ff00)
            embed.add_field(name=x[])
            await ctx.send(

                embed=value
            )

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
