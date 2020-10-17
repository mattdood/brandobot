import discord
from discord.ext import commands

import settings


class BrandoBot(commands.Bot):
    """I reject my humanity, Jojo!

    The more carefully you scheme, the more
    unexpected events come along.
    """

    async def on_ready(self):
        """Logging information to server on startup.

        Logs information about the bot and the guild to the terminal.

        Returns:
            message (class Message): A message with the `user`, `guild.name`,
                                    `guild.id`, and guild `members`.
        """
        guild = self.get_guild(id=settings.DISCORD_GUILD_ID)
        print(f"{self.user} has connected to Discord")
        print(
            f"{self.user} is connected to the following guild:\n"
            f"{guild.name}(id: {guild.id})\n"
        )
        members = "\n - ".join([member.name for member in guild.members])
        print(f"Guild Members:\n - {members}")
        await self.change_presence(
            activity=discord.Activity(
                name="""your every move Joestar! Use !help for a list of commands""",
                type=discord.ActivityType.watching,
            )
        )

    async def on_member_join(self, member: discord.Member):
        """Welcome message on member joining.

        Dio Brando style welcome message.

        Returns:
            message (class Message): A welcome message.
        """
        guild = self.get_guild(id=settings.DISCORD_GUILD_ID)
        if guild.system_channel is not None:
            msg = """{member.mention} - you thought this
                was a welcome message, but it was I! Dio!""".format(
                member=member
            )
        await guild.system_channel.send(msg)
