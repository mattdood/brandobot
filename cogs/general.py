import typing as t
import discord
from discord import Member, Role
from discord.ext import commands


class GeneralCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # @commands.command()
    # async def test(self, ctx):
    #     """Test that a Cog is reachable"""
    #     await ctx.send('test successful')

    @commands.command()
    async def add_role(self, ctx, name: str, hoist=True):
        """Add a new role to the server"""
        await ctx.guild.create_role(name=name, hoist=hoist)
    