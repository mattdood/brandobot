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
        self.screen_name = self.api.me.screen_name

    # @commands.command()
    # async def test(self, ctx):
    #     """Test that a Cog is reachable"""
    #     await ctx.send('test successful')

    @commands.command()
    async def rate_limit_tweets(self, ctx):
        """Return status of the Twitter API rate limit"""
        try:
            status = self.api.rate_limit_status()
            await ctx.send(
                f'Current rate limit status: '
                f'{status}'
            )
        except Exception as e:
            await ctx.send(f'Rate limit failed, exception: {e}')

    @commands.command()
    async def expire_tweets(self, ctx, days: int, test: bool):
        """Delete tweets that are older than X days"""
        deletion_count = 0
        ignored_count = 0

        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        try:
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
                f'Total tweets remaining: {timeline}'.format(range(timeline)-deletion_count)
                f'Deleted {deletion_count} tweet(s), ignored {ignored_count} tweet(s)'
            )
        except Exception as e:
            await ctx.send(f'Expire tweets failed, exception: {e}')

    @commands.command()
    async def create_list(self, ctx, list_name: str, description: str):
        """Create a private Twitter list object"""
        new_list = self.api.create_list(list_name, private, description)
        await ctx.send(
            f'Created list object: '
            f'name - {new_list.name}'
            f'mode - {new_list.member_count}'
            f'created at - {new_list.created_at}'
            f'owner - {new_list.user}'
        )

    @commands.command()
    async def add_list_members(self, ctx, list_name: str, *members):
        """
        Add Twitter users to a private list created
        
        Add up to 100 members to a list at a time.
        Lists may have up to 5,000 members.
        """
        self.api.add_list_members(slug=list_name, owner_screen_name=self.screen_name)

    @commands.command()
    async def remove_list_members(self, ctx list_name: str, *members):
        """
        Remove Twitter users from a private list

        Remove up to 100 members from a list at a time.
        Lists may have up to 5,000 members 
        """
        remove_members = self.api.remove_list_members(slug=list_name, owner_screen_name=self.screen_name)
        list_obj = self.api.get_list(slug=list_name, owner_screen_name=self.screen_name)
        remaining_members_list = [x.slug for x in list_obj.list_members()]
        removed_members_list = [x for x in members]
        await ctx.send(
            f'Removed members from list: '
            f'name - {new_list.name}'
            f'members removed - {removed_members_list}'
            f'remaining members - {remaining_members_list}'
            f'owner - {new_list.user}' # TODO finish output
        )

    @commands.command()
    async def pm_list(self, ctx, user_list):
        """PM list timeline (20 tweets) to user"""
        # TODO: migrate tweets to table.
        tweets = []
        for username in usernames:
            tweets.append(self.api.user_timeline(username))
        
