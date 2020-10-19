import discord

import settings
from brandobot.brando import BrandoBot
from cogs.general import GeneralCog
from cogs.reddit import RedditCog
from cogs.twitter import TwitterCog
from cogs.weather import WeatherCog

# register intents
intents = discord.Intents.default()
intents.members = True


def main():

    bot = BrandoBot(command_prefix="!", intents=intents)

    # add cogs
    bot.add_cog(GeneralCog(bot))
    bot.add_cog(TwitterCog(bot))
    bot.add_cog(RedditCog(bot))
    bot.add_cog(WeatherCog(bot))

    bot.run(settings.DISCORD_TOKEN)


# create bot instance

if __name__ == "__main__":
    main()
