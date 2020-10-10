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

    # @commands.command()
    # async def test(self, ctx):
    #     """Test that a Cog is reachable"""
    #     await ctx.send('test successful')

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
    async def pm_tweets(self, ctx, *usernames):
        pass
