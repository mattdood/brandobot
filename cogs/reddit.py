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
        Options:
            timeframe (str): Available options: "hour", "day", "week", "month", "year", "all".
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
        Options:
            timeframe (str): Available options: "hour", "day", "week", "month", "year", "all".
        Returns:
            message (class Embed): A series of embedded messages with `Submission` content.
        """
        subreddit = self.reddit.subreddit(sub)
        content = subreddit.top(timeframe)
        posts = RedditCog._structure_posts(content)

        for x in posts:
            await ctx.author.send(embed=x)

    @commands.command()
    async def pm_comments(self, ctx, post_id: str, sort: str = 'top'):
        """PM a list of comments from a `Submission`.

        Send a Discord message of comments from a `Submission` object.
        Takes parameters for different sort options for comments. 
        Parses the `CommentForest` return from `Submission`.

        Parameters:
            post_id (str): The `post_id` from a Reddit post.
            sort (str): Default `top`, has other options.
        Options:
            sort (str): Available options: "confidence", "controversial", "new", "old", "q&a", "top".
        Returns:
            message (class Embed): A series of embedded messages with `Comment` content.
        """
        submission = self.reddit.submission(post_id)
        submission.comment_sort = sort 
        content = submission.comments.list()
        comments = RedditCog._structure_comments(content)

        for x in comments:
            await ctx.author.send(embed=x)

    @commands.command()
    async def pm_more_comments(self, ctx, comment_id: str, sort: str = 'top'):
        """PM a list of comments from a `Comment`.

        Send a Discord message of comments from a `Comment` object.
        Takes parameters for different sort options for comments. 
        Parses the `CommentForest` return from `Comment`.

        Parameters:
            comment_id (str): The `comment_id` from a Reddit comment.
            sort (str): Default `top`, has other options.
        Options:
            sort (str): Available options: "confidence", "controversial", "new", "old", "q&a", "top".
        Returns:
            message (class Embed): A series of embedded messages with `Comment` content.
        """
        comment = self.reddit.comment(comment_id)
        comment.refresh()
        comment.reply_sort = sort
        content = comment.replies
        comments = RedditCog._structure_comments(content)

        for x in comments:
            await ctx.author.send(embed=x) 

    @staticmethod
    def _structure_posts(content: list):
        """Structure Reddit posts.

        Create `Embed` objects as Discord messages for each post.
        Structured from a dictionary of content data from each message.

        Parameters:
            content (class Submission): A list of `Submission` subreddit objects.

        Returns:
            embeds (class Embed): A formatted list of `Embed` messages to be sent to Discord.
        """
        posts = []
        for x in content:
            posts.append({
                'title': x.title,
                'subreddit': x.subreddit_name_prefixed,
                'self_text': x.selftext,
                'thumbnail': x.thumbnail,
                'score': str(x.score),
                'num_comments': x.num_comments,
                'flair': x.link_flair_text,
                'post_id': x.id,
                'post_author': x.author.name,
                'url': x.url,
                'created_at': datetime.utcfromtimestamp(x.created_utc).strftime('%m-%d-%Y %H:%M:%S')
            })
        embeds = []
        for x in posts:
            embed = discord.Embed(title=x['title'], color=0xFF5700)
            embed.set_author(name='BrandoBot#9684', url='https://github.com/mattdood')
            embed.description = x['self_text']
            embed.set_image(url=x['thumbnail'])
            embed.url = x['url']
            embed.add_field(name='Score', value=x['score'], inline=True)
            embed.add_field(name='# Comments', value=x['num_comments'], inline=True)
            embed.add_field(name='Flair', value=x['flair'], inline=True)
            embed.add_field(name='Subreddit', value=x['subreddit'], inline=True)
            embed.add_field(name='Post ID', value=x['post_id'], inline=True)
            embed.add_field(name='OP', value=x['post_author'], inline=True)
            embed.set_footer(text=f'Use `!post_comments <post_id>` to read more!  |  {x["created_at"]}')
            embeds.append(embed)
        return embeds

    @staticmethod
    def _structure_comments(content: list):
        """Structure `Submission` comments.

        Create `Embed` objects as Discord messages for each post comment.
        Structured from a dictionary of content data from each message.

        Parameters:
            content (class CommentForest): A list of `Comment` subreddit objects.

        Returns:
            embeds (class Embed): A formatted list of `Embed` messages to be sent to Discord.
        """
        comments = []
        for x in content:
            comments.append({
                'submission_name': x.submission.title,
                'subreddit': x.subreddit.display_name,
                'body': x.body,
                'score': str(x.score),
                'num_comments': len(x.replies),
                'comment_id': x.id,
                'comment_author': x.author.name,
                'url': x.permalink,
                'created_at': datetime.utcfromtimestamp(x.created_utc).strftime('%m-%d-%Y %H:%M:%S')
            })
        embeds = []
        for x in comments:
            embed = discord.Embed(title=x['submission_name'], color=0xFF5700)
            embed.set_author(name='BrandoBot#9684', url='https://github.com/mattdood')
            embed.description = x['body']
            embed.url = 'https://reddit.com' + x['url']
            embed.add_field(name='Score', value=x['score'], inline=True)
            embed.add_field(name='# Comments', value=x['num_comments'], inline=True)
            embed.add_field(name='Subreddit', value=x['subreddit'], inline=True)
            embed.add_field(name='Comment ID', value=x['comment_id'], inline=True)
            embed.add_field(name='OP', value=x['comment_author'], inline=True)
            embed.set_footer(text=f'Use `!pm_more_comments <comment_id>` to read more!  |  {x["created_at"]}')
            embeds.append(embed)
        return embeds