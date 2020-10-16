import discord
from discord.ext import commands

class GeneralCog(commands.Cog):
    """General commands available outside specific modules."""
    def __init__(self, bot):
        self.bot = bot

    # @commands.command()
    # async def test(self, ctx):
    #     """Test that a Cog is reachable"""
    #     await ctx.send('test successful')

    @commands.command()
    async def add_role(self, ctx, name: str, hoist=True):
        """Add a new role to the server.
        
        Add a new role to the server. The new role defaults to 
        showing separately from other roles. 

        Parameters:
            name (str): The role name.
            hoist (bool): Display role separately when online, default `True`.
        
        Returns:
            role (class Role): Creates a role.
        """
        await ctx.guild.create_role(name=name, hoist=hoist)
    