import typing as t
import discord
from discord import Member
from discord.ext import commands


class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def test(self, ctx):
        await ctx.send('test successful')

    @commands.command()
    async def add_role(self, ctx, name: str, hoist=True):
        await ctx.guild.create_role(name=name, hoist=hoist)

    @commands.command()
    async def add_role_member(self, ctx, members: t.List[Member]):
        for member in members:
            await ctx.send(member)