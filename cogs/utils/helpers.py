import discord
from discord.ext import commands

class Helpers(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    def break_message(text: str, wrap_at: int = 40, limit: int = 2000):
        """Breaks long text from lines.
        
        Breaks text into 2,000 character chunks for Discord messages.
        Creates a pseudo "max-width" with `wrap_at`.
        
        Parameters:
            text (str): Text to break up.
            wrap_at (int): Default 40, the "width" of the column to create.
            limit (int): Default to 2,000 for the Discord character limit.
        """
        messages = []
        for x in [text[i:i+limit] for i in range(0, len(text), limit)]:
           messages.append(x)
        return messages 

    def truncate_text(text: str, trunc_at: int = 40):
        """Add elipses on long messages.

        Add elipses to the end of a long message as '...' to provide max lengths to messages.
        This is used to create the illusion of max-width on the `tabulate` library.
        A full-screen Discord client has a message window that is 60 characters wide.
        
        Parameters:
            text (str): Text to truncate.
            trunc_at (int): Width of the column you want to create.

        Returns:
            text (str): Text of the `trunc_at` length.
        """
        if len(text) > trunc_at:
            return text[:trunc_at]
        return text
