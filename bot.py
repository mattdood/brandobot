import discord
from discord.ext import commands
import settings

from cogs.general import GeneralCog
from cogs.reddit import RedditCog
from cogs.twitter import TwitterCog

# register intents
intents = discord.Intents.default()
intents.members = True

class BrandoBot(commands.Bot):
    
    async def on_ready(self):
        """Logging information to server on startup.
        
        Logs information about the bot and the guild to the terminal.

        Returns:
            message (class Message): A message with the `user`, `guild.name`, `guild.id`, and guild `members`.
        """
        guild = discord.utils.get(bot.guilds, name=settings.DISCORD_GUILD)
        print(f'{bot.user} has connected to Discord')    
        print(
            f'{bot.user} is connected to the following guild:\n'
            f'{guild.name}(id: {guild.id})\n'
        )
        members = '\n - '.join([member.name for member in guild.members])
        print(f'Guild Members:\n - {members}')  

    async def on_member_join(self, member):
        """Welcome message on member joining.
        
        Dio Brando style welcome message.

        Returns:
            message (class Message): A welcome message.
        """
        guild = discord.utils.get(bot.guilds, name=settings.DISCORD_GUILD)
        if guild.system_channel is not None:
            msg = '{member.mention} - you thought this was a welcome message, but it was I! Dio!'.format(member=member)
        await guild.system_channel.send(msg)

# create bot instance

if __name__ == "__main__":
    bot = BrandoBot(command_prefix='!', intents=intents)

    # add cogs
    bot.add_cog(GeneralCog(bot))
    bot.add_cog(TwitterCog(bot))
    bot.add_cog(RedditCog(bot))

    bot.run(settings.DISCORD_TOKEN)
