import settings
import discord
from discord.ext import commands

import tweepy
from datetime import datetime, timedelta

class TwitterCog(commands.Cog):
    
    auth = tweepy.OAuthHandler(settings.TWITTER_API_KEY, settings.TWITTER_API_SECRET_KEY)
    auth.set_access_token(settings.TWITTER_ACCESS_TOKEN, settings.TWITTER_ACCESS_TOKEN_SECRET)

    def __init__(self, bot):
        self.bot = bot
        self.api = tweepy.API(TwitterCog.auth)
        self.screen_name = self.api.me().screen_name

    # @commands.command()
    # async def test(self, ctx):
    #     """Test that a Cog is reachable"""
    #     await ctx.send('test successful')

    @commands.command()
    async def rate_limit_tweets(self, ctx):
        """Return status of the Twitter API rate limit"""
        status = self.api.rate_limit_status()
        await ctx.send(
            f'Current rate limit status: \n'
            f'{status}'
        )

    @commands.command()
    async def expire_tweets(self, ctx, days: int, test: bool):
        """
        Delete tweets that are older than X days
        
        Passing 'True' denotes a test delete.
        """
        deletion_count = 0
        ignored_count = 0

        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        timeline = tweepy.Cursor(self.api.user_timeline).items()
        await ctx.send('Total tweets: {timeline}'.format(range(timeline)))
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
            'Total tweets remaining: {timeline}\n Deleted {deletion_count} tweet(s), ignored {ignored_count} tweet(s)'.format(range(timeline))
        )

    @commands.command()
    async def create_list(self, ctx, list_name: str, description: str):
        """Create a private Twitter list object"""
        new_list = self.api.create_list(name=list_name, mode='private', description=description)
        await ctx.send(
            f'Created list object: \n'
            f'name - {new_list.name}\n'
            # f'mode - {new_list.mode}'
            f'created at - {new_list.created_at}'
            # f'owner - {new_list.user}'
        )

    @commands.command(hidden=True)
    async def delete_list(self, ctx, list_name: str):
        """Delete a private Twitter list object"""
        remove_list = self.api.destroy_list(slug=list_name, owner_screen_name=self.screen_name)
        await ctx.send(
            f'Deleted list object: \n'
            f'name - {list_name}'
        )

    @commands.command()
    async def list_lists(self, ctx):
        """Lists available Twitter list objects"""
        lists = self.api.lists_all(screen_name=self.screen_name)
        formatted_lists = [x.name + '\n' for x.name in lists]
        await ctx.send(
            f'Available lists: \n'
            f'{formatted_lists}'
        )

    @commands.command()
    async def add_list_members(self, ctx, list_name: str, *members):
        """
        Add Twitter users to an existing private list
        
        Add up to 100 members to a list at a time.
        Lists may have up to 5,000 members.
        """
        added_members_list = self.api.add_list_members(slug=list_name, owner_screen_name=self.screen_name)
        members_list = self.api.list_members(slug=list_name, owner_screen_name=self.screen_name)
        await ctx.send(
            f'Added members to list: \n'
            f'name - {list_name}\n'
            f'members added - {added_members_list}\n'
            f'all members - {members_list}'
        )

    @commands.command()
    async def remove_list_members(self, ctx, list_name: str, *members):
        """
        Remove Twitter users from an existing private list

        Remove up to 100 members from a list at a time.
        Lists may have up to 5,000 members 
        """
        remove_members = self.api.remove_list_members(slug=list_name, owner_screen_name=self.screen_name)
        list_obj = self.api.get_list(slug=list_name, owner_screen_name=self.screen_name)
        remaining_members_list = [x.slug for x in list_obj.list_members()]
        removed_members_list = [x for x in members]
        await ctx.send(
            f'Removed members from list: \n'
            f'name - {list_name}\n'
            f'members removed - {removed_members_list}\n'
            f'remaining members - {remaining_members_list}'
        )

    @commands.command()
    async def pm_list(self, ctx, list_name):
        """PM list timeline (20 tweets) to user"""
        # TODO: migrate tweets to table.
        timeline = self.api.list_timeline(slug=list_name, owner_screen_name=self.screen_name)
        await ctx.send(
            f'List of tweets from {list_name}\n'
            f'{timeline}'
        )

    @commands.command()
    async def display_list(self, ctx, user_list):
        """Display list timeline (20 tweets) in message channel"""
        pass