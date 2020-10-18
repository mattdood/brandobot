import discord
from discord.ext import commands

from cogs.utils.helpers import Helpers


class GeneralCog(commands.Cog):
    """General commands available outside specific modules."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def create_role(self, ctx, role_name: str, hoist=True):
        """Add a new role to the server.

        Add a new role to the server. The new role defaults to
        showing separately from other roles.

        Parameters:
            role_name (str): The role name.
            hoist (bool): Display role separately when online, default `True`.

        Returns:
            role (class Role): Creates a role.
        """
        await ctx.guild.create_role(name=role_name, hoist=hoist)
        await ctx.send(f"Created role: {role_name}")

    @commands.command()
    async def add_role(self, ctx, role_name: str, member: discord.Member):
        """Grant a user role.

        Give a user the role passed.

        Parameters:
            role_name (str): The role name.
            member (class Member): Discord member.

        Returns:
            role (class Role): Adds a role to the `Member`.

        TODO:
            * ensure it will find the role
        """
        user = ctx.message.author
        role = discord.utils.get(ctx.guild.roles, name=role_name)
        await user.add_roles(member, role)

    @commands.command()
    async def create_channel(
        self, ctx, channel_name: str, channel_type: str, category_name: str
    ):
        """Create a channel in a category.

        Creates a channel (text or voice) within the given category.

        Parameters:
            channel_name (str): Name of the channel.
            channel_type (str): Accepts "text" or "voice".
            category_name (str): The category to add the channel to.
                                One will be created if necessary.
        Returns:
            channel (class TextChannel or VoiceChannel): The channel created.
        """
        category = discord.utils.get(ctx.guild.categories, name=category_name)
        if category is None:
            category = await ctx.guild.create_category_channel(name=category_name)
        if channel_type == "text":
            await ctx.guild.create_text_channel(name=channel_name, category=category)
            await ctx.send(f"Created channel: {channel_name}")
        elif channel_type == "voice":
            await ctx.guild.create_voice_channel(name=channel_name, category=category)
            await ctx.send(f"Created channel: {channel_name}")
        else:
            await ctx.send(
                f"Incorrect parameter for channel type. Given: {category_name}."
            )

    @commands.command()
    async def create_category(self, ctx, category_name: str):
        """Create a category.

        Creates a category if one does not already exist.

        Parameters:
            category_name (str): The category to create.
        Returns:
            category (class CategoryChannel): The category created.
        """
        category = discord.utils.get(ctx.guild.categories, name=category_name)
        if category is None:
            await ctx.guild.create_category_channel(name=category_name)
            await ctx.send(f"Created category: {category_name}")
        else:
            await ctx.send(f"Category already exists. Given: {category_name}")

    @commands.command()
    async def list_roles(self, ctx):
        """List all roles.

        Lists the current roles in the guild.

        Returns:
            message (class Message): List of Role.name values.
        """
        roles = "\n -".join([x.name for x in ctx.guild.roles])
        roles = Helpers.break_message(roles)
        await ctx.send("Current roles: \n")
        for x in roles:
            await ctx.send(x)

    @commands.command()
    async def list_channels(self, ctx):
        """List channels of a guild.

        Sends a list of channel names by type (text and voice).

        Returns:
            message (class Message): List of channel names by type.
        """
        text_channels = "\n".join([channel.name for channel in ctx.guild.text_channels])
        voice_channels = "\n".join(
            [channel.name for channel in ctx.guild.voice_channels]
        )
        text_channels = Helpers.break_message(text_channels)
        voice_channels = Helpers.break_message(voice_channels)
        await ctx.send("Text channels: \n")
        for x in text_channels:
            await ctx.send(x)
        await ctx.send("Voice channels: \n")
        for x in voice_channels:
            await ctx.send(x)

    @commands.command()
    async def list_categories(self, ctx):
        """List categories of the guild.

        Sends a list of guild categories.

        Returns:
            message (class Message): List of category names.
        """
        categories = "\n".join([category.name for category in ctx.guild.categories])
        categories = Helpers.break_message(categories)
        await ctx.send("List of categories: \n")
        for x in categories:
            await ctx.send(x)

    @commands.command()
    async def list_members(self, ctx):
        """List members of the guild.

        Sends a list of guild members.

        Returns:
            message (class Message): List of member names.
        """
        members = "\n".join([member.name for member in ctx.guild.members])
        members = Helpers.break_message(members)
        await ctx.send("Members list: \n")
        for x in members:
            await ctx.send(x)
