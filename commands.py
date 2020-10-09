import discord
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
