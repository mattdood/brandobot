import json
from datetime import datetime, timedelta

import discord
import tweepy
from discord.ext import commands
from tabulate import tabulate

import settings
from cogs.utils.helpers import Helpers


class TwitterCog(commands.Cog):
    """Twitter functionality.

    This cog is used to provide Twitter functionality through Tweepy. The basic implementation
    utilizes `List` objects as curated timelines created by users.

    The `ctx` argument is treated as `self` for commands and is omitted from documentation.

    """

    auth = tweepy.OAuthHandler(
        settings.TWITTER_API_KEY, settings.TWITTER_API_SECRET_KEY
    )
    auth.set_access_token(
        settings.TWITTER_ACCESS_TOKEN, settings.TWITTER_ACCESS_TOKEN_SECRET
    )

    def __init__(self, bot):
        """Twitter Authentication and bot extension.

        Inherits the bot instance and provides API extension with Tweepy.
        Offers access to authenticated screenname and extendable `self.api`.

        Attributes:
            bot: BrandoBot (class `BrandoBot`)
                Instance of the BrandoBot client.
            api: tweepy.API (class `API`)
                Instance of Tweepy API.
            screen_name: `api.me().screen_name`
                Authenticated user screen name
        """
        self.bot = bot
        self.api = tweepy.API(TwitterCog.auth)
        self.screen_name = self.api.me().screen_name

    @commands.command()
    async def rate_limit_tweets(self, ctx):
        """Twitter API rate limit.

        Return status of the Twitter API rate limit as a .txt file.

        Returns:
            logs/: Directory for log files.
            rate_limit.txt: JSON dump of current API rate limit.
            message (class Message): Message including `rate_limit.txt` file.
        """
        status = self.api.rate_limit_status()
        file_path = "logs/rate_limit.txt"
        with open(file_path, "w") as f:
            f.write(json.dumps(status))
            f.close()
        file = discord.File(file_path, filename="rate_limit.txt")
        await ctx.send(file=file, content="Current rate limit status")

    @commands.command()
    async def expire_tweets(self, ctx, days: int, test: bool):
        """Delete tweets that are older than X days.

        Deletes tweets older than a specified timeframe, can be run in test mode
        by using the `True` parameter in `test`.

        Parameters:
            days (int): Number of days to save.
            test (bool): `True` = testing, no delete. `False` = not testing, delete.

        Returns:
            message (class Message): Total tweets deleted and ignored.
        """
        deletion_count = 0
        ignored_count = 0

        cutoff_date = datetime.utcnow() - timedelta(days=days)

        timeline = tweepy.Cursor(self.api.user_timeline).items()
        await ctx.send("**Total tweets:** {timeline}".format(timeline=range(timeline)))
        for tweet in timeline:
            if tweet.created_at < cutoff_date:
                if not test:
                    self.api.destroy_status(tweet.id)
                else:
                    ignored_count += 1
                deletion_count += 1
            else:
                ignored_count += 1
        await ctx.send(
            "**Total tweets remaining:** {timeline}\n Deleted {deletion_count} tweet(s), ignored {ignored_count} tweet(s)".format(
                timeline=range(timeline),
                deletion_count=deletion_count,
                ignored_count=ignored_count,
            )
        )

    @commands.command()
    async def create_list(self, ctx, list_name: str, description: str = None):
        """Create a private Twitter list object.

        A Twitter list is a special Timeline object with only the specified members in it.
        This is a curated feed of content by subject.

        Parameters:
            list_name (str): Twitter list name.
            description (str): Description in quotations (`""`).

        Returns:
            message (class Message): The new list name and creation time.

        TODO:
            * Resolve incorrect `created_at` from 1970 to current year.
        """
        new_list = self.api.create_list(
            name=list_name, mode="private", description=description
        )
        await ctx.send(
            f"**Created list object:** \n"
            f"name - {new_list.name}\n"
            # f'mode - {new_list.mode}'
            # f'created at - {new_list.created_at}'
            # f'owner - {new_list.user}'
        )

    @commands.command(hidden=True)
    async def delete_list(self, ctx, list_name: str):
        """Delete a private Twitter list object.

        Removes a specified `List` object using the `slug`.

        Parameters:
            list_name (str): Slug for the `List` object.

        Returns:
            message (class Message): Delete message confirmation.
        """
        self.api.destroy_list(slug=list_name, owner_screen_name=self.screen_name)
        await ctx.send(f"Deleted list object: \n" f"name - {list_name}")

    @commands.command()
    async def list_lists(self, ctx):
        """Lists available Twitter list objects.

        Creates a list of all `List` objects with names, member counts, and descriptions.

        Returns:
            message (class Message): Messages with list names, member counts, and descriptions.
        """
        lists = self.api.lists_all(screen_name=self.screen_name)
        formatted_lists = []
        for x in lists:
            formatted_lists.append(
                {
                    "name": x.name,
                    "member count": x.member_count,
                    "description": x.description,
                }
            )
        formatted_lists = Helpers.break_message(
            tabulate(formatted_lists, headers="keys", tablefmt="presto")
        )
        await ctx.send("**Available lists:** \n")
        for x in formatted_lists:
            await ctx.send(f"{x}")

    @commands.command()
    async def add_list_members(self, ctx, list_name: str, *members):
        """Add Twitter users to an existing private list.

        Does not require the `@`.
        Adds a list of members to a list.
        Add up to 100 members to a list at a time.
        Lists may have up to 5,000 members.

        Parameters:
            list_name (str): Slug for the `List` object.
            members (*): Unquoted list of usernames without `@`.

        Returns:
            message (class Message): List of members added.
        """
        added_members_list = []
        for x in members:
            self.api.add_list_member(
                slug=list_name, owner_screen_name=self.screen_name, screen_name=x
            )
            added_members_list.append(x)
        await ctx.send(
            f"**Added members to list:** \n"
            f"name - {list_name}\n"
            f"members added - \n"
        )
        messages = Helpers.break_message(added_members_list)
        for x in messages:
            await ctx.send(f"{x}")

    @commands.command()
    async def remove_list_members(self, ctx, list_name: str, *members):
        """Remove Twitter users from an existing private list.

        Does not require the `@`.
        Remove up to 100 members from a list at a time.
        Lists may have up to 5,000 members.

        Parameters:
            list_name (str): Slug for the `List` object.
            members (*): Unquoted list of usernames without `@`.

        Returns:
            message (class Message): List of members removed.
        """
        removed_members_list = []
        for x in members:
            self.api.remove_list_member(
                slug=list_name, owner_screen_name=self.screen_name, screen_name=x
            )
            removed_members_list.append(x)
        await ctx.send(
            f"**Removed members from list:** \n"
            f"name - {list_name}\n"
            f"members removed - \n"
        )
        messages = Helpers.break_message(removed_members_list)
        for x in messages:
            await ctx.send(f"{x}")

    @commands.command()
    async def pm_list(
        self, ctx, list_name: str, count: int = 20, include_rts: bool = True
    ):
        """PM list timeline (default 20 tweets) to user.

        Will send a list of messages with a specified count to the user via Discord PM.
        These are formatted as a table.

        Parameters:
            list_name (str): Slug fro the `List` object.
            Count (int): Default 20, specified count of tweets to return.
            include_rts (bool): Default `True` to include retweets.

        Returns:
            message (class Message): Messages of tweets formatted as a table.
        """
        timeline = self.api.list_timeline(
            slug=list_name,
            owner_screen_name=self.screen_name,
            include_entities=True,
            count=count,
            include_rts=include_rts,
        )
        tweets = TwitterCog._format_tweets(timeline)
        await ctx.author.send(f"**List of tweets from:** {list_name}\n")
        for x in tweets:
            await ctx.author.send(embed=x)

    @commands.command()
    async def display_list(
        self, ctx, list_name: str, count: int = 20, include_rts: bool = True
    ):
        """Display list timeline (default 20 tweets) in message channel

        Will send a list of messages with a specified count to the channel.
        These are formatted as a table.

        Parameters:
            list_name (str): Slug fro the `List` object.
            Count (int): Default 20, specified count of tweets to return.
            include_rts (bool): Default `True` to include retweets.

        Returns:
            message (class Message): Messages of tweets formatted as a table.
        """
        timeline = self.api.list_timeline(
            slug=list_name,
            owner_screen_name=self.screen_name,
            include_entities=True,
            count=count,
            include_rts=include_rts,
        )
        tweets = TwitterCog._format_tweets(timeline)
        await ctx.send(f"**List of tweets from:** {list_name}\n")
        for x in tweets:
            await ctx.send(embed=x)

    @commands.command()
    async def pm_user(self, ctx, screen_name: str, count: int = 20):
        """PM user timeline (default 20 tweets) to user.

        Will send a list of messages with a specified count to the user via Discord PM.
        These are formatted as a table.

        Parameters:
            list_name (str): Slug fro the `List` object.
            Count (int): Default 20, specified count of tweets to return.
            include_rts (bool): Default `True` to include retweets.

        Returns:
            message (class Message): Messages of tweets formatted as a table.
        """
        timeline = self.api.user_timeline(screen_name=screen_name, count=count)
        tweets = TwitterCog._format_tweets(timeline)
        await ctx.author.send(f"**List of tweets from:** {screen_name}\n")
        for x in tweets:
            await ctx.author.send(embed=x)

    @commands.command()
    async def display_user(self, ctx, screen_name: str, count: int = 20):
        """Display user timeline (default 20 tweets) in message channel.

        Will send a list of messages with a specified count to the channel.
        These are formatted as a table.

        Parameters:
            list_name (str): Slug fro the `List` object.
            Count (int): Default 20, specified count of tweets to return.
            include_rts (bool): Default `True` to include retweets.

        Returns:
            message (class Message): Messages of tweets formatted as a table.
        """
        timeline = self.api.user_timeline(screen_name=screen_name, count=count)
        tweets = TwitterCog._format_tweets(timeline)
        await ctx.send(f"**List of tweets from:** {screen_name}\n")
        for x in tweets:
            await ctx.send(embed=x)

    @staticmethod
    def _format_tweets(timeline: list):
        """Formats tweets as a table.

        Creates `Embed` objects from Tweepy `Status` objects.

        Parameters:
            timeline (list): A list of tweet objects.

        Returns:
            table (list): A list of rows modified to be a set character width.

        TODO:
            * media: add `set_image` to Discord message.
        """
        statuses = []
        for x in timeline:
            media = []

            if "media" in x.entities:
                for y in x.entities["media"]:
                    if "media_url_https" in y:
                        if y["media_url_https"] is not "":
                            media.append(y["media_url_https"])
            statuses.append(
                {
                    "text": x.text,
                    "user": x.user.screen_name,
                    "retweet_count": x.retweet_count,
                    "favorite_count": x.favorite_count,
                    "media": [media[0] if len(media) > 0 else ""],
                    "created_at": datetime.strftime(x.created_at, "%m-%d-%Y %I:%M %p"),
                    "link": [link["url"] for link in x.entities["urls"]],
                }
            )
        embeds = []
        for x in statuses:
            embed = discord.Embed(title=x["user"], color=0x1DA1F2)
            embed.set_author(
                name="BrandoBot#9684", url="https://github.com/mattdood/brandobot"
            )
            embed.description = x["text"]
            embed.add_field(name="# RTs", value=x["retweet_count"], inline=True)
            embed.add_field(name="# Favs", value=x["favorite_count"], inline=True)
            # embed.set_image(url=x['media'])
            embed.url = x["link"]
            embed.set_footer(text=f'{x["created_at"]}')
            embeds.append(embed)
        return embeds
